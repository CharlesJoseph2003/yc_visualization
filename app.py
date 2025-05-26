import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px
import os
from dotenv import load_dotenv
import dataset

# Load environment variables
load_dotenv()

# Initialize the Dash app
app = dash.Dash(__name__, title="Sundai Projects")
server = app.server  # Needed for deployment platforms like Render

# Load the data
def load_data():
    df_q = db.query("""
SELECT
  p.id AS id,
  p.title AS title,
  p.preview AS preview,
  p.description AS description,
  h.name AS launchLeadId,
  p.is_starred AS is_starred,
  COUNT(pl.id) AS count
FROM
  public."Project" p
JOIN
  public."Hacker" h ON p."launchLeadId" = h.id
LEFT JOIN
  public."ProjectLike" pl ON pl."projectId" = p.id
WHERE
  NOT p.is_broken
  AND p.status = 'APPROVED'::"ProjectStatus"
GROUP BY
  p.id, p.title, h.name
ORDER BY
  count DESC;
""")
    df = pd.DataFrame([row for row in df_q])
    # Create a count column for sizing based on starred status and description length
    df['count'] = df.apply(lambda row: row['count'] if row['is_starred'] else row['count'] / 2, axis=1)
    # Create hyperlinked titles
    df['linked_title'] = df.apply(
        lambda row: f'<a href="https://sundai.club/projects/{row["id"]}" style="color: black; text-decoration: none; target="_blank">{row["title"]}</a>', axis=1
    )
    # Truncate long descriptions for hover to keep them compact
    df['short_description'] = df['title']+': '+df['preview']

    # Save DataFrame to CSV
    #df.to_csv('hacks.csv', index=False)
    return df

# Load the data
try:
    # Get database URL from environment
    db_url = os.getenv('DB_URL')
    # Connect to database
    db = dataset.connect(db_url)

    df = load_data()
except: 
    # use cached
    print("Using cached data")
    df = pd.read_csv('hacks.csv')


# Create the treemap figure
def create_treemap(df):
    fig = px.treemap(
        df,
        path=['launchleadid', 'linked_title'],  # Hierarchy using linked titles
        title='Sundai Projects by Launch Lead',
        height=800,  # Taller to fit more content
        values='count',  # Scale rectangles by count
        hover_data=['short_description'],  # Include shortened description in hover data
        custom_data=['short_description'],  # Include for potential JavaScript use
        hover_name='title',  # Use title as the main hover title
        color='launchleadid',  # Color by cluster_label
        branchvalues='total'  # Ensure proper sizing
    )

    # Update hover template to include more information but keep it compact
    fig.update_traces(
        hovertemplate='%{customdata[0]}',
        texttemplate='%{label}',
        textposition='middle center',  # Center text
        insidetextfont=dict(size=11),  # Slightly smaller font for better fit
        marker_line_width=0.5,  # Thin lines between cells
        marker_line_color='white',
        hoverinfo='skip',  # This will hide hover for non-leaf nodes
    )

    # Update layout for better readability
    fig.update_layout(
        margin=dict(t=50, l=25, r=25, b=25),
        font=dict(size=12),
        title={
            'text': 'Sundai Projects by Launch Lead',
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

app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        <script>
        !function(t,e){var o,n,p,r;e.__SV||(window.posthog=e,e._i=[],e.init=function(i,s,a){function g(t,e){var o=e.split(".");2==o.length&&(t=t[o[0]],e=o[1]),t[e]=function(){t.push([e].concat(Array.prototype.slice.call(arguments,0)))}}(p=t.createElement("script")).type="text/javascript",p.crossOrigin="anonymous",p.async=!0,p.src=s.api_host.replace(".i.posthog.com","-assets.i.posthog.com")+"/static/array.js",(r=t.getElementsByTagName("script")[0]).parentNode.insertBefore(p,r);var u=e;for(void 0!==a?u=e[a]=[]:a="posthog",u.people=u.people||[],u.toString=function(t){var e="posthog";return"posthog"!==a&&(e+="."+a),t||(e+=" (stub)"),e},u.people.toString=function(){return u.toString(1)+".people (stub)"},o="init be ys Ss me gs ws capture Ne calculateEventProperties xs register register_once register_for_session unregister unregister_for_session Rs getFeatureFlag getFeatureFlagPayload isFeatureEnabled reloadFeatureFlags updateEarlyAccessFeatureEnrollment getEarlyAccessFeatures on onFeatureFlags onSurveysLoaded onSessionId getSurveys getActiveMatchingSurveys renderSurvey canRenderSurvey canRenderSurveyAsync identify setPersonProperties group resetGroups setPersonPropertiesForFlags resetPersonPropertiesForFlags setGroupPropertiesForFlags resetGroupPropertiesForFlags reset get_distinct_id getGroups get_session_id get_session_replay_url alias set_config startSessionRecording stopSessionRecording sessionRecordingStarted captureException loadToolbar get_property getSessionProperty Is ks createPersonProfile Ps bs opt_in_capturing opt_out_capturing has_opted_in_capturing has_opted_out_capturing clear_opt_in_out_capturing $s debug Es getPageViewId captureTraceFeedback captureTraceMetric".split(" "),n=0;n<o.length;n++)g(u,o[n]);e._i.push([i,s,a])},e.__SV=1)}(document,window.posthog||[]);
        posthog.init('phc_W56RYVhEsXxwY3dVEDBfQRVvkMwjJ4dTOLq7Zb2lCZb', {
            api_host: 'https://us.i.posthog.com',
            person_profiles: 'identified_only', // or 'always' to create profiles for anonymous users as well
        })
        </script>
        {%metas%}
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
'''

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
            html.P("Click on the name of a box to open the hack page. The area of each hack is proportional to popularity. Zoom in to see the detail!", 
                style={'textAlign': 'center', 'marginTop': '20px', 'color': '#666'}),
            html.P("Project by Jordan Tian, Charles Joseph, Aleks Jakulin, Jack Yu, Jonas Schafer, with help from Artem Lukoianov.",
                style={'textAlign': 'center', 'marginTop': '20px', 'color': '#666'}),
            html.A("Hack Home Page", href="https://www.sundai.club/projects/c5be2116-c856-4aad-a852-b257d264d3e9", target="_blank", style={'textAlign': 'center', 'marginTop': '20px', 'color': '#666'}),
        ])
    ], style={'fontFamily': 'Arial, sans-serif', 'margin': '0 auto', 'maxWidth': '1800px', 'display': 'flex', 'flexDirection': 'column', 'alignItems': 'center'})

# Run the app
if __name__ == '__main__':
    app.run_server(debug=False, host='0.0.0.0', port=int(os.environ.get('PORT', 8050)))
