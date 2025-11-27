from typing import Dict, Any, List

def compile_report(
    summaries: List[Dict[str, Any]],
    trends_summary: str
) -> str:
    """
    Assembles the digest complete with an introductory statement, a summary of trends over the collected news
    story, a list of summaries for top stories foudn to be relevant. 

    Args:
        summaries: list of dicts containing summarised stories, with fields title (str), summary (str), 
            url (str), score (int) frmo the HN site. 
        trend_summary: paragraph containing summary of cross-stroy trends
    
    Returns:
        Markdown string containing the complete digest.
    
    """
    x = len(summaries)

    lines = [
        "# Hacker News Tech Digest",
        "",
        f"Welcome to your daily Hacker News Tech Digest. We’ve found {x} stories that we think you might be interested in today.",
        "",
        "## Trends & Themes",
        trends_summary or "No trend summary available.",
        "",
        "## Top Stories",
        ""
    ]

    if x == 0:
        lines.append("No relevant tech stories found today.")
    else:
        for idx, s in enumerate(summaries, start=1):
            lines.append(f"### {idx}. {s['title']}")
            if s.get("url"):
                lines.append(f"- Link: {s['url']}")
            if s.get("score") is not None:
                lines.append(f"- HN Score: {s['score']}")
            lines.append(f"- Summary: {s['summary']}")
            lines.append("")

    return "\n".join(lines)
