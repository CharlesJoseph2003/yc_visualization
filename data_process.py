import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio
from plotly.subplots import make_subplots
import numpy as np

# Set the renderer to open in browser
pio.renderers.default = 'browser'

# Load the data
# df = pd.read_csv('data_yc_all.csv')
df = pd.read_csv('all_companies_raw.csv')

# Print column names for reference
print(df.columns)

# Select the columns we want, including the logo URL and team size
new_df = df[['name', 'industry', 'subindustry', 'small_logo_thumb_url', 'one_liner', 'team_size']]
print(new_df.head())

# Drop any rows with missing values in the required columns
new_df = new_df.dropna(subset=['name', 'industry'])

# Handle missing team_size values - set to 1 if missing
new_df['team_size'] = new_df['team_size'].fillna(1)

# Convert team_size to numeric, handling any non-numeric values
new_df['team_size'] = pd.to_numeric(new_df['team_size'], errors='coerce')
new_df['team_size'] = new_df['team_size'].fillna(1)  # Replace any NaN after conversion

# Ensure team_size is at least 1 for visualization purposes
new_df['team_size'] = new_df['team_size'].apply(lambda x: max(1, x))

# Create a new column for hover text that includes the logo URL and team size
new_df['hover_text'] = new_df.apply(
    lambda row: f"<b>{row['name']}</b><br>{row['one_liner'] if pd.notna(row['one_liner']) else ''}<br>Industry: {row['industry']}<br>Subindustry: {row['subindustry'] if pd.notna(row['subindustry']) else 'N/A'}<br>Team Size: {int(row['team_size'])}",
    axis=1
)

# Create the treemap visualization with hover information and sized by team_size
fig = px.treemap(
    new_df,
    path=['subindustry', 'name'],  # Hierarchy: industry -> name
    title='YC Companies by Industry (Sized by Team Size)',
    width=1200,
    height=900,
    values='team_size',  # Scale rectangles by team size
    hover_data=['small_logo_thumb_url', 'team_size'],  # Include logo URL and team size in hover data
    custom_data=['small_logo_thumb_url', 'one_liner', 'team_size'],  # Include for potential JavaScript use
    hover_name='name',  # Use name as the main hover title
    color='subindustry',  # Color by industry instead of team size
)

# Update hover template to include more information
fig.update_traces(
    hovertemplate='<b>%{label}</b><br>%{customdata[1]}<br>Industry: %{parent}<br>Team Size: %{customdata[2]}<br>',
    texttemplate='%{label}',
)

# Update layout for better readability
fig.update_layout(
    margin=dict(t=50, l=25, r=25, b=25),
    font=dict(size=12),
    title={
        'text': 'YC Companies by Industry (Sized by Team Size)',
        'x': 0.5,
        'xanchor': 'center',
        'font': {'size': 24}
    },

)

# Add a title to the figure
fig.update_layout(
    title_text="YC Companies by Industry (Sized by Team Size)",
    title_x=0.5,
    title_font_size=24
)

# Show the figure in the browser
fig.show()