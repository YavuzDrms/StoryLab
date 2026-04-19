from dotenv import load_dotenv
import os
import groq
from customtkinter import StringVar
from enum import Enum

load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
ai_model_llama33 = os.getenv("AI_MODEL_LLAMA33")
ai_model_llama31 = os.getenv("AI_MODEL_LLAMA31")

system_prompt = (
    "Sen Türk edebiyatına hakim, usta bir yazarsın. "
    "Kullanıcının gönderdiği hikayeyi, dil bilgisi kurallarına uyarak, "
    "zengin betimlemelerle ve akıcı bir Türkçeyle devam ettir. "
    "Sadece hikayenin devamını yaz, başka bir açıklama ekleme."
    "Türkçe dili dışında hiç bir kelime kullanma."
    "Kullanıcının köşeli parantez [] içine aldığı yazılarda sana hikayeyi nasıl bir tonda gitmen gerektiğini söyleyecek,"
    "Örneğin gerilimli, hüzünlü veya neşeli bir biçimde."
    "Bunları dikkate alarak devamını getir. Eğer paragrafta [] yoksa görmezden gel."
    "Kullanıcının süslü parantez {} içine aldığı yerlerde sana hikayeyi nasıl bitirmen gerektiğini söyleyecek,"
    "Bunu dikkate alarak başlangıç ve sonunu bildiğin hikayenin ortasını ve olay düğümünü oluştur."
    "Eğer paragrafta {} yoksa görmezden gel."
)

class Models(Enum):
    LLAMA33 = 1
    LLAMA31 = 2

def generate_prompt(input) -> str:
    sys = system_prompt
    prompt = f"{sys}\nHikaye: {input}"
    return prompt

client = groq.Groq(api_key=GROQ_API_KEY)

ai_model_selected : Models = Models.LLAMA33

def get_ai_response(prompt: str, input: str):
    m: str
    if ai_model_selected.name == "LLAMA33":
        m = ai_model_llama33
    if ai_model_selected.name == "LLAMA31":
        m = ai_model_llama31
    
    try:
        response = client.chat.completions.create(
            model=m,
            messages=[{"role":"user","content":prompt}]
        )
        res = f"{input} {response.choices[0].message.content}"
        return res
    except Exception as e:
        print(f"{e}")
        return None