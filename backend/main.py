from fastapi import FastAPI
from fastapi import FastAPI
from fastapi.responses import JSONResponse
import datetime

vocabularies_dict = {
    1: {'word_id': 1, 'word': 'Ephemeral', 'definition': 'Lasting for a very short time.', 'sentence': 'The beauty of cherry blossoms is ephemeral.', 'start_date': str(datetime.date.today()), 'current_memory_index': 1},
    2: {'word_id': 2, 'word': 'Pernicious', 'definition': 'Having a harmful effect, especially in a gradual or subtle way.', 'sentence': 'The pernicious effects of smoking are well-documented.', 'start_date': str(datetime.date.today()), 'current_memory_index': 2},
    3: {'word_id': 3, 'word': 'Ameliorate', 'definition': 'Make (something bad or unsatisfactory) better.', 'sentence': 'The new policies aim to ameliorate the working conditions.', 'start_date': str(datetime.date.today()), 'current_memory_index': 3},
    4: {'word_id': 4, 'word': 'Obfuscate', 'definition': 'Render obscure, unclear, or unintelligible.', 'sentence': 'The politician speech was deliberately obfuscated.', 'start_date': str(datetime.date.today()), 'current_memory_index': 4},
    5: {'word_id': 5, 'word': 'Plethora', 'definition': 'A large or excessive amount of (something).', 'sentence': 'The store offers a plethora of options for shoppers.', 'start_date': str(datetime.date.today()), 'current_memory_index': 5}
}

app = FastAPI()

@app.get('/')
def read_root():
    return {'Hello': 'World'}

@app.post('/upload')
def upload_db():
    return {'status': 'success'}

@app.post('/puch_in')
def puch_in():
    return {'status': 'success'}

@app.get('/today')
def today():
    return JSONResponse(content=vocabularies_dict)
