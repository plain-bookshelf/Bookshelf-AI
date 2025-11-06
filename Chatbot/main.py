from fastapi import APIRouter
from .models import Chat
from .llm_chain import chain_with_memory
from .embeddings import retrieve_context
from fastapi.responses import StreamingResponse

router = APIRouter(prefix="/chatbot", tags=["chatbot"])

@router.post("/Bookshelf_AI")
async def chat(ch: Chat):
    session_id = ch.user_id
    query = ch.user_said
    context = retrieve_context(query)

    async def agen():
        try:
            # astream: 비동기 스트리밍
            async for chunk in chain_with_memory.astream(
                {"input": query, "context": context},
                config={"configurable": {"session_id": session_id}},
            ):
                # chunk 타입이 문자열이거나 AIMessageChunk일 수 있음
                # 문자열이면 그대로, 메시지 청크면 content만 꺼내 전송
                piece = getattr(chunk, "content", chunk)
                if piece:
                    # 줄바꿈은 선택사항. 보기 좋게 한 줄씩 밀어내고 싶다면 붙이세요.
                    yield str(piece)
        except Exception as e:
            yield f"\n[오류] {e}\n"

    # text/event-stream(서버센트 이벤트)로 보내고 싶다면 media_type을 바꾸세요.
    return StreamingResponse(agen(), media_type="text/plain")

# @app.post("/Bookshelf_AI")
# async def chat(ch: Chat):
#     session_id = ch.user_id
#     query = ch.user_said
#     context = retrieve_context(query)
#     result = chain_with_memory.invoke(
#         {"input": query, "context": context},
#         config={"configurable": {"session_id": session_id}}
#     )
#
#     return {"response": result.content}
    # print(context)
    # return {"text": context}

# uvicorn Chatbot.main:app --host 0.0.0.0 --port 8000
# uvicorn Chatbot.main:app --reload --host 127.0.0.1 --port 8000
# uvicorn Chatbot.main:app --host 0.0.0.0 --port 8000 --reload

