"""
JARVIS V7.9 - Memory Commands

Natural-language command layer for JARVIS persistent memory.

Responsibilities:
- Detect memory-related commands.
- Classify memory commands.
- Extract memory operation data.
- Execute save, search, list, count, update, and delete operations.
- Support natural conversational memory phrases.
- Return structured results for voice/router integration.

This module intentionally does NOT:
- Modify main.py.
- Modify CommandRouter.
- Call Ollama.
- Perform speech recognition.
- Perform text-to-speech.
- Automatically save normal conversation.

Design goal:
Memory should feel conversational, while destructive operations
remain explicit and safe.

V7.9 precision improvement:
- Natural "what is my favourite ..." questions are only treated
  as memory questions when the requested subject is sufficiently
  specific.
- Incomplete questions such as:
      "what is my favourite programming"
  are allowed to fall through to normal Ollama conversation.
"""

from __future__ import annotations

import re
from typing import Any

from memory.memory_manager import MemoryManager
from memory.memory_search import MemorySearch


class MemoryCommandLayer:
    """Parser and executor for JARVIS memory commands."""

    # ------------------------------------------------------------------
    # SAVE COMMANDS
    # ------------------------------------------------------------------

    REMEMBER_PREFIXES = (
        "always remember that",
        "always remember",
        "please remember that",
        "please remember",
        "remember that",
        "remember",
        "save memory",
        "save that",
        "save this",
        "keep in mind that",
        "keep in mind",
        "don't forget that",
        "dont forget that",
        "don't forget",
        "dont forget",
    )

    # ------------------------------------------------------------------
    # EXPLICIT SEARCH COMMANDS
    # ------------------------------------------------------------------

    SEARCH_PREFIXES = (
        "what do you remember about",
        "what do you remember regarding",
        "do you remember",
        "do you remember that",
        "can you remember",
        "can you remember that",
        "tell me what you remember about",
        "what can you remember about",
        "search my memory for",
        "search my memories for",
        "search my memory about",
        "search my memories about",
        "search memory for",
        "search memories for",
        "search memory about",
        "search memories about",
        "find my memory about",
        "find my memories about",
        "find memory for",
        "find memories for",
        "find memory about",
        "find memories about",
        "remember anything about",
    )

    # ------------------------------------------------------------------
    # NATURAL MEMORY QUESTIONS
    # ------------------------------------------------------------------

    # These patterns allow normal conversational questions to access
    # persistent memory without searching memory for every sentence.
    #
    # IMPORTANT:
    # The generic "what is my favourite ..." pattern is NOT enough
    # by itself. The subject is validated by
    # _is_specific_favourite_subject().
    #
    # Examples accepted:
    #
    #   what is my favourite fruit
    #   what's my favourite dish
    #   what is my favorite color
    #   what is my favourite programming language
    #   what is my name
    #   who is my creator
    #
    # Example intentionally NOT treated as a memory command:
    #
    #   what is my favourite programming
    #
    # That incomplete question falls through to Ollama.

    NATURAL_MEMORY_QUESTION_PATTERNS = (
        r"^what(?:'s| is) my (?:favourite|favorite|preferred) .+$",
        r"^what(?:'s| is) my name$",
        r"^who is my creator$",
        r"^who created you$",
        r"^do you remember .+$",
        r"^can you remember .+$",
        r"^did i tell you .+$",
        r"^what did i tell you about .+$",
        r"^what do you know about my .+$",
    )

    # ------------------------------------------------------------------
    # FAVOURITE / PREFERRED SUBJECT VALIDATION
    # ------------------------------------------------------------------

    # Common personal-memory subjects that are meaningful enough
    # to be interpreted as explicit memory retrieval.
    #
    # This is intentionally conservative. Unknown/incomplete subjects
    # should fall through to Ollama instead of producing an unrelated
    # memory result.

    FAVOURITE_SUBJECTS = {
        "dish",
        "food",
        "fruit",
        "color",
        "colour",
        "movie",
        "film",
        "song",
        "book",
        "game",
        "sport",
        "team",
        "actor",
        "actress",
        "artist",
        "band",
        "singer",
        "programming language",
        "language",
        "programming",
        "hobby",
        "animal",
        "pet",
        "place",
        "city",
        "country",
        "car",
        "vehicle",
        "subject",
        "course",
        "college",
        "university",
        "framework",
        "library",
        "technology",
        "tech",
        "tool",
        "editor",
        "ide",
    }

    # Subjects that are incomplete on their own.
    #
    # "programming" is deliberately included here because:
    #
    #   what is my favourite programming
    #
    # is incomplete, while:
    #
    #   what is my favourite programming language
    #
    # is a valid memory question.

    INCOMPLETE_FAVOURITE_SUBJECTS = {
        "programming",
        "coding",
        "development",
        "software",
        "computer",
        "technology",
        "tech",
    }

    # ------------------------------------------------------------------
    # LIST COMMANDS
    # ------------------------------------------------------------------

    LIST_COMMANDS = {
        "show my memories",
        "show memories",
        "list my memories",
        "list memories",
        "what do you remember",
        "what do you remember about me",
        "what memories do you have",
        "what memories do i have",
        "tell me what you remember",
    }

    # ------------------------------------------------------------------
    # COUNT COMMANDS
    # ------------------------------------------------------------------

    COUNT_COMMANDS = {
        "how many memories do you have",
        "how many memories do i have",
        "how many memories are there",
        "how many memories",
        "count my memories",
        "count memories",
    }

    # ------------------------------------------------------------------
    # DELETE COMMANDS
    # ------------------------------------------------------------------

    FORGET_PATTERNS = (
        r"^forget memory number (\d+)$",
        r"^delete memory number (\d+)$",
        r"^remove memory number (\d+)$",
        r"^forget memory (\d+)$",
        r"^delete memory (\d+)$",
        r"^remove memory (\d+)$",
    )

    DELETE_ROOTS = (
        "forget memory",
        "delete memory",
        "remove memory",
    )

    # ------------------------------------------------------------------
    # UPDATE COMMANDS
    # ------------------------------------------------------------------

    UPDATE_PATTERNS = (
        r"^update memory (?:number )?(\d+) to (.+)$",
        r"^change memory (?:number )?(\d+) to (.+)$",
        r"^edit memory (?:number )?(\d+) to (.+)$",
    )

    UPDATE_ROOTS = (
        "update memory",
        "change memory",
        "edit memory",
    )

    # ------------------------------------------------------------------
    # CATEGORIZED SAVE
    # ------------------------------------------------------------------

    CATEGORY_PATTERN = re.compile(
        r"^(?:remember|please remember|always remember)"
        r"\s+(?:this\s+)?as\s+"
        r"(preference|project|fact|instruction|person|system|general)"
        r"\s*:\s*(.+)$",
        re.IGNORECASE,
    )

    # ------------------------------------------------------------------
    # NATURAL SAVE PREFIXES
    # ------------------------------------------------------------------

    NATURAL_SAVE_PREFIXES = (
        "always remember that",
        "always remember",
        "please remember that",
        "please remember",
        "remember that",
        "remember",
        "keep in mind that",
        "keep in mind",
        "don't forget that",
        "dont forget that",
        "don't forget",
        "dont forget",
        "save memory",
        "save that",
        "save this",
    )

    # ------------------------------------------------------------------
    # INITIALIZATION
    # ------------------------------------------------------------------

    def __init__(
        self,
        manager: MemoryManager | None = None,
        search: MemorySearch | None = None,
    ) -> None:
        """Initialize the memory command layer."""

        if manager is None and search is None:
            self.manager = MemoryManager()
            self.search = MemorySearch(self.manager.store)

        elif manager is not None and search is None:
            self.manager = manager
            self.search = MemorySearch(manager.store)

        elif manager is None and search is not None:
            self.search = search
            self.manager = MemoryManager(search.store)

        else:
            self.manager = manager
            self.search = search

    # ==================================================================
    # NORMALIZATION
    # ==================================================================

    @staticmethod
    def _normalize_command(command: str) -> str:
        """
        Normalize whitespace and harmless trailing punctuation.

        The user's capitalization is preserved.
        """

        if not isinstance(command, str):
            raise TypeError(
                "Memory command must be a string."
            )

        normalized = " ".join(
            command.strip().split()
        )

        normalized = normalized.rstrip(
            " \t\r\n.!?,"
        )

        return normalized

    @staticmethod
    def _lower(command: str) -> str:
        """Return normalized command in lowercase."""

        return command.lower()

    # ==================================================================
    # PREFIX HELPERS
    # ==================================================================

    @classmethod
    def _matches_prefix(
        cls,
        command: str,
        prefix: str,
    ) -> bool:
        """
        Check whether a command belongs to a prefix family.

        Both forms are accepted:

            "remember"

            "remember that I like Python"
        """

        command = command.strip().lower()
        prefix = prefix.strip().lower()

        return (
            command == prefix
            or command.startswith(prefix + " ")
        )

    @classmethod
    def _matches_any_prefix(
        cls,
        command: str,
        prefixes: tuple[str, ...],
    ) -> bool:
        """Check a command against multiple prefix families."""

        return any(
            cls._matches_prefix(command, prefix)
            for prefix in prefixes
        )

    # ==================================================================
    # FAVOURITE SUBJECT VALIDATION
    # ==================================================================

    @classmethod
    def _is_specific_favourite_subject(
        cls,
        subject: str,
    ) -> bool:
        """
        Determine whether the subject of a favourite/preferred
        question is specific enough to enter persistent memory.

        Examples:

            "dish"
                -> True

            "fruit"
                -> True

            "programming language"
                -> True

            "programming"
                -> False

            "coding"
                -> False
        """

        normalized_subject = " ".join(
            subject.strip().lower().split()
        )

        if not normalized_subject:
            return False

        # --------------------------------------------------------------
        # Explicitly incomplete subjects.
        # --------------------------------------------------------------

        if normalized_subject in (
            cls.INCOMPLETE_FAVOURITE_SUBJECTS
        ):
            return False

        # --------------------------------------------------------------
        # Exact known subjects.
        # --------------------------------------------------------------

        if normalized_subject in (
            cls.FAVOURITE_SUBJECTS
        ):
            return True

        # --------------------------------------------------------------
        # Multi-word subjects.
        #
        # Example:
        #     programming language
        # --------------------------------------------------------------

        words = normalized_subject.split()

        if len(words) >= 2:

            if normalized_subject in (
                cls.FAVOURITE_SUBJECTS
            ):
                return True

            # If the final word makes the subject meaningful,
            # allow the phrase.
            meaningful_final_words = {
                "language",
                "dish",
                "food",
                "fruit",
                "movie",
                "film",
                "song",
                "book",
                "game",
                "sport",
                "team",
                "subject",
                "course",
                "framework",
                "library",
                "technology",
                "tool",
                "editor",
                "ide",
            }

            if words[-1] in meaningful_final_words:
                return True

        # --------------------------------------------------------------
        # Unknown single-word subjects are intentionally rejected.
        #
        # This prevents vague/incomplete questions from triggering
        # memory retrieval and returning an unrelated memory.
        # --------------------------------------------------------------

        return False

    # ==================================================================
    # NATURAL MEMORY QUESTION HELPERS
    # ==================================================================

    @classmethod
    def _matches_natural_memory_question(
        cls,
        command: str,
    ) -> bool:
        """
        Return True when the command is a natural question that
        clearly asks for information from persistent memory.
        """

        normalized = cls._normalize_command(command)
        lowered = normalized.lower()

        if not lowered:
            return False

        # --------------------------------------------------------------
        # Special precision handling for:
        #
        #   what is my favourite ...
        #   what's my favourite ...
        #   what is my favorite ...
        #   what is my preferred ...
        #
        # --------------------------------------------------------------

        favourite_match = re.match(
            r"^what(?:'s| is) my "
            r"(?:favourite|favorite|preferred) "
            r"(.+)$",
            lowered,
            re.IGNORECASE,
        )

        if favourite_match:

            subject = (
                favourite_match.group(1).strip()
            )

            return cls._is_specific_favourite_subject(
                subject
            )

        # --------------------------------------------------------------
        # Other explicitly safe natural-memory questions.
        # --------------------------------------------------------------

        remaining_patterns = (
            r"^what(?:'s| is) my name$",
            r"^who is my creator$",
            r"^who created you$",
            r"^do you remember .+$",
            r"^can you remember .+$",
            r"^did i tell you .+$",
            r"^what did i tell you about .+$",
            r"^what do you know about my .+$",
        )

        return any(
            re.match(
                pattern,
                lowered,
                re.IGNORECASE,
            )
            for pattern in remaining_patterns
        )

    @classmethod
    def _extract_natural_memory_query(
        cls,
        command: str,
    ) -> str:
        """
        Convert a natural memory question into a useful search query.

        Examples:

            what is my favourite fruit
                -> my favourite fruit

            what's my favourite dish
                -> my favourite dish

            what is my favourite programming language
                -> my favourite programming language

            what is my name
                -> my name

            who is my creator
                -> my creator

            who created you
                -> creator

            did I tell you about my project
                -> my project

            what did I tell you about Python
                -> Python
        """

        normalized = cls._normalize_command(command)
        lowered = normalized.lower()

        # --------------------------------------------------------------
        # "what is/what's my favourite ..."
        # --------------------------------------------------------------

        match = re.match(
            r"^what(?:'s| is) my "
            r"(?:favourite|favorite|preferred) "
            r"(.+)$",
            lowered,
            re.IGNORECASE,
        )

        if match:

            subject = match.group(1).strip()

            if not cls._is_specific_favourite_subject(
                subject
            ):
                raise ValueError(
                    "The favourite subject is incomplete."
                )

            return (
                "my "
                + (
                    "favourite "
                    if "favourite" in lowered
                    else "favorite "
                    if "favorite" in lowered
                    else "preferred "
                )
                + subject
            )

        # --------------------------------------------------------------
        # "what is/what's my name"
        # --------------------------------------------------------------

        if re.match(
            r"^what(?:'s| is) my name$",
            lowered,
            re.IGNORECASE,
        ):
            return "my name"

        # --------------------------------------------------------------
        # "who is my creator"
        # --------------------------------------------------------------

        if lowered == "who is my creator":
            return "my creator"

        # --------------------------------------------------------------
        # "who created you"
        # --------------------------------------------------------------

        if lowered == "who created you":
            return "creator"

        # --------------------------------------------------------------
        # "did I tell you ..."
        # --------------------------------------------------------------

        match = re.match(
            r"^did i tell you (?:about )?(.+)$",
            lowered,
            re.IGNORECASE,
        )

        if match:

            query = match.group(1).strip()

            return query

        # --------------------------------------------------------------
        # "what did I tell you about ..."
        # --------------------------------------------------------------

        match = re.match(
            r"^what did i tell you about (.+)$",
            lowered,
            re.IGNORECASE,
        )

        if match:

            return match.group(1).strip()

        # --------------------------------------------------------------
        # "what do you know about my ..."
        # --------------------------------------------------------------

        match = re.match(
            r"^what do you know about (my .+)$",
            lowered,
            re.IGNORECASE,
        )

        if match:

            return match.group(1).strip()

        # --------------------------------------------------------------
        # "do you remember ..."
        # --------------------------------------------------------------

        match = re.match(
            r"^(?:do you remember|can you remember) "
            r"(?:that )?(.+)$",
            lowered,
            re.IGNORECASE,
        )

        if match:

            return match.group(1).strip()

        raise ValueError(
            "Unable to understand the natural memory question."
        )

    # ==================================================================
    # COMMAND DETECTION
    # ==================================================================

    @classmethod
    def is_memory_command(
        cls,
        command: str,
    ) -> bool:
        """
        Return True when the command belongs to the memory system.

        Ordinary conversation is NOT automatically searched.
        """

        normalized = cls._normalize_command(command)
        lowered = normalized.lower()

        if not lowered:
            return False

        # Exact list commands.
        if lowered in cls.LIST_COMMANDS:
            return True

        # Exact count commands.
        if lowered in cls.COUNT_COMMANDS:
            return True

        # Save commands.
        if cls._matches_any_prefix(
            lowered,
            cls.REMEMBER_PREFIXES,
        ):
            return True

        # Explicit search commands.
        if cls._matches_any_prefix(
            lowered,
            cls.SEARCH_PREFIXES,
        ):
            return True

        # Natural conversational memory questions.
        if cls._matches_natural_memory_question(
            lowered
        ):
            return True

        # Delete commands.
        if cls._matches_any_prefix(
            lowered,
            cls.DELETE_ROOTS,
        ):
            return True

        # Update commands.
        if cls._matches_any_prefix(
            lowered,
            cls.UPDATE_ROOTS,
        ):
            return True

        return False

    # ==================================================================
    # COMMAND CLASSIFICATION
    # ==================================================================

    @classmethod
    def classify(
        cls,
        command: str,
    ) -> str | None:
        """
        Classify a memory command.

        Returns:

            "save"
            "search"
            "list"
            "count"
            "delete"
            "update"
            None
        """

        normalized = cls._normalize_command(command)
        lowered = normalized.lower()

        if not lowered:
            return None

        # --------------------------------------------------------------
        # LIST
        # --------------------------------------------------------------

        if lowered in cls.LIST_COMMANDS:
            return "list"

        # --------------------------------------------------------------
        # COUNT
        # --------------------------------------------------------------

        if lowered in cls.COUNT_COMMANDS:
            return "count"

        # --------------------------------------------------------------
        # DELETE
        # --------------------------------------------------------------

        if cls._matches_any_prefix(
            lowered,
            cls.DELETE_ROOTS,
        ):
            return "delete"

        # --------------------------------------------------------------
        # UPDATE
        # --------------------------------------------------------------

        if cls._matches_any_prefix(
            lowered,
            cls.UPDATE_ROOTS,
        ):
            return "update"

        # --------------------------------------------------------------
        # EXPLICIT SEARCH
        # --------------------------------------------------------------

        if cls._matches_any_prefix(
            lowered,
            cls.SEARCH_PREFIXES,
        ):
            return "search"

        # --------------------------------------------------------------
        # NATURAL MEMORY QUESTION
        # --------------------------------------------------------------

        if cls._matches_natural_memory_question(
            lowered
        ):
            return "search"

        # --------------------------------------------------------------
        # SAVE
        # --------------------------------------------------------------

        if cls._matches_any_prefix(
            lowered,
            cls.REMEMBER_PREFIXES,
        ):
            return "save"

        return None

    # ==================================================================
    # SAVE EXTRACTION
    # ==================================================================

    def _extract_save_data(
        self,
        command: str,
    ) -> tuple[str, str]:
        """
        Extract category and content from a save command.
        """

        normalized = self._normalize_command(command)
        lowered = normalized.lower()

        empty_save_commands = {
            "remember",
            "remember that",
            "always remember",
            "always remember that",
            "please remember",
            "please remember that",
            "save memory",
            "save that",
            "save this",
            "keep in mind",
            "keep in mind that",
            "don't forget",
            "dont forget",
            "don't forget that",
            "dont forget that",
        }

        if lowered in empty_save_commands:

            raise ValueError(
                "Please specify what should be remembered."
            )

        # --------------------------------------------------------------
        # Categorized save
        # --------------------------------------------------------------

        category_match = self.CATEGORY_PATTERN.match(
            normalized
        )

        if category_match:

            category = (
                category_match.group(1).lower()
            )

            content = (
                category_match.group(2).strip()
            )

            if not content:

                raise ValueError(
                    "Please specify what should be remembered."
                )

            return category, content

        # --------------------------------------------------------------
        # Natural save
        # --------------------------------------------------------------

        for prefix in sorted(
            self.NATURAL_SAVE_PREFIXES,
            key=len,
            reverse=True,
        ):

            if self._matches_prefix(
                lowered,
                prefix,
            ):

                content = normalized[
                    len(prefix):
                ].strip()

                if not content:

                    raise ValueError(
                        "Please specify what should be remembered."
                    )

                if content.lower() == "that":

                    raise ValueError(
                        "Please specify what should be remembered."
                    )

                return "general", content

        raise ValueError(
            "Unable to understand the memory command."
        )

    # ==================================================================
    # SEARCH EXTRACTION
    # ==================================================================

    def _extract_search_query(
        self,
        command: str,
    ) -> str:
        """
        Extract search text from a memory search command.

        Supports both explicit memory searches and natural questions.
        """

        normalized = self._normalize_command(command)
        lowered = normalized.lower()

        # --------------------------------------------------------------
        # Explicit search commands
        # --------------------------------------------------------------

        for prefix in sorted(
            self.SEARCH_PREFIXES,
            key=len,
            reverse=True,
        ):

            if self._matches_prefix(
                lowered,
                prefix,
            ):

                query = normalized[
                    len(prefix):
                ].strip()

                if not query:

                    raise ValueError(
                        "Please specify what memory to search for."
                    )

                return query

        # --------------------------------------------------------------
        # Natural memory questions
        # --------------------------------------------------------------

        if self._matches_natural_memory_question(
            lowered
        ):

            return self._extract_natural_memory_query(
                normalized
            )

        raise ValueError(
            "Unable to understand the memory search command."
        )

    # ==================================================================
    # MEMORY ID EXTRACTION
    # ==================================================================

    @staticmethod
    def _extract_memory_id(
        command: str,
        patterns: tuple[str, ...],
    ) -> int:
        """Extract a numeric memory ID."""

        normalized = command.strip().lower()

        for pattern in patterns:

            match = re.match(
                pattern,
                normalized,
                re.IGNORECASE,
            )

            if match:

                return int(
                    match.group(1)
                )

        raise ValueError(
            "Please specify the memory number."
        )

    # ==================================================================
    # UPDATE EXTRACTION
    # ==================================================================

    @staticmethod
    def _extract_update_data(
        command: str,
    ) -> tuple[int, str]:
        """
        Extract memory ID and new content.
        """

        normalized = " ".join(
            command.strip().split()
        )

        for pattern in MemoryCommandLayer.UPDATE_PATTERNS:

            match = re.match(
                pattern,
                normalized,
                re.IGNORECASE,
            )

            if match:

                memory_id = int(
                    match.group(1)
                )

                new_content = (
                    match.group(2).strip()
                )

                if not new_content:

                    raise ValueError(
                        "Please specify the updated memory content."
                    )

                return memory_id, new_content

        raise ValueError(
            "Please specify the memory number and new content."
        )

    # ==================================================================
    # DELETE VALIDATION
    # ==================================================================

    @classmethod
    def _is_delete_command_complete(
        cls,
        command: str,
    ) -> bool:
        """Return True when a delete command contains a memory ID."""

        normalized = command.strip().lower()

        return any(
            re.match(
                pattern,
                normalized,
                re.IGNORECASE,
            )
            for pattern in cls.FORGET_PATTERNS
        )

    # ==================================================================
    # UPDATE VALIDATION
    # ==================================================================

    @classmethod
    def _is_update_command_complete(
        cls,
        command: str,
    ) -> bool:
        """Return True when an update command is complete."""

        normalized = command.strip()

        return any(
            re.match(
                pattern,
                normalized,
                re.IGNORECASE,
            )
            for pattern in cls.UPDATE_PATTERNS
        )

    # ==================================================================
    # EXECUTION
    # ==================================================================

    def execute(
        self,
        command: str,
    ) -> dict[str, Any]:
        """
        Execute a memory command.

        Returns:

            {
                "success": bool,
                "action": str | None,
                "message": str,
                "data": Any
            }
        """

        normalized = self._normalize_command(command)

        action = self.classify(normalized)

        # --------------------------------------------------------------
        # NOT A MEMORY COMMAND
        # --------------------------------------------------------------

        if action is None:

            return {
                "success": False,
                "action": None,
                "message": "Not a memory command.",
                "data": None,
            }

        try:

            # ==========================================================
            # SAVE
            # ==========================================================

            if action == "save":

                category, content = (
                    self._extract_save_data(
                        normalized
                    )
                )

                memory = self.manager.save_memory(
                    content=content,
                    category=category,
                )

                return {
                    "success": True,
                    "action": "save",
                    "message": (
                        f"Memory {memory['id']} "
                        "saved successfully."
                    ),
                    "data": memory,
                }

            # ==========================================================
            # SEARCH
            # ==========================================================

            if action == "search":

                query = self._extract_search_query(
                    normalized
                )

                results = self.search.search_content(
                    query
                )

                return {
                    "success": True,
                    "action": "search",
                    "message": (
                        f"Found {len(results)} "
                        "matching memories."
                    ),
                    "data": results,
                }

            # ==========================================================
            # LIST
            # ==========================================================

            if action == "list":

                memories = (
                    self.manager.get_all_memories()
                )

                return {
                    "success": True,
                    "action": "list",
                    "message": (
                        f"Found {len(memories)} "
                        "stored memories."
                    ),
                    "data": memories,
                }

            # ==========================================================
            # COUNT
            # ==========================================================

            if action == "count":

                count = self.manager.count_memories()

                return {
                    "success": True,
                    "action": "count",
                    "message": (
                        f"I have {count} "
                        "stored memories."
                    ),
                    "data": {
                        "count": count,
                    },
                }

            # ==========================================================
            # DELETE
            # ==========================================================

            if action == "delete":

                if not self._is_delete_command_complete(
                    normalized
                ):

                    return {
                        "success": False,
                        "action": "delete",
                        "message": (
                            "Please specify the memory number."
                        ),
                        "data": None,
                    }

                memory_id = self._extract_memory_id(
                    normalized,
                    self.FORGET_PATTERNS,
                )

                deleted = (
                    self.manager.delete_memory(
                        memory_id
                    )
                )

                if deleted:

                    message = (
                        f"Memory {memory_id} "
                        "deleted successfully."
                    )

                else:

                    message = (
                        f"Memory {memory_id} "
                        "was not found."
                    )

                return {
                    "success": deleted,
                    "action": "delete",
                    "message": message,
                    "data": {
                        "memory_id": memory_id,
                        "deleted": deleted,
                    },
                }

            # ==========================================================
            # UPDATE
            # ==========================================================

            if action == "update":

                if not self._is_update_command_complete(
                    normalized
                ):

                    return {
                        "success": False,
                        "action": "update",
                        "message": (
                            "Please specify the memory "
                            "number and new content."
                        ),
                        "data": None,
                    }

                memory_id, new_content = (
                    self._extract_update_data(
                        normalized
                    )
                )

                updated = (
                    self.manager.update_memory(
                        memory_id=memory_id,
                        content=new_content,
                    )
                )

                if updated is None:

                    return {
                        "success": False,
                        "action": "update",
                        "message": (
                            f"Memory {memory_id} "
                            "was not found."
                        ),
                        "data": None,
                    }

                return {
                    "success": True,
                    "action": "update",
                    "message": (
                        f"Memory {memory_id} "
                        "updated successfully."
                    ),
                    "data": updated,
                }

            # ==========================================================
            # FALLBACK
            # ==========================================================

            return {
                "success": False,
                "action": action,
                "message": "Unsupported memory action.",
                "data": None,
            }

        except (TypeError, ValueError) as exc:

            return {
                "success": False,
                "action": action,
                "message": str(exc),
                "data": None,
            }
