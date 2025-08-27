# Asymchem BD Dashboard

A comprehensive Business Development dashboard built with Python Dash, featuring AI-powered pitch generation, network analysis, and data persistence.

## Features

### 🎯 Core Functionality
- **Market Prioritization**: Interactive bubble chart showing business potential vs. technical mapping
- **Network Visualization**: Advanced network graph with precise connection matching
- **Data Management**: Persistent storage with SQLite database
- **AI-Powered Pitch Generation**: Personalized pitches using Google Gemini AI
- **Real-time Analytics**: Network statistics and company fit analysis

### 🔧 Technical Improvements

#### 1. Enhanced Network Analysis
- **Precise Connection Matching**: Improved algorithm that accurately identifies connections between people
- **Connection Classification**: Automatically categorizes connections (alumni, work, event, network)
- **Network Statistics**: Real-time metrics including connection counts and centrality analysis
- **Smart Suggestions**: AI-powered connection recommendations

#### 2. Data Persistence
- **SQLite Database**: All data is now stored persistently
- **Structured Schema**: Proper database models for market data, BD personnel, and leadership
- **CRUD Operations**: Full create, read, update, delete functionality
- **Data Integrity**: Automatic timestamps and validation

#### 3. AI Integration
- **Google Gemini API**: Advanced AI for pitch generation and analysis
- **Personalized Content**: Context-aware pitch generation based on company data
- **Fallback System**: Graceful degradation when AI is unavailable
- **Multiple AI Features**: Pitch generation, company fit analysis, connection insights

## Installation

### Prerequisites
- Python 3.8+
- pip

### Setup

1. **Clone the repository**
```bash
git clone <repository-url>
cd asymchem_bd_dashboard
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Set up environment variables**
```bash
cp env_example.txt .env
# Edit .env and add your Google Gemini API key
```

4. **Get Google Gemini API Key**
- Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
- Create a new API key
- Add it to your `.env` file

5. **Run the application**
```bash
python app.py
```

6. **Access the dashboard**
- Open your browser and go to `http://localhost:8050`

## Project Structure

```
asymchem_bd_dashboard/
├── app.py                 # Main Dash application
├── database.py            # Database models and operations
├── network_analyzer.py    # Enhanced network analysis
├── ai_pitch_generator.py  # AI-powered pitch generation
├── requirements.txt       # Python dependencies
├── env_example.txt        # Environment variables template
├── README.md             # This file
└── asymchem_bd.db        # SQLite database (created automatically)
```

## Usage

### Adding New BD Personnel
1. Fill out the form in the "BD Personnel Network" section
2. Include connections in the format: "Person: Detail; Person: Detail"
3. Click "Add to Network" to save to database
4. Network graph updates automatically

### Generating AI Pitches
1. Select a company from the dropdown
2. Click "Generate AI Pitch" for personalized content
3. Click "Analyze Fit" for strategic analysis
4. AI uses company data and connections for context

### Network Analysis
- Hover over nodes to see detailed information
- Node size indicates connection count
- Different colors represent different roles (leaders vs BD personnel)
- Network statistics show real-time metrics

## Database Schema

### Market Data
- Company information
- Business potential and market value
- Pain points and solutions
- Technical mapping scores

### BD Data
- Personnel information
- Company affiliations
- Connection details
- Action items

### Leadership Data
- Internal team information
- Key connections
- Titles and roles

## AI Features

### Pitch Generation
- Personalized based on company focus
- References specific pain points and solutions
- Incorporates connection context
- Professional tone and structure

### Company Analysis
- Strategic fit assessment
- Market opportunity analysis
- Recommended approach
- Data-driven insights

### Connection Insights
- Leverage opportunities
- Relationship building strategies
- Introduction suggestions

## Configuration

### Environment Variables
- `GOOGLE_API_KEY`: Required for AI features
- `DATABASE_URL`: Optional database configuration

### Customization
- Modify `database.py` to change data models
- Update `network_analyzer.py` for different connection logic
- Customize `ai_pitch_generator.py` for different AI prompts

## Troubleshooting

### Common Issues

1. **AI Features Not Working**
   - Check your Google Gemini API key
   - Ensure `.env` file is in the project root
   - Verify API key has proper permissions

2. **Database Errors**
   - Delete `asymchem_bd.db` to reset
   - Check file permissions
   - Ensure SQLite is installed

3. **Network Graph Issues**
   - Clear browser cache
   - Check connection format in data
   - Verify all required fields are filled

### Performance
- Database queries are optimized for speed
- Network analysis uses efficient algorithms
- AI calls are cached when possible

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is proprietary to Asymchem. All rights reserved.

## Support

For technical support or questions:
- Check the troubleshooting section
- Review the code comments
- Contact the development team

## Future Enhancements

- [ ] Real-time data synchronization
- [ ] Advanced analytics dashboard
- [ ] Integration with CRM systems
- [ ] Mobile-responsive design
- [ ] Multi-language support
- [ ] Advanced AI features
- [ ] Export functionality
- [ ] User authentication
