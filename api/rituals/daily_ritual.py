from datetime import datetime
from fastapi import APIRouter, HTTPException

from schemas.rituals.ritual_models import RitualRequest, RitualResponse
from services.rituals.ritual_generator import generate_ai_ritual
from services.rituals.ritual_repository import (
    fetch_today_ritual,
    fetch_user_profile,
    save_ritual,
)

router = APIRouter()


@router.post("/daily", response_model=RitualResponse)
def get_or_generate_ritual(req: RitualRequest):
    today_date = datetime.utcnow().strftime("%Y-%m-%d")

    cached = fetch_today_ritual(req.user_id, today_date)
    if cached:
        return {
            "status": f"already_generated for {today_date}",
            "date": today_date,
            "data": cached,
        }

    user = fetch_user_profile(req.user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User profile not found")

    ritual_data = generate_ai_ritual(
        user_name=user[0],
        dob=str(user[1]),
        tob=str(user[2]),
        birth_city=user[3],
        birth_country=user[4],
        today_date=today_date,
        raasi=user[5],
    )

    save_ritual(req.user_id, today_date, ritual_data)

    return {
        "status": "newly_generated",
        "date": today_date,
        "data": ritual_data,
    }
