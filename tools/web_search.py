from ddgs import DDGS


def web_search(
    query: str,
    engine: str = "duckduckgo",
    safesearch: str = "moderate",
    region: str = "wt-wt",
    max_results: int = 5,
):
    """
    Performs a web search using DuckDuckGo, Google, Bing, etc.

    For the model: Use this as a primary tool to answer questions about current
    events, general knowledge, or anything you don't know. Use it when the user
    asks you to "google" something, or "look it up". Formulate an effective and
    concise search query based on the user's prompt. Utilize search operators
    like `site:`, `filetype:`, `intitle:`, etc. for more precise results.

    Args:
        query (str): The search query.
        engine (str, optional): The search engine to use. Defaults to "duckduckgo".
            Supported engines include: duckduckgo, google, bing, yahoo, yandex, brave, startpage.
            See ddgs documentation for a full list.
        safesearch (str, optional): The safesearch level. Defaults to "moderate".
            Options: off, moderate, strict.
        region (str, optional): The region to search in (ISO 3166-1 alpha-2 code). Defaults to "wt-wt" (World).
        max_results (int, optional): The maximum number of results to return. Defaults to 5.

    Returns:
        dict: A JSON list of search result objects. Each object has a 'title',
              'href', and 'body' (snippet). You should parse this, present a
              summary of the results to the user, and use the 'href' links for
              subsequent calls to this tool if more details are needed.
    """
    with DDGS() as ddgs:
        results = ddgs.text(
            query,
            max_results=max_results,
            safesearch=safesearch,
            region=region,
            engine=engine,
        )
    return results
