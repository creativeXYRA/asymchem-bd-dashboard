import google.generativeai as genai
import os
from dotenv import load_dotenv
import json

# Load environment variables
load_dotenv()

# Configure Google Gemini API
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
if GOOGLE_API_KEY:
    genai.configure(api_key=GOOGLE_API_KEY)

def generate_pitch_with_ai(bd_person, market_data, connection_context=""):
    """
    Generate a personalized pitch using Google Gemini AI
    
    Args:
        bd_person (dict): BD person information
        market_data (dict): Market data for the company
        connection_context (str): Additional connection context
    
    Returns:
        str: Generated pitch text
    """
    
    if not GOOGLE_API_KEY:
        return generate_fallback_pitch(bd_person, market_data, connection_context)
    
    try:
        # Configure the model
        model = genai.GenerativeModel('gemini-pro')
        
        # Create the prompt
        prompt = f"""
        You are a Business Development professional at Asymchem, a leading pharmaceutical CDMO. 
        Generate a personalized, professional pitch email for a potential client.
        
        Target Person: {bd_person['name']} at {bd_person['company']}
        Company Focus: {market_data['focus']}
        Pain Point: {market_data['pain_point']}
        Asymchem Solution: {market_data['solution']}
        Connection Context: {connection_context}
        
        Requirements:
        1. Professional and personalized tone
        2. Reference the specific pain point and solution
        3. Mention the connection context naturally
        4. Keep it concise (150-200 words)
        5. Include a clear call-to-action
        6. Use business development best practices
        7. Make it specific to their company's focus area
        
        Format the response as a professional email with subject line and body.
        """
        
        # Generate the response
        response = model.generate_content(prompt)
        
        if response.text:
            return response.text
        else:
            return generate_fallback_pitch(bd_person, market_data, connection_context)
            
    except Exception as e:
        print(f"AI generation failed: {e}")
        return generate_fallback_pitch(bd_person, market_data, connection_context)

def generate_fallback_pitch(bd_person, market_data, connection_context=""):
    """
    Fallback pitch generator when AI is not available
    """
    
    subject = f"Partnership Opportunity: {market_data['focus']} Solutions"
    
    pitch_text = f"""
    Subject: {subject}
    
    Dear {bd_person['name']},
    
    I hope this email finds you well. I'm reaching out regarding {bd_person['company']}'s work in {market_data['focus']}.
    
    I understand that {market_data['pain_point']} is a key challenge in your development pipeline. At Asymchem, we've developed {market_data['solution']}, which has helped similar companies overcome this exact challenge.
    
    {connection_context if connection_context else "I believe there's a strong alignment between our capabilities and your needs."}
    
    Would you be available for a brief call next week to discuss how we might support {bd_person['company']}'s {market_data['focus']} initiatives? I'd be happy to share more details about our specific solutions and success stories.
    
    Best regards,
    [Your Name]
    Business Development
    Asymchem
    """
    
    return pitch_text

def analyze_company_fit(company_data, market_data):
    """
    Analyze the fit between a company and Asymchem's capabilities
    """
    
    if not GOOGLE_API_KEY:
        return "AI analysis not available. Please check API configuration."
    
    try:
        model = genai.GenerativeModel('gemini-pro')
        
        prompt = f"""
        Analyze the business fit between {company_data['company']} and Asymchem based on the following data:
        
        Company: {company_data['company']}
        Focus: {market_data['focus']}
        Pain Point: {market_data['pain_point']}
        Market Value: ${market_data['market_value']}M
        Business Potential: ${market_data['business_potential']}M
        Tech Mapping Score: {market_data['tech_mapping']}/10
        
        Provide a brief analysis (2-3 sentences) of:
        1. Strategic fit
        2. Market opportunity
        3. Recommended approach
        
        Keep it concise and actionable.
        """
        
        response = model.generate_content(prompt)
        return response.text if response.text else "Analysis not available."
        
    except Exception as e:
        return f"Analysis failed: {e}"

def generate_connection_insights(connections_text):
    """
    Generate insights about network connections
    """
    
    if not GOOGLE_API_KEY:
        return "AI insights not available. Please check API configuration."
    
    try:
        model = genai.GenerativeModel('gemini-pro')
        
        prompt = f"""
        Analyze these business connections and provide strategic insights:
        
        Connections: {connections_text}
        
        Provide 2-3 actionable insights about:
        1. Leverage opportunities
        2. Relationship building strategies
        3. Potential introduction opportunities
        
        Keep it concise and practical.
        """
        
        response = model.generate_content(prompt)
        return response.text if response.text else "Insights not available."
        
    except Exception as e:
        return f"Insights generation failed: {e}"
