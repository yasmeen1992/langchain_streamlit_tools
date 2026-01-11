import os
from dotenv import load_dotenv
load_dotenv()
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import create_agent
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.messages import HumanMessage
from langchain_core.messages import SystemMessage

# Tools الخاصة بيك
from tools import (
    multi_web_search,
    youtube_search,
    weather_search,
    news_search,
)

# -----------------------
# API Keys
# -----------------------
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")
NEWS_API_KEY = os.getenv("NEWS_API_KEY")

# ----------------------
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash-lite",  # مودل قوي مجاني
     google_api_key=GOOGLE_API_KEY,
    temperature=0.7
)

# -----------------------
# الأدوات
# -----------------------
tools = [
    multi_web_search,
    youtube_search,
    weather_search,
    news_search,
    
]



# -----------------------
# إنشاء ReAct Agent (مهم جدًا)
# -----------------------
agent = create_agent(
    llm,
    tools,

)



# -----------------------
# إعداد الذاكرة لكل session
# -----------------------
store = {}

def get_session_history(session_id: str):
    if session_id not in store:
        store[session_id] = InMemoryChatMessageHistory()
    return store[session_id]

# -----------------------
# Agent مع Memory
# -----------------------
agent_with_memory = RunnableWithMessageHistory(
    agent,
    get_session_history,
    input_messages_key="messages",  # مهم جدًا لـ Gemini
    history_messages_key="chat_history",
)
SYSTEM_MESSAGE = SystemMessage(
    content="""
أنت مساعد ذكي.
- يمكنك الإجابة مباشرة على الأسئلة العامة والدردشة (مثل: كيف حالك).
- استخدم الأدوات فقط عندما يكون السؤال يحتاج معلومات خارجية.
- لا تستخدم أي أداة غير مذكورة لك.
- لا تطلب من المستخدم استخدام الأدوات بنفسه.
- إذا لم تنجح الأداة، أجب نصيًا واذكر أن البيانات غير متاحة حاليًا.
"""
)

# -----------------------
# دالة الاستخدام من أي مكان
# -----------------------
def get_agent_response(query: str) -> str:
    """
    ترجع الرد من الـ Agent
    """
    if not query or not query.strip():
        return "الرجاء كتابة سؤال أولاً."

    try:
        result = agent_with_memory.invoke(
            { 
                 "messages": [
                SYSTEM_MESSAGE,
                HumanMessage(content=query.strip())
            ]
        },
            config={"configurable": {"session_id": "default"},
                      "tool_choice": "auto"
                    }
        )

        # أغلب الوقت ده الصح
        return result["messages"][-1].content

    except Exception as e:
        return f"Agent error: {e}"
