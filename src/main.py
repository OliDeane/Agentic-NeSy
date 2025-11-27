from clients.hn_client import HackerNewsClient
from clients.email_client import EmailClient
from services.summarizer_service import SummarizerService
from graph.digest_graph import build_digest_graph  

def main():
    """
    Entrypoint for running the agentic pipeline.

    Instantiates required clients and services, builds the LangGraph workslow, 
    executes digest generation, emails it, prints the digest to terminal. 
    """
    hn_client = HackerNewsClient()
    email_client = EmailClient("email_config.json")
    summarizer = SummarizerService()

    graph = build_digest_graph(
        hn_client=hn_client,
        email_client=email_client,
        summarizer=summarizer,
        top_fetch_limit=60,
        relevant_limit=5,
    )

    final_state = graph.invoke({})
    print("\n=== Digest Sent ===\n")
    print(final_state["report_md"])

if __name__ == "__main__":
    main()