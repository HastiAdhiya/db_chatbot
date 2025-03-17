# **Flask Chatbot API with Llama 3**

This project provides a Flask-based chatbot API designed to assist administrators by processing user queries and retrieving relevant data from an SQLite database. The chatbot uses **Llama 3** (via Ollama) to convert natural language queries into SQL statements.

## **Features**

* **Database Setup:** Initializes the SQLite database from a CSV file.  
* **AI-Powered Query Processing:** Converts user queries into SQL using Llama 3\.  
* **User Information Retrieval:** Fetches user details from the database.  
* **Predefined Greetings:** Recognizes and responds to common greetings.

## **Installation**

### **Prerequisites**

* Python 3.9  
* [Ollama](https://ollama.com/) installed with Llama 3  
* Required Python packages (Flask, sqlite3, python-dotenv, csv)

### **Setup**

Clone the repository:  
[HastiAdhiya/db\_chatbot](https://github.com/HastiAdhiya/db_chatbot)

1. Install dependencies:  
    pip install \-r requirements.txt  
2. Create a .env file and set the database path:  
3.  echo "DB\_PATH=admin\_db.db" \> .env  
4. Run the Flask app:  
    python app.py

## **API Endpoints**

### **1\. Initialize Database (/setup\_db)**

**Method:** POST

**Request:**

{  
  "csv\_file\_path": "path/to/users.csv"  
}

**Response:**

{  
  "message": "Database setup completed"  
}

### **2\. Query Chatbot (/query)**

**Method:** POST

**Request:**

{  
  "query": "I want to know about John's department?"  
}

**Response:**

{  
	‘IT’  
}

## **Author**

[HastiAdhiya](https://github.com/HastiAdhiya)

