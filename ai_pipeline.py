#Connecting with LLM
import google.generativeai as genai
from config import *

genai.configure(api_key=api_key)

model= genai.GenerativeModel("gemini-2.5-flash")


#Connecting to the database
import snowflake.connector

conn = snowflake.connector.connect(
    user=user,
    password=password,
    account=account,
    warehouse=warehouse,
    database=database,
    schema=schema
)

import pandas as pd
query = "SELECT * FROM GOLD_HOTELBOOKINGS"

df = pd.read_sql(query, conn)

blocked_keywords = [
    "import os",
    "import sys",
    "subprocess",
    "shutil",
    "open(",
    "__import__",
    "pip install",
    "rm ",
    "del ",
    "os.system",
    "os.remove",
    "os.rmdir",
    "os.listdir",
    "os.walk",
    "sys.exit",
    "socket",
    "requests",
    "urllib"
]

def ask_question(question):
    
    schema = """
    Dataset: Hotel Bookings

    Columns:
    BOOKING_ID
    HOTEL_ID
    HOTEL_CITY
    CUSTOMER_ID
    CUSTOMER_NAME
    CUSTOMER_EMAIL
    CHECK_IN_DATE
    CHECK_OUT_DATE
    ROOM_TYPE
    NUM_GUESTS
    BOOKING_STATUS
    REVENUE_USD
    """

    prompt = f"""
    You are a data analyst.

    Dataset schema:
    {schema}

    A pandas dataframe called df already contains the data.

    Write ONLY Python pandas code to answer the following question.

    Question:
    {question}

    Do not include any explanations. The code you return will be executed directly. 
    Return only executable Python code without any extra words or space or quotes. 
    
    No need to mention whether it is a python script.
    Your example outputs for summarization answers: 
    df.groupby(column1)[column2].sum()
    df.groupby(column1)[column2].mean()

    When an answer has more than 2 rows, show the appropriate chart for the question:
    Your example output for answers with more than 2 rows:

    import matplotlib.pyplot as plt
    city_revenue = df.groupby('HOTEL_CITY')['REVENUE_USD'].sum().nlargest(5)
    city_revenue.plot(kind='bar', figsize=(10, 6), title='Top 5 Cities by Revenue', xlabel='City', ylabel='Total Revenue')
    plt.tight_layout()
    plt.show()


    This is how your outputs should be. 
    """
    
    response = model.generate_content(prompt)
    generated_code = response.text
    code_lower = generated_code.lower()
    for keyword in blocked_keywords:
        if keyword in code_lower:
            raise ValueError(f"Unsafe code detected: {keyword}")

    import matplotlib.pyplot as plt

    # Prepare environment for exec
    local_env = {"df": df, "plt": plt, "__result__": None}

    # If AI returned a single line, wrap it to capture the output
    wrapped_code = f"__result__ = {generated_code}" if "\n" not in generated_code else generated_code

    # Execute the AI-generated code
    exec(wrapped_code, {}, local_env)

    # Check if a chart was generated
    fig = plt.gcf()
    if len(fig.get_axes()) > 0:
        return fig

    # Otherwise return the result of single-line code
    if local_env.get("__result__") is not None:
        return local_env["__result__"]

    # If multi-line code created variables, return the last one
    variables = {k:v for k,v in local_env.items() if k not in ["df","plt","__result__"]}
    if variables:
        return list(variables.values())[-1]

    return None
