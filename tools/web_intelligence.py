from typing import List, Dict
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError
from ddgs import DDGS
import trafilatura
import re
import gzip
import zlib
from html import unescape


class WebIntelligence:
    """
    JARVIS V5 Web Intelligence module.

    Responsibilities:
    - Search the web using DDGS
    - Fetch webpages
    - Handle compressed HTTP responses
    - Extract useful main content using Trafilatura
    - Clean extracted text
    - Format search results
    """

    def __init__(self, max_results: int = 5):
        self.max_results = max_results

    # ==========================================================
    # WEB SEARCH
    # ==========================================================

    def search(self, query: str) -> List[Dict]:
        """
        Search the web using DDGS.

        Returns:
            List of dictionaries containing:
            title, url, snippet
        """

        if not query or not query.strip():
            return []

        try:
            results = []

            with DDGS() as ddgs:
                search_results = ddgs.text(
                    query,
                    max_results=self.max_results
                )

                for result in search_results:
                    results.append({
                        "title": result.get("title", ""),
                        "url": result.get("href", ""),
                        "snippet": result.get("body", "")
                    })

            return results

        except Exception as e:
            print(f"Web search error: {e}")
            return []

    # ==========================================================
    # FETCH WEBPAGE
    # ==========================================================

    def fetch_page(self, url: str) -> str:
        """
        Download a webpage and correctly handle compressed
        HTTP responses such as gzip and deflate.

        Returns:
            Raw HTML as a string.
        """

        if not url or not url.strip():
            return ""

        try:
            request = Request(
                url,
                headers={
                    "User-Agent": (
                        "Mozilla/5.0 "
                        "(Windows NT 10.0; Win64; x64) "
                        "AppleWebKit/537.36 "
                        "(KHTML, like Gecko) "
                        "Chrome/139.0 Safari/537.36"
                    ),
                    "Accept": (
                        "text/html,application/xhtml+xml,"
                        "application/xml;q=0.9,*/*;q=0.8"
                    ),
                    "Accept-Encoding": "gzip, deflate"
                }
            )

            with urlopen(request, timeout=15) as response:

                content_type = response.headers.get(
                    "Content-Type",
                    ""
                ).lower()

                content_encoding = response.headers.get(
                    "Content-Encoding",
                    ""
                ).lower()

                # --------------------------------------------------
                # Only process HTML pages.
                # --------------------------------------------------

                if "text/html" not in content_type:
                    print(
                        f"Unsupported content type: {content_type}"
                    )
                    return ""

                data = response.read()

                # --------------------------------------------------
                # Decompress gzip.
                # --------------------------------------------------

                if "gzip" in content_encoding:
                    try:
                        data = gzip.decompress(data)

                    except Exception as e:
                        print(
                            f"Gzip decompression error: {e}"
                        )
                        return ""

                # --------------------------------------------------
                # Decompress deflate.
                # --------------------------------------------------

                elif "deflate" in content_encoding:
                    try:
                        data = zlib.decompress(data)

                    except zlib.error:
                        try:
                            # Some servers use raw DEFLATE.
                            data = zlib.decompress(
                                data,
                                -zlib.MAX_WBITS
                            )

                        except Exception as e:
                            print(
                                f"Deflate decompression error: {e}"
                            )
                            return ""

                # --------------------------------------------------
                # Decode character data.
                # --------------------------------------------------

                charset = response.headers.get_content_charset()

                if charset:
                    try:
                        return data.decode(
                            charset,
                            errors="replace"
                        )
                    except LookupError:
                        pass

                # UTF-8 is the normal fallback.
                try:
                    return data.decode(
                        "utf-8",
                        errors="replace"
                    )

                except UnicodeDecodeError:
                    return data.decode(
                        "latin-1",
                        errors="replace"
                    )

        except HTTPError as e:
            print(
                f"HTTP error while fetching page: "
                f"{e.code} {e.reason}"
            )
            return ""

        except URLError as e:
            print(
                f"URL error while fetching page: {e.reason}"
            )
            return ""

        except TimeoutError:
            print("Page request timed out.")
            return ""

        except Exception as e:
            print(f"Page fetch error: {e}")
            return ""

    # ==========================================================
    # BASIC HTML CLEANUP
    # ==========================================================

    def clean_html(self, html: str) -> str:
        """
        Basic HTML cleanup fallback.

        Used when Trafilatura cannot extract meaningful content.
        """

        if not html:
            return ""

        text = html

        # Remove comments.
        text = re.sub(
            r"<!--.*?-->",
            " ",
            text,
            flags=re.DOTALL
        )

        # Remove unwanted sections.
        unwanted_tags = [
            "script",
            "style",
            "noscript",
            "svg",
            "nav",
            "header",
            "footer",
            "aside"
        ]

        for tag in unwanted_tags:
            text = re.sub(
                rf"<{tag}\b[^>]*>.*?</{tag}>",
                " ",
                text,
                flags=re.IGNORECASE | re.DOTALL
            )

        # Convert common block tags into spaces.
        text = re.sub(
            r"</?(?:p|div|br|li|h[1-6]|tr|td|section|article)"
            r"\b[^>]*>",
            " ",
            text,
            flags=re.IGNORECASE
        )

        # Remove remaining HTML tags.
        text = re.sub(
            r"<[^>]+>",
            " ",
            text
        )

        # Decode HTML entities.
        text = unescape(text)

        # Normalize whitespace.
        text = re.sub(
            r"\s+",
            " ",
            text
        )

        return text.strip()

    # ==========================================================
    # EXTRACT MAIN CONTENT
    # ==========================================================

    def extract_text(self, html: str) -> str:
        """
        Extract useful readable content from a webpage.

        Trafilatura is the primary extraction engine.
        Basic HTML cleanup is used as a fallback.
        """

        if not html:
            return ""

        extracted = ""

        try:
            extracted = trafilatura.extract(
                html,
                include_comments=False,
                include_tables=True,
                include_links=False,
                include_images=False,
                include_formatting=False,
                favor_precision=True
            )

        except Exception as e:
            print(
                f"Trafilatura extraction error: {e}"
            )

        # ------------------------------------------------------
        # Clean Trafilatura output.
        # ------------------------------------------------------

        if extracted:
            extracted = self._clean_extracted_text(
                extracted
            )

        # ------------------------------------------------------
        # Fallback.
        # ------------------------------------------------------

        if not extracted or len(extracted) < 100:
            extracted = self.clean_html(html)

        return extracted.strip()

    # ==========================================================
    # CLEAN EXTRACTED TEXT
    # ==========================================================

    def _clean_extracted_text(self, text: str) -> str:
        """
        Clean text returned by Trafilatura.
        """

        if not text:
            return ""

        # Normalize line endings.
        text = text.replace(
            "\r\n",
            "\n"
        ).replace(
            "\r",
            "\n"
        )

        # Remove HTML comments.
        text = re.sub(
            r"<!--.*?-->",
            " ",
            text,
            flags=re.DOTALL
        )

        # Remove obvious HTML tags.
        text = re.sub(
            r"<[^>]+>",
            " ",
            text
        )

        # Remove wiki-style links.
        text = re.sub(
            r"\[\[([^|\]]+)\|([^\]]+)\]\]",
            r"\2",
            text
        )

        text = re.sub(
            r"\[\[([^\]]+)\]\]",
            r"\1",
            text
        )

        # Remove simple template remnants.
        text = re.sub(
            r"\{\{.*?\}\}",
            " ",
            text,
            flags=re.DOTALL
        )

        # Remove excessive blank lines.
        text = re.sub(
            r"\n\s*\n\s*\n+",
            "\n\n",
            text
        )

        # Remove excessive spaces.
        text = re.sub(
            r"[ \t]+",
            " ",
            text
        )

        # Clean spaces around newlines.
        text = re.sub(
            r" *\n *",
            "\n",
            text
        )

        return text.strip()

    # ==========================================================
    # READ WEBPAGE
    # ==========================================================

    def read_page(self, url: str) -> str:
        """
        Fetch and extract readable text from a webpage.
        """

        html = self.fetch_page(url)

        if not html:
            return ""

        return self.extract_text(html)

    # ==========================================================
    # FORMAT SEARCH RESULTS
    # ==========================================================

    def format_results(self, results: List[Dict]) -> str:
        """
        Convert search results into readable text.
        """

        if not results:
            return "Sir, I could not find any web results."

        output = []

        for index, result in enumerate(
            results,
            start=1
        ):
            title = result.get(
                "title",
                "Untitled"
            )

            snippet = result.get(
                "snippet",
                ""
            )

            url = result.get(
                "url",
                ""
            )

            output.append(
                f"{index}. {title}\n"
                f"   {snippet}\n"
                f"   {url}"
            )

        return "\n\n".join(output)

    # ==========================================================
    # SEARCH + FORMAT
    # ==========================================================

    def search_text(self, query: str) -> str:
        """
        Search the web and return formatted results.
        """

        results = self.search(query)

        return self.format_results(results)


# ==============================================================
# STANDALONE TEST
# ==============================================================

if __name__ == "__main__":

    print("=" * 60)
    print("          JARVIS V5 WEB INTELLIGENCE TEST")
    print("=" * 60)

    web = WebIntelligence(max_results=5)

    query = "python programming"

    print()
    print(f"Searching for: {query}")
    print()

    results = web.search(query)

    if not results:
        print("Sir, I could not find any web results.")

    else:

        print("SEARCH RESULTS")
        print("-" * 60)

        print(
            web.format_results(results)
        )

        # ------------------------------------------------------
        # Test first result.
        # ------------------------------------------------------

        first_url = results[0].get(
            "url",
            ""
        )

        if first_url:

            print()
            print("=" * 60)
            print("TESTING PAGE EXTRACTION")
            print("=" * 60)

            print()
            print(f"URL: {first_url}")
            print()

            page_text = web.read_page(
                first_url
            )

            if page_text:

                print(
                    page_text[:3000]
                )

                if len(page_text) > 3000:
                    print()
                    print(
                        "... [output truncated]"
                    )

            else:
                print(
                    "Sir, I could not extract readable "
                    "content from this page."
                )

    print()
    print("=" * 60)
    print("              TEST COMPLETE")
    print("=" * 60)