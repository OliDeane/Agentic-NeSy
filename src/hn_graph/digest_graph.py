from typing import List, Dict, Any, TypedDict
from langgraph.graph import StateGraph, END

from clients.hn_client import HackerNewsClient
from clients.email_client import EmailClient
from services.filter_service import filter_tech_stories
from services.summarizer_service import SummarizerService
from services.report_service import compile_report


class HNState(TypedDict, total=False):
    top_ids: List[int]
    stories: List[Dict[str, Any]]
    relevant_stories: List[Dict[str, Any]]
    summaries: List[Dict[str, Any]]
    trends_summary: str
    report_md: str
    email_sent: bool


def build_digest_graph(
    hn_client: HackerNewsClient,
    email_client: EmailClient,
    summarizer: SummarizerService,
    *,
    top_fetch_limit: int = 60,
    relevant_limit: int = 5,
):
    """
    Build and return a compiled LangGraph app that:
      - pulls top HN stories
      - filters relevant tech stories
      - summarizes top N
      - summarizes cross-story trends
      - compiles report
      - emails report
    """

    # ----------------------------
    # Graph nodes (closures capture dependencies)
    # ----------------------------
    def get_top_ids(state: HNState) -> HNState:
        top_ids = hn_client.top_story_ids(limit=top_fetch_limit)
        return {"top_ids": top_ids}

    def get_stories(state: HNState) -> HNState:
        stories = []
        for sid in state["top_ids"]:
            item = hn_client.get_item(sid)
            if item and item.get("type") == "story":
                stories.append(item)
        return {"stories": stories}

    def filter_tech_node(state: HNState) -> HNState:
        relevant = filter_tech_stories(state["stories"], limit=relevant_limit)
        return {"relevant_stories": relevant}

    def summarize_stories(state: HNState) -> HNState:
        summaries = [summarizer.summarize_story(s) for s in state["relevant_stories"]]
        return {"summaries": summaries}

    def summarize_trends(state: HNState) -> HNState:
        trends = summarizer.summarize_trends(state["summaries"])
        return {"trends_summary": trends}

    def compile_report_node(state: HNState) -> HNState:
        report_md = compile_report(
            summaries=state["summaries"],
            trends_summary=state.get("trends_summary", "")
        )
        return {"report_md": report_md}

    def email_report(state: HNState) -> HNState:
        subject = f"HN Tech Digest (Top {relevant_limit} Relevant Stories)"
        email_client.send(subject, state["report_md"])
        return {"email_sent": True}

    # ----------------------------
    # Wire graph
    # ----------------------------
    g = StateGraph(HNState)

    g.add_node("get_top_ids", get_top_ids)
    g.add_node("get_stories", get_stories)
    g.add_node("filter_tech", filter_tech_node)
    g.add_node("summarize_stories", summarize_stories)
    g.add_node("summarize_trends", summarize_trends)
    g.add_node("compile_report", compile_report_node)
    g.add_node("email_report", email_report)

    g.set_entry_point("get_top_ids")
    g.add_edge("get_top_ids", "get_stories")
    g.add_edge("get_stories", "filter_tech")
    g.add_edge("filter_tech", "summarize_stories")
    g.add_edge("summarize_stories", "summarize_trends")
    g.add_edge("summarize_trends", "compile_report")
    g.add_edge("compile_report", "email_report")
    g.add_edge("email_report", END)

    return g.compile()
