from dotenv import load_dotenv
import os
import groq
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
ai_model = os.getenv("AI_MODEL")

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

def generate_prompt(input) -> str:
    sys = system_prompt
    prompt = f"{system_prompt}\nHikaye: {input}"
    return prompt

client = groq.Groq(api_key=GROQ_API_KEY)

def get_ai_response(prompt: str, input: str):
    try:
        response = client.chat.completions.create(
            model=ai_model,
            messages=[{"role":"user","content":prompt}]
        )
        res = f"{input} {response.choices[0].message.content}"
        return res
    except Exception as e:
        print(f"{e}")
        return None