import openai
from configs.config import openai_config


class SQLPromptProcessor:
    def __init__(self):
        """
        Initialize the SQLPromptProcessor with OpenAI API key.

        :param api_key: OpenAI API key.
        """
        openai.api_key = openai_config["openai_api_key"]

    def get_table_schema(self):
        """
        Provide the table schema for ServiceJobs.

        :return: SQL table schema as a string.
        """
        return """
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
        """

    def generate_response(self, user_question):
        """
        Generate a response for the given user question using OpenAI API.

        :param user_question: The user's question to include in the prompt.
        :return: JSON string with KPIs, queries, visualization chart names, and referenced columns.
        """
        table_schema = self.get_table_schema()
        prompt = f"""
        You are SQL Server expert and have access to below tables:

        ```
        {table_schema}
        ```

        User Query:  "{user_question}"
        Request:
        - Suggest up to 4 Key Performance Indicators (KPIs) (with no space names) with trends and relationships.
        - Provide single class SQL queries (WITHOUT <distinct> CLAUSE) having at least one metric and one dimension.

        Requirements:
        - Provide a UNSTRINGIFY VALID JSON array (enclosed in square brackets:[]) with keys: "kpi_name", "query", "visualization_chart_name" and "referenced_source_columns".
        - Visualization chart names applicable for the query: Pie Chart, Bar Chart, Line Chart, Funnel Chart.
        - referenced_columns is comma seperated list of all the columns that are being referenced in select, where and group by clauses.

        Validations:
        - SQL queries must be valid and compatible with SQL Server.
        - Put LIMIT 100 in every query.
        - Query contains only the column names from the table definitions provided. Be careful to not query for columns that do not exist. Also, pay attention to which column is in which table.

        Please provide the response in JSON format, adhering strictly to these instructions, without introductory text, additional comments, or explanations.
        """
        try:
            response = openai.Completion.create(
                model="gpt",
                prompt=prompt,
                max_tokens=1000,
                temperature=0.3,
            )
            return response.choices[0].text.strip()
        except Exception as e:
            return f"An error occurred: {e}"


# Example usage
if __name__ == "__main__":

    processor = SQLPromptProcessor()
    user_question = (
        "How many vehicles were serviced each month over the last three months?"
    )
    result = processor.generate_response(user_question)

    print("Response:", result)
