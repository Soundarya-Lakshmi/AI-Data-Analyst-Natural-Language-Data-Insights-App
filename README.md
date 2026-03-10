# AI-Data-Analyst-Natural-Language-Data-Insights-App

# Project Overview

This project is an AI-powered analytics assistant that allows users to ask questions in natural language and receive data insights instantly.

The system converts user questions into Python pandas code, executes the code on a dataset, and returns either:
A numerical/text answer
A visualization chart

The application is deployed using Streamlit, providing a simple interface where users can interact with the dataset like they would with a human data analyst.

# Problem Statement

Business users often want quick insights but may not know SQL, Python, or BI tools.

This project solves that problem by creating an AI assistant that understands plain English questions and automatically performs the required data analysis.

The AI automatically performs the required data aggregation, filtering, or visualization.

# Workflow

Raw Dataset
   |
Data Cleaning & Transformation
(Bronze → Silver → Gold layers in Snowflake)
   |
Clean Analytics Dataset
   |
Python Application
   |
Integration with Gemini LLM via API
   |
AI converts Natural Language Questions → Executable Pandas Code
   |
Code Execution on Dataset
   |
Results & Visualizations Generated
   |
Streamlit Web Interface for User Interaction

# Workflow Explanation

1. Data Cleaning & Transformation

The dataset is first processed in Snowflake using a layered architecture:

Bronze Layer – Raw data ingestion
Silver Layer – Data cleaning and validation
Gold Layer – Analytics-ready dataset

This ensures the AI model works with clean and reliable data.

2. Python Application

The cleaned dataset is accessed using Python where the analytics logic is implemented.

3. AI Integration

A generative AI model (Google Gemini) is integrated via API.
The AI interprets user questions and generates pandas code to answer them.

4. Code Execution

The generated pandas code is executed dynamically on the dataset to produce the required insight.

Depending on the question, the output may be:
Numeric answer
Table
Visualization

5. User Interface

A simple web interface is built using Streamlit.
Users can:
Enter a natural language question
Click Get Answer
View the generated insight or chart instantly

# Code Safety

Code Safety

Since the AI generates executable Python code, a security validation layer is implemented.

The system blocks potentially dangerous operations such as:
OS commands
File deletion
System execution
Environment modification

This ensures the generated code remains safe to execute.

# Key Learnings

Integrating AI models with data analysis workflows
Converting natural language queries to executable Python code
Implementing safe execution of AI generated code
Building simple data applications with Streamlit
Creating AI-powered analytics assistants
