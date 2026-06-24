import json
import re

from transformers import pipeline

MODEL_NAME = "Qwen/Qwen2.5-1.5B-Instruct"

generator = pipeline(
    "text-generation",

    model=MODEL_NAME,

    device_map="auto",
)


def safe_json_parse(text):

    try:

        return json.loads(text)

    except Exception:

        try:

            match = re.search(
                r"\{.*\}",
                text,
                re.DOTALL
            )

            if match:

                return json.loads(
                    match.group()
                )

        except Exception:

            pass

    return None


def analyze_paper(
    user_query,

    paper
):

    prompt = f"""

You are an ML Research Advisor.

User Problem:

{user_query}

Paper:

{paper['title']}

Abstract:

{paper['abstract']}

Return ONLY JSON.

{{
 "paper_title":"",
 "what_is_this_about":"",
 "problem_trying_to_solve":"",
 "their_approach":"",
 "novelty":"",
 "advantages":[],
 "limitations":[],
 "why_should_i_read_this":""
}}

"""

    try:

        output = generator(

            prompt,

            max_new_tokens=400,

            do_sample=False

        )

        text = output[0][
            "generated_text"
        ]

        parsed = safe_json_parse(
            text
        )

        if parsed:

            return parsed

        return {

            "paper_title":

            paper["title"],

            "raw_output":

            text
        }

    except Exception as e:

        return {

            "paper_title":

            paper["title"],

            "error":

            str(e),

            "what_is_this_about":

            paper["abstract"],

            "why_should_i_read_this":

            "Fallback used."
        }