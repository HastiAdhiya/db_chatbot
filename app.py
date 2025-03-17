"""
    This code consists of functions related to the following APIs:

    1. /setup_db - Initializes the SQLite database from a CSV file.  
    2. /query - Processes user queries by converting natural language into SQL queries using Llama 3  
       and retrieving relevant information from the database.

"""
from flask import Flask, request, jsonify
import ollama
import sqlite3
import os
import csv
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Database path from .env file
DB_PATH = os.getenv("DB_PATH")
if not DB_PATH:
    raise ValueError("Database path not set")

app = Flask(__name__)

# Predefined greeting responses
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

# Function to check if input is a greeting
def check_greeting(user_input):
    return GREETING_RESPONSES.get(user_input.lower().strip(), None)

# Function to execute SQL queries
def execute_query(query, params=()):
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute(query, params)
        result = cursor.fetchall()
        conn.close()
        return result
    except Exception as e:
        return f"Database Error: {str(e)}"

# Function to convert user queries to SQL using Llama 3
def ask_llama(query):
    prompt = f"""
    You are an AI that converts user queries into SQL queries for a SQLite database.
    Convert the following user question into an SQL query:
    
    User Query: "{query}"
    
    Ensure the query is structured correctly for a table named 'users' with these columns:
    - user_id, first_name, last_name, email, phone, department, role, salary
    If the query is about a specific attribute (e.g., phone number, department, role, email, salary), return only that attribute.
    Respond with only the SQL query and no additional text.
    
    Respond with only the SQL query and no additional text.
    """
    
    response = ollama.chat(model="llama3", messages=[{"role": "user", "content": prompt}])
    
    sql_query = response["message"]["content"].strip()
    print("SQL Query----->", sql_query)
    return sql_query if "SELECT" in sql_query.upper() else None

# Chatbot response function
def chatbot_response(user_input):
    greeting_response = check_greeting(user_input)
    if greeting_response:
        return greeting_response
    
    sql_query = ask_llama(user_input)
    if not sql_query:
        return "I'm not sure about that. Could you clarify?"
    
    results = execute_query(sql_query)
    print("Result----->", results)
    return results if results else "No user found."

# Flask API endpoint
@app.route("/query", methods=["POST"])
def query_api():
    data = request.get_json()
    if not data or "query" not in data:
        return jsonify({"error": "Query is required"}), 400
    
    user_input = data["query"].strip()
    response = chatbot_response(user_input)
    print("Response----->", response)
    return jsonify(response)

# API endpoint to setup the database from CSV
@app.route("/setup_db", methods=["POST"])
def setup_database():
    data = request.json
    csv_file_path = data.get("csv_file_path")

    if not csv_file_path or not os.path.exists(csv_file_path):
        return jsonify({"error": f"CSV file not found at path: {csv_file_path}"}), 400
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY,
        first_name TEXT NOT NULL,
        last_name TEXT NOT NULL,
        email TEXT NOT NULL,
        phone TEXT,
        department TEXT,
        role TEXT NOT NULL,
        salary REAL
    )
    """)
    
    with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
        csvreader = csv.DictReader(csvfile)
        for row in csvreader:
            try:
                salary = float(row['salary']) if row['salary'] else None
                cursor.execute("""
                INSERT OR IGNORE INTO users (user_id, first_name, last_name, email, phone, department, role, salary)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    int(row['user_id']),
                    row['first_name'] or 'Unknown',
                    row['last_name'] or 'Unknown',
                    row['email'] or 'unknown@example.com',
                    row['phone'],
                    row['department'],
                    row['role'] or 'Unknown',
                    salary
                ))
            except (ValueError, KeyError) as e:
                continue
    
    conn.commit()
    conn.close()
    return jsonify({"message": "Database setup completed"})

# Run the Flask app
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
