from fastapi import FastAPI
from pydantic import BaseModel

# Kullacının gireceği verinin modeli (test)
class DataModel(BaseModel):
    text: str # Kullanıcının gireceği veri

app = FastAPI()

@app.post("/test-data")
def get_data(data: DataModel):
    message = data.text # Kullanıcının girdisi
    
    print(f'Text reached backend: {message}')
    
    # Client e yanıt
    return {
        "situation" : "succesful",
        "input" : message,
        "input_lenght" : len(message)
    }

@app.get("/")
def dead_root():
    return {"Hello" : "World"}

@app.get("/items/{item_id}")
def read_item(item_id : int, q : str | None = None):
    return {"item_id": item_id, "q": q}