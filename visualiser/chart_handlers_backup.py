import json
import dateutil.parser as parser
import pandas as pd
import plotly.graph_objs as go
import plotly.io as pio


def generate_plotly_figure_js(data_frame, x_column, y_column, title, chart_type):
    chart_type_mapping = {
        'Bar Chart': 'bar',
        'Line Chart': 'line',
        'Pie Chart': 'pie',
        'Funnel Chart': 'funnel'
    }
    # Extract x and y data from the DataFrame
    df_columns = list(data_frame.keys())

    data_frame = trim_lists(data_frame, 400)

    if x_column in df_columns:
        data_frame = sort_dict_data(data_frame, x_column)

    data_frame = date_parser(data_frame, x_column, y_column, chart_type)

    if len(data_frame[x_column]) >= 8 and chart_type == "Pie Chart" and x_column in df_columns:
        chart_type = 'Line Chart'

    if len(data_frame) == 1 and len(df_columns) == 1:
        y_column = df_columns[0]
        y_data = data_frame[df_columns[0]]
        x_column = "x-axis"
        x_data = [1]
    else:
        x_data = data_frame[x_column]
        y_data = data_frame[y_column]

    # Create Plotly graph object based on chart type
    if chart_type == 'Bar Chart':
        trace = go.Bar(x=x_data, y=y_data)
    elif chart_type == 'Line Chart':
        trace = go.Scatter(x=x_data, y=y_data, mode='lines')
    elif chart_type == 'Pie Chart':
        trace = go.Pie(labels=x_data, values=y_data)
    elif chart_type == 'Funnel Chart':
        trace = go.Funnel(y=y_data, x=x_data)
    else:
        raise ValueError("Invalid chart type. Supported types are: 'bar', 'line', 'pie', 'funnel'.")

    # Create layout with title
    layout = go.Layout(title=title)

    figure = go.Figure(data=[trace], layout=layout)

    figure_json = pio.to_json(figure)

    # Generate the chart image
    image_path = f"{title.replace(' ', '_').lower()}_chart.png"
    pio.write_image(figure, image_path, format='png')

    return figure_json, image_path


def generate_plotly_chart_js(data_frame, x_column, y_column, title, chart_type):
    # Define a dictionary to map chart types to Plotly chart types
    chart_type_mapping = {
        'Bar Chart': 'bar',
        'Line Chart': 'line',
        'Pie Chart': 'pie',
        'Funnel Chart': 'funnel'
    }
    df_columns = list(data_frame.keys())

    data_frame = trim_lists(data_frame, 400)

    # if x_column is None or x_column == "":
    #     if(len(df_columns)>1):
    #         x_column =df_columns[0]
    #     else:
    #         x_column = "x"

    if len(data_frame[x_column]) >= 8 and chart_type == "Pie Chart" and x_column in df_columns:
        chart_type = 'Line Chart'

    # if y_column is None or y_column == "":
    #     if(len(df_columns)>1):
    #         y_column =df_columns[1]
    #     else:
    #         y_column = df_columns[0]

    if x_column in df_columns:
        data_frame = sort_dict_data(data_frame, x_column)

    data_frame = date_parser(data_frame, x_column, y_column, chart_type)

    if len(data_frame) == 1 and len(df_columns) == 1:
        y_column = df_columns[0]
        y_data = data_frame[df_columns[0]]
        x_column = "x-axis"
        x_data = [1]
    else:
        x_data = data_frame[x_column]
        y_data = data_frame[y_column]

    # Check if the chart_type is valid
    if chart_type not in chart_type_mapping:
        raise ValueError(
            "Invalid chart_type. Supported chart types are: 'Bar Chart', 'Line Chart', 'Pie Chart', 'Funnel Chart'")

    # Create the JavaScript code for the selected chart type
    js_code = f'''
      // Extract data from the data frame
      var data = {{
        x: {json.dumps(x_data)},
        y: {json.dumps(y_data)},
        type: '{chart_type_mapping[chart_type]}',
        marker: {{
          color: 'rgb(0, 128, 255)'
        }}
      }};

      // Create the layout for the chart
      var layout = {{
        title: '{title}',
        xaxis: {{
          title: '{x_column}'
        }},
        yaxis: {{
          title: '{y_column}'
        }}
      }};

      // Plot the chart using Plotly
      Plotly.newPlot('chartId', [data], layout);
    '''

    if chart_type == 'Pie Chart':
        js_code = js_code.replace("x:", "labels:")
        js_code = js_code.replace("y:", "values:")

    return js_code


def sort_dict_data(data_dict, sort_column):
    # Get the data from the dictionary
    data_lists = list(data_dict.values())

    # Find the index of the sort column
    try:
        sort_index = list(data_dict.keys()).index(sort_column)
    except ValueError:
        raise ValueError(f"'{sort_column}' not found in the dictionary keys.")

    # Transpose the data to sort by the specified column
    try:
        transposed_data = list(zip(*data_lists))

        # Sort the data based on the specified column
        sorted_data = sorted(transposed_data, key=lambda x: x[sort_index])

        # Transpose the sorted data back to the original format
        sorted_data_lists = list(zip(*sorted_data))

        # Create a new dictionary with the sorted data
        sorted_dict = {column: sorted_data_list for column, sorted_data_list in
                       zip(data_dict.keys(), sorted_data_lists)}

        return sorted_dict
    except Exception as e:
        return data_dict


def date_parser(data_dict, x_column, y_column, chart_type):
    if chart_type == 'Funnel Chart':
        date_column = y_column
    else:
        date_column = x_column

    date_list = data_dict[date_column]

    parsed_list = []

    if date_column not in list(data_dict.keys()):
        return data_dict

    try:
        for date_value in date_list:
            d = parser.parse(date_value).strftime('%Y-%m-%d')
            parsed_list.append(d)
        data_dict[date_column] = parsed_list
    except Exception as e:
        return data_dict

    # print(data_dict)
    return data_dict


def trim_lists(dictionary, m):
    trimmed_dict = {}
    for key, value in dictionary.items():
        trimmed_dict[key] = value[:m]
    return trimmed_dict
