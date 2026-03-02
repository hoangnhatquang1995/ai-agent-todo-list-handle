import os

from langchain.chat_models import BaseChatModel, init_chat_model
from langchain_openai.chat_models import ChatOpenAI
from langchain_classic.chat_models.ollama import ChatOllama
from langchain_google_genai.chat_models import ChatGoogleGenerativeAI

from enum import Enum
import settings
class LLM:
    class Cloud(Enum):
        GOOGLE_CHAT = "genai"   # Require GOOGLE_API_KEY in .env to used
        OPEN_AI = "openai"      # Require OPENAI_API_KEY in .env to used
        DEEPSEEK = "deepseek"   # Require DEEPSEEK_API_KEY in .env to used
    class Local(Enum):
        OLLAMA = "ollama"

def get_llm (llm : LLM.Cloud | LLM.Local, model : str  = "" ) -> BaseChatModel :
    if llm == LLM.Cloud.GOOGLE_CHAT:
        return ChatGoogleGenerativeAI(
            model=model,
            temperature = settings.LLM_TEMPERATURE,
            max_tokens = settings.LLM_MAX_TOKENS
        )
    elif llm == LLM.Cloud.OPEN_AI:
        return ChatOpenAI(
            model = model,
            temperature= settings.LLM_TEMPERATURE,
            max_completion_tokens= settings.LLM_MAX_TOKENS
        )
    elif llm == LLM.Cloud.DEEPSEEK:
        return init_chat_model(
            model = model,
            model_provider= "deepseek",
            api_key = os.getenv("DEEPSEEK_API_KEY"),
            temperature= settings.LLM_TEMPERATURE,
            max_tokens = settings.LLM_MAX_TOKENS
        )
    elif llm == LLM.Local.OLLAMA :
        return ChatOllama(
            model= model,
            temperature= settings.LLM_TEMPERATURE
        )
    else :
        raise ValueError("Unsupported LLM type")


llm_module = get_llm(
    LLM.Cloud.DEEPSEEK, model="deepseek-chat"
)