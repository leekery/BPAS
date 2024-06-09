import json
import os
import sys
from openai import OpenAI
from datetime import datetime

bracket = str("{}")
language = ["English", "Russian"]

def read_places_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = file.read()
            json_data = json.loads(data)
        return json_data
    except FileNotFoundError:
        print(f"Файл {file_path} не найден.")
        return None
    except json.JSONDecodeError as e:
        print(f"Ошибка при декодировании JSON: {e}")
        return None

places_content = read_places_file("places.json")

client = OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio") # local server lm-studio app

def ai_question_process(message):
    current_date = datetime.now().date()
    completion = client.chat.completions.create(
        model="MaziyarPanahi/NeuralBeagle14-7B-GGUF",
        messages=[
            {"role": "system", "content": f"you have info about order places and time when user can order it, answer on questions about time and places from this content: {places_content}. do not answer on questions with another themes! response language: {language[1]}. give answers shortly, just with answer to question. current date {current_date}. do not write any text if no needed, if user asks aobut free time on some place just write only the time for example. if user ask about free time between first time and second time just output all free time beetween these two hours."},
            {"role": "user", "content": message}
        ],
        temperature=0.7,
    )
    
    output = completion.choices[0].message.content
    cleaned_data = output.strip()

    return(cleaned_data)
def ai_order_process(message):
    current_date = datetime.now().date()
    completion = client.chat.completions.create(
        model="MaziyarPanahi/NeuralBeagle14-7B-GGUF",
        messages=[
            {"role": "system", "content": f"Your purpose is to get from user message time for registration and place and output place and time of order in json format in brackets you can only use words of places and time in answer from this content: {places_content}. current date {current_date}. No other text exclude json. no comments. if user asks to place order and time you can put only 1 place and 1 time in json response. you can only put in `time` one time and only 1 place in `place` in one response. if user write пк клуб, комп клуб, компы - it means `Компьютерный клуб`. `комп клуб` in user message means `Компьютерный клуб`."},
            {"role": "user", "content": message}
        ],
        temperature=0.7,
    )
    
    output = completion.choices[0].message.content
    cleaned_data = output.strip()

    return(cleaned_data)
data1 = ai_question_process("Какое есть время записи на комп клуб сегодня между 18 и 21 часами?")

# data = process_ai_output("Я хотел бы записаться в комп клуб завтра в 14:30.")
print(data1)
print()
data2 = ai_order_process("Запиши меня в комп клуб завтра между 13 и 16 часами.")
print(data2)
# parsed_data = json.loads(data)

# place = parsed_data.get("place")
# time = parsed_data.get("time")

# print(f"{place} в {time}")
