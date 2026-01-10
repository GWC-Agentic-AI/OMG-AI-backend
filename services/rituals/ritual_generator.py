import os
import json
from datetime import datetime
from tavily import TavilyClient
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

TAVILY_API_KEY = os.environ.get("TAVILY_API_KEY")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

tavily = TavilyClient(api_key=TAVILY_API_KEY)
client = OpenAI(api_key=OPENAI_API_KEY)


def generate_ai_ritual(
    user_name: str,
    dob: str,
    tob: str,
    birth_city: str,
    birth_country: str,
    today_date: str,
    raasi: str | None,
):
    search_query = (
        f"Hindu Panchang {today_date}: "
        f"Tithi, Nakshatra, Yoga, Karana, Choghadiya for India"
    )

    search_result = tavily.search(
        query=search_query,
        search_depth="advanced",
    )

    context_data = "\n".join(
        res["content"] for res in search_result.get("results", [])
    )

    system_prompt = f"""
You are an expert Vedic Astrologer.
Create a personalized daily ritual and parikaram plan.

USER PROFILE:
- Name: {user_name}
- Birth: {dob} at {tob}
- Birth Place: {birth_city}, {birth_country}
- Raasi: {raasi or "Determine from birth data"}
- Date: {today_date}

PANCHANG CONTEXT (REFERENCE ONLY):
{context_data}

Follow STRICT JSON output. Do NOT add explanations.
"""

    response = client.chat.completions.create(
        model="gpt-4.1",
        temperature=0.3,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": "Generate today's ritual and parikaram plan."},
        ],
        response_format={"type": "json_object"},
    )

    return json.loads(response.choices[0].message.content)
