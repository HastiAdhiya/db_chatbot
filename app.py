import sqlite3
from langchain_community.chat_models import ChatOllama  # Importing ChatOllama
from langchain_core.prompts import ChatPromptTemplate
import requests

# Path to the SQLite database
db_path = 'admin_db.db'

# Function to connect to the SQLite database
def connectDatabase():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    return conn, cursor  # Returning both conn and cursor for later use

# Function to run a SQL query
def runQuery(cursor, query):
    try:
        cursor.execute(query)
        return cursor.fetchall()
    except sqlite3.Error as e:
        return f"Error executing query: {str(e)}"

# Function to retrieve the database schema (users table)
def getDatabaseSchema(cursor):
    cursor.execute("PRAGMA table_info(users);")
    schema = cursor.fetchall()
    print("Database Schema:")
    for row in schema:
        print(row)
    return schema

# Llama model using ChatOllama
llm = ChatOllama(model="llama3")  # Use the Llama model here (ChatOllama)

# Function to generate SQL query from user's natural language question
def getQueryFromLLM(question, cursor):
    template = """Below is the schema of the connected database. Read the schema carefully, paying attention to the table and column names. Ensure that table or column names are used exactly as they appear in the schema. Answer the user's question in the form of an SQL query.

    {schema}

    Please provide only the SQL query and nothing else.

    question: {question}
    SQL query:"""
    
    prompt = ChatPromptTemplate.from_template(template)
    chain = prompt | llm

    response = chain.invoke({
        "question": question,
        "schema": getDatabaseSchema(cursor)
    })
    return response.content.strip()

# Function to generate a response for the query result
def getResponseForQueryResult(question, query, result):
    template = """Below is the schema of the connected database. Based on the schema and the query result, write a natural language response to the user's question.

    {schema}

    Examples:
    question: How many users are in the database?
    SQL query: SELECT COUNT(*) FROM users;
    Result: [(34,)]
    Response: There are 34 users in the database.

    Now it's your turn to write a response based on the result:
    question: {question}
    SQL query: {query}
    Result: {result}
    Response:"""
    
    prompt2 = ChatPromptTemplate.from_template(template)
    chain2 = prompt2 | llm

    response = chain2.invoke({
        "question": question,
        "schema": getDatabaseSchema(cursor),
        "query": query,
        "result": result
    })

    return response.content.strip()

# Function to simulate interaction with the chatbot
def chatbot(query):
    conn, cursor = connectDatabase()  # Connect to the database
    try:
        # Generate SQL query from LLM
        sql_query = getQueryFromLLM(query, cursor)
        print(f"Generated SQL Query: {sql_query}")

        # Execute the query
        result = runQuery(cursor, sql_query)
        
        # If there is an error, we should handle it
        if isinstance(result, str) and result.startswith("Error"):
            return result
        
        # Generate a response based on the query result
        response = getResponseForQueryResult(query, sql_query, result)
        return response
    finally:
        conn.close()  # Ensure the database connection is closed after use

# Example questions to test with
questions = [
    "What is the salary of Lisa?",
    "How many users are in the database?",
    "Show me users in the marketing department."
]

# Running chatbot for each question
for question in questions:
    print(f"Question: {question}")
    response = chatbot(question)
    print(f"Response: {response}")
    print("="*50)

# In your Python code for making an external API request (if needed)
response = requests.post("http://127.0.0.1:11434/api/chat", json={"query": "What is the salary of Lisa?"})
print(response.json())
