from fastapi import FastAPI, UploadFile
from fastapi.responses import JSONResponse
import datetime
from io import BytesIO
import os
import sqlite3
import sqlite3

# vocabularies_dict = {
#     1: {'word_id': 1, 'word': 'Ephemeral', 'definition': 'Lasting for a very short time.', 'sentence': 'The beauty of cherry blossoms is ephemeral.', 'start_date': str(datetime.date.today()), 'current_memory_index': 1},
#     2: {'word_id': 2, 'word': 'Pernicious', 'definition': 'Having a harmful effect, especially in a gradual or subtle way.', 'sentence': 'The pernicious effects of smoking are well-documented.', 'start_date': str(datetime.date.today()), 'current_memory_index': 2},
#     3: {'word_id': 3, 'word': 'Ameliorate', 'definition': 'Make (something bad or unsatisfactory) better.', 'sentence': 'The new policies aim to ameliorate the working conditions.', 'start_date': str(datetime.date.today()), 'current_memory_index': 3},
#     4: {'word_id': 4, 'word': 'Obfuscate', 'definition': 'Render obscure, unclear, or unintelligible.', 'sentence': 'The politician speech was deliberately obfuscated.', 'start_date': str(datetime.date.today()), 'current_memory_index': 4},
#     5: {'word_id': 5, 'word': 'Plethora', 'definition': 'A large or excessive amount of (something).', 'sentence': 'The store offers a plethora of options for shoppers.', 'start_date': str(datetime.date.today()), 'current_memory_index': 5}
# }

app = FastAPI()

@app.get('/')
def read_root():
    return {'Hello': 'World'}

@app.post('/upload')
async def upload(file: UploadFile):
    folder = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(folder, "uploaded_db.db")
    contents = await file.read()
    with open(file_path, 'wb') as file_save:
        file_save.write(contents)
    return {'status': 'success'}

@app.post('/punch_in')
def punch_in():
    # modify the current_memory_index -> +1
    return {'status': 'success'}

@app.get('/today')
def today():
    # Connect to the database
    conn = sqlite3.connect('uploaded_db.db')
    cursor = conn.cursor()

    # Read 10 words from the word table
    cursor.execute("SELECT * FROM word LIMIT 10")
    rows = cursor.fetchall()

    # Organize the data and output in a dictionary
    words_dict = {}
    for row in rows:
        word_id, word, definition, sentence, start_date, current_memory_index = row
        words_dict[word_id] = {
            'word_id': word_id,
            'word': word,
            'definition': definition,
            'sentence': sentence,
            'start_date': start_date,
            'current_memory_index': current_memory_index
        }

    # Close the database connection
    cursor.close()
    conn.close()

    return JSONResponse(content=words_dict)
