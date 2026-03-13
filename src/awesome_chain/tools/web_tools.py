"""
Web-related tools for searching and fetching content.
"""

import json
from typing import Optional

from src.awesome_chain.core.tool_registry import tool


@tool
def search_web(query: str, num_results: int = 5) -> str:
    """
    Search the web using DuckDuckGo.

    Args:
        query: Search query
        num_results: Number of results to return

    Returns:
        Search results
    """
    try:
        from ddgs import DDGS
        
        results = []
        with DDGS() as ddgs:
            search_results = ddgs.text(
                query,
                max_results=num_results
            )
            
            for result in search_results:
                results.append({
                    "title": result.get("title", ""),
                    "url": result.get("href", ""),
                    "snippet": result.get("body", "")
                })
        
        return json.dumps(results, indent=2, ensure_ascii=False)

    except Exception as e:
        return f"Error searching web: {str(e)}"


@tool
def fetch_url(url: str) -> str:
    """
    Fetch content from a URL.

    Args:
        url: URL to fetch

    Returns:
        URL content
    """
    import requests
    from urllib.parse import urlparse

    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }

        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()

        content_type = response.headers.get('content-type', '')
        
        if 'text/html' in content_type:
            from bs4 import BeautifulSoup
            soup = BeautifulSoup(response.text, 'html.parser')
            for script in soup(['script', 'style', 'nav', 'footer', 'header']):
                script.decompose()
            text = soup.get_text(separator='\n', strip=True)
            lines = [line.strip() for line in text.split('\n') if line.strip()]
            return '\n'.join(lines[:500])
        elif 'application/json' in content_type:
            return json.dumps(response.json(), indent=2, ensure_ascii=False)
        else:
            return response.text[:10000]

    except requests.exceptions.Timeout:
        return f"Error: Request to {url} timed out after 30 seconds"
    except requests.exceptions.RequestException as e:
        return f"Error fetching URL {url}: {str(e)}"
    except Exception as e:
        return f"Error processing content from {url}: {str(e)}"


# Example of integrating with Tavily API (uncomment and configure):
# @tool
# def tavily_search(query: str, search_depth: str = "basic") -> str:
#     """Search the web using Tavily API."""
#     from tavily import TavilyClient
#
#     client = TavilyClient(api_key=settings.TAVILY_API_KEY)
#     result = client.search(query, search_depth=search_depth)
#     return json.dumps(result, indent=2)


def register_web_tools() -> None:
    """Register all web tools manually."""
    # Tools are already registered via decorators
    pass
