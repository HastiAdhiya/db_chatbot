# Importing necessary libraries
import ollama
import sqlite3
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Database path from .env file (fallback to None if not found)
DB_PATH = os.getenv("DB_PATH")

# Ensure DB_PATH is set, otherwise raise an error
if not DB_PATH:
    raise ValueError("Database path not set. Please configure the .env file correctly.")

# Predefined responses for greetings and general queries
GREETING_RESPONSES = {
    "hello": "Hello! How can I assist you today?",
    "hi": "Hi there! What can I do for you?",
    "hey": "Hey! How can I help?",
    "good morning": "Good morning! How can I assist you?",
    "good afternoon": "Good afternoon! What do you need help with?",
    "good evening": "Good evening! How can I assist?",
    "how are you": "I'm just a chatbot, but I'm here to help!",
    "what's up": "Not much! Just here to answer your queries.",
    "thank you": "You're welcome!",
    "thanks": "Happy to help!"
}

# Function to check if user input is a greeting
def check_greeting(user_input):
    user_input_lower = user_input.lower().strip()
    return GREETING_RESPONSES.get(user_input_lower, None)

# Function to execute query
def execute_query(query, params=()):
    try:
        # Connect to the database
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute(query, params)
        result = cursor.fetchall()
        print("Result ---->", result)
        conn.close()
        return result
    except Exception as e:
        print("Database Error:", e)
        return None

# Function to extract an SQL Query from user input using Llama 3
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
    print("SQL Query ---->", sql_query)
    
    return sql_query if "SELECT" in sql_query.upper() else None

# Extract user queries using Llama 3
def chatbot_response(user_input):
    # Check if input is a greeting
    greeting_response = check_greeting(user_input)
    if greeting_response:
        return greeting_response
    
    # Otherwise, process as a database query
    sql_query = ask_llama(user_input)
    if not sql_query:
        return "I'm not sure about that. Could you clarify?"
    
    results = execute_query(sql_query)
    print("Results ---->", results)
    
    if not results:
        return "No user found."
    
    return results[0][0] if len(results[0]) == 1 else results

if __name__ == "__main__":
    while True:
        user_input = input("User Query: ")
        if user_input.lower() in ["exit", "quit"]:
            print("Goodbye!")
            break
        print("Chatbot Response:", chatbot_response(user_input))
