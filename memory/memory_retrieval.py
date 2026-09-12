"""
JARVIS V7.7 - Advanced Memory Retrieval

Adds a deterministic reranking layer on top of the existing
V7.3 MemorySearch system.

Responsibilities:
- Retrieve candidate memories.
- Normalize user queries.
- Ignore common stop words during reranking.
- Reward exact phrase matches.
- Reward meaningful term matches.
- Reward category relevance.
- Reward meaningful phrase matches.
- Return deterministic results.

This module does NOT:
- Modify the database.
- Save memories.
- Delete memories.
- Modify MemorySearch.
- Call Ollama.
- Modify main.py.
- Modify CommandRouter.
"""

from __future__ import annotations

import re
from typing import Any

from memory.memory_search import MemorySearch


class MemoryRetrieval:
    """Advanced deterministic memory retrieval and reranking."""

    DEFAULT_LIMIT = 5
    MAX_LIMIT = 10

    CANDIDATE_MULTIPLIER = 3

    EXACT_PHRASE_BONUS = 10
    MEANINGFUL_PHRASE_BONUS = 8
    TERM_MATCH_BONUS = 3
    CATEGORY_MATCH_BONUS = 2

    STOP_WORDS = {
        "a",
        "about",
        "am",
        "an",
        "and",
        "are",
        "do",
        "does",
        "for",
        "from",
        "how",
        "i",
        "in",
        "is",
        "it",
        "me",
        "my",
        "of",
        "on",
        "or",
        "please",
        "the",
        "that",
        "this",
        "to",
        "when",
        "where",
        "which",
        "who",
        "why",
        "with",
        "you",
        "your",
    }

    def __init__(
        self,
        search: MemorySearch | None = None,
    ) -> None:
        """Initialize the retrieval layer."""

        self.search_engine = (
            search or MemorySearch()
        )

    # ------------------------------------------------------------------
    # VALIDATION
    # ------------------------------------------------------------------

    @staticmethod
    def _validate_query(query: str) -> str:
        """Validate and normalize a query."""

        if not isinstance(query, str):
            raise TypeError(
                "Memory retrieval query must be a string."
            )

        normalized = " ".join(
            query.strip().split()
        )

        if not normalized:
            raise ValueError(
                "Memory retrieval query cannot be empty."
            )

        return normalized

    @classmethod
    def _validate_limit(cls, limit: int) -> int:
        """Validate and cap the result limit."""

        if not isinstance(limit, int):
            raise TypeError(
                "Memory retrieval limit must be an integer."
            )

        if limit < 1:
            raise ValueError(
                "Memory retrieval limit must be at least 1."
            )

        return min(
            limit,
            cls.MAX_LIMIT,
        )

    # ------------------------------------------------------------------
    # QUERY PROCESSING
    # ------------------------------------------------------------------

    @classmethod
    def _normalize_text(
        cls,
        text: str,
    ) -> str:
        """Normalize text for matching."""

        return " ".join(
            re.findall(
                r"[a-z0-9]+",
                text.lower(),
            )
        )

    @classmethod
    def _extract_terms(
        cls,
        text: str,
    ) -> list[str]:
        """Extract meaningful non-stop-word terms."""

        words = re.findall(
            r"[a-z0-9]+",
            text.lower(),
        )

        return [
            word
            for word in words
            if word not in cls.STOP_WORDS
        ]

    @classmethod
    def _extract_meaningful_phrases(
        cls,
        text: str,
    ) -> list[str]:
        """
        Extract useful multi-word phrases while ignoring
        leading/trailing stop words.

        Example:

            "my favourite dish"

        becomes:

            ["favourite dish"]

        This allows a memory containing:

            "my favourite dish is biryani"

        to receive a strong phrase-match bonus.
        """

        words = re.findall(
            r"[a-z0-9]+",
            text.lower(),
        )

        if not words:
            return []

        phrases: list[str] = []

        current: list[str] = []

        for word in words:

            if word in cls.STOP_WORDS:

                if len(current) >= 2:
                    phrases.append(
                        " ".join(current)
                    )

                current = []
                continue

            current.append(word)

        if len(current) >= 2:
            phrases.append(
                " ".join(current)
            )

        # Also consider adjacent meaningful terms.
        # This handles cases where stop words occur inside
        # a natural question.
        meaningful_words = [
            word
            for word in words
            if word not in cls.STOP_WORDS
        ]

        if len(meaningful_words) >= 2:

            for index in range(
                len(meaningful_words) - 1
            ):
                phrase = " ".join(
                    meaningful_words[
                        index:index + 2
                    ]
                )

                if phrase not in phrases:
                    phrases.append(phrase)

        return phrases

    # ------------------------------------------------------------------
    # RERANKING
    # ------------------------------------------------------------------

    @classmethod
    def _calculate_relevance(
        cls,
        query: str,
        memory: dict[str, Any],
    ) -> int:
        """Calculate an additional deterministic relevance score."""

        content = str(
            memory.get("content", "")
        )

        category = str(
            memory.get("category", "")
        )

        normalized_query = cls._normalize_text(
            query
        )

        normalized_content = cls._normalize_text(
            content
        )

        normalized_category = cls._normalize_text(
            category
        )

        query_terms = cls._extract_terms(
            query
        )

        meaningful_phrases = (
            cls._extract_meaningful_phrases(
                query
            )
        )

        score = int(
            memory.get("score", 0)
        )

        # --------------------------------------------------------------
        # Exact full-query phrase match
        # --------------------------------------------------------------

        if (
            normalized_query
            and normalized_query in normalized_content
        ):
            score += cls.EXACT_PHRASE_BONUS

        # --------------------------------------------------------------
        # Meaningful phrase matching
        # --------------------------------------------------------------

        for phrase in meaningful_phrases:

            if phrase in normalized_content:
                score += cls.MEANINGFUL_PHRASE_BONUS

        # --------------------------------------------------------------
        # Meaningful term matching
        # --------------------------------------------------------------

        for term in query_terms:

            if term in normalized_content:
                score += cls.TERM_MATCH_BONUS

            if term in normalized_category:
                score += cls.CATEGORY_MATCH_BONUS

        # Keep the variable explicitly used so category matching
        # remains clear and intentional.
        _ = normalized_category

        return score

    @classmethod
    def _rerank(
        cls,
        query: str,
        memories: list[dict[str, Any]],
    ) -> list[dict[str, Any]]:
        """Rerank candidate memories."""

        ranked: list[dict[str, Any]] = []

        for memory in memories:

            item = dict(memory)

            item["retrieval_score"] = (
                cls._calculate_relevance(
                    query,
                    item,
                )
            )

            ranked.append(item)

        ranked.sort(
            key=lambda item: (
                -int(
                    item.get(
                        "retrieval_score",
                        0,
                    )
                ),
                int(
                    item.get(
                        "id",
                        0,
                    )
                ),
            )
        )

        return ranked

    # ------------------------------------------------------------------
    # PUBLIC SEARCH
    # ------------------------------------------------------------------

    def search(
        self,
        query: str,
        limit: int = DEFAULT_LIMIT,
    ) -> list[dict[str, Any]]:
        """
        Retrieve and rerank relevant memories.
        """

        normalized_query = self._validate_query(
            query
        )

        validated_limit = self._validate_limit(
            limit
        )

        candidate_limit = min(
            self.MAX_LIMIT * self.CANDIDATE_MULTIPLIER,
            50,
        )

        candidates = self.search_engine.search(
            normalized_query,
            limit=candidate_limit,
        )

        ranked = self._rerank(
            normalized_query,
            candidates,
        )

        return ranked[:validated_limit]

    def search_content(
        self,
        query: str,
        limit: int = DEFAULT_LIMIT,
    ) -> list[dict[str, Any]]:
        """Retrieve memories primarily by content."""

        normalized_query = self._validate_query(
            query
        )

        validated_limit = self._validate_limit(
            limit
        )

        candidate_limit = min(
            self.MAX_LIMIT * self.CANDIDATE_MULTIPLIER,
            50,
        )

        candidates = (
            self.search_engine.search_content(
                normalized_query,
                limit=candidate_limit,
            )
        )

        ranked = self._rerank(
            normalized_query,
            candidates,
        )

        return ranked[:validated_limit]

    # ------------------------------------------------------------------
    # BEST MEMORY
    # ------------------------------------------------------------------

    def best_match(
        self,
        query: str,
    ) -> dict[str, Any] | None:
        """Return the single strongest memory match."""

        results = self.search(
            query,
            limit=1,
        )

        if not results:
            return None

        return results[0]