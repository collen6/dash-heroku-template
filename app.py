import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plotly.figure_factory as ff

import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output


# In[2]:


mj_df = pd.read_csv("https://sports-statistics.com/database/basketball-data/nba/michael-jordan-nba-career-regular-season-stats-by-game.csv", low_memory=False)


# In[3]:


mj_df.head().T


# In[4]:


# Calculate career averages for key metrics
career_stats = mj_df[['PTS', 'AST', 'TRB', 'MP', 'FG_PCT', 'STL', 'BLK', 'TOV', 'PF']].mean()

# Convert to DataFrame for easier display and clear labeling
career_stats_df = career_stats.reset_index()
career_stats_df.columns = ['Metric', 'Career Average (Per Game)']

# Display the career averages
print(career_stats_df)


# In[5]:


# Calculate career totals for key metrics
career_totals = mj_df[['PTS', 'AST', 'TRB', 'MP', 'STL', 'BLK', 'TOV', 'PF']].sum()

# Convert to DataFrame for easier display and clear labeling
career_totals_df = career_totals.reset_index()
career_totals_df.columns = ['Metric', 'Career Total (All Games)']

# Display the career totals
print(career_totals_df)


# In[6]:


fig_avg = px.bar(career_stats_df, x='Metric', y='Career Average (Per Game)',
                 title="Michael Jordan's Career Averages (Per Game)",
                 labels={'Career Average (Per Game)': 'Average'},
                 template='plotly_dark',
                 color='Metric')

fig_avg.update_layout(
    title_x=0.5,  # Center the title
    font=dict(family="Arial, sans-serif", size=14, color="white"),
    xaxis_title='Metric',
    yaxis_title='Average Value',
    hovermode='x unified',
    legend_title_text='Metric',
    yaxis=dict(range=[0, 45])  # Set y-axis range
)

fig_avg.update_traces(
    texttemplate='%{y:.1f}',  # Round to 1 decimal place
    textposition='outside'  # Place text outside the bars
)
fig_avg.show()


# In[7]:


fig_totals = px.bar(career_totals_df, x='Metric', y='Career Total (All Games)',
                    title="Michael Jordan's Career Totals (All Games)",
                    labels={'Career Total (All Games)': 'Total'},
                    template='plotly_dark',
                    color='Metric')

fig_totals.update_layout(
    title_x=0.5,
    font=dict(family="Arial, sans-serif", size=14, color="white"),
    xaxis_title='Metric',
    yaxis_title='Total Value',
    hovermode='x unified',
    legend_title_text='Metric',
    yaxis=dict(range=[0, 50000])
)

fig_totals.update_traces(
    texttemplate='%{y:.1f}',
    textposition='outside'
)
fig_totals.show()


# In[11]:


# Create bins for point differential
bins = [-50, -20, -10, 0, 10, 20, 50]
labels = ['Big Loss', 'Loss', 'Close Loss', 'Close Win', 'Win', 'Big Win']
mj_df['Diff_Bins'] = pd.cut(mj_df['Diff'], bins=bins, labels=labels)

# Group by the bins and calculate average FG_PCT with observed=True to silence the warning
fg_pct_by_diff = mj_df.groupby('Diff_Bins', observed=True)['FG_PCT'].mean().reset_index()

# Create bar plot
fig = px.bar(fg_pct_by_diff, x='Diff_Bins', y='FG_PCT',
             labels={'Diff_Bins': 'Game Difficulty (Point Differential)', 'FG_PCT': 'Average FG %'},
             title="Michael Jordan's Average FG% by Game Difficulty",
             text_auto=True,
             color='Diff_Bins',
             template='plotly_dark')

# Customize layout and text position on top of bars
fig.update_layout(
    yaxis_tickformat='.0%',
    xaxis_title='Game Difficulty (Point Differential)', 
    yaxis_title='Average Field Goal Percentage',
    title_x=0.5,
    font=dict(family="Arial, sans-serif", size=14, color="white"),
    hovermode='x unified',
    yaxis=dict(range=[0, 0.7])  # Set y-axis range from 0 to 70% (0.7)
)

# Display percentages in white on top of the bars
fig.update_traces(
    texttemplate='%{y:.1%}',  # Format as percentage
    textposition='outside',   # Position text outside the bars
    textfont=dict(color="white")  # Set text color to white
)

fig.show()


# In[13]:


fig1 = px.line(mj_df, x='Age', y=['PTS', 'AST', 'TRB', 'MP'],
               labels={'value': 'Count', 'variable': 'Metric'},
               title="Michael Jordan's Performance Over Time",
               template='plotly_dark')

fig1.update_layout(
    title_x=0.5,
    font=dict(family="Arial, sans-serif", size=14, color="white"),
    xaxis_title='Age',
    yaxis_title='Count',
    hovermode='x unified',
    legend_title_text='Metric',
    legend=dict(
        orientation="h",
        yanchor="bottom", y=1,
        xanchor="right", x=1
    )
)

fig1.update_traces(line=dict(width=1.5))
fig1.show()


# In[15]:


# Replace '1' with 'Win' and '0' with 'Loss' in the 'Win' column for better labels
mj_df['Win'] = mj_df['Win'].replace({'1': 'Win', '0': 'Loss'})

# Scatter plot: Points vs Minutes Played (colored by Wins or Losses)
fig_scatter = px.scatter(mj_df, x='MP', y='PTS', color='Win',
                 labels={'MP': 'Minutes Played', 'PTS': 'Points Scored', 'Win': 'Result'},
                 title='Points Scored vs Minutes Played (Colored by Wins and Losses)',
                 color_discrete_map={'Win': 'deepskyblue', 'Loss': 'orange'},  # Bright colors for better contrast
                 template='plotly_dark')  # Use dark template for consistency

# Customize layout
fig_scatter.update_layout(
    title_x=0.5,  # Center the title
    font=dict(family="Arial, sans-serif", size=14, color="white"),  # Consistent font
    xaxis_title='Minutes Played',
    yaxis_title='Points Scored',
    hovermode='x unified',  # Unified hover for consistent display
    legend_title_text='Game Outcome'  # Update legend title to say "Game Outcome"
)

# Show the figure
fig_scatter.show()


# In[27]:


# Create Dash App
app = dash.Dash(__name__)
server = app.server

# CSS styling for a light theme with dark text
app.layout = html.Div(
    style={'backgroundColor': '#f9f9f9', 'padding': '20px', 'fontFamily': 'Arial, sans-serif'},
    children=[
        html.H1("Michael Jordan's Career Performance Analysis", style={'color': '#333', 'textAlign': 'center'}),
        
        # General introduction paragraph
        html.P(
            "This app presents an in-depth analysis of Michael Jordan's career performance, including career totals, averages, game stats, and field goal percentage analysis.",
            style={'color': '#555', 'textAlign': 'center', 'fontSize': '18px'}
        ),
        
        # Analysis section placeholder
        html.Div(
            style={'backgroundColor': '#f1f1f1', 'padding': '20px', 'marginTop': '20px', 'borderRadius': '8px'},
            children=[
                html.H2("Analysis & Insights", style={'color': '#333'}),
                dcc.Markdown(
                    """
                    Add your detailed analysis for each graph here. Explain trends, highlight key moments in Michael Jordan's career, and discuss how the metrics reflect his performance across different phases of his career.
                    """,
                    style={'color': '#333'}
                )
            ]
        ),

        # Section for career totals
        html.Div([
            html.H2("Michael Jordan's Career Totals (All Games)", style={'color': '#333'}),
            dcc.Graph(figure=fig_totals),
            html.P("This graph represents Michael Jordan's total statistics across all games in his career.", style={'color': '#555'})
        ], style={'marginTop': '20px'}),

        # Section for career averages
        html.Div([
            html.H2("Michael Jordan's Career Averages (Per Game)", style={'color': '#333'}),
            dcc.Graph(figure=fig_avg),
            html.P("This chart highlights Michael Jordan's per-game performance averages throughout his career, including points, assists, and rebounds.", style={'color': '#555'})
        ], style={'marginTop': '20px'}),

        # Section for scatter plot (Points vs Minutes Played)
        html.Div([
            html.H2("Points Scored vs Minutes Played (Colored by Wins and Losses)", style={'color': '#333'}),
            dcc.Graph(figure=fig_scatter),
            html.P("This scatter plot shows the relationship between minutes played and points scored, with colors indicating wins and losses.", style={'color': '#555'})
        ], style={'marginTop': '20px'}),

        # Section for performance over time
        html.Div([
            html.H2("Average Points, Assists, Rebounds, and Minutes Played by Age", style={'color': '#333'}),
            dcc.Graph(figure=fig1),
            html.P("This line graph shows how Michael Jordan's performance changed over time in terms of points, assists, rebounds, and minutes played by age.", style={'color': '#555'})
        ], style={'marginTop': '20px'}),

        # Section for FG% by game difficulty
        html.Div([
            html.H2("Average Field Goal Percentage by Game Difficulty", style={'color': '#333'}),
            dcc.Graph(figure=fig),
            html.P("This bar chart breaks down Michael Jordan's average field goal percentage based on the difficulty of the game (point differential).", style={'color': '#555'})
        ], style={'marginTop': '20px'}),
    ]
)


# Run the app
if __name__ == '__main__':
    app.run_server(debug=False)
