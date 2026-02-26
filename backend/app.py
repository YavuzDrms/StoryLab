from fastapi import FastAPI
from pydantic import BaseModel
import random

app = FastAPI()

# Kullacının gireceği verinin modeli (test)
class DataModel(BaseModel):
    text: str # Kullanıcının gireceği veri

# Hikaye devamları (test) sonrasında bunu zaten ai yapacak
fake_story = [
    " Blablalbalblablablablablablalba",
    " BNJRNBJSNRIJBNSŞKRIJNBJŞNSRJNB",
    " HİKAYE DEVAMI"
]

@app.post("/create-story-test")
def get_data(data: DataModel):
    message = data.text # Kullanıcının girdisi
    
    print(f'Text reached backend: {message}')
    
    ai_story = random.choice(fake_story)
    full_story = f'Story: {message} {ai_story}'
    
    # Client e yanıt
    return {
        "situation" : "succesful",
        "story" : full_story,
        "story_lenght" : len(full_story)
    }

@app.get("/")
def dead_root():
    return {"Hello" : "World"}

@app.get("/items/{item_id}")
def read_item(item_id : int, q : str | None = None):
    return {"item_id": item_id, "q": q}