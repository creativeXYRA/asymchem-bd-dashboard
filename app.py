import dash
from dash import Dash, html, dcc, dash_table, Input, Output, State, callback_context
import plotly.graph_objects as go
import pandas as pd
import dash_cytoscape as cyto
import json
import os
from dotenv import load_dotenv

# Import our custom modules
from database import init_database, populate_initial_data, get_market_data, get_bd_data, get_leadership_data, add_bd_person
from network_analyzer import NetworkAnalyzer
from ai_pitch_generator import generate_pitch_with_ai, analyze_company_fit, generate_connection_insights

# Load environment variables
load_dotenv()

# Initialize database
init_database()
populate_initial_data()

# Initialize network analyzer
network_analyzer = NetworkAnalyzer()

# Initialize the Dash app
app = Dash(__name__, external_stylesheets=['https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css'])

# Get initial data
df_market = get_market_data()
df_bd = get_bd_data()
leadership_data = get_leadership_data()

# Step 3: Prepare Additional Data for New Visualizations
# Competitor Analysis Radar Chart Data
competitor_data = [
    { "name": "Asymchem", "data": [9, 5, 9, 8, 7, 7] },
    { "name": "Lonza", "data": [5, 10, 6, 9, 10, 10] },
    { "name": "WuXi AppTec", "data": [7, 9, 9, 10, 8, 9] },
    { "name": "Catalent", "data": [6, 9, 8, 9, 10, 10] }
]

# Customer Opportunity Matrix Data
customer_opportunity_data = [
    { "client": "CRISPR Therapeutics", "x": 8, "y": 500, "note": "Pain Point: Scalability. Solution: Biocatalysis reduces impurities by 20% for vector purification." },
    { "client": "Mersana Therapeutics", "x": 6, "y": 300, "note": "Pain Point: Cost. Solution: OEB5 facility cuts solvent waste by 25%." },
    { "client": "LaNova Medicines", "x": 7, "y": 200, "note": "Pain Point: Regulatory. Solution: STAR AI optimizes yields 15% faster." },
    { "client": "Beam Therapeutics", "x": 7.5, "y": 350, "note": "Pain Point: Efficiency. Solution: Flow chemistry improves efficiency." },
    { "client": "Sana Biotechnology", "x": 6.5, "y": 250, "note": "Pain Point: Yield. Solution: Biocatalysis boosts yield for cell therapy vectors." },
    { "client": "Intellia Therapeutics", "x": 8.5, "y": 400, "note": "Pain Point: Scalability. Solution: OEB5 facility supports multi-kg scaling." },
    { "client": "Moderna", "x": 9, "y": 450, "note": "Pain Point: Cost. Solution: STAR AI optimizes mRNA production costs." },
    { "client": "Verve Therapeutics", "x": 6.8, "y": 280, "note": "Pain Point: Regulatory. Solution: Biocatalysis ensures regulatory compliance." },
    { "client": "Caribou Biosciences", "x": 7.2, "y": 320, "note": "Pain Point: Yield. Solution: Flow chemistry enhances yield." },
    { "client": "Editas Medicine", "x": 6.3, "y": 270, "note": "Pain Point: Efficiency. Solution: OEB5 facility improves efficiency." }
]

# CDMO Competitive Analysis Table Data
cdmo_comparison_data = [
    {
        'Criteria': 'Core Technology',
        'Asymchem': 'Strengths: Flow Chemistry, Biocatalysis, Synthetic Biology.<br>Focus: Small Molecules, ADC Linker-Payloads, Peptides.',
        'Lonza': 'Strengths: Mammalian Biologics, Cell and Gene Therapies.<br>Focus: Large molecules, advanced modalities (mRNA, viral vectors).',
        'WuXi AppTec': 'Strengths: Integrated CRDMO platform.<br>Focus: Small molecule R&D, Biologics, Cell and Gene Therapy.',
        'Catalent': 'Strengths: Drug Delivery Tech (Softgels, Zydis®).<br>Focus: Small & Large Molecules, Oral Solid, Biologics, Gene Therapy.'
    },
    {
        'Criteria': 'Regulatory Record',
        'Asymchem': 'Strengths: 65+ successful inspections (FDA, EMA, etc.).<br>Focus: End-to-end CMC from R&D to commercialization.',
        'Lonza': 'Strengths: Long-standing reputation for global regulatory compliance.<br>Focus: Highly regulated markets (U.S., EU).',
        'WuXi AppTec': 'Strengths: Strong track record of passing FDA inspections in China.<br>Focus: Comprehensive quality and compliance across its global network.',
        'Catalent': 'Strengths: Over 50 regulatory inspections per year.<br>Focus: Proven track record for FDA and other global agency approvals.'
    },
    {
        'Criteria': 'Market Focus',
        'Asymchem': 'Strengths: Global reach (China, U.S., UK).<br>Focus: Both large pharma (Merck, Pfizer) and emerging biotechs.',
        'Lonza': 'Strengths: Global footprint across five continents.<br>Focus: Major pharmaceutical companies and emerging biotechs, particularly in the U.S. and EU.',
        'WuXi AppTec': 'Strengths: Global footprint (Asia, U.S., Europe).<br>Focus: A broad customer base, including top 20 global pharma companies and ~6,000 active customers.',
        'Catalent': 'Strengths: Over 50 global sites.<br>Focus: Serves 49 of the top 50 pharma companies and 36 of the top 50 biotechs.'
    },
    {
        'Criteria': 'Key Differentiator',
        'Asymchem': 'STAR AI Platform: Tech-driven approach, green chemistry leadership.',
        'Lonza': 'Biologics Expertise: A pioneer and world leader in large-molecule CDMO.',
        'WuXi AppTec': 'Fully Integrated CRDMO: A one-stop-shop model from discovery to commercialization.',
        'Catalent': 'Drug Delivery: Patented technologies that solve complex bioavailability and formulation issues.'
    }
]

# Create bubble chart
fig_bubble = go.Figure(data=[
    go.Scatter(
        x=df_market['business_potential'],
        y=df_market['tech_mapping'],
        mode='markers',
        marker=dict(
            size=df_market['market_value'] / 10,  # Adjusted scaling
            sizemode='area',
            sizemin=15,
            sizeref=2 * max(df_market['market_value']) / (40**2),  # Better size reference
            color=df_market['tech_mapping'],
            colorscale='Viridis',
            showscale=True
        ),
        text=df_market['company'] + '<br>Pain Point: ' + df_market['pain_point'] + '<br>Potential: $' + df_market['business_potential'].astype(str) + 'M' + '<br>Focus: ' + df_market['focus'] + '<br>Solution: ' + df_market['solution'],
        hoverinfo='text'
    )
])

fig_bubble.update_layout(
    title='Market Prioritization: Biosynthesis Opportunities',
    xaxis_title='Business Potential ($M)',
    yaxis_title='Tech Mapping (0-10)',
    plot_bgcolor='#111827',
    paper_bgcolor='#111827',
    font=dict(color='white')
)

# Create visualization functions
def create_radar_chart(data, dimensions):
    """
    Create a radar chart for competitor analysis
    """
    fig = go.Figure()
    
    colors = ['#3B82F6', '#EF4444', '#10B981', '#F59E0B']  # Blue, Red, Green, Yellow
    
    for i, competitor in enumerate(data):
        fig.add_trace(go.Scatterpolar(
            r=competitor['data'],
            theta=dimensions,
            fill='toself',
            name=competitor['name'],
            line_color=colors[i % len(colors)],
            opacity=0.7
        ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 10]
            )),
        showlegend=True,
        title="CDMO Competitor Analysis",
        font=dict(color='white'),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        polar_bgcolor='rgba(31, 41, 55, 0.8)',
        legend=dict(
            bgcolor='rgba(31, 41, 55, 0.8)',
            bordercolor='rgba(75, 85, 99, 0.3)',
            borderwidth=1
        )
    )
    
    return fig

def create_opportunity_matrix(data):
    """
    Create a scatter plot for customer opportunity matrix
    """
    fig = go.Figure()
    
    # Create scatter plot
    fig.add_trace(go.Scatter(
        x=[item['x'] for item in data],
        y=[item['y'] for item in data],
        mode='markers+text',
        text=[item['client'] for item in data],
        textposition="top center",
        marker=dict(
            size=[item['y']/20 for item in data],  # Size based on commercial potential
            color=[item['x'] for item in data],  # Color based on technical fit
            colorscale='Viridis',
            showscale=True,
            colorbar=dict(title="Technical Fit")
        ),
        hovertemplate="<b>%{text}</b><br>" +
                      "Technical Fit: %{x}<br>" +
                      "Commercial Potential: $%{y}M<br>" +
                      "<extra></extra>",
        hoverinfo='all'
    ))
    
    fig.update_layout(
        title="Customer Opportunity Matrix",
        xaxis_title="Technical Fit (1-10)",
        yaxis_title="Commercial Potential ($M)",
        xaxis=dict(range=[5, 10]),
        yaxis=dict(range=[0, 600]),
        plot_bgcolor='rgba(31, 41, 55, 0.8)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white'),
        showlegend=False
    )
    
    return fig

# Create network elements
nodes, edges = network_analyzer.create_precise_network_elements(df_bd, leadership_data)
network_elements = nodes + edges

# App layout
app.layout = html.Div(
    className="bg-gradient-to-br from-gray-900 via-gray-800 to-gray-900 text-white min-h-screen p-4 md:p-6 font-sans",
    children=[
        # Store for BD data
        dcc.Store(id='bd-data-store', data=df_bd.to_json(date_format='iso', orient='split')),
        
        # Store for network statistics
        dcc.Store(id='network-stats-store', data=json.dumps(network_analyzer.get_network_statistics())),

        html.H1("Asymchem BD Dashboard", className="text-2xl md:text-3xl lg:text-4xl font-bold text-center mb-4 md:mb-6 lg:mb-8 text-indigo-400"),

        # Competitor Analysis Radar Chart Section
        html.Div(
            className="bg-gray-800/50 backdrop-blur-sm p-4 md:p-6 rounded-xl shadow-2xl mb-6 md:mb-8 border border-gray-700/50",
            children=[
                html.Div(
                    className="flex justify-between items-center mb-3 md:mb-4",
                    children=[
                        html.H2("CDMO Competitor Analysis", className="text-lg md:text-xl lg:text-2xl font-semibold text-indigo-300 text-center md:text-left"),
                        html.Button(
                            "📋 Copy Data",
                            id="copy-competitor-data",
                            className="px-3 py-1 bg-blue-600 hover:bg-blue-700 text-white text-xs rounded transition-colors"
                        )
                    ]
                ),
                dcc.Graph(
                    id='competitor-radar-chart',
                    figure=create_radar_chart(competitor_data, ['Green Tech', 'Large Molecule', 'Small Molecule', 'Tech Integration', 'Global Footprint', 'Commercial Experience']),
                    className="rounded-lg mb-6"
                ),
                html.H3("CDMO Competitive Analysis Table", className="text-base md:text-lg lg:text-xl font-semibold mb-3 md:mb-4 text-indigo-300 text-center md:text-right"),
                html.Div(
                    className="overflow-x-auto",
                    children=[
                        dash_table.DataTable(
                            id='cdmo-comparison-table',
                            columns=[
                                {'name': 'Criteria', 'id': 'Criteria'},
                                {'name': 'Asymchem', 'id': 'Asymchem'},
                                {'name': 'Lonza', 'id': 'Lonza'},
                                {'name': 'WuXi AppTec', 'id': 'WuXi AppTec'},
                                {'name': 'Catalent', 'id': 'Catalent'}
                            ],
                            data=cdmo_comparison_data,
                            style_table={
                                'overflowX': 'auto',
                                'minWidth': '100%',
                                'maxWidth': '100%',
                                'fontSize': '12px'
                            },
                            style_cell={
                                'backgroundColor': '#1f2937',
                                'color': 'white',
                                'fontFamily': 'sans-serif',
                                'padding': '6px',
                                'border': '1px solid #374151',
                                'textAlign': 'left',
                                'minWidth': '120px',
                                'maxWidth': '250px',
                                'whiteSpace': 'normal',
                                'height': 'auto',
                                'fontSize': '12px'
                            },
                            style_header={
                                'backgroundColor': '#4338ca',
                                'color': 'white',
                                'fontWeight': 'bold',
                                'textTransform': 'uppercase',
                                'padding': '12px',
                                'textAlign': 'center'
                            },
                            style_data_conditional=[
                                {
                                    'if': {'row_index': 'odd'},
                                    'backgroundColor': '#374151'
                                },
                                {
                                    'if': {'column_id': 'Criteria'},
                                    'fontWeight': 'bold',
                                    'backgroundColor': '#1e40af'
                                }
                            ],

                        )
                    ]
                ),
            ]
        ),

        # Customer Opportunity Matrix Section
        html.Div(
            className="bg-gray-800/50 backdrop-blur-sm p-4 md:p-6 rounded-xl shadow-2xl mb-6 md:mb-8 border border-gray-700/50",
            children=[
                html.Div(
                    className="flex justify-between items-center mb-3 md:mb-4",
                    children=[
                        html.H2("Customer Opportunity Matrix", className="text-lg md:text-xl lg:text-2xl font-semibold text-indigo-300 text-center md:text-left"),
                        html.Button(
                            "📋 Copy Data",
                            id="copy-opportunity-data",
                            className="px-3 py-1 bg-blue-600 hover:bg-blue-700 text-white text-xs rounded transition-colors"
                        )
                    ]
                ),
                dcc.Graph(
                    id='opportunity-matrix-chart',
                    figure=create_opportunity_matrix(customer_opportunity_data),
                    className="rounded-lg"
                ),
            ]
        ),

        # Market Prioritization Section
        html.Div(
            className="bg-gray-800/50 backdrop-blur-sm p-4 md:p-6 rounded-xl shadow-2xl mb-6 md:mb-8 border border-gray-700/50",
            children=[
                html.H2("Market Prioritization", className="text-lg md:text-xl lg:text-2xl font-semibold mb-3 md:mb-4 text-indigo-300 text-center md:text-right"),
                dcc.Graph(id='bubble-chart', figure=fig_bubble, className="rounded-lg"),
            ]
        ),

        # Market Analysis Table Section
        html.Div(
            className="bg-gray-800/50 backdrop-blur-sm p-4 md:p-6 rounded-xl shadow-2xl mb-6 md:mb-8 border border-gray-700/50",
            children=[
                html.Div(
                    className="flex justify-between items-center mb-3 md:mb-4",
                    children=[
                        html.H2("Market Analysis Table", className="text-lg md:text-xl lg:text-2xl font-semibold text-indigo-300 text-center md:text-left"),
                        html.Button(
                            "📋 Copy Data",
                            id="copy-market-data",
                            className="px-3 py-1 bg-blue-600 hover:bg-blue-700 text-white text-xs rounded transition-colors"
                        )
                    ]
                ),
                html.Div(
                    className="overflow-x-auto",
                    children=[
                        dash_table.DataTable(
                            id='market-analysis-table',
                            columns=[
                                {'name': 'Company', 'id': 'company'},
                                {'name': 'Potential ($M)', 'id': 'business_potential'},
                                {'name': 'Tech Mapping (0-10)', 'id': 'tech_mapping'},
                                {'name': 'Market Value ($M)', 'id': 'market_value'},
                                {'name': 'Pain Point', 'id': 'pain_point'},
                                {'name': 'Focus', 'id': 'focus'},
                                {'name': "Asymchem's Value", 'id': 'solution'}
                            ],
                            data=df_market.to_dict('records'),
                            style_table={
                                'overflowX': 'auto',
                                'minWidth': '100%',
                                'maxWidth': '100%',
                                'fontSize': '12px'
                            },
                            style_cell={
                                'backgroundColor': '#1f2937',
                                'color': 'white',
                                'fontFamily': 'sans-serif',
                                'padding': '8px',
                                'border': '1px solid #374151',
                                'textAlign': 'left',
                                'minWidth': '120px',
                                'maxWidth': '200px',
                                'whiteSpace': 'normal',
                                'height': 'auto'
                            },
                            style_header={
                                'backgroundColor': '#4338ca',
                                'color': 'white',
                                'fontWeight': 'bold',
                                'textTransform': 'uppercase',
                                'padding': '12px',
                                'textAlign': 'center'
                            },
                            style_data_conditional=[
                                {
                                    'if': {'row_index': 'odd'},
                                    'backgroundColor': '#374151'
                                }
                            ]
                        )
                    ]
                ),
            ]
        ),

        # Network Statistics Section
        html.Div(
            className="bg-gray-800/50 backdrop-blur-sm p-4 md:p-6 rounded-xl shadow-2xl mb-6 md:mb-8 border border-gray-700/50",
            children=[
                html.H2("Network Statistics", className="text-lg md:text-xl lg:text-2xl font-semibold mb-3 md:mb-4 text-indigo-300 text-center md:text-right"),
                html.Div(id='network-stats-display', className="text-right"),
            ]
        ),

        # BD Personnel Network Section
        html.Div(
            className="bg-gray-800/50 backdrop-blur-sm p-4 md:p-6 rounded-xl shadow-2xl mb-6 md:mb-8 border border-gray-700/50",
            children=[
                html.Div(
                    className="flex justify-between items-center mb-3 md:mb-4",
                    children=[
                        html.H2("BD Personnel Network", className="text-lg md:text-xl lg:text-2xl font-semibold text-indigo-300 text-center md:text-left"),
                        html.Button(
                            "📋 Copy Data",
                            id="copy-bd-data",
                            className="px-3 py-1 bg-blue-600 hover:bg-blue-700 text-white text-xs rounded transition-colors"
                        )
                    ]
                ),
                html.P("Enter person information to dynamically update the network graph.", className="text-gray-400 mb-4 text-right"),
                
                # Enhanced input form
                html.Div(
                    className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3 md:gap-4 mb-4",
                    children=[
                        dcc.Input(id='new-name-input', type='text', placeholder='Enter Name...', className='bg-gray-700 p-2 md:p-3 rounded-md text-white border border-gray-600 text-sm md:text-base'),
                        dcc.Input(id='new-company-input', type='text', placeholder='Enter Company...', className='bg-gray-700 p-2 md:p-3 rounded-md text-white border border-gray-600 text-sm md:text-base'),
                        dcc.Input(id='new-email-input', type='email', placeholder='Enter Email...', className='bg-gray-700 p-2 md:p-3 rounded-md text-white border border-gray-600 text-sm md:text-base'),
                        dcc.Input(id='new-linkedin-input', type='url', placeholder='Enter LinkedIn URL...', className='bg-gray-700 p-2 md:p-3 rounded-md text-white border border-gray-600 text-sm md:text-base'),
                        dcc.Input(id='new-school-input', type='text', placeholder='Enter School...', className='bg-gray-700 p-2 md:p-3 rounded-md text-white border border-gray-600 text-sm md:text-base'),
                        dcc.Textarea(id='new-connections-input', placeholder='Enter Connections... (e.g., Becky: CPHI 2025; Chen: Merck network)', className='bg-gray-700 p-2 md:p-3 rounded-md text-white border border-gray-600 text-sm md:text-base'),
                    ]
                ),
                
                html.Button('Add to Network', id='add-person-button', n_clicks=0, className="px-4 md:px-6 py-2 md:py-3 rounded-md font-bold text-gray-900 bg-indigo-400 hover:bg-indigo-300 transition-colors duration-200 mb-4 text-sm md:text-base"),
                
                # Network Graph
                cyto.Cytoscape(
                    id='network-graph',
                    layout={'name': 'cose', 'animate': True, 'animationDuration': 1000},
                    style={'width': '100%', 'height': '400px', 'minHeight': '300px', 'backgroundColor': 'rgba(31, 41, 55, 0.8)', 'borderRadius': '1rem', 'border': '1px solid rgba(75, 85, 99, 0.3)'},
                    stylesheet=[
                        {
                            'selector': 'node',
                            'style': {
                                'label': 'data(label)',
                                'text-valign': 'bottom',
                                'text-halign': 'center',
                                'font-family': 'sans-serif',
                                'font-size': '11px',
                                'font-weight': 'bold',
                                'color': 'white',
                                'height': 'data(size)',
                                'width': 'data(size)',
                                'border-width': 3,
                                'border-color': 'rgba(255, 255, 255, 0.3)',
                                'text-wrap': 'wrap',
                                'text-max-width': '80px',
                                'background-color': '#60a5fa',
                                'background-opacity': 0.8,
                                'transition-property': 'background-color, border-color, height, width',
                                'transition-duration': '0.3s'
                            }
                        },
                        {
                            'selector': '.leader',
                            'style': {
                                'background-color': '#f59e0b',
                                'background-opacity': 0.9,
                                'border-color': 'rgba(245, 158, 11, 0.5)',
                                'border-width': 4
                            }
                        },
                        {
                            'selector': '.bd_person',
                            'style': {
                                'background-color': '#f87171',
                                'background-opacity': 0.9,
                                'border-color': 'rgba(248, 113, 113, 0.5)',
                                'border-width': 4
                            }
                        },
                        {
                            'selector': 'edge',
                            'style': {
                                'line-color': 'rgba(156, 163, 175, 0.6)',
                                'width': 2,
                                'curve-style': 'bezier',
                                'opacity': 0.7,
                                'transition-property': 'line-color, width, opacity',
                                'transition-duration': '0.3s'
                            }
                        }
                    ],
                    elements=network_elements
                ),
                
                html.P("Hover over nodes to see details. Node size indicates the number of connections.", className="text-gray-400 mb-4 text-right"),
                
                # BD Personnel Table
                html.Div(
                    className="overflow-x-auto",
                    children=[
                        dash_table.DataTable(
                            id='bd-personnel-table',
                            columns=[{'name': i, 'id': i} for i in df_bd.columns],
                            data=df_bd.to_dict('records'),
                            style_table={
                                'overflowX': 'auto',
                                'minWidth': '100%',
                                'maxWidth': '100%',
                                'fontSize': '12px'
                            },
                            style_cell={
                                'backgroundColor': '#1f2937',
                                'color': 'white',
                                'fontFamily': 'sans-serif',
                                'padding': '6px',
                                'border': '1px solid #374151',
                                'textAlign': 'left',
                                'minWidth': '100px',
                                'maxWidth': '180px',
                                'whiteSpace': 'normal',
                                'height': 'auto',
                                'fontSize': '12px'
                            },
                            style_header={
                                'backgroundColor': '#4338ca',
                                'color': 'white',
                                'fontWeight': 'bold',
                                'textTransform': 'uppercase',
                                'padding': '12px',
                                'textAlign': 'center'
                            },
                            style_data_conditional=[
                                {
                                    'if': {'row_index': 'odd'},
                                    'backgroundColor': '#374151'
                                }
                            ]
                        )
                    ]
                ),
            ]
        ),

        # AI-Powered Pitch Generation Section
        html.Div(
            className="bg-gray-800/50 backdrop-blur-sm p-4 md:p-6 rounded-xl shadow-2xl mb-6 md:mb-8 border border-gray-700/50",
            children=[
                html.H2("AI-Powered Pitch Generation", className="text-lg md:text-xl lg:text-2xl font-semibold mb-3 md:mb-4 text-indigo-300 text-center md:text-right"),
                
                # Company selection and analysis
                html.Div(
                    className="flex flex-col sm:flex-row items-center space-y-2 sm:space-y-0 sm:space-x-4 mb-4 justify-center sm:justify-end",
                    children=[
                        dcc.Dropdown(
                            id='company-dropdown',
                            options=[{'label': d['company'], 'value': d['company']} for d in df_bd.to_dict('records')],
                            value=df_bd.iloc[0]['company'] if not df_bd.empty else None,
                            className="bg-gray-700 text-white rounded-md flex-grow w-full sm:w-auto",
                            style={
                                'width': '100%',
                                'minWidth': '200px',
                                'backgroundColor': '#374151',
                                'color': 'white'
                            }
                        ),
                        html.Button(
                            'Generate AI Pitch',
                            id='pitch-button',
                            n_clicks=0,
                            className="px-4 md:px-6 py-2 md:py-3 rounded-md font-bold text-gray-900 bg-indigo-400 hover:bg-indigo-300 transition-colors duration-200 text-sm md:text-base w-full sm:w-auto"
                        )
                    ]
                ),
                

                
                # Pitch Output
                html.Div(
                    id='pitch-output',
                    className="bg-gray-700 p-4 rounded-lg text-white text-left"
                ),
            ]
        ),

        # Footer
        html.Div(
            className="bg-gray-800/50 backdrop-blur-sm p-6 rounded-xl shadow-2xl text-right border border-gray-700/50",
            children=[
                html.P('Assumptions: Data is based on public reports, events, and alumni networks for reference only.', className="text-sm text-gray-400 mb-2"),
                html.P('Data Sources:', className="text-sm font-semibold text-gray-400"),
                html.A('LinkedIn', href='https://www.linkedin.com', target='_blank', className="text-blue-400 hover:underline text-sm mr-4"),
                html.A('Company Websites', href='https://www.crisprtx.com', target='_blank', className="text-blue-400 hover:underline text-sm mr-4"),
                html.A('Public News', href='https://www.merck.com/news', target='_blank', className="text-blue-400 hover:underline text-sm mr-4"),
                html.A('Event Schedules', href='https://www.cphi.com', target='_blank', className="text-blue-400 hover:underline text-sm")
            ]
        )
    ]
)

# Callbacks

# Copy data callbacks
@app.callback(
    Output('copy-competitor-data', 'children'),
    Input('copy-competitor-data', 'n_clicks')
)
def copy_competitor_data(n_clicks):
    if n_clicks:
        import pyperclip
        try:
            # Format competitor data for copying
            data_text = "CDMO Competitor Analysis\n\n"
            for item in cdmo_comparison_data:
                data_text += f"{item['Criteria']}:\n"
                data_text += f"  Asymchem: {item['Asymchem'].replace('<br>', ' ')}\n"
                data_text += f"  Lonza: {item['Lonza'].replace('<br>', ' ')}\n"
                data_text += f"  WuXi AppTec: {item['WuXi AppTec'].replace('<br>', ' ')}\n"
                data_text += f"  Catalent: {item['Catalent'].replace('<br>', ' ')}\n\n"
            
            pyperclip.copy(data_text)
            return "✅ Copied!"
        except:
            return "📋 Copy Data"
    return "📋 Copy Data"

@app.callback(
    Output('copy-opportunity-data', 'children'),
    Input('copy-opportunity-data', 'n_clicks')
)
def copy_opportunity_data(n_clicks):
    if n_clicks:
        import pyperclip
        try:
            # Format opportunity data for copying
            data_text = "Customer Opportunity Matrix\n\n"
            for item in customer_opportunity_data:
                data_text += f"{item['client']}:\n"
                data_text += f"  Technical Fit: {item['x']}/10\n"
                data_text += f"  Commercial Potential: ${item['y']}M\n"
                data_text += f"  Note: {item['note']}\n\n"
            
            pyperclip.copy(data_text)
            return "✅ Copied!"
        except:
            return "📋 Copy Data"
    return "📋 Copy Data"

@app.callback(
    Output('copy-market-data', 'children'),
    Input('copy-market-data', 'n_clicks')
)
def copy_market_data(n_clicks):
    if n_clicks:
        import pyperclip
        try:
            # Format market data for copying
            data_text = "Market Analysis Data\n\n"
            for _, row in df_market.iterrows():
                data_text += f"{row['company']}:\n"
                data_text += f"  Business Potential: ${row['business_potential']}M\n"
                data_text += f"  Tech Mapping: {row['tech_mapping']}/10\n"
                data_text += f"  Market Value: ${row['market_value']}M\n"
                data_text += f"  Pain Point: {row['pain_point']}\n"
                data_text += f"  Focus: {row['focus']}\n"
                data_text += f"  Solution: {row['solution']}\n\n"
            
            pyperclip.copy(data_text)
            return "✅ Copied!"
        except:
            return "📋 Copy Data"
    return "📋 Copy Data"

@app.callback(
    Output('copy-bd-data', 'children'),
    Input('copy-bd-data', 'n_clicks'),
    State('bd-data-store', 'data')
)
def copy_bd_data(n_clicks, current_data):
    if n_clicks:
        import pyperclip
        try:
            # Get current BD data
            import io
            df_bd_current = pd.read_json(io.StringIO(current_data), orient='split')
            
            # Format BD data for copying
            data_text = "BD Personnel Data\n\n"
            for _, row in df_bd_current.iterrows():
                data_text += f"{row['name']} ({row['company']}):\n"
                data_text += f"  Email: {row['email']}\n"
                data_text += f"  LinkedIn: {row['linkedin']}\n"
                data_text += f"  School: {row['school']}\n"
                data_text += f"  Connections: {row['connections']}\n"
                data_text += f"  Action: {row['action']}\n\n"
            
            pyperclip.copy(data_text)
            return "✅ Copied!"
        except:
            return "📋 Copy Data"
    return "📋 Copy Data"

@app.callback(
    Output('bd-data-store', 'data'),
    Output('bd-personnel-table', 'data'),
    Output('network-graph', 'elements'),
    Output('network-stats-store', 'data'),
    Input('add-person-button', 'n_clicks'),
    State('new-name-input', 'value'),
    State('new-company-input', 'value'),
    State('new-email-input', 'value'),
    State('new-linkedin-input', 'value'),
    State('new-school-input', 'value'),
    State('new-connections-input', 'value'),
    State('bd-data-store', 'data')
)
def update_bd_data(n_clicks, new_name, new_company, new_email, new_linkedin, new_school, new_connections, current_data):
    if not n_clicks or not new_name or not new_company:
        raise dash.exceptions.PreventUpdate

    # Add to database
    add_bd_person(new_name, new_company, new_email, new_linkedin, new_school, new_connections, '')
    
    # Refresh data from database
    df_bd_updated = get_bd_data()
    leadership_data_updated = get_leadership_data()
    
    # Update network
    global network_analyzer
    nodes, edges = network_analyzer.create_precise_network_elements(df_bd_updated, leadership_data_updated)
    network_elements_updated = nodes + edges
    
    # Get updated statistics
    stats = network_analyzer.get_network_statistics()
    
    return (
        df_bd_updated.to_json(date_format='iso', orient='split'),
        df_bd_updated.to_dict('records'),
        network_elements_updated,
        json.dumps(stats)
    )

@app.callback(
    Output('network-stats-display', 'children'),
    Input('network-stats-store', 'data')
)
def update_network_stats(stats_data):
    if not stats_data:
        return "No statistics available"
    
    stats = json.loads(stats_data)
    
    return html.Div([
        html.P(f"Total People: {stats.get('total_people', 0)}", className="text-gray-300 text-sm md:text-base"),
        html.P(f"Total Connections: {stats.get('total_connections', 0)}", className="text-gray-300 text-sm md:text-base"),
        html.P(f"Valid Connections: {stats.get('valid_connections', 0)}", className="text-gray-300 text-sm md:text-base"),
        html.P(f"Average Connections: {stats.get('average_connections', 0):.1f}", className="text-gray-300 text-sm md:text-base"),
    ])

@app.callback(
    Output('pitch-output', 'children'),
    Input('pitch-button', 'n_clicks'),
    State('company-dropdown', 'value'),
    State('bd-data-store', 'data')
)
def generate_pitch(n_clicks, company_name, current_data):
    if n_clicks is None or not company_name:
        raise dash.exceptions.PreventUpdate
    
    # Get current BD data
    import io
    df_bd_current = pd.read_json(io.StringIO(current_data), orient='split')
    
    # Find matching BD data
    target_bd = df_bd_current[df_bd_current['company'] == company_name]
    if target_bd.empty:
        return "No BD data found for this company."
    
    target_bd_row = target_bd.iloc[0]
    
    # Find matching market data
    target_market = df_market[df_market['company'] == company_name]
    if target_market.empty:
        return "No market data found for this company."
    
    target_market_row = target_market.iloc[0]
    
    # Generate AI pitch
    pitch_text = generate_pitch_with_ai(
        target_bd_row.to_dict(),
        target_market_row.to_dict(),
        target_bd_row.get('connections', '')
    )
    
    return dcc.Markdown(pitch_text)



if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8050)
