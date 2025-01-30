import os
import re
import pandas as pd
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(
    api_key=os.environ.get("GROQ_API_KEY"),
)

# Load the student responses and questions
df = pd.read_csv('data.csv')
pattern = r'^\d+:.*'

# Find columns that match the pattern (questions)
matching_columns = [col for col in df.columns if re.match(pattern, col)]

new_df = df[matching_columns]
new_df.to_csv('questions.csv', index=False)

# Initialize a dictionary to store the scores for each question
scores_dict = {}

# Process each question and score the responses
for i, question_col in enumerate(matching_columns, start=1):
    question = question_col
    
    # Handle missing values and ensure all responses are strings    
    responses = new_df[question_col].dropna().astype(str).tolist()
    responses = [response for response in responses if response.lower() != 'nan']
    
    # Format the question and responses for Groq
    formatted_question = f"Question {i}: {question}"
    formatted_responses = [f"Response {j + 1}: {response}" for j, response in enumerate(responses)]
    
    prompt = """
    Please score the responses to the questions from 0-3 based on the following rubric:
    0: All incorrect information
    1: One piece of correct information but missing some understanding or explanation
    2: One piece of correct information but with a thorough explanation
    3: Two pieces of correct information with a thorough explanation.
    
    Please give the score in the format 'Score 1: 1/3' for which corresponded to responses 1 for example.
    
    Additionally, please give a short analysis of the student responses in 2 sentences. Please take an extra look at commonly missed concepts or ideas and summarize that for me.
    Do not take a specific look into the responses but rather a generalization of the ideas missed so I, as an instructor, can see areas where students can improve.
    Please respond in the format 'Explanation: xxx '.
    """
    
    input_string = f"{prompt}\n\n{formatted_question}\n" + "\n".join(formatted_responses)

    # Run the questions through Groq
    chat_completion = client.chat.completions.create(
        messages=[{
            "role": "user",
            "content": input_string,
        }],
        model="llama-3.3-70b-versatile",
    )

    # Get the response from Groq
    grading_response = chat_completion.choices[0].message.content
    
    # Parse the score for each response (e.g., Score 1: 1/3)
    all_scores = []
    for j in range(len(responses)):
        score_match = re.search(rf"Score {j + 1}: (\d)/3", grading_response)
        if score_match:
            all_scores.append(score_match.group(1))  # Extract the score (e.g., "1")
        else:
            all_scores.append('0')  # Default if no score is found

    # Add the scores to the dictionary with the question as the key
    scores_dict[formatted_question] = all_scores

# Create a new DataFrame from the scores_dict
df_scores = pd.DataFrame(scores_dict)

# Read the student info data
df_student = pd.read_csv('data.csv')
df_student_info = df_student[['name', 'id', 'sis_id', 'root_account', 'section_id', 'section_sis_id', 'submitted', 'attempt']]

# Concatenate the scores DataFrame with the student info DataFrame
final_df = pd.concat([df_student_info, df_scores], axis=1)

# Save the final DataFrame to a new CSV
final_df.to_csv('graded_students.csv', index=False)

# Print the final DataFrame
print(final_df.head())
