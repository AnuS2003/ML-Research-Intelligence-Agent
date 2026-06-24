from sentence_transformers import SentenceTransformer
from sentence_transformers.util import cos_sim


model = SentenceTransformer(
    "sentence-transformers/all-MiniLM-L6-v2"
)


def rank_papers(user_query, papers):

    abstracts = [paper["abstract"] for paper in papers]

    query_embedding = model.encode(
        user_query,
        convert_to_tensor=True
    )

    abstract_embeddings = model.encode(
        abstracts,
        convert_to_tensor=True
    )

    similarities = cos_sim(
        query_embedding,
        abstract_embeddings
    )[0]

    for paper, score in zip(papers, similarities):

        paper["score"] = float(score)

    ranked = sorted(
        papers,
        key=lambda x: x["score"],
        reverse=True
    )

    return ranked[:3]