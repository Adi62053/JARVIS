import re

from tools.web_intelligence import WebIntelligence

try:
    from ollama import chat
except ImportError:
    chat = None


class WebRouter:
    """
    V5 Web Intelligence Router.

    Two main modes:

    1. Explicit web-search commands:
       "search for latest Python news"
       "search the web for Python"
       "google Python programming"

       -> Shows search results.

    2. Natural current/latest questions:
       "what is the latest news about Python?"
       "what are the latest Python updates?"
       "tell me the latest news about Python"

       -> Searches internally, analyzes the results with Ollama,
          and returns a direct answer instead of showing five pages.
    """

    def __init__(self):
        self.web = WebIntelligence(max_results=5)
        self.last_results = []

        # Same local model already used by JARVIS.
        self.ai_model = "llama3.2:3b"

    # ==========================================================
    # COMMAND DETECTION
    # ==========================================================

    def is_web_command(self, command):
        """
        Determine whether a command belongs to V5 web intelligence.
        """

        command = command.lower().strip()

        # ------------------------------------------------------
        # EXPLICIT SEARCH COMMANDS
        # ------------------------------------------------------

        search_prefixes = [
            "search for ",
            "search ",
            "look up ",
            "lookup ",
            "find online ",
            "find on the internet ",
            "search online for ",
            "search the web for ",
            "search the internet for ",
            "google ",
            "web search ",
            "internet search ",
        ]

        for prefix in search_prefixes:
            if command.startswith(prefix):
                return True

        # ------------------------------------------------------
        # NATURAL CURRENT / LATEST QUESTIONS
        # ------------------------------------------------------

        current_prefixes = [
            "what is the latest ",
            "what are the latest ",
            "latest news about ",
            "current news about ",
            "latest ",
            "current ",
            "recent ",
            "today's ",
            "todays ",
            "news about ",
            "tell me the latest ",
            "tell me the current ",
            "tell me recent ",
        ]

        for prefix in current_prefixes:
            if command.startswith(prefix):
                return True

        # ------------------------------------------------------
        # DIRECT WEBPAGE COMMANDS
        # ------------------------------------------------------

        page_prefixes = [
            "read this webpage",
            "read this web page",
            "read webpage",
            "read web page",
            "read this page",
            "open and read",
        ]

        for prefix in page_prefixes:
            if command.startswith(prefix):
                return True

        # ------------------------------------------------------
        # RESULT NUMBER COMMANDS
        # ------------------------------------------------------

        result_patterns = [
            r"read the first web page",
            r"read the second web page",
            r"read the third web page",
            r"read the fourth web page",
            r"read the fifth web page",
            r"read result 1",
            r"read result 2",
            r"read result 3",
            r"read result 4",
            r"read result 5",
            r"open result 1",
            r"open result 2",
            r"open result 3",
            r"open result 4",
            r"open result 5",
        ]

        for pattern in result_patterns:
            if re.fullmatch(pattern, command):
                return True

        return False

    # ==========================================================
    # EXPLICIT SEARCH DETECTION
    # ==========================================================

    def _is_explicit_search_command(self, command):
        """
        Return True only when the user explicitly asks JARVIS
        to search the web.
        """

        command = command.lower().strip()

        search_prefixes = [
            "search the web for ",
            "search the internet for ",
            "search online for ",
            "internet search ",
            "web search ",
            "search for ",
            "search ",
            "look up ",
            "lookup ",
            "find online ",
            "find on the internet ",
            "google ",
        ]

        for prefix in search_prefixes:
            if command.startswith(prefix):
                return True

        return False

    # ==========================================================
    # CURRENT QUESTION DETECTION
    # ==========================================================

    def _is_current_question(self, command):
        """
        Detect natural-language questions where the user expects
        a direct current/latest answer rather than a list of links.
        """

        command = command.lower().strip()

        current_prefixes = [
            "what is the latest ",
            "what are the latest ",
            "latest news about ",
            "current news about ",
            "latest ",
            "current ",
            "recent ",
            "today's ",
            "todays ",
            "news about ",
            "tell me the latest ",
            "tell me the current ",
            "tell me recent ",
        ]

        for prefix in current_prefixes:
            if command.startswith(prefix):
                return True

        return False

    # ==========================================================
    # SEARCH QUERY EXTRACTION
    # ==========================================================

    def _extract_search_query(self, command):
        """
        Extract a search query from either an explicit search
        command or a natural current/latest question.

        Example:

            what is the latest news about Python

        becomes:

            latest news about python
        """

        command = command.lower().strip()

        # ------------------------------------------------------
        # EXPLICIT SEARCH COMMANDS
        # ------------------------------------------------------

        search_prefixes = [
            "search the web for ",
            "search the internet for ",
            "search online for ",
            "internet search ",
            "web search ",
            "search for ",
            "search ",
            "look up ",
            "lookup ",
            "find online ",
            "find on the internet ",
            "google ",
        ]

        for prefix in search_prefixes:
            if command.startswith(prefix):
                query = command[len(prefix):].strip()

                if query:
                    return query

        # ------------------------------------------------------
        # "WHAT IS THE LATEST..."
        # ------------------------------------------------------

        latest_question_prefixes = [
            "what is the latest ",
            "what are the latest ",
        ]

        for prefix in latest_question_prefixes:
            if command.startswith(prefix):
                query = command[len(prefix):].strip()

                if query:
                    return "latest " + query

        # ------------------------------------------------------
        # OTHER CURRENT QUESTIONS
        # ------------------------------------------------------

        current_prefixes = [
            "latest news about ",
            "current news about ",
            "latest ",
            "current ",
            "recent ",
            "today's ",
            "todays ",
            "news about ",
            "tell me the latest ",
            "tell me the current ",
            "tell me recent ",
        ]

        for prefix in current_prefixes:
            if command.startswith(prefix):
                query = command[len(prefix):].strip()

                if query:
                    return query

        return None

    # ==========================================================
    # WEBPAGE TARGET EXTRACTION
    # ==========================================================

    def _extract_page_target(self, command):
        """
        Extract a URL from a direct webpage-reading command.
        """

        command = command.strip()

        prefixes = [
            "read this webpage ",
            "read this web page ",
            "read webpage ",
            "read web page ",
            "read this page ",
            "open and read ",
        ]

        for prefix in prefixes:
            if command.lower().startswith(prefix):
                target = command[len(prefix):].strip()

                if target:
                    return target

        if command.startswith("http://") or command.startswith("https://"):
            return command

        return None

    # ==========================================================
    # RESULT NUMBER EXTRACTION
    # ==========================================================

    def _extract_result_number(self, command):
        """
        Convert commands such as:

            read the first web page
            read the second web page
            read result 3

        into an integer result number.
        """

        command = command.lower().strip()

        word_numbers = {
            "first": 1,
            "second": 2,
            "third": 3,
            "fourth": 4,
            "fifth": 5,
        }

        for word, number in word_numbers.items():

            patterns = [
                f"read the {word} web page",
                f"read the {word} webpage",
                f"open the {word} web page",
                f"open the {word} webpage",
                f"read {word} web page",
                f"read {word} webpage",
            ]

            for pattern in patterns:
                if command == pattern:
                    return number

        match = re.fullmatch(
            r"(?:read|open)\s+(?:the\s+)?result\s+([1-5])",
            command,
        )

        if match:
            return int(match.group(1))

        return None

    # ==========================================================
    # EXPLICIT SEARCH
    # ==========================================================

    def search(self, query):
        """
        Explicit web search.

        Search -> show results on terminal.
        """

        if not query:
            return "Sorry, sir. I couldn't determine what to search for."

        try:
            results = self.web.search(query)
        except Exception as exc:
            print(f"Web search error: {exc}")
            return "Sorry, sir. The web search failed."

        self.last_results = results

        print()
        print("=" * 70)
        print("V5 WEB SEARCH RESULTS")
        print("=" * 70)
        print(f"Query: {query}")
        print(f"Results found: {len(results)}")
        print()

        if not results:
            print("No results found.")
            print("=" * 70)

            return f"Sir, I couldn't find any web results for {query}."

        for index, result in enumerate(results, start=1):

            title = result.get("title", "Untitled")
            url = result.get("url", "")
            snippet = result.get("body", "")

            print(f"{index}. {title}")
            print(f"   URL: {url}")

            if snippet:
                print(f"   {snippet}")

            print()

        print("=" * 70)
        print()

        return (
            f"I've searched for {query}, sir. "
            f"I found {len(results)} results. "
            f"The results are displayed on the screen."
        )

    # ==========================================================
    # CURRENT QUESTION -> DIRECT ANSWER
    # ==========================================================

    def answer_current_question(self, query):
        """
        Search the web internally and produce a direct,
        source-grounded answer using local Ollama.

        The user does NOT get a five-page selection flow.
        """

        if not query:
            return (
                "Sorry, sir. I couldn't determine what current "
                "information you need."
            )

        print()
        print("=" * 70)
        print("V5 CURRENT INFORMATION")
        print("=" * 70)
        print(f"Internal query: {query}")
        print("Searching web internally...")
        print()

        try:
            results = self.web.search(query)
        except Exception as exc:
            print(f"Web search error: {exc}")
            print("=" * 70)

            return "Sorry, sir. I couldn't access the web right now."

        self.last_results = results

        if not results:
            print("No web results found.")
            print("=" * 70)

            return (
                f"Sorry, sir. I couldn't find recent information "
                f"about {query}."
            )

        # ------------------------------------------------------
        # DISPLAY SOURCES IN TERMINAL
        # ------------------------------------------------------

        print(f"Sources found: {len(results)}")
        print()

        for index, result in enumerate(results, start=1):

            title = result.get("title", "Untitled")
            url = result.get("url", "")

            print(f"{index}. {title}")
            print(f"   {url}")
            print()

        # ------------------------------------------------------
        # BUILD SOURCE CONTEXT
        # ------------------------------------------------------

        context_parts = []

        for index, result in enumerate(results, start=1):

            title = result.get("title", "")
            body = result.get("body", "")
            url = result.get("url", "")

            if not body:
                body = result.get("snippet", "")

            body = body.strip()[:1800]

            context_parts.append(
                f"SOURCE {index}\n"
                f"TITLE: {title}\n"
                f"URL: {url}\n"
                f"CONTENT: {body}\n"
            )

        web_context = "\n".join(context_parts)

        # ------------------------------------------------------
        # LOCAL AI AVAILABILITY
        # ------------------------------------------------------

        if chat is None:

            print("=" * 70)

            first = results[0]

            title = first.get("title", "")
            body = first.get("body", "")

            if not body:
                body = first.get("snippet", "")

            body = body.strip()

            return (
                f"Sir, based on the available web information, "
                f"{title}. {body[:900]}"
            )

        # ------------------------------------------------------
        # SOURCE-GROUNDED ANALYSIS PROMPT
        # ------------------------------------------------------

        prompt = f"""
You are JARVIS, a concise and careful laptop assistant.

The user asked for current or latest information.

USER QUESTION:
{query}

RETRIEVED WEB SOURCES:
{web_context}

YOUR TASK:
Answer the user's question directly using ONLY the information
contained in the retrieved web sources above.

SOURCE-GROUNDING RULES:

1. Do NOT use your own memory to add current facts.
2. Do NOT invent facts, dates, releases, features, events,
   statistics, or announcements.
3. Do NOT assume that a search-result title proves that the
   underlying claim is true.
4. Treat snippets as potentially incomplete.
5. Only state a specific claim when it is supported by the
   supplied source content.
6. If a claim appears in only one source, do not present it as
   confirmed by multiple sources.
7. Prefer official sources when the retrieved sources provide
   relevant official information.
8. For "latest" questions, pay attention to dates or release
   information actually present in the sources.
9. If the sources do not contain enough information to establish
   something as the latest information, say that clearly instead
   of guessing.
10. If sources disagree, mention the disagreement briefly.
11. Never fabricate a source or citation.
12. Do not claim that you opened or read a webpage unless the
    supplied source content actually contains the information.

ANSWER STYLE:

- Answer the user's question directly.
- Do NOT say "I found 5 results."
- Do NOT ask the user to choose a webpage.
- Do NOT list all five sources.
- Do NOT list URLs.
- Do NOT describe the search process.
- Do NOT repeat the source text word-for-word.
- Summarize and combine the useful information.
- Keep the answer concise and natural for voice.
- Aim for approximately 3 to 6 sentences.
- Address the user as "sir" naturally when appropriate.
- If there is not enough reliable information, be honest about it.
"""

        try:

            response = chat(
                model=self.ai_model,
                messages=[
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ],
            )

            answer = response["message"]["content"].strip()

            if not answer:
                raise RuntimeError(
                    "Ollama returned an empty response."
                )

            print("JARVIS WEB ANALYSIS:")
            print(answer)
            print()
            print("=" * 70)
            print()

            return answer

        except Exception as exc:

            print(f"Ollama analysis error: {exc}")
            print()

            # --------------------------------------------------
            # SAFE FALLBACK
            # --------------------------------------------------

            first = results[0]

            title = first.get("title", "")
            body = first.get("body", "")

            if not body:
                body = first.get("snippet", "")

            body = body.strip()

            if body:
                answer = (
                    f"Sir, the available web information says "
                    f"{body[:1000]}"
                )
            else:
                answer = (
                    f"Sir, I found recent information about "
                    f"{query}, but I couldn't generate a "
                    f"reliable analysis."
                )

            print("=" * 70)

            return answer

    # ==========================================================
    # READ DIRECT WEBPAGE
    # ==========================================================

    def read_page(self, target):
        """
        Read a directly specified webpage.
        """

        if not target:
            return (
                "Sorry, sir. I couldn't determine which webpage "
                "to read."
            )

        target = target.strip()

        if not target.startswith("http://") and not target.startswith(
            "https://"
        ):
            target = "https://" + target

        print()
        print("=" * 70)
        print("V5 WEBPAGE READER")
        print("=" * 70)
        print(f"URL: {target}")
        print()

        try:
            text = self.web.read_page(target)
        except Exception as exc:
            print(f"Webpage read error: {exc}")

            return "Sorry, sir. I couldn't read that webpage."

        if not text:
            return (
                "Sorry, sir. I couldn't extract readable information "
                "from that webpage."
            )

        spoken_text = text[:2500]

        if len(text) > 2500:
            spoken_text += (
                "\n\nThe webpage contains more information, "
                "but I have limited the spoken response."
            )

        print("Extracted webpage text:")
        print(text[:5000])
        print()

        print("=" * 70)
        print()

        return spoken_text

    # ==========================================================
    # READ RESULT SNIPPET FALLBACK
    # ==========================================================

    def _read_result_snippet(self, result_number):
        """
        If direct webpage access fails, use the search-result
        snippet as a fallback.
        """

        if not self.last_results:
            return (
                "Sorry, sir. There are no stored web search results. "
                "Please search first."
            )

        if result_number < 1 or result_number > len(self.last_results):
            return (
                f"Sorry, sir. Result {result_number} is not available."
            )

        result = self.last_results[result_number - 1]

        title = result.get("title", "Untitled")
        url = result.get("url", "")
        snippet = result.get("body", "")

        if not snippet:
            snippet = result.get("snippet", "")

        print()
        print("=" * 70)
        print("SEARCH RESULT FALLBACK")
        print("=" * 70)
        print(f"Result: {result_number}")
        print(f"Title: {title}")
        print(f"URL: {url}")
        print()
        print(
            "Using search-result information because direct webpage"
        )
        print("access was unavailable.")
        print("=" * 70)
        print()

        if not snippet:
            return (
                "Sorry, sir. Direct webpage access failed and "
                "there was no search-result information available."
            )

        return (
            "Sir, direct access to that webpage was blocked. "
            "Here is the information available from the search result.\n\n"
            + snippet[:2500]
        )

    # ==========================================================
    # READ SELECTED SEARCH RESULT
    # ==========================================================

    def read_result(self, result_number):
        """
        Read a previously searched result.

        Direct webpage access is attempted first.
        Search-result fallback is used if direct access fails.
        """

        if not self.last_results:
            return (
                "Sorry, sir. There are no stored web search results. "
                "Please search for something first."
            )

        if result_number < 1 or result_number > len(self.last_results):
            return (
                f"Sorry, sir. Result {result_number} is not available."
            )

        result = self.last_results[result_number - 1]

        title = result.get("title", "Untitled")
        url = result.get("url", "")

        print()
        print("=" * 70)
        print(f"READING WEB RESULT {result_number}")
        print("=" * 70)
        print(f"Title: {title}")
        print(f"URL: {url}")
        print()

        text = self.read_page(url)

        if text.startswith("Sorry, sir."):

            print("Direct webpage access failed.")
            print("Using search-result snippet fallback.")
            print()

            return self._read_result_snippet(result_number)

        print("=" * 70)
        print()

        return (
            f"Reading result {result_number}, sir.\n\n"
            + text
        )

    # ==========================================================
    # MAIN EXECUTION
    # ==========================================================

    def execute(self, command):
        """
        Main V5 web-router entry point.
        """

        if not command:
            return None

        command = command.strip()

        if not command:
            return None

        # ======================================================
        # 1. EXPLICIT SEARCH
        # ======================================================

        if self._is_explicit_search_command(command):

            query = self._extract_search_query(command)

            if query:
                return self.search(query)

        # ======================================================
        # 2. NATURAL CURRENT/LATEST QUESTION
        # ======================================================

        if self._is_current_question(command):

            query = self._extract_search_query(command)

            if query:
                return self.answer_current_question(query)

        # ======================================================
        # 3. RESULT NUMBER
        # ======================================================

        result_number = self._extract_result_number(command)

        if result_number is not None:
            return self.read_result(result_number)

        # ======================================================
        # 4. DIRECT WEBPAGE
        # ======================================================

        page_target = self._extract_page_target(command)

        if page_target:
            return self.read_page(page_target)

        # ======================================================
        # 5. DIRECT URL
        # ======================================================

        if (
            command.startswith("http://")
            or command.startswith("https://")
        ):
            return self.read_page(command)

        return None


# ==============================================================
# STANDALONE TEST
# ==============================================================

if __name__ == "__main__":

    router = WebRouter()

    print()
    print("=" * 70)
    print("V5 WEB ROUTER TEST")
    print("=" * 70)
    print()

    test_command = "what is the latest news about Python"

    print(f"Command: {test_command}")
    print()

    result = router.execute(test_command)

    print()
    print("FINAL RESPONSE:")
    print(result)
    print()