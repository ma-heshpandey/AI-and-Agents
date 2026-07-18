import json
import urllib.parse
import urllib.request
from strands import tool


@tool
def web_search(query: str) -> str:
    """
    Search the web for information using DuckDuckGo Instant Answer API.
    Returns relevant information for the given query.
    """
    encoded = urllib.parse.quote_plus(query)
    url = f"https://api.duckduckgo.com/?q={encoded}&format=json&no_html=1&skip_disambig=1"

    try:
        req = urllib.request.Request(url, headers={"User-Agent": "course-creation-agent/1.0"})
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode())

        results = []

        if data.get("AbstractText"):
            results.append(f"Summary: {data['AbstractText']}")
            if data.get("AbstractSource"):
                results.append(f"Source: {data['AbstractSource']}")

        if data.get("RelatedTopics"):
            results.append("\nRelated Topics:")
            for topic in data["RelatedTopics"][:5]:
                if isinstance(topic, dict) and topic.get("Text"):
                    results.append(f"  - {topic['Text']}")

        if data.get("Answer"):
            results.append(f"\nDirect Answer: {data['Answer']}")

        if not results:
            results.append(f"No direct results found for '{query}'. Consider refining your search.")

        return "\n".join(results)

    except Exception as e:
        return f"Search failed for '{query}': {str(e)}. Use your knowledge to research this topic."
