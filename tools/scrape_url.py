import requests
from bs4 import BeautifulSoup


class ScrapeError(Exception):
    pass


def scrape_url(url: str):
    """
    Fetches the main text content from a given URL.

    For the model: Use this tool to get detailed information from a webpage link,
    provided by the user or by the 'web_search' tool. Do not invent URLs; only
    use URLs provided by the user or by a previous 'web_search' tool call.

    Args:
        url (str): The full URL to scrape (e.g., "https://example.com/article").

    Returns:
        str: The extracted text content, including the page title. You should
             read this content and summarize the key points for the user.

    Raises:
        ScrapeError: If the URL cannot be fetched, is not HTML, or cannot be parsed.
    """
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) Gecko/20100101 Firefox/141.0"
        }
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        if "text/html" not in response.headers.get("Content-Type", ""):
            raise ScrapeError(
                f"Content type is not text/html, but '{response.headers.get('Content-Type', '')}'."
            )

        soup = BeautifulSoup(response.text, "html.parser")
        for tag in ["script", "style", "nav", "header", "footer", "aside"]:
            for s in soup.select(tag):
                s.decompose()

        main_content = soup.find("article") or soup.find("main") or soup.body
        text = main_content.get_text(separator="\n", strip=True)
        page_title = soup.title.string if soup.title else "No title found."

        return f"Title: {page_title}\n\nContent:\n{text}"
    except requests.exceptions.RequestException as e:
        raise ScrapeError(f"Could not retrieve URL: {e}")
    except Exception as e:
        raise ScrapeError(f"An error occurred during scraping: {e}")
