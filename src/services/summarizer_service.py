from typing import Dict, Any, List
from langchain_google_genai import ChatGoogleGenerativeAI


class SummarizerService:
    """
    A class of summarizers: one for individual stories, one for trends over the colelcted stories.
    """

    def __init__(self, model: str = "gemini-2.5-flash", temperature: float = 0.2):
        self.llm = ChatGoogleGenerativeAI(model=model, temperature=temperature)

    def summarize_story(self, story: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate short summary for single story

        Args: 
            story: dictionary of a new story item.
        
        Returns:
            Dict containing summary output with title, url, score fields. 
        """

        title = story.get("title")
        url = story.get("url")
        score = story.get("score")

        prompt = f"""
Summarize this Hacker News tech story in 2–3 sentences.
Focus on what happened, why it matters to a tech company, and any notable implications.

Title: {title}
URL: {url}
HN Score: {score}
""".strip()

        resp = self.llm.invoke(prompt)
        return {
            "title": title,
            "url": url,
            "score": score,
            "summary": resp.content.strip()
        }

    def summarize_trends(self, summaries: List[Dict[str, Any]]) -> str:
        """
        Identify and summarize trends across collected story summaries.

        Args:
            summaries: a list of summaries of dictionary form (keys: title and summary)

        Returns:
            string containing generated summary

        """
        bullets = [f"- {s['title']}: {s['summary']}" for s in summaries]

        prompt = f"""
You are writing a short 'Trends & Themes' section for a daily tech digest.

Based on the stories below, identify:
1) 1–3 high-level trends or recurring themes,
2) why they matter for a modern tech company,
3) any suggested actions or watch-outs.

Keep it concise (3–5 sentences total).

Stories:
{chr(10).join(bullets)}
""".strip()

        resp = self.llm.invoke(prompt)
        return resp.content.strip()
