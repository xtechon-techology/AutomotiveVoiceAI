# Pre-requisite: Install langchain-core and langchain-openai packages
# Pre-requisite: Create OpenAI API key and set it in the environment variable OPENAI_API_KEY

# Load the package for loading environment variables
from dotenv import load_dotenv
from langchain_core.output_parsers import JsonOutputParser

# Load the package langchain core for PromptTemplate & ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain.chains import LLMChain

from connectors.sqlserver_database_connector import SQLServerDatabaseConnector
from response.sql_query_response import SQLQueryResponse
from visualiser.chart_handlers import generate_plotly_figure_js


def get_llm_response_reprocessed(user_question, previous_query, previous_query_error):

    # Create prompt template for the KPI suggestions
    prompt = """
    You are an SQL Server expert and have access to the below table:

    ```
    CREATE TABLE ServiceJobs (
        JobID INT PRIMARY KEY IDENTITY(1,1),
        ServiceDate DATE NOT NULL,
        JobNumber VARCHAR(20) NOT NULL,
        CustomerName VARCHAR(100) NOT NULL,
        VehicleType VARCHAR(50) NOT NULL,
        PartsCost DECIMAL(10,2) NOT NULL,
        LaborCost DECIMAL(10,2) NOT NULL,
        BillableHours DECIMAL(5,2) NOT NULL,
        TechnicianName VARCHAR(100) NOT NULL,
        CustomerSatisfactionRating INT CHECK (CustomerSatisfactionRating BETWEEN 1 AND 5)
    )
    ```

    User Query: "{question}"
    Request:
    - Suggest up to 1 Key Performance Indicators (KPIs) (with no space names) with trends and relationships.
    - Provide single class SQL queries (WITHOUT <distinct> CLAUSE) having at least one metric and one dimension.

    Requirements:
    - Provide a UNSTRINGIFY VALID JSON array (enclosed in square brackets:[]) with keys: "kpi_name", "query", "visualization_chart_name" and "referenced_source_columns".
    - Visualization chart names applicable for the query: Pie Chart, Bar Chart, Line Chart, Funnel Chart, Table Chart, Indicator Chart".
    - referenced_columns is comma separated list of all the columns that are being referenced in select, where and group by clauses.

    Validations:
    - SQL queries must be valid and compatible with SQL Server.
    - Query contains only the column names from the table definitions provided. Be careful to not query for columns that do not exist. Also, pay attention to which column is in which table.

    Previous Query: "{previous_query}"
    
    Previous Query Execution Error: "{previous_query_error}"
         
    Please provide the response in JSON format, adhering strictly to these instructions, without introductory text, additional comments, or explanations.
    """
    # Create PromptTemplate object with the KPI prompt template
    prompt_template = PromptTemplate(
        input_variables=["question", "format_instructions", "previous_query", "previous_query_error"], template=prompt
    )
    # Create LLM object with ChatOpenAI model
    llm = ChatOpenAI(temperature=0.5, model="gpt-4o")
    # Create a chain of PromptTemplate and LLM objects with the user input
    runnable = LLMChain(llm=llm, prompt=prompt_template,
                        output_parser=JsonOutputParser(pydantic_object=SQLQueryResponse))
    # user_question = (
    #     "How many vehicles were serviced each month over the last three months?"
    # )
    parser = JsonOutputParser(pydantic_object=SQLQueryResponse)
    format_instructions = parser.get_format_instructions()
    # runnable = prompt | llm | parser
    response = runnable.invoke(
        {
            "format_instructions": format_instructions,
            "question": user_question,
            "previous_query": previous_query,
            "previous_query_error": previous_query_error
        }
    )
    return response



