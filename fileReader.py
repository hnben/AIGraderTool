import pandas as pd

# Read the CSV file into a DataFrame
df = pd.read_csv('CAPSTONE TEST.csv')

#check column names
#print(df.columns)
# question1 = df[['178498165: No more than 2-3 sentences\nList 2 potential challenges with implementing an RL agent for the game you chose in question #1. Briefly explain the problem / concern that each present.']]
# print("QUESTION 1: "+question1)
# Access specific columns
print(df[['name', 'id', 'score', 'n correct' , 'n incorrect']])

#print(df.info())
# question1 = df.iloc[:, 9]
# question2 = df.iloc[:,11]
# question3 = df.iloc[:, 13]
# print(question1)
# print(question2)
# print(question3)


# calculate the average score
average_score = df['score'].mean()
print(f'Average score: {average_score}')