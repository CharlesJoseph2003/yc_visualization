import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px
import os

# Initialize the Dash app
app = dash.Dash(__name__, title="Sundai Projects Visualization")
server = app.server  # Needed for deployment platforms like Render

# Load the data
def load_data():
    df = pd.read_csv('data_sundai_data.csv')
    # Select the columns we want
    new_df = df[['title', 'cluster_label', 'description', 'color']]
    # Drop any rows with missing values in the required columns
    new_df = new_df.dropna(subset=['title', 'cluster_label'])
    # Create a count column for sizing
    new_df['count'] = 1
    # Truncate long descriptions for hover to keep them compact
    new_df['short_description'] = new_df['description'].apply(
        lambda x: (x[:100] + '...') if isinstance(x, str) and len(x) > 100 else x
    )
    return new_df

# Create the treemap figure
def create_treemap(df):
    fig = px.treemap(
        df,
        path=['cluster_label', 'title'],  # Hierarchy: cluster_label -> title
        title='Sundai Projects by Cluster Label',
        height=800,  # Taller to fit more content
        values='count',  # Scale rectangles by count
        hover_data=['short_description'],  # Include shortened description in hover data
        custom_data=['short_description'],  # Include for potential JavaScript use
        hover_name='title',  # Use title as the main hover title
        color='cluster_label',  # Color by cluster_label
        branchvalues='total'  # Ensure proper sizing
    )

    # Update hover template to include more information but keep it compact
    fig.update_traces(
        hovertemplate='<b>%{label}</b><br>%{customdata[0]}<br><i>Cluster: %{parent}</i>',
        texttemplate='%{label}',
        textposition='middle center',  # Center text
        insidetextfont=dict(size=11),  # Slightly smaller font for better fit
        marker_line_width=0.5,  # Thin lines between cells
        marker_line_color='white',
    )

    # Update layout for better readability
    fig.update_layout(
        margin=dict(t=50, l=25, r=25, b=25),
        font=dict(size=12),
        title={
            'text': 'Sundai Projects by Cluster Label',
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 24}
        },
        hoverlabel=dict(
            bgcolor="white",
            font_size=12,  # Smaller font for hover
            font_family="Arial",
            font_color="black",  # Explicitly set hover text to black
            bordercolor="#c7c7c7",
            align="left"
        ),
    )
    
    return fig

# Load the data
df = load_data()

# Define the app layout
app.layout = html.Div([
    html.H1("Sundai Projects Visualization", style={'textAlign': 'center', 'marginTop': '20px'}),
    
    html.Div([
        dcc.Graph(
            id='treemap-graph',
            figure=create_treemap(df),
            style={'height': '80vh', 'width': '100%'},
            config={'responsive': True}
        )
    ], style={'width': '100%', 'display': 'flex', 'justifyContent': 'center', 'alignItems': 'center'}),
 
    html.Footer([
        html.P("Sundai Projects Visualization Dashboard", 
               style={'textAlign': 'center', 'marginTop': '20px', 'color': '#666'})
    ])
], style={'fontFamily': 'Arial, sans-serif', 'margin': '0 auto', 'maxWidth': '1800px', 'display': 'flex', 'flexDirection': 'column', 'alignItems': 'center'})

# No callbacks needed since we removed the filter

# Run the app
if __name__ == '__main__':
    app.run_server(debug=False, host='0.0.0.0', port=int(os.environ.get('PORT', 8050)))
