"""
JARVIS V7.3 - Memory Search

Provides local SQLite-based search for persistent JARVIS memories.

Responsibilities:
- Search memory content.
- Search by category.
- Support multi-word queries.
- Rank results by relevance.
- Limit returned results.

This module does not:
- Call Ollama.
- Handle voice commands.
- Modify memories.
"""

from __future__ import annotations

import re
from typing import Any

from memory.memory_store import MemoryStore


class MemorySearch:
    """Search engine for JARVIS persistent memories."""

    DEFAULT_LIMIT = 10
    MAX_LIMIT = 50

    def __init__(self, store: MemoryStore | None = None) -> None:
        """Initialize the memory search service."""
        self.store = store or MemoryStore()
        self.store.initialize()

    @staticmethod
    def _validate_query(query: str) -> str:
        """Validate and normalize a search query."""
        if not isinstance(query, str):
            raise TypeError("Search query must be a string.")

        normalized = query.strip()

        if not normalized:
            raise ValueError("Search query cannot be empty.")

        return normalized

    @classmethod
    def _validate_limit(cls, limit: int) -> int:
        """Validate and normalize the result limit."""
        if not isinstance(limit, int):
            raise TypeError("Search limit must be an integer.")

        if limit < 1:
            raise ValueError("Search limit must be at least 1.")

        return min(limit, cls.MAX_LIMIT)

    @staticmethod
    def _normalize_terms(query: str) -> list[str]:
        """Extract meaningful search terms from a query."""
        terms = re.findall(r"\b[\w'-]+\b", query.lower())

        # Remove duplicate terms while preserving order.
        unique_terms = list(dict.fromkeys(terms))

        return unique_terms

    @staticmethod
    def _calculate_score(
        content: str,
        category: str,
        terms: list[str],
    ) -> int:
        """
        Calculate a simple local relevance score.

        Scoring:
        - Exact full-query match is handled by the caller.
        - Each occurrence of a term in content adds points.
        - A term appearing in the category receives additional weight.
        """
        content_lower = content.lower()
        category_lower = category.lower()

        score = 0

        for term in terms:
            content_matches = content_lower.count(term)
            category_matches = category_lower.count(term)

            score += content_matches * 2
            score += category_matches * 3

        return score

    def search(
        self,
        query: str,
        category: str | None = None,
        limit: int = DEFAULT_LIMIT,
    ) -> list[dict[str, Any]]:
        """
        Search memories using local SQLite retrieval.

        Args:
            query:
                Text to search for.
            category:
                Optional category filter.
            limit:
                Maximum number of results.

        Returns:
            List of matching memories ordered by relevance.
        """
        normalized_query = self._validate_query(query)
        normalized_limit = self._validate_limit(limit)

        if category is not None:
            if not isinstance(category, str):
                raise TypeError("Search category must be a string.")

            category = category.strip().lower()

            if not category:
                raise ValueError("Search category cannot be empty.")

        terms = self._normalize_terms(normalized_query)

        if not terms:
            raise ValueError("Search query contains no searchable terms.")

        with self.store.get_connection() as connection:
            if category is None:
                rows = connection.execute(
                    """
                    SELECT id, category, content, created_at, updated_at
                    FROM memories
                    ORDER BY id ASC
                    """
                ).fetchall()
            else:
                rows = connection.execute(
                    """
                    SELECT id, category, content, created_at, updated_at
                    FROM memories
                    WHERE LOWER(category) = ?
                    ORDER BY id ASC
                    """,
                    (category,),
                ).fetchall()

        results: list[dict[str, Any]] = []

        for row in rows:
            memory = dict(row)

            score = self._calculate_score(
                memory["content"],
                memory["category"],
                terms,
            )

            if score == 0:
                continue

            memory["score"] = score

            results.append(memory)

        results.sort(
            key=lambda item: (
                -item["score"],
                item["id"],
            )
        )

        return results[:normalized_limit]

    def search_content(
        self,
        query: str,
        limit: int = DEFAULT_LIMIT,
    ) -> list[dict[str, Any]]:
        """Search memory content without a category filter."""
        return self.search(
            query=query,
            category=None,
            limit=limit,
        )

    def search_category(
        self,
        category: str,
        limit: int = DEFAULT_LIMIT,
    ) -> list[dict[str, Any]]:
        """
        Search memories belonging to a category.

        The category itself is used as the search query so that
        results are still relevance-ranked.
        """
        normalized_category = category.strip().lower()

        if not normalized_category:
            raise ValueError("Search category cannot be empty.")

        return self.search(
            query=normalized_category,
            category=normalized_category,
            limit=limit,
        )