from typing import Dict, Any, List, Set

TECH_KEYWORDS: Set[str] = {
    "ai", "artificial intelligence", "ml", "machine learning", "llm", "genai",
    "software", "developer", "programming", "open source", "api",
    "cloud", "saas", "devops", "kubernetes", "docker",
    "data", "database", "distributed", "security", "infosec",
    "robotics", "hardware", "chip", "gpu", "semiconductor",
    "startup", "vc", "product", "engineering",
    "google", "apple", "microsoft", "amazon", "meta", "nvidia", "openai",
    "linux", "rust", "python", "typescript", "go", "java", "react"
}

def is_tech_story(story: Dict[str, Any], keywords: Set[str] = TECH_KEYWORDS) -> bool:

    """
    Determine the relevancy of collected news story. 

    Performs a simple keyword-based heuristic check by scanning
    the story's title and text for any known tech-related terms.

    Args:
        story: A dictionary representing a Hacker News `item` frmo the API, containing
            fields: `"title"`, `"text"`, `"url"`, `"score"`, etc.
        keywords: A set of lowercase strings to match against the story content.
            Defaults to TECH_KEYWORDS (defined above).

    Returns:
        True if the story contains one or more tech-related keywords
        in either the title or the text; otherwise False.

    """

    title = (story.get("title") or "").lower()
    text = (story.get("text") or "").lower()
    haystack = f"{title} {text}"
    return any(k in haystack for k in keywords)

def filter_tech_stories(
    stories: List[Dict[str, Any]],
    limit: int = 5,
    keywords: Set[str] = TECH_KEYWORDS
) -> List[Dict[str, Any]]:
    
    """
    Filter the list of collected news stories to only those that are relevant. 

    The function applies `is_tech_story()` to each story and returns the first
    `limit` items that match.

    Args:
        stories: list of news story objects (dicts) from hn API.
        limit: Maximum number of relevant stories to return (defaults to 5).
        keywords: Pre-defined set of key words that determine relevance

    Returns:
        A list of up to `limit` stories.

    """

    return [s for s in stories if is_tech_story(s, keywords=keywords)][:limit]
