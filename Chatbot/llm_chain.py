from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.runnables import RunnableWithMessageHistory
from .config import OLLAMA_MODEL
from langchain_community.chat_models import ChatOllama
from .config import GEMINI_MODEL, KEY
from langchain_google_genai import ChatGoogleGenerativeAI

#--------------------
# 제미나이 버전
llm = ChatGoogleGenerativeAI(
    model=GEMINI_MODEL,
    temperature=0.5,
    api_key=KEY
    # 선택: safety_settings, generation_config 등 추가 가능
    # generation_config={"max_output_tokens": 1024}
)

prompt = ChatPromptTemplate.from_messages([
    ("system",
     "너는 한국어로 책을 추천하거나 설명하는 도우미야. "
     "이전 대화를 기억해서 자연스럽게 이어가고, "
     "책과 관련 없는 질문이면 책 관련 대화를 유도해."),
    MessagesPlaceholder(variable_name="chat_history"),
    ("human",
     "다음은 관련 책 정보야:\n\n{context}\n\n사용자 질문: {input}\n\n"
     "이전 대화 맥락을 고려했을 때, 사용자의 질문이 그 책, 저 책, 전에, 근데 등 이전 대화 맥락과 연결되는 질문이면 반드시 이전 정보나 대화를 바탕으로 대답하고, "
     "새로운 책을 추천받으려하는 등의 경우에만 새로 들어온 관련 책 정보를 바탕으로 대답해줘. "
     "책을 추천할 땐 반드시 관련 책 정보에 있는 책들 중에서 내용이 가장 비슷한 것을 추천해."
     "또한 단답으로 대답해도 좋으니(절대 단답이 좋다는 뜻은 아니야 그냥 괜찮다는거지) 무조건 책을 추천하거나 설명하겠다는 관념은 버려. "
     "또한 관련 책 정보에 없더라도 니가 알고있는 내용이면 답해줘"
     "그리고 사용자가 질문한 내용에 대해 제공된 책 정보에 원하는 것이 없더라도 이전 대화 내용에 있을 확률이 매우 높으니 이전 대화 내용을 반드시 참고하도록 해"
     )
])

chain = prompt | llm

# 세션별 메모리
store = {}
def get_session_history(session_id: str):
    if session_id not in store:
        store[session_id] = InMemoryChatMessageHistory()
    return store[session_id]

chain_with_memory = RunnableWithMessageHistory(
    chain,
    get_session_history,
    input_messages_key="input",
    history_messages_key="chat_history"
)


#-------------------------------------
# 올라마 버전
# llm = ChatOllama(
#     model=OLLAMA_MODEL,
#     temperature=0.5,
#     keep_alive="30m",
#     num_predict=1024,
# )
#
# prompt = ChatPromptTemplate.from_messages([
#     ("system",
#      "너는 한국어로 책을 추천하고 설명하는 도우미야. "
#      "이전 대화를 기억해서 자연스럽게 이어가고, "
#      "책과 관련 없는 질문이면 책 관련 대화를 유도해."),
#     MessagesPlaceholder(variable_name="chat_history"),
#     ("human",
#      "다음은 관련 책 정보야:\n\n{context}\n\n사용자 질문: {input}\n\n"
#      "이전 대화 맥락을 고려했을 때, 사용자의 질문이 그 책, 저 책, 전에, 근데 등 이전 대화 맥락과 연결되는 질문이면 반드시 이전 정보나 대화를 바탕으로 대답하고, "
#      "새로운 책을 추천받으려는 등의 경우에만 새로 들어온 관련 책 정보를 바탕으로 대답해줘. "
#      "책을 추천할 땐 반드시 관련 책 정보에 있는 책들 중에서 내용이 가장 비슷한 것을 추천해."
#      "또한 단답으로 대답해도 좋으니 무조건 책을 추천하거나 설명하겠다는 관념은 버려. "
#      "그리고 절대 관련 책 정보에 없는 책을 추천하거나 지어내지마"
#      "사용자의 질문과 관련 책 정보간의 관련도가 거의 없으면 그 책이 현재 데이터베이스에 없다고 말해줘"
#      )
# ])
#
# chain = prompt | llm
#
# store = {}
#
# def get_session_history(session_id: str):
#     if session_id not in store:
#         store[session_id] = InMemoryChatMessageHistory()
#     return store[session_id]
#
# chain_with_memory = RunnableWithMessageHistory(
#     chain,
#     get_session_history,
#     input_messages_key="input",
#     history_messages_key="chat_history"
# )