from fastapi import APIRouter, Depends
from app.api.deps import require_roles
from app.models.user import User
from app.schemas import GenerateQuestions
from app.services.gemini_service import generate_questions
router = APIRouter(prefix="/ai", tags=["AI tools"])
@router.post("/generate-questions")
async def generate(payload: GenerateQuestions, user: User = Depends(require_roles("teacher"))):
    questions = await generate_questions(payload.topic, payload.count, payload.difficulty, payload.question_type)
    return {"topic": payload.topic, "count": len(questions), "questions": questions}
