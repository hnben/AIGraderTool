import os
import re
import pandas as pd

from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(
    api_key=os.environ.get("GROQ_API_KEY"),
)

#seperate the questions into a new csv 
df = pd.read_csv('data.csv')
pattern = r'^\d+:.*'

# Find columns that match the pattern
matching_columns = [col for col in df.columns if re.match(pattern, col)]

new_df = df[matching_columns]
new_df.to_csv('questions.csv', index=False)

for i, question_col in enumerate(matching_columns, start=1):
    question = question_col
    
    # Handle missing values and ensure all responses are strings    
    responses = new_df[question_col].dropna().astype(str).tolist()
    responses = [response for response in responses if response.lower() != 'nan']
    formatted_question = f"Question {i}: {question}"
    formatted_responses = [f"Response {j + 1}: {response}" for j, response in enumerate(responses)]
    
    prompt = """
    Please score the responses to the questions from 0-3 based on the following rubric:
    0: All incorrect information
    1: One piece of correct information but missing some understanding or explanation
    2: One piece of correct information but with a thorough explanation
    3: Two pieces of correct information with a thorough explanation.
    
    Please give the score in the format 'Score 1: 1/3' for which corresponded to responses 1 for example.
    
    Additionally, please give an short analysis of the student responses in 2 sentences. Please take an extra look at commonly missed concepts or ideas and summarize that for me.
    Do not take a specific look into the responses but rather a generalization of the ideas missed so I, as an instructor can see areas where students can improve.
    Please response in the format 'Explaination: xxx '.
    """
    
    input_string = f"{prompt}\n\n{formatted_question}\n" + "\n".join(formatted_responses)

    #run the questions through Groq
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": input_string,
            }
        ],
        model="llama-3.3-70b-versatile",
    )

    # Print the response from Groq
    print(f"Grading for question: {question}")
    print(chat_completion.choices[0].message.content)
    