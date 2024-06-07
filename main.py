import json
import os
import sys
from openai import OpenAI
from datetime import datetime

current_date = datetime.now().date()
print(current_date)

client = OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio") # local server lm-studio app

def process_ai_output(message):
    completion = client.chat.completions.create(
        model="tinybiggames/Phi-3-mini-4k-instruct-Q4_K_M-GGUF",
        messages=[
            {"role": "system", "content": "Your purpose is to get from user message time for registration and place and output place and time of order in json format with keys (name,time, place). list of places to set in json: `игровой клуб`, `бильярд`, `покер`, `казино`. current date ``"},
            {"role": "user", "content": message}
        ],
        temperature=0.7,
    )

    return(completion.choices[0].message.content)

print(process_ai_output("Я хотел бы записаться на прием к терапевту на 15 июня в 14:30."))