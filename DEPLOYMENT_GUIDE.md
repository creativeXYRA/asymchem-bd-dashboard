# Asymchem BD Dashboard - Deployment Guide

## Option 1: Deploy to GitHub Pages

### Step 1: Create GitHub Repository
1. Go to [GitHub](https://github.com) and create a new repository
2. Name it `asymchem-bd-dashboard`
3. Make it public

### Step 2: Prepare for Static Deployment
Since Dash apps are Python-based, we need to convert them to static HTML for GitHub Pages:

1. **Install gunicorn and dash-bootstrap-components:**
```bash
pip install gunicorn dash-bootstrap-components
```

2. **Create a static export script:**
```python
# static_export.py
import dash
from app import app
import dash_bootstrap_components as dbc

# Add bootstrap theme
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Export to static HTML
app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>Asymchem BD Dashboard</title>
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

if __name__ == '__main__':
    app.run_server(debug=True)
```

3. **Create GitHub Actions workflow:**
```yaml
# .github/workflows/deploy.yml
name: Deploy to GitHub Pages

on:
  push:
    branches: [ main ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: '3.9'
    
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
        pip install dash-bootstrap-components gunicorn
    
    - name: Build static site
      run: |
        python static_export.py
    
    - name: Deploy to GitHub Pages
      uses: peaceiris/actions-gh-pages@v3
      with:
        github_token: ${{ secrets.GITHUB_TOKEN }}
        publish_dir: ./_build
```

### Step 3: Push to GitHub
```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/asymchem-bd-dashboard.git
git push -u origin main
```

## Option 2: Deploy to CodePen

### Step 1: Convert to HTML/CSS/JS
Since CodePen doesn't support Python, we need to create a static version:

1. **Create HTML structure:**
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Asymchem BD Dashboard</title>
    <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.js"></script>
    <link href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css" rel="stylesheet">
</head>
<body class="bg-gradient-to-br from-gray-900 via-gray-800 to-gray-900 text-white min-h-screen p-4 md:p-6 font-sans">
    <div id="app">
        <h1 class="text-2xl md:text-3xl lg:text-4xl font-bold text-center mb-4 md:mb-6 lg:mb-8 text-indigo-400">
            Asymchem BD Dashboard
        </h1>
        
        <!-- Add your dashboard sections here -->
        <div id="dashboard-content">
            <!-- Content will be populated by JavaScript -->
        </div>
    </div>
    
    <script src="dashboard.js"></script>
</body>
</html>
```

2. **Create JavaScript file (dashboard.js):**
```javascript
// Sample data
const competitorData = [
    { "name": "Asymchem", "data": [9, 5, 9, 8, 7, 7] },
    { "name": "Lonza", "data": [5, 10, 6, 9, 10, 10] },
    { "name": "WuXi AppTec", "data": [7, 9, 9, 10, 8, 9] },
    { "name": "Catalent", "data": [6, 9, 8, 9, 10, 10] }
];

// Create radar chart
function createRadarChart() {
    const data = competitorData.map(company => ({
        type: 'scatterpolar',
        r: company.data,
        theta: ['Green Tech', 'Large Molecule', 'Small Molecule', 'Tech Integration', 'Global Footprint', 'Commercial Experience'],
        fill: 'toself',
        name: company.name
    }));

    const layout = {
        polar: {
            radialaxis: {
                visible: true,
                range: [0, 10]
            }
        },
        showlegend: true,
        title: "CDMO Competitor Analysis",
        font: { color: 'white' },
        paper_bgcolor: 'rgba(0,0,0,0)',
        plot_bgcolor: 'rgba(0,0,0,0)',
        polar_bgcolor: 'rgba(31, 41, 55, 0.8)'
    };

    Plotly.newPlot('radar-chart', data, layout);
}

// Initialize dashboard
document.addEventListener('DOMContentLoaded', function() {
    createRadarChart();
    
    // Add copy functionality
    document.querySelectorAll('.copy-btn').forEach(btn => {
        btn.addEventListener('click', function() {
            const dataType = this.dataset.type;
            copyData(dataType);
        });
    });
});

function copyData(type) {
    // Implementation for copying data
    console.log(`Copying ${type} data`);
}
```

### Step 2: Upload to CodePen
1. Go to [CodePen](https://codepen.io)
2. Click "Create Pen"
3. Paste the HTML in the HTML panel
4. Add the CSS (Tailwind classes will be automatically processed)
5. Paste the JavaScript in the JS panel
6. Save and share

## Option 3: Deploy to Heroku (Recommended for Full Functionality)

### Step 1: Create Heroku App
1. Install Heroku CLI
2. Create app:
```bash
heroku create asymchem-bd-dashboard
```

### Step 2: Create Procfile
```
web: gunicorn app:server
```

### Step 3: Update app.py
Add this line at the end:
```python
server = app.server
```

### Step 4: Deploy
```bash
git add .
git commit -m "Deploy to Heroku"
git push heroku main
```

## Option 4: Deploy to Streamlit Cloud (Alternative)

### Step 1: Convert to Streamlit
Create `streamlit_app.py`:
```python
import streamlit as st
import plotly.graph_objects as go
import pandas as pd

st.set_page_config(
    page_title="Asymchem BD Dashboard",
    page_icon="📊",
    layout="wide"
)

st.title("Asymchem BD Dashboard")

# Add your visualizations here
# This is a simplified version of your dashboard
```

### Step 2: Deploy to Streamlit Cloud
1. Push to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your repository
4. Deploy

## Recommended Approach

For your use case, I recommend:

1. **GitHub Pages** - For static demo
2. **Heroku** - For full functionality with database
3. **Streamlit Cloud** - For easy deployment and sharing

The GitHub Pages approach will give you a public URL that you can share, while Heroku will maintain all the interactive features.
