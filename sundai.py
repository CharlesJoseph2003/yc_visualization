import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio
from plotly.subplots import make_subplots
import numpy as np

# Set the renderer to open in browser
pio.renderers.default = 'browser'

# Load the data
df = pd.read_csv('data_sundai_data.csv')

# Print column names for reference
print(df.columns)

# Select the columns we want
new_df = df[['title', 'cluster_label', 'description', 'color']]
print(new_df.head())

# Drop any rows with missing values in the required columns
new_df = new_df.dropna(subset=['title', 'cluster_label'])

# Create a count column for sizing (since we don't have team_size)
# This will ensure each item has at least a size of 1
new_df['count'] = 1

# Create a new column for hover text
new_df['hover_text'] = new_df.apply(
    lambda row: f"<b>{row['title']}</b><br>{row['description'] if pd.notna(row['description']) else ''}<br>Cluster: {row['cluster_label']}",
    axis=1
)

# Truncate long descriptions for hover to keep them compact
new_df['short_description'] = new_df['description'].apply(
    lambda x: (x[:100] + '...') if isinstance(x, str) and len(x) > 100 else x
)

# Create the treemap visualization
fig = px.treemap(
    new_df,
    path=['cluster_label', 'title'],  # Hierarchy: cluster_label -> title
    title='Projects by Cluster Label',
    width=1500,  # Wider to fit more content
    height=1000,  # Taller to fit more content
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

# Add a title to the figure
fig.update_layout(
    title_text="Sundai Projects by Cluster Label",
    title_x=0.5,
    title_font_size=24
)

# Show the figure in the browser
fig.show()
