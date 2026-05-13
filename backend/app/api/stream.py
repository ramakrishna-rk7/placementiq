from fastapi import APIRouter, Body
from fastapi.responses import StreamingResponse
from app.services.rag import answer_question_stream
import json

router = APIRouter()

@router.post('/query/stream')
async def query_stream(payload: dict = Body(...)):
    question = payload.get('question', '')
    filters = payload.get('filters')

    def event_stream():
        for item in answer_question_stream(question, filters):
            yield f"data: {json.dumps(item)}\n\n"
        yield "data: [DONE]\n\n"

    return StreamingResponse(event_stream(), media_type='text/event-stream')
