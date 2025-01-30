import os
import re
import pandas as pd

from groq import Groq
from dotenv import load_dotenv

#seperate the questions into a new csv 
df = pd.read_csv('data.csv')
pattern = r'^\d+:.*'

# Find columns that match the pattern
matching_columns = [col for col in df.columns if re.match(pattern, col)]

new_df = df[matching_columns]
new_df.to_csv('questions.csv', index=False)

#run the questions through Groq
load_dotenv()

client = Groq(
    api_key=os.environ.get("GROQ_API_KEY"),
)

chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": "Explain the importance of fast language models",
        }
    ],
    model="llama-3.3-70b-versatile",
)

print(chat_completion.choices[0].message.content)