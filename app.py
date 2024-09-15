import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plotly.figure_factory as ff

import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output


# In[9]:


mj_df = pd.read_csv("https://sports-statistics.com/database/basketball-data/nba/michael-jordan-nba-career-regular-season-stats-by-game.csv", low_memory=False)


# In[10]:


mj_df.head().T


# In[11]:


# Calculate career averages for key metrics
career_stats = mj_df[['PTS', 'AST', 'TRB', 'MP', 'FG_PCT', 'STL', 'BLK', 'TOV', 'PF']].mean()

# Convert to DataFrame for easier display and clear labeling
career_stats_df = career_stats.reset_index()
career_stats_df.columns = ['Metric', 'Career Average (Per Game)']

# Display the career averages
print(career_stats_df)


# In[12]:


# Calculate career totals for key metrics
career_totals = mj_df[['PTS', 'AST', 'TRB', 'MP', 'STL', 'BLK', 'TOV', 'PF']].sum()

# Convert to DataFrame for easier display and clear labeling
career_totals_df = career_totals.reset_index()
career_totals_df.columns = ['Metric', 'Career Total (All Games)']

# Display the career totals
print(career_totals_df)


# In[13]:


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


# In[14]:


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


# In[15]:


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


# In[33]:


bar_chart_caption = (
    "This bar chart displays Michael Jordan's average field goal percentage across different game difficulties, "
    "from 'Big Loss' to 'Big Win'. The x-axis categorizes the games based on the point differential, and the y-axis shows the shooting efficiency in percentage. "
    "The chart highlights how Jordan's performance typically improved in games where his team won by larger margins. "
    "Notably, his field goal percentage peaked in 'Big Win' scenarios, suggesting that either he performed exceptionally well in less competitive games "
    "or his stellar play was crucial in securing large victories."
)


# In[16]:


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


# In[17]:


line_caption = (
    "This line graph presents Michael Jordan's performance metrics throughout his career, highlighting points (PTS) in purple, "
    "assists (AST) in red, total rebounds (TRB) in green, and minutes played (MP) in blue. The x-axis represents his age from 22 to 40 years. "
    "Notable gaps in his career around ages 30-32 and 35-38 correspond to his retirements. During his first retirement, MJ left to play professional "
    "baseball for the Birmingham Barons, a minor league affiliate of the Chicago White Sox. Following MJ's second retirement, he returned to play for the "
    "Washington Wizards. In two seasons with the Wizards, the team finished with 74 wins and 90 losses and failed to make the playoffs both years. "
    "Not even the GOAT could save the Wizards."
)


# In[18]:


# Convert 'Win' column to categorical strings for discrete color mapping
mj_df['Win'] = mj_df['Win'].astype(str).replace({'1': 'Win', '0': 'Loss'})

# Scatter plot: Points vs Minutes Played (colored by Wins and Losses)
fig_scatter = px.scatter(
    mj_df, 
    x='MP', 
    y='PTS', 
    color='Win',  # Use 'Win' as a discrete category
    labels={'MP': 'Minutes Played', 'PTS': 'Points Scored', 'Win': 'Game Result'},
    title='Points Scored vs Minutes Played (Colored by Wins and Losses)',
    color_discrete_map={'Win': 'deepskyblue', 'Loss': 'orange'},  # Bright colors for better visibility on dark background
    template='plotly_dark'  # Dark theme
)

# Customize layout
fig_scatter.update_layout(
    title_x=0.5,  # Center the title
    font=dict(family="Arial, sans-serif", size=14, color="white"),  # White text for better contrast
    xaxis_title='Minutes Played',
    yaxis_title='Points Scored',
    hovermode='x unified',  # Unified hover for consistent display
    legend_title_text='Game Outcome'  # Update legend title
)

# Show the figure
fig_scatter.show()


# In[37]:


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
    "This app takes a look at the statistics of arguably the greatest player to ever play the game of basketball and"
    "presents an in-depth analysis of Michael Jordan's career performance, including career totals, "
    "averages, game stats, and field goal percentage analysis.",
            style={'color': '#555', 'textAlign': 'center', 'fontSize': '18px'}
        ),
        
        # Analysis section placeholder
        html.Div(
            style={'backgroundColor': '#f1f1f1', 'padding': '20px', 'marginTop': '20px', 'borderRadius': '8px'},
            children=[
                html.H2("Analysis & Insights", style={'color': '#333'}),
                dcc.Markdown(
                    """
                    
Michael Jordan’s career statistics place him among the greatest players in NBA history. His 30.1 points per game average is the highest of any player in league history, cementing his reputation as an elite scorer. 
Jordan's 32,292 career points rank him 5th all-time in total points scored, an impressive feat considering he played fewer games than many of the players ranked above him. In addition to his scoring prowess, Jordan 
contributed significantly in other areas, with 6,672 rebounds and 5,633 assists, showcasing his versatility. His 251.1 playoff games played rank him 5th all-time, further demonstrating his endurance and ability to 
perform under pressure. These rankings emphasize not only Jordan's dominance but also his all-around impact on the game, across multiple eras.
                    """,
                    style={'color': '#333'}
                )
            ]
        ),

        # Side-by-side layout for Career Totals and Career Averages (same size)
        html.Div([
            # Career Totals Section
            html.Div([
                html.H2("Career Totals (All Games)", style={'color': '#333', 'textAlign': 'center'}),
                dcc.Graph(figure=fig_totals, style={'height': '500px'}),  # Fixed height for uniformity
                 html.P(
                    "This chart highlights Michael Jordan's per-game performance averages throughout his career, including points, assists, and rebounds. MJ has amassed an incredible 32,292 points in his career." 
                    "However he is 6,360 points behind the current all-time scoring leader Lebron James and that gap is still growing becuase the timeless 39 year old LBJ is going into his 21st season.  ", 
                    style={'color': '#555', 'textAlign': 'center'})
            ], style={'width': '48%', 'display': 'inline-block', 'padding': '10px', 'verticalAlign': 'top'}),

            # Career Averages Section
            html.Div([
                html.H2("Career Averages (Per Game)", style={'color': '#333', 'textAlign': 'center'}),
                dcc.Graph(figure=fig_avg, style={'height': '500px'}),  # Fixed height for uniformity
                html.P(
                    "This chart highlights Michael Jordan's per-game performance averages throughout his career, including an astounding 30.1 points per game, the highest in NBA history. In addition to scoring," 
                    "Jordan averaged 6.2 rebounds and 5.3 assists per game, showcasing his versatility on both ends of the court.", 
                    style={'color': '#555', 'textAlign': 'center'})
            ], style={'width': '48%', 'display': 'inline-block', 'padding': '10px', 'verticalAlign': 'top'}),
        ], style={'marginTop': '20px', 'textAlign': 'center', 'display': 'flex', 'justifyContent': 'space-between'}),

        # Section for scatter plot (Points vs Minutes Played)
        html.Div([
            html.H2("Points Scored vs Minutes Played (Colored by Wins and Losses)", style={'color': '#333', 'textAlign': 'center'}),
            dcc.Graph(figure=fig_scatter),
            html.P("This scatter plot is interactive! Feel free to hover over data points or draw a box to view specific sections of data! Two cool data points to show are Michael Jordan's career-high points"
                   " in a single game came on March 28, 1990, when he scored 69 points in an overtime victory against none other but the Cleveland Cavaliers. Also Michael Jordan played an incredible 56 minutes in a game during"
                   ". This occurred on December 18, 1987, in a thrilling 4-overtime loss against the Utah Jazz!", 
                   style={'color': '#555', 'textAlign': 'center'})
        ], style={'marginTop': '20px'}),

        # Side-by-side layout for Performance over Time and FG% by Game Difficulty
        html.Div([
            # Performance over Time Section
            html.Div([
                html.H2("Performance Over Time (Points, Assists, Rebounds)", style={'color': '#333', 'textAlign': 'center'}),
                dcc.Graph(figure=fig1, style={'height': '500px'}),
                html.P(line_caption, style={'color': '#555', 'textAlign': 'center'})
            ], style={'width': '48%', 'display': 'inline-block', 'padding': '10px', 'verticalAlign': 'top'}),

            # FG% by Game Difficulty Section
            html.Div([
                html.H2("Field Goal Percentage by Game Difficulty", style={'color': '#333', 'textAlign': 'center'}),
                dcc.Graph(figure=fig, style={'height': '500px'}),
                html.P(bar_chart_caption, style={'color': '#555', 'textAlign': 'center'})
            ], style={'width': '48%', 'display': 'inline-block', 'padding': '10px', 'verticalAlign': 'top'}),
        ], style={'marginTop': '20px', 'textAlign': 'center', 'display': 'flex', 'justifyContent': 'space-between'}),
    ]
)



# Run the app
if __name__ == '__main__':
    app.run_server(debug=False)
