import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.io as pio
import random
import dateutil.parser as parser
from pyarrow import int64


def generate_plotly_figure_js(data_frame, x_column, y_column, title, chart_type):
    chart_type_mapping = {
        'Bar Chart': 'bar',
        'Line Chart': 'line',
        'Pie Chart': 'pie',
        'Funnel Chart': 'funnel',
        'Table Chart': 'table',
        'Indicator Chart': 'indicator'
    }

    # Extract columns from DataFrame
    df_columns = list(data_frame.keys())

    # Trim and preprocess data
    data_frame = trim_lists(data_frame, 400)

    if x_column in df_columns:
        data_frame = sort_dict_data(data_frame, x_column)

    if x_column is None or x_column == "" :
        chart_type = 'Indicator Chart'
    elif (y_column is None or y_column == "") and (x_column is not None and x_column != ""):
        chart_type = 'Indicator Chart'
        y_column = x_column
        x_column = ""

    else:
        data_frame = date_parser(data_frame, x_column, y_column, chart_type)
        # Fallback to Line Chart if Pie Chart has too many categories
        if len(data_frame[x_column]) >= 8 and chart_type == "Pie Chart" and x_column in df_columns:
            chart_type = 'Line Chart'

        if len(data_frame[x_column]) >= 8 and chart_type == "Bar Chart" and x_column in df_columns:
            chart_type = 'Line Chart'





    # Handle cases with single data column
    if len(data_frame) == 1 and len(df_columns) == 1:
        y_column = df_columns[0]
        y_data = data_frame[df_columns[0]]
        x_column = "x-axis"
        x_data = [1]
    else:
        x_data = data_frame[x_column]
        if isinstance(y_column, list):
            y_data = [data_frame[col] for col in y_column]
        else:
            y_data = data_frame[y_column]


    if isinstance(y_column, list):
        y_data = [data_frame[col] for col in y_column]
    else:
        y_data = data_frame[y_column]

    # if (x_column is not None and x_column != ""):
    #     x_data = data_frame[x_column] if x_column else [f"Category {i + 1}" for i in range(
    #         len(y_data[0]) if isinstance(y_data, list) else len(y_data))]

    # Define chart-specific logic
    traces = []
    if chart_type == 'Bar Chart':
        if isinstance(y_data, list):
            for y, col in zip(y_data, y_column):
                color = generate_random_color()
                traces.append(go.Bar(x=x_data, y=y, name=col, marker=dict(color=color)))
        else:
            color = generate_random_color()
            traces.append(go.Bar(x=x_data, y=y_data, marker=dict(color=color)))
    elif chart_type == 'Line Chart':
        if isinstance(y_data, list):
            for y, col in zip(y_data, y_column):
                color = generate_random_color()
                traces.append(go.Scatter(x=x_data, y=y, mode='lines', name=col, line=dict(color=color)))
        else:
            color = generate_random_color()
            traces.append(go.Scatter(x=x_data, y=y_data, mode='lines', line=dict(color=color)))
    elif chart_type == 'Pie Chart':
        colors = [generate_random_color() for _ in range(len(x_data))]
        traces.append(go.Pie(labels=x_data, values=y_data, marker=dict(colors=colors)))
    elif chart_type == 'Funnel Chart':
        color = generate_random_color()
        traces.append(go.Funnel(y=y_data, x=x_data, marker=dict(color=color)))
    elif chart_type == 'Table Chart':
        traces.append(go.Table(
            header=dict(values=list(data_frame.keys()), align='center'),
            cells=dict(values=[data_frame[col] for col in data_frame.keys()], align='center')
        ))
    elif chart_type == 'Indicator Chart':
        # Extract a single numeric value from y_data
        if isinstance(y_data, pd.Series):
            value = y_data.iloc[0]  # Take the first value from the Series
        elif isinstance(y_data, (list, np.ndarray, tuple)):
            value = y_data[0] if len(y_data) > 0 else None  # Take the first value from list/array/tuple
        else:
            value = y_data  # Use directly if it's already a number

            # Convert to native Python int or float
        if isinstance(value, (np.integer, np.floating)):
            value = value.item()  # Convert NumPy type to native Python type

        if not isinstance(value, (int, float)):
            raise ValueError(
                f"Expected a numeric value for 'Indicator Chart', got {type(value).__name__} with value: {value}")

        traces.append(go.Indicator(
            mode="gauge+number",
            value=value,
            title={'text': title},
            domain={'x': [0, 1], 'y': [0, 1]}
        ))
    else:
        raise ValueError("Invalid chart type. Supported types are: 'bar', 'line', 'pie', 'funnel', 'table', 'indicator'.")

    # Create layout with a title
    y_title = ', '.join(y_column) if isinstance(y_column, list) else y_column

    layout = go.Layout(
        title={
            'text': title,
            'x': 0.5,  # Center-align the title
            'font': {'size': 18}
        },
        xaxis=dict(title=x_column),
        yaxis=dict(title=y_title),
        plot_bgcolor="#f9f9f9",  # Light gray background for the plot
        paper_bgcolor="#ffffff",  # White background for the chart
    )

    # Create the figure
    figure = go.Figure(data=traces, layout=layout)

    # Export to JSON and image
    figure_json = pio.to_json(figure)
    image_path = f"{title.replace(' ', '_').lower()}_chart.png"
    pio.write_image(figure, image_path, format='png')

    return figure_json, image_path

def generate_random_color():
    """Generates a random HEX color."""
    return "#" + "".join(random.choices("0123456789ABCDEF", k=6))

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
        sorted_dict = {column: sorted_data_list for column, sorted_data_list in zip(data_dict.keys(), sorted_data_lists)}

        return sorted_dict
    except Exception as e:
        return data_dict

def trim_lists(dictionary, m):
    trimmed_dict = {}
    for key, value in dictionary.items():
        trimmed_dict[key] = value[:m]
    return trimmed_dict


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
