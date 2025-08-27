from sqlalchemy import create_engine, Column, Integer, String, Text, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import pandas as pd

Base = declarative_base()

class MarketData(Base):
    __tablename__ = 'market_data'
    
    id = Column(Integer, primary_key=True)
    company = Column(String(255), nullable=False)
    business_potential = Column(Float, nullable=False)
    tech_mapping = Column(Float, nullable=False)
    market_value = Column(Float, nullable=False)
    pain_point = Column(String(255), nullable=False)
    focus = Column(Text, nullable=False)
    solution = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class BDData(Base):
    __tablename__ = 'bd_data'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    company = Column(String(255), nullable=False)
    email = Column(String(255))
    linkedin = Column(String(500))
    school = Column(String(255))
    connections = Column(Text)
    action = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class LeadershipData(Base):
    __tablename__ = 'leadership_data'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    title = Column(String(255), nullable=False)
    key_connections = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class NetworkConnection(Base):
    __tablename__ = 'network_connections'
    
    id = Column(Integer, primary_key=True)
    person1_id = Column(Integer, nullable=False)
    person2_id = Column(Integer, nullable=False)
    connection_type = Column(String(100))  # e.g., 'alumni', 'work', 'event'
    connection_detail = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

def init_database():
    """Initialize the database and create tables"""
    engine = create_engine('sqlite:///asymchem_bd.db', echo=False)
    Base.metadata.create_all(engine)
    return engine

def get_session():
    """Get a database session"""
    engine = create_engine('sqlite:///asymchem_bd.db', echo=False)
    Session = sessionmaker(bind=engine)
    return Session()

def populate_initial_data():
    """Populate the database with initial data"""
    session = get_session()
    
    # Check if data already exists
    if session.query(MarketData).count() > 0:
        session.close()
        return
    
    # Market Data
    market_data = [
        {'company': 'CRISPR Therapeutics', 'business_potential': 500, 'tech_mapping': 8, 'market_value': 1000, 'pain_point': 'Scalability', 'focus': 'Gene therapy and CRISPR-based treatments', 'solution': 'Biocatalysis reduces impurities by 20% for vector purification.'},
        {'company': 'Mersana Therapeutics', 'business_potential': 300, 'tech_mapping': 6, 'market_value': 600, 'pain_point': 'Cost', 'focus': 'ADC development for oncology', 'solution': 'OEB5 facility cuts solvent waste by 25%.'},
        {'company': 'LaNova Medicines', 'business_potential': 200, 'tech_mapping': 7, 'market_value': 400, 'pain_point': 'Regulatory', 'focus': 'ADC and biologics in APAC markets', 'solution': 'STAR AI optimizes yields 15% faster.'},
        {'company': 'Beam Therapeutics', 'business_potential': 350, 'tech_mapping': 7.5, 'market_value': 700, 'pain_point': 'Efficiency', 'focus': 'Base editing therapies', 'solution': 'Flow chemistry improves efficiency.'},
        {'company': 'Sana Biotechnology', 'business_potential': 250, 'tech_mapping': 6.5, 'market_value': 500, 'pain_point': 'Yield', 'focus': 'Cell and gene therapy platforms', 'solution': 'Biocatalysis boosts yield for cell therapy vectors.'},
        {'company': 'Intellia Therapeutics', 'business_potential': 400, 'tech_mapping': 8.5, 'market_value': 800, 'pain_point': 'Scalability', 'focus': 'CRISPR/Cas9 therapeutics', 'solution': 'OEB5 facility supports multi-kg scaling.'},
        {'company': 'Moderna', 'business_potential': 450, 'tech_mapping': 9, 'market_value': 900, 'pain_point': 'Cost', 'focus': 'mRNA-based therapies', 'solution': 'STAR AI optimizes mRNA production costs.'},
        {'company': 'Verve Therapeutics', 'business_potential': 280, 'tech_mapping': 6.8, 'market_value': 560, 'pain_point': 'Regulatory', 'focus': 'Gene editing for cardiovascular diseases', 'solution': 'Biocatalysis ensures regulatory compliance.'},
        {'company': 'Caribou Biosciences', 'business_potential': 320, 'tech_mapping': 7.2, 'market_value': 640, 'pain_point': 'Yield', 'focus': 'CRISPR genome engineering', 'solution': 'Flow chemistry enhances yield.'},
        {'company': 'Editas Medicine', 'business_potential': 270, 'tech_mapping': 6.3, 'market_value': 540, 'pain_point': 'Efficiency', 'focus': 'Gene editing for inherited diseases', 'solution': 'OEB5 facility improves efficiency.'}
    ]
    
    for data in market_data:
        market_record = MarketData(**data)
        session.add(market_record)
    
    # BD Data
    bd_data = [
        {
            'name': 'Adam Macnaughton',
            'company': 'CRISPR Therapeutics',
            'email': 'adam.macnaughton@crisprtx.com',
            'linkedin': 'https://www.linkedin.com/in/adam-macnaughton-502482149',
            'school': 'Harvard Business School',
            'connections': 'Cheng Yi Chen: Shared Merck and Bristol Myers Squibb network; Becky: Attended BIO 2025; James Gage: Harvard University alumni network',
            'action': 'Email Sep 10, 2025: Pitch biocatalysis for vector purification'
        },
        {
            'name': 'Sam Kay',
            'company': 'Mersana Therapeutics',
            'email': 'sam.kay@mersana.com',
            'linkedin': 'https://www.linkedin.com/in/swkay',
            'school': 'McGill University',
            'connections': 'Becky: Attended BIO 2025; Cheng Yi Chen: Merck network via Immunomedics/Gilead deal; You: Novartis network; Xinhui Hu: Roche R&D background',
            'action': 'Becky meets at CPHI, pitch OEB5 for ADC linker scaling'
        },
        {
            'name': 'Paul Kong',
            'company': 'LaNova Medicines',
            'email': 'paul.kong@lanovamed.com',
            'linkedin': 'https://www.linkedin.com/in/paul-kong-lanova',
            'school': 'Shanghai Jiao Tong University School of Medicine',
            'connections': 'Xinhui Hu: Shared Roche and Everest Medicines experience; Cheng Yi Chen: Merck network via LaNova deal; Elut Hsu: Shared background in China',
            'action': 'Email Sep 5, 2025: Pitch OEB5 for ADC scaling'
        }
    ]
    
    for data in bd_data:
        bd_record = BDData(**data)
        session.add(bd_record)
    
    # Leadership Data
    leadership_data = [
        {'name': 'Hao Hong', 'title': 'Chairman & Co-CEO', 'key_connections': 'West China Medical Center; Capital Medical University; Chinese Academy of Medical Sciences'},
        {'name': 'James Gage', 'title': 'CSO', 'key_connections': 'Pfizer; Harvard University (Ph.D.)'},
        {'name': 'Xinhui Hu', 'title': 'CTO', 'key_connections': 'GlaxoSmithKline; Roche; Everest Medicines; Brown University'},
        {'name': 'Cheng Yi Chen', 'title': 'CTO', 'key_connections': 'Bristol Myers Squibb; Mirati; Janssen; Merck; The Ohio State University; Xiamen University'},
        {'name': 'Rui Yang', 'title': 'Co-CEO', 'key_connections': 'Peking University; Tianjin University'},
        {'name': 'Xin Xin Zhi', 'title': 'Chairman-Supervisory Board', 'key_connections': 'Missouri State University'},
        {'name': 'Elut Hsu', 'title': 'President & GM', 'key_connections': 'University of Hong Kong; North Carolina State University'},
        {'name': 'Da Zhang', 'title': 'Director, COO & CFO', 'key_connections': 'Tsinghua University; Tianjin University'}
    ]
    
    for data in leadership_data:
        leadership_record = LeadershipData(**data)
        session.add(leadership_record)
    
    # BD Team Data (as LeadershipData with special title)
    bd_team_data = [
        {'name': 'Becky', 'title': 'Sr. Director of BD', 'key_connections': 'Catalent; Primera Analytical Solutions; BIO 2025; CPHI'},
        {'name': 'You', 'title': 'BD Director', 'key_connections': 'Novartis; Merck; shared network'}
    ]
    
    for data in bd_team_data:
        bd_team_record = LeadershipData(**data)
        session.add(bd_team_record)
    
    session.commit()
    session.close()

def get_market_data():
    """Get market data from database"""
    session = get_session()
    data = session.query(MarketData).all()
    session.close()
    return pd.DataFrame([{
        'company': d.company,
        'business_potential': d.business_potential,
        'tech_mapping': d.tech_mapping,
        'market_value': d.market_value,
        'pain_point': d.pain_point,
        'focus': d.focus,
        'solution': d.solution
    } for d in data])

def get_bd_data():
    """Get BD data from database"""
    session = get_session()
    data = session.query(BDData).all()
    session.close()
    return pd.DataFrame([{
        'name': d.name,
        'company': d.company,
        'email': d.email,
        'linkedin': d.linkedin,
        'school': d.school,
        'connections': d.connections,
        'action': d.action
    } for d in data])

def get_leadership_data():
    """Get leadership data from database"""
    session = get_session()
    data = session.query(LeadershipData).all()
    session.close()
    return [{
        'name': d.name,
        'title': d.title,
        'key_connections': d.key_connections
    } for d in data]

def add_bd_person(name, company, email, linkedin, school, connections, action):
    """Add a new BD person to the database"""
    session = get_session()
    new_person = BDData(
        name=name,
        company=company,
        email=email or '',
        linkedin=linkedin or '',
        school=school or '',
        connections=connections or '',
        action=action or ''
    )
    session.add(new_person)
    session.commit()
    session.close()
    return True
