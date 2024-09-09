import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plotly.figure_factory as ff

import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output


# In[5]:


mj_df = pd.read_csv("https://sports-statistics.com/database/basketball-data/nba/michael-jordan-nba-career-regular-season-stats-by-game.csv", low_memory=False)


# In[11]:


mj_df.head().T


# In[23]:


# Create bins for point differential
bins = [-50, -20, -10, 0, 10, 20, 50] 
labels = ['Big Loss', 'Loss', 'Close Loss', 'Close Win', 'Win', 'Big Win'] 
mj_df['Diff_Bins'] = pd.cut(mj_df['Diff'], bins=bins, labels=labels)

# Group by the bins and calculate average FG_PCT
fg_pct_by_diff = mj_df.groupby('Diff_Bins', observed=True)['FG_PCT'].mean().reset_index()

# Bar plot: Average Field Goal Percentage by Game Difficulty
fig = px.bar(fg_pct_by_diff, x='Diff_Bins', y='FG_PCT',
             labels={'Diff_Bins': 'Game Difficulty (Point Differential)', 'FG_PCT': 'Average FG %'},
             title='Average Field Goal Percentage by Game Difficulty',
             text_auto=True)

# Customize the layout
fig.update_layout(yaxis_tickformat='.0%', xaxis_title='Game Difficulty (Point Differential)', yaxis_title='Average Field Goal Percentage',
                  title_x=0.5)
fig.show()


# In[ ]:


### Create app
app = dash.Dash(__name__)
server = app.server

app.layout = html.Div(
    [
        html.H1("Michael Jordan's Field Goal Percentage by Game Difficulty"),
        
        dcc.Markdown(children="This app shows how Michael Jordan's field goal percentage varied based on the difficulty of the game."),
        
        html.H2("Average Field Goal Percentage by Game Difficulty"),
        
        dcc.Graph(figure=fig_bar)
    ]
)

if __name__ == '__main__':
    app.run_server(debug=True, port=8051, host='0.0.0.0')
