import re
from typing import List, Dict, Tuple, Set
import pandas as pd

class NetworkAnalyzer:
    """
    Improved network analyzer with precise connection matching
    """
    
    def __init__(self):
        self.person_names = set()
        self.connection_map = {}
        self.edge_data = []
    
    def extract_person_names(self, all_people: List[Dict]) -> Set[str]:
        """
        Extract all person names from the data
        """
        names = set()
        for person in all_people:
            names.add(person['name'])
        return names
    
    def parse_connections(self, connections_text: str) -> List[Dict]:
        """
        Parse connection text into structured data
        Format: "Person1: Detail1; Person2: Detail2"
        """
        if not connections_text:
            return []
        
        connections = []
        # Split by semicolon first, then by colon
        parts = re.split(r';\s*', connections_text.strip())
        
        for part in parts:
            if ':' in part:
                person_detail = part.split(':', 1)
                if len(person_detail) == 2:
                    person_name = person_detail[0].strip()
                    detail = person_detail[1].strip()
                    connections.append({
                        'person': person_name,
                        'detail': detail,
                        'type': self._classify_connection(detail)
                    })
        
        return connections
    
    def _classify_connection(self, detail: str) -> str:
        """
        Classify the type of connection based on the detail
        """
        detail_lower = detail.lower()
        
        if any(word in detail_lower for word in ['alumni', 'university', 'school', 'college']):
            return 'alumni'
        elif any(word in detail_lower for word in ['work', 'company', 'merck', 'roche', 'pfizer']):
            return 'work'
        elif any(word in detail_lower for word in ['event', 'conference', 'bio', 'cphi']):
            return 'event'
        elif any(word in detail_lower for word in ['network', 'shared']):
            return 'network'
        else:
            return 'other'
    
    def create_precise_network_elements(self, bd_data: pd.DataFrame, leadership_data: List[Dict]) -> Tuple[List[Dict], List[Dict]]:
        """
        Create network elements with precise connection matching
        """
        # Combine all people
        all_people = leadership_data + bd_data.to_dict('records')
        
        # Extract all person names
        self.person_names = self.extract_person_names(all_people)
        
        # Build connection map
        self.connection_map = {}
        connection_counts = {}
        
        for person in all_people:
            person_name = person['name']
            connections_text = person.get('connections') or person.get('key_connections', '')
            
            if connections_text:
                parsed_connections = self.parse_connections(connections_text)
                self.connection_map[person_name] = parsed_connections
                
                # Count valid connections (only to people in our dataset)
                valid_connections = [
                    conn for conn in parsed_connections 
                    if conn['person'] in self.person_names
                ]
                connection_counts[person_name] = len(valid_connections)
            else:
                connection_counts[person_name] = 0
        
        # Create nodes
        nodes = self._create_nodes(all_people, connection_counts)
        
        # Create edges
        edges = self._create_edges()
        
        return nodes, edges
    
    def _create_nodes(self, all_people: List[Dict], connection_counts: Dict[str, int]) -> List[Dict]:
        """
        Create node elements for the network graph
        """
        nodes = []
        max_connections = max(connection_counts.values()) if connection_counts else 1
        
        for person in all_people:
            person_name = person['name']
            conn_count = connection_counts.get(person_name, 0)
            
            # Scale size from 20 to 80 based on connection count
            node_size = 20 + (conn_count / max_connections) * 60 if max_connections > 0 else 20
            
            # Determine node class
            if person.get('company') and person['company'] != 'Asymchem':
                node_class = 'bd_person'
            else:
                node_class = 'leader'
            
            # Create detailed tooltip
            tooltip = self._create_node_tooltip(person, conn_count)
            
            nodes.append({
                'data': {
                    'id': person_name,
                    'label': person_name,
                    'size': node_size,
                    'tooltip': tooltip,
                    'title': person.get('title', ''),
                    'company': person.get('company', 'Asymchem'),
                    'connections_count': conn_count
                },
                'classes': node_class
            })
        
        return nodes
    
    def _create_node_tooltip(self, person: Dict, conn_count: int) -> str:
        """
        Create detailed tooltip for a node with enhanced connection details
        """
        name = person['name']
        title = person.get('title', '')
        company = person.get('company', 'Asymchem')
        
        tooltip = f"<b>{name}</b><br>Title: {title}<br>Company: {company}<br>Connections: {conn_count}"
        
        # Add connection details with better formatting
        connections_text = person.get('connections') or person.get('key_connections', '')
        if connections_text:
            parsed_connections = self.parse_connections(connections_text)
            if parsed_connections:
                tooltip += "<br><br><b>Key Connections:</b>"
                for conn in parsed_connections[:5]:  # Show first 5 connections
                    if conn['person'] in self.person_names:
                        # Format connection type with emoji
                        type_emoji = {
                            'alumni': '🎓',
                            'work': '💼',
                            'event': '🎪',
                            'network': '🔗',
                            'other': '📞'
                        }.get(conn['type'], '📞')
                        
                        tooltip += f"<br>{type_emoji} <b>{conn['person']}</b>: {conn['detail']}"
        
        return tooltip
    
    def _create_edges(self) -> List[Dict]:
        """
        Create edge elements based on precise connection matching
        """
        edges = []
        processed_edges = set()
        
        for person_name, connections in self.connection_map.items():
            for connection in connections:
                target_person = connection['person']
                
                # Only create edge if target person exists in our dataset
                if target_person in self.person_names and person_name != target_person:
                    # Create unique edge ID
                    edge_id = tuple(sorted([person_name, target_person]))
                    
                    if edge_id not in processed_edges:
                        edges.append({
                            'data': {
                                'source': person_name,
                                'target': target_person,
                                'connection_type': connection['type'],
                                'detail': connection['detail']
                            }
                        })
                        processed_edges.add(edge_id)
        
        return edges
    
    def get_network_statistics(self) -> Dict:
        """
        Get network statistics for analysis
        """
        if not self.connection_map:
            return {}
        
        total_people = len(self.person_names)
        total_connections = sum(len(conns) for conns in self.connection_map.values())
        valid_connections = sum(
            len([c for c in conns if c['person'] in self.person_names])
            for conns in self.connection_map.values()
        )
        
        # Connection type distribution
        connection_types = {}
        for connections in self.connection_map.values():
            for conn in connections:
                conn_type = conn['type']
                connection_types[conn_type] = connection_types.get(conn_type, 0) + 1
        
        return {
            'total_people': total_people,
            'total_connections': total_connections,
            'valid_connections': valid_connections,
            'connection_types': connection_types,
            'average_connections': valid_connections / total_people if total_people > 0 else 0
        }
    
    def find_central_people(self, top_n: int = 5) -> List[Dict]:
        """
        Find the most connected people in the network
        """
        if not self.connection_map:
            return []
        
        # Count incoming connections for each person
        incoming_counts = {}
        for person_name, connections in self.connection_map.items():
            for connection in connections:
                target = connection['person']
                if target in self.person_names:
                    incoming_counts[target] = incoming_counts.get(target, 0) + 1
        
        # Sort by connection count
        sorted_people = sorted(
            incoming_counts.items(),
            key=lambda x: x[1],
            reverse=True
        )
        
        return [
            {'name': name, 'connections': count}
            for name, count in sorted_people[:top_n]
        ]
    
    def suggest_connections(self, person_name: str) -> List[Dict]:
        """
        Suggest potential connections for a person
        """
        if person_name not in self.connection_map:
            return []
        
        current_connections = {
            conn['person'] for conn in self.connection_map[person_name]
            if conn['person'] in self.person_names
        }
        
        # Find people not currently connected
        potential_connections = self.person_names - current_connections - {person_name}
        
        suggestions = []
        for potential in potential_connections:
            # Find common connections
            common_connections = []
            if potential in self.connection_map:
                for conn in self.connection_map[potential]:
                    if conn['person'] in current_connections:
                        common_connections.append(conn['person'])
            
            if common_connections:
                suggestions.append({
                    'person': potential,
                    'common_connections': common_connections,
                    'reason': f"Connected through: {', '.join(common_connections[:2])}"
                })
        
        return sorted(suggestions, key=lambda x: len(x['common_connections']), reverse=True)
