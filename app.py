# Importing necessary libraries
import ollama
import sqlite3
import re

# database path
db_path= r"C:\Hasti\db_chatbot\database_file.db"

# Function to execute query
def execute_query(query, params=()):
    # connect to database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute(query, params)
    result = cursor.fetchall()
    print("Result---->", result)
    conn.close()
    return result

# function which extract an SQL Query from user input using llama3
def ask_llama(query):
    prompt = f"""
    You are an AI that converts user queries into SQL queries to retrieve information from a SQLite database.
    Convert the following user question into an SQL query:
    
    User Query: "{query}"
    
    Ensure the query is structured correctly for a table named 'users' with the following columns:
    - user_id
    - first_name
    - last_name
    - email
    - phone
    - department
    - role
    - salary
    
    If the query is about a specific attribute (e.g., phone number, department, role, email, salary), return only that attribute.
    
    Respond with only the SQL query and no additional text.
    """
    
    response = ollama.chat(
        model="llama3",
        messages=[{"role": "user", "content": prompt}]
    )
    
    sql_query = response["message"]["content"].strip()
    print("SQL Query------>", sql_query)
    return sql_query if "SELECT" in sql_query else None

# Extract user queries using llama3
def chatbot_response(user_input):

    sql_query = ask_llama(user_input)
    if not sql_query:
        return "I'm not sure about that. Could you clarify?"
    
    results = execute_query(sql_query)
    print("Results------>", results)
    if not results:
        return "No user found."
    
    return results[0][0] if len(results[0]) == 1 else results

if __name__ == "__main__":
    while True:
        user_input = input("USer Query: ")
        if user_input.lower() in ["exit", "quit"]:
            print("Goodbye!")
            break
        print("Chatbot Response:", chatbot_response(user_input))
