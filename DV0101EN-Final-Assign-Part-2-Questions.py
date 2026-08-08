#!/usr/bin/env python
# coding: utf-8

import dash
import more_itertools
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.graph_objs as go
import plotly.express as px


# ---------------------------------------------------------
# Load the data
# ---------------------------------------------------------

data = pd.read_csv(
    "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/d51iMGfp_t0QpO30Lym-dw/automobile-sales.csv"
)


# ---------------------------------------------------------
# Initialize the Dash app
# ---------------------------------------------------------

app = dash.Dash(__name__)

app.title = "Automobile Sales Statistics Dashboard"


# ---------------------------------------------------------
# Dropdown options
# ---------------------------------------------------------

dropdown_options = [
    {
        'label': 'Yearly Statistics',
        'value': 'Yearly Statistics'
    },
    {
        'label': 'Recession Period Statistics',
        'value': 'Recession Period Statistics'
    }
]


# List of years
year_list = [i for i in range(1980, 2024, 1)]


# ---------------------------------------------------------
# Create the layout
# ---------------------------------------------------------

app.layout = html.Div([

    # TASK 2.1
    html.H1(
        "Automobile Sales Statistics Dashboard",
        style={
            'textAlign': 'center',
            'color': '#503D36',
            'font-size': 24
        }
    ),


    # TASK 2.2 - Report type dropdown
    html.Div([

        html.Label("Select Statistics:"),

        dcc.Dropdown(
            id='dropdown-statistics',

            options=dropdown_options,

            value='Select Statistics',

            placeholder='Select a report type',

            style={
                'width': '80%',
                'padding': '3px',
                'font-size': '20px',
                'text-align-last': 'center'
            }
        )

    ]),


    # TASK 2.2 - Year dropdown
    html.Div([

        html.Label("Select Year:"),

        dcc.Dropdown(
            id='select-year',

            options=[
                {'label': i, 'value': i}
                for i in year_list
            ],

            value='Select-year',

            placeholder='Select-year'
        )

    ]),


    # TASK 2.3
    html.Div([

        html.Div(
            id='output-container',
            className='chart-grid',

            style={
                'display': 'flex',
                'flexDirection': 'column'
            }
        )

    ])

])


# ---------------------------------------------------------
# TASK 2.4
# Enable / Disable year dropdown
# ---------------------------------------------------------

@app.callback(

    Output(
        component_id='select-year',
        component_property='disabled'
    ),

    Input(
        component_id='dropdown-statistics',
        component_property='value'
    )

)

def update_input_container(selected_statistics):

    if selected_statistics == 'Yearly Statistics':

        return False

    else:

        return True


# ---------------------------------------------------------
# TASK 2.4
# Callback for displaying graphs
# ---------------------------------------------------------

@app.callback(

    Output(
        component_id='output-container',
        component_property='children'
    ),

    [

        Input(
            component_id='dropdown-statistics',
            component_property='value'
        ),

        Input(
            component_id='select-year',
            component_property='value'
        )

    ]

)

def update_output_container(selected_statistics, input_year):


    # =====================================================
    # TASK 2.5
    # Recession Period Statistics
    # =====================================================

    if selected_statistics == 'Recession Period Statistics':


        # Filter recession data
        recession_data = data[
            data['Recession'] == 1
        ]


        # -------------------------------------------------
        # Recession Plot 1
        # Average automobile sales by year
        # -------------------------------------------------

        yearly_rec = recession_data.groupby(
            'Year'
        )['Automobile_Sales'].mean().reset_index()


        R_chart1 = dcc.Graph(

            figure=px.line(

                yearly_rec,

                x='Year',

                y='Automobile_Sales',

                title='Average Automobile Sales fluctuation over Recession Period'

            ),

            style={'width': '50%'}

        )


        # -------------------------------------------------
        # Recession Plot 2
        # Average vehicles sold by vehicle type
        # -------------------------------------------------

        average_sales = recession_data.groupby(
            'Vehicle_Type'
        )['Automobile_Sales'].mean().reset_index()


        R_chart2 = dcc.Graph(

            figure=px.bar(

                average_sales,

                x='Vehicle_Type',

                y='Automobile_Sales',

                title='Average Number of Vehicles Sold by Vehicle Type'

            ),

            style={'width': '50%'}

        )


        # -------------------------------------------------
        # Recession Plot 3
        # Advertisement expenditure share by vehicle type
        # -------------------------------------------------

        exp_rec = recession_data.groupby(
            'Vehicle_Type'
        )['Advertising_Expenditure'].sum().reset_index()


        R_chart3 = dcc.Graph(

            figure=px.pie(

                exp_rec,

                values='Advertising_Expenditure',

                names='Vehicle_Type',

                title='Total Expenditure Share by Vehicle Type during Recessions'

            ),

            style={'width': '50%'}

        )


        # -------------------------------------------------
        # Recession Plot 4
        # Unemployment rate vs automobile sales
        # -------------------------------------------------

        unemp_data = recession_data.groupby(

            [
                'unemployment_rate',
                'Vehicle_Type'
            ]

        )['Automobile_Sales'].mean().reset_index()


        R_chart4 = dcc.Graph(

            figure=px.bar(

                unemp_data,

                x='unemployment_rate',

                y='Automobile_Sales',

                color='Vehicle_Type',

                labels={

                    'unemployment_rate':
                    'Unemployment Rate',

                    'Automobile_Sales':
                    'Average Automobile Sales'

                },

                title='Effect of Unemployment Rate on Vehicle Type and Sales'

            ),

            style={'width': '50%'}

        )


        # Display four graphs in 2 rows × 2 columns
        return [

            html.Div(

                className='chart-item',

                children=[
                    R_chart1,
                    R_chart2
                ],

                style={
                    'display': 'flex',
                    'width': '100%'
                }

            ),


            html.Div(

                className='chart-item',

                children=[
                    R_chart3,
                    R_chart4
                ],

                style={
                    'display': 'flex',
                    'width': '100%'
                }

            )

        ]


    # =====================================================
    # TASK 2.6
    # Yearly Statistics
    # =====================================================

    elif (
        selected_statistics == 'Yearly Statistics'
        and input_year != 'Select-year'
    ):


        # Filter data for selected year
        yearly_data = data[
            data['Year'] == input_year
        ]


        # -------------------------------------------------
        # Yearly Plot 1
        # Yearly automobile sales for whole period
        # -------------------------------------------------

        yas = data.groupby(
            'Year'
        )['Automobile_Sales'].mean().reset_index()


        Y_chart1 = dcc.Graph(

            figure=px.line(

                yas,

                x='Year',

                y='Automobile_Sales',

                title='Yearly Automobile Sales'

            ),

            style={'width': '50%'}

        )


        # -------------------------------------------------
        # Yearly Plot 2
        # Total monthly sales for selected year
        # -------------------------------------------------

        mas = yearly_data.groupby(
            'Month'
        )['Automobile_Sales'].sum().reset_index()


        Y_chart2 = dcc.Graph(

            figure=px.line(

                mas,

                x='Month',

                y='Automobile_Sales',

                title='Total Monthly Automobile Sales'

            ),

            style={'width': '50%'}

        )


        # -------------------------------------------------
        # Yearly Plot 3
        # Average vehicles sold by vehicle type
        # -------------------------------------------------

        avr_vdata = yearly_data.groupby(
            'Vehicle_Type'
        )['Automobile_Sales'].mean().reset_index()


        Y_chart3 = dcc.Graph(

            figure=px.bar(

                avr_vdata,

                x='Vehicle_Type',

                y='Automobile_Sales',

                title=
                'Average Vehicles Sold by Vehicle Type in the year {}'.format(
                    input_year
                )

            ),

            style={'width': '50%'}

        )


        # -------------------------------------------------
        # Yearly Plot 4
        # Advertisement expenditure by vehicle type
        # -------------------------------------------------

        exp_data = yearly_data.groupby(
            'Vehicle_Type'
        )['Advertising_Expenditure'].sum().reset_index()


        Y_chart4 = dcc.Graph(

            figure=px.pie(

                exp_data,

                values='Advertising_Expenditure',

                names='Vehicle_Type',

                title='Total Advertisement Expenditure for Each Vehicle'

            ),

            style={'width': '50%'}

        )


        # Display four graphs in 2 rows × 2 columns
        return [

            html.Div(

                className='chart-item',

                children=[
                    Y_chart1,
                    Y_chart2
                ],

                style={
                    'display': 'flex',
                    'width': '100%'
                }

            ),


            html.Div(

                className='chart-item',

                children=[
                    Y_chart3,
                    Y_chart4
                ],

                style={
                    'display': 'flex',
                    'width': '100%'
                }

            )

        ]


    else:

        return None


# ---------------------------------------------------------
# Run the Dash application
# ---------------------------------------------------------

if __name__ == '__main__':

    app.run(debug=True)