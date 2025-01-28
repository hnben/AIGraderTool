import pandas as pd

# Read the CSV file into a DataFrame
df = pd.read_csv('CAPSTONE TEST.csv')

#check column names
#print(df.columns)
# question1 = df[['178498165: No more than 2-3 sentences\nList 2 potential challenges with implementing an RL agent for the game you chose in question #1. Briefly explain the problem / concern that each present.']]
# print("QUESTION 1: "+question1)
# Access specific columns
print(df[['name', 'id', 'score', 'n correct' , 'n incorrect']])


# calculate the average score
average_score = df['score'].mean()
print(f'Average score: {average_score}')