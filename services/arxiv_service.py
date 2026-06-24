from urllib.parse import quote
from urllib.request import urlopen
import xml.etree.ElementTree as ET


def preprocess_query(
    user_query,
):

    mapping = {

        "movie":

        (
            "movie recommendation systems "
            "content based filtering "
            "user preference modeling"
        )

    }

    lower = user_query.lower()

    for key, value in mapping.items():

        if key in lower:

            return value

    return user_query


def fetch_arxiv_papers(

    user_query,

    max_results=20

):

    search_query = preprocess_query(

        user_query

    )

    encoded = quote(

        search_query

    )

    url = (

        f"http://export.arxiv.org/api/query?"

        f"search_query=all:{encoded}"

        f"+AND+(cat:cs.LG+OR+cat:cs.AI)"

        f"&max_results={max_results}"

        f"&sortBy=relevance"

    )

    response = urlopen(url)

    xml_data = response.read()

    root = ET.fromstring(

        xml_data

    )

    namespace = {

        "atom":

        "http://www.w3.org/2005/Atom"

    }

    papers = []

    for entry in root.findall(

        "atom:entry",

        namespace

    ):

        papers.append(

            {

                "title":

                entry.find(

                    "atom:title",

                    namespace

                ).text.strip(),

                "abstract":

                entry.find(

                    "atom:summary",

                    namespace

                ).text.strip(),

                "published":

                entry.find(

                    "atom:published",

                    namespace

                ).text,

                "url":

                entry.find(

                    "atom:id",

                    namespace

                ).text,

            }

        )

    return papers