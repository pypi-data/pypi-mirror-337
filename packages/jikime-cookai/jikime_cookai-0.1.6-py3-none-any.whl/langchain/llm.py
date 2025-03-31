from dotenv import load_dotenv
from openai import OpenAI
from langchain_ollama import ChatOllama
from langchain.schema import SystemMessage, HumanMessage

load_dotenv()

def response_from_llm(model: str, system: str, user: str) -> str:
    try:
        client = OpenAI()
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
            model=model,
            temperature=0.0,
        )
        return chat_completion.choices[0].message.content
    except Exception as e:
        raise RuntimeError(f"Error in LLM Chat response: {e}")

def response_from_llm_local(model: str, system: str, user: str) -> str:
  try:
    client = OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")
    completion = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
        temperature=0.0,
    )

    return completion.choices[0].message.content
  except Exception as e:
    raise RuntimeError(f"Error in LLM Chat response: {e}")
  
# langchain LLM 사용
def response_from_llm_langchain(model: str, system: str, user: str) -> str:
    try:
        llm = ChatOllama(model=model, temperature=0.0)
        messages = [
            SystemMessage(content=system),
            HumanMessage(content=user)
        ]
        response = llm.invoke(messages)
        return response.content
    except Exception as e:
        raise RuntimeError(f"Error in LLM Chat response: {e}")

def generate_speech_openai(text: str) -> bytes:
    try:
      # alloy, echo, fable, onyx, nova, and shimmer
      client = OpenAI()
      response = client.audio.speech.create(model="tts-1", voice="nova", input=text)
      return response.content
    except Exception as e:
      raise RuntimeError(f"Error in LLM Speach response: {e}")

