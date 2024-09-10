import numpy as np
import pandas as pd
import plotly.express as px
import dash
from dash import dcc, html
from dash.dependencies import Input, Output

# Load Michael Jordan data
mj_df = pd.read_csv("https://sports-statistics.com/database/basketball-data/nba/michael-jordan-nba-career-regular-season-stats-by-game.csv", low_memory=False)

# Create bins for point differential
bins = [-50, -20, -10, 0, 10, 20, 50]
labels = ['Big Loss', 'Loss', 'Close Loss', 'Close Win', 'Win', 'Big Win']
mj_df['Diff_Bins'] = pd.cut(mj_df['Diff'], bins=bins, labels=labels)

# Group by the bins and calculate average FG_PCT
fg_pct_by_diff = mj_df.groupby('Diff_Bins', observed=True)['FG_PCT'].mean().reset_index()

# Bar plot: Average Field Goal Percentage by Game Difficulty
fig = px.bar(fg_pct_by_diff, x='Diff_Bins', y='FG_PCT',
             labels={'Diff_Bins': 'Game Difficulty (Point Differential)', 'FG_PCT': 'Average FG %'},
             title="Michael Jordan's Average FG% by Game Difficulty",
             text_auto=True,
             color='Diff_Bins')  # Add color for more visual appeal

# Customize layout
fig.update_layout(yaxis_tickformat='.0%',
                  xaxis_title='Game Difficulty (Point Differential)', 
                  yaxis_title='Average Field Goal Percentage',
                  title_x=0.5,
                  template='plotly_dark')  # Use Plotly's dark template for a modern look

# Create the Dash app
app = dash.Dash(__name__)
server = app.server  # For Heroku deployment

# App layout with enhanced formatting
app.layout = html.Div(
    style={'backgroundColor': '#f9f9f9', 'padding': '40px', 'fontFamily': 'Arial, sans-serif'},  # Background styling
    children=[
        html.H1("Michael Jordan's Performance Dashboard", 
                style={'textAlign': 'center', 'color': '#333', 'fontWeight': 'bold'}),
        
        dcc.Markdown(children="""
        This dashboard visualizes how Michael Jordan's field goal percentage varied based on the 
        difficulty of the game. Games are categorized into different point differential bins 
        (e.g., 'Big Win', 'Close Loss', etc.).
        """, style={'textAlign': 'center', 'color': '#666'}),
        
        html.H2("Average Field Goal Percentage by Game Difficulty", 
                style={'textAlign': 'center', 'marginTop': '40px', 'color': '#333'}),

        # Graph component with the formatted figure
        dcc.Graph(
            id='fg_pct_bar_chart',
            figure=fig,
            config={'displayModeBar': False}  # Hide Plotly mode bar for a cleaner look
        )
    ]
)

# Run the app
if __name__ == '__main__':
    app.run_server(debug=False)
