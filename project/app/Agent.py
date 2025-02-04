import os
import os
import sqlite3
import mysql.connector
import streamlit as st
from langchain_groq import ChatGroq
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
load_dotenv()
groq_api_key = os.getenv('GROQ_API_KEY')




def get_sql_query(user_query):
    groq_sys_prompt = ChatPromptTemplate.from_template("""
                    You are an expert in converting English questions to SQL query!
                    The SQL database has the name STUDENT and has the following columns - NAME, COURSE, 
                    SECTION and MARKS. For example, 
                    Example 1 - How many entries of records are present?, 
                        the SQL command will be something like this SELECT COUNT(*) FROM STUDENT;
                    Example 2 - Tell me all the students studying in Data Science COURSE?, 
                        the SQL command will be something like this SELECT * FROM STUDENT 
                        where COURSE="Data Science"; 
                    also the sql code should not have ``` in beginning or end and sql word in output.
                    Now convert the following question in English to a valid SQL Query: {user_query}. 
                    No preamble, only valid SQL please
                                                       """)
    model="llama3-8b-8192"
    llm = ChatGroq(
    groq_api_key = groq_api_key,
    model_name=model
    )

    chain = groq_sys_prompt | llm | StrOutputParser()
    response = chain.invoke({"user_query": user_query})
    print(response)
    return response



def return_sql_response(sql_query):
    database = "student.db"
    with sqlite3.connect(database) as conn:
        cursor = conn.cursor()
        try:
            cursor.execute(sql_query)
            if sql_query.strip().lower().startswith("select"):
                column_names = [description[0] for description in cursor.description]  
                rows = cursor.fetchall()
                return column_names, rows
            else:
                conn.commit() 
                return [], [["Query executed successfully"]] 
        except Exception as e:
            return [], [[f"Error: {str(e)}"]] 