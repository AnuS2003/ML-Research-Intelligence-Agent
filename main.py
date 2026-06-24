from services.arxiv_service import fetch_arxiv_papers
from services.embedding_service import rank_papers
from services.llm_service import analyze_paper


def main():

    user_query = input(
        "\nEnter your ML problem:\n\n"
    )

    print("Fetching papers...")

    papers = fetch_arxiv_papers(
        user_query
    )

    print("Ranking papers...")

    top_papers = rank_papers(
        user_query,
        papers
    )

    print("\nTop papers:\n")

    for idx, paper in enumerate(
        top_papers,
        start=1
    ):

        print(
            f"{idx}. {paper['title']}"
        )

    print("\nGenerating analysis...\n")

    for paper in top_papers:

        result = analyze_paper(
            user_query,
            paper
        )

        print(result)

        print("-" * 80)


if __name__ == "__main__":

    main()