import streamlit as st
import pyodbc
import pandas as pd
import random
import datetime
import openai
import plotly.express as px
import sys

sys.path.append("/Users/vishald/Documents/DWL/AutomotiveVoiceAI/")

from voiceai.speech_converter_v2 import recognize_speech_continuously


# # Azure SQL Connection Setup
# def connect_to_azure_sql():
#     connection = pyodbc.connect(
#         'DRIVER={ODBC Driver 17 for SQL Server};'
#         'SERVER=your_server_name;'  # Replace with your Azure SQL server name
#         'DATABASE=your_database_name;'  # Replace with your database name
#         'UID=your_username;'  # Replace with your username
#         'PWD=your_password;'  # Replace with your password
#     )
#     return connection
#
# # Generate Dummy Data
# def generate_dummy_data():
#     data = []
#     vehicle_types = ['Sedan', 'SUV', 'Truck', 'EV', 'Coupe']
#     technicians = ['Alice', 'Bob', 'Charlie', 'David']
#     customer_names = ['John Doe', 'Jane Smith', 'Mike Johnson', 'Anna Brown']
#
#     start_date = datetime.date.today() - datetime.timedelta(days=90)
#     for _ in range(500):
#         date = start_date + datetime.timedelta(days=random.randint(0, 90))
#         job_number = random.randint(1000, 9999)
#         customer_name = random.choice(customer_names)
#         vehicle_type = random.choice(vehicle_types)
#         parts_cost = random.uniform(50, 500)
#         labor_cost = random.uniform(50, 500)
#         billable_hours = random.uniform(1, 10)
#         technician_name = random.choice(technicians)
#         satisfaction_rating = random.randint(1, 5)
#         data.append(
#             [date, job_number, customer_name, vehicle_type, parts_cost, labor_cost,
#              billable_hours, technician_name, satisfaction_rating]
#         )
#     columns = ["Date", "Job #", "Customer Name", "Vehicle Type", "Parts $", "Labor $", "Billable hours", "Technician Name", "Customer Satisfaction Rating"]
#     return pd.DataFrame(data, columns=columns)

# # Load Dummy Data to Azure SQL
# def load_data_to_azure(data):
#     conn = connect_to_azure_sql()
#     cursor = conn.cursor()
#
#     cursor.execute("""CREATE TABLE IF NOT EXISTS JobData (
#         Date DATE,
#         JobNumber INT,
#         CustomerName NVARCHAR(50),
#         VehicleType NVARCHAR(50),
#         Parts FLOAT,
#         Labor FLOAT,
#         BillableHours FLOAT,
#         TechnicianName NVARCHAR(50),
#         SatisfactionRating INT)""")
#     conn.commit()
#
#     for _, row in data.iterrows():
#         cursor.execute("INSERT INTO JobData VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", tuple(row))
#     conn.commit()
#     conn.close()

# # Fetch Data from Azure SQL
# def fetch_data_from_azure(query):
#     conn = connect_to_azure_sql()
#     data = pd.read_sql(query, conn)
#     conn.close()
#     return data


# Voice Command Processing
def process_voice_command(command):
    openai.api_key = "your_openai_api_key"  # Replace with your OpenAI API key
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=f"Interpret this command for SQL: {command}",
        max_tokens=100,
    )
    return response["choices"][0]["text"].strip()


# Streamlit App
st.title("Azure Voice to BI Proof of Concept")

st.sidebar.header("Voice Command")
voice_input = st.sidebar.text_input(
    "Enter a command:", "How many Toyota Camrys were serviced last month?"
)

if st.sidebar.button("Submit Command"):
    st.sidebar.write("Processing command...")
    sql_query = process_voice_command(voice_input)
    st.sidebar.write(f"Generated SQL Query: {sql_query}")

    try:
        results = recognize_speech_continuously()

        # fetch_data_from_azure(sql_query))
        st.write("Results:")
        st.write(results)

        # Visualize results based on command
        if "pie chart" in voice_input.lower():
            fig = px.pie(results, names=results.columns[0], values=results.columns[1])
            st.plotly_chart(fig)
        elif "bar chart" in voice_input.lower():
            fig = px.bar(results, x=results.columns[0], y=results.columns[1])
            st.plotly_chart(fig)
        elif "line graph" in voice_input.lower():
            fig = px.line(results, x=results.columns[0], y=results.columns[1])
            st.plotly_chart(fig)
        else:
            st.write("Unsupported visualization request. Showing data as a table.")
    except Exception as e:
        st.error(f"Error processing command: {e}")

# Generate and Load Dummy Data
if st.button("Generate and Load Dummy Data"):
    pass
    # st.write("Generating dummy data...")
    # dummy_data = generate_dummy_data()
    # st.write(dummy_data.head())
    #
    # st.write("Loading data to Azure SQL...")
    # load_data_to_azure(dummy_data)
    # st.success("Data loaded successfully!")
