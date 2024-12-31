#
# from src.org.adobe.adx.insights.common_utils.logger import CommonLogger
# from src.utils.enums import ServiceNameEnum
# from src.utils.prompt_util import fetch_filter_days, filter_kpi, generate_schema
# from src.utils.constants import KPI_COUNT, DEFAULT_NO_OF_DAYS
# from src.prompt_template.sql_server_template import (
#     kpi_generator_prompt,
#     kpi_generator_validation_prompt,
#     query_generator_prompt,
# )
#
# logger = CommonLogger(ServiceNameEnum.CoPilotInsights.value).logger
#
#
# class SqlServerPromptSelector:
#     def __init__(self):
#         pass
#
#     def kpi_generator(self, raw_dict: dict, user_query):
#         days = fetch_filter_days(user_query)
#         kpi_count = KPI_COUNT
#         logger.info(f"####user_prompt::{user_query}####")
#         kpi_count = filter_kpi(kpi_count, user_query)
#         dbx_limit = 100
#         schema_context = generate_schema(raw_dict)
#         prompt = kpi_generator_prompt(days, kpi_count, user_query, schema_context, dbx_limit)
#         context_prompt = f"""You are a SQL Server expert. Given an input question, create a syntactically and contextually correct SQL Server query and return the answer to the input question at the end.
#         {prompt}
#
#         """
#         final_prompt = context_prompt + """
#         Question: {question}
#
#         Answer the user query: \n{format_instructions}\n
#         """
#         logger.debug("####prompt:kpi_name, query & chart_type####")
#         logger.debug(f"\t{final_prompt}")
#         logger.debug("###############################################")
#         return final_prompt
#
#     def kpi_generator_modified(self, kpi_details, relevant_table_name, non_partition_column_list, partition_column_list,
#                                user_query):
#         return kpi_generator_validation_prompt(kpi_details, relevant_table_name, partition_column_list,
#                                                non_partition_column_list, user_query)
#
#     def query_generator(self, raw_dict: dict, user_query, number_of_days):
#         logger.info(f"####user_prompt::{user_query}####")
#         filter_days = DEFAULT_NO_OF_DAYS
#         if number_of_days > 0:
#             filter_days = number_of_days
#         schema_context = generate_schema(raw_dict)
#         prompt = query_generator_prompt(schema_context, filter_days)
#         context_prompt = f"""You are a SQL Server expert. Given an input question, create a syntactically and contextually correct SQL Server query and return the answer to the input question at the end.
#         {prompt}
#
#         """
#         final_prompt = context_prompt + """
#         Question: {question}
#
#         Answer the user query: \n{format_instructions}\n
#         """
#
#         logger.debug(f"\t{final_prompt}")
#         return final_prompt
