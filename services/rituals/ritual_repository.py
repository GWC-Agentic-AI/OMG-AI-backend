import json
from db.session import get_db
from config import settings

APP_DB_NAME = settings.AI_DB


def fetch_today_ritual(user_id: int, today_date: str):
    with get_db(APP_DB_NAME) as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT ritual_json
                FROM daily_rituals
                WHERE user_id = %s AND ritual_date = %s
                """,
                (user_id, today_date),
            )
            row = cur.fetchone()

    return row[0] if row else None


def fetch_user_profile(user_id: int):
    with get_db(APP_DB_NAME) as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT user_name, dob, tob, birth_city, birth_country, raasi
                FROM ritual_users
                WHERE user_id = %s
                """,
                (user_id,),
            )
            row = cur.fetchone()

    return row


def save_ritual(user_id: int, today_date: str, ritual_data: dict):
    with get_db(APP_DB_NAME) as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO daily_rituals (user_id, ritual_date, ritual_json)
                VALUES (%s, %s, %s)
                """,
                (user_id, today_date, json.dumps(ritual_data)),
            )
        conn.commit()
