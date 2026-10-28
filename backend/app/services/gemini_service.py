import json, re
import httpx
from fastapi import HTTPException
from app.core.config import settings
async def generate_questions(topic: str, count: int, difficulty: str, question_type: str) -> list[dict]:
    if not settings.gemini_api_key:
        raise HTTPException(status_code=503, detail="AI is not configured. Set GEMINI_API_KEY in backend/.env.")
    prompt = f'''Create {count} educational questions about {topic}. Difficulty: {difficulty}. Type: {question_type}.
Return ONLY a JSON array of objects with keys: type (mcq or short_answer), question, options (array), answer, explanation, marks (integer).
For MCQs, give 4 options and make answer equal the correct option text.'''
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{settings.gemini_model}:generateContent"
    try:
        async with httpx.AsyncClient(timeout=45) as client:
            response = await client.post(url, params={"key": settings.gemini_api_key}, json={
                "contents":[{"parts":[{"text":prompt}]}],
                "generationConfig":{"temperature":0.3,"responseMimeType":"application/json"}})
            response.raise_for_status()
        raw = response.json()["candidates"][0]["content"]["parts"][0]["text"]
        match = re.search(r"\[[\s\S]*\]", raw)
        if not match: raise ValueError("No JSON array")
        values = json.loads(match.group(0)); result = []
        for q in values[:count]:
            if not isinstance(q, dict) or not isinstance(q.get("question"), str) or "answer" not in q: continue
            opts = q.get("options", [])
            result.append({"type": q.get("type","mcq") if q.get("type") in ("mcq","short_answer") else "short_answer",
                "question": q["question"][:2000], "options": [str(x)[:500] for x in opts[:6]] if isinstance(opts,list) else [],
                "answer": str(q["answer"])[:1000], "explanation": str(q.get("explanation",""))[:2000],
                "marks": max(1,min(int(q.get("marks",1)),100))})
        if not result: raise ValueError("Invalid generated questions")
        return result
    except httpx.HTTPStatusError as exc:
        raise HTTPException(status_code=502, detail=f"AI provider returned HTTP {exc.response.status_code}")
    except (httpx.HTTPError, KeyError, IndexError, ValueError, TypeError, json.JSONDecodeError):
        raise HTTPException(status_code=502, detail="AI response could not be processed. Please retry.")
