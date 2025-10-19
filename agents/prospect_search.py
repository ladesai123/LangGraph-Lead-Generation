"""
Prospect Search Agent - Finds leads using Clay and Apollo APIs.
"""

from typing import Dict, Any, List
import sys
import json
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from agents.base_agent import BaseAgent
from tools.apollo_api import ApolloClient
from utils.validators import validate_lead_data

class ProspectSearchAgent(BaseAgent):
    """
    Agent responsible for searching and discovering prospects
    that match the Ideal Customer Profile (ICP).
    """
    
    def execute(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        """
        Search for prospects matching ICP criteria.
        
        Args:
            inputs: Dictionary containing:
                - icp: ICP criteria (industry, location, etc.)
                - signals: Growth signals to look for
                - limit: Number of leads to find
                - use_real_data: If True, load from real_leads_data.json
        
        Returns:
            Dictionary with 'leads' list
        """
        self.log_execution_start(inputs)
        
        try:
            # Check if we should use real data
            use_real_data = inputs.get('use_real_data', False)
            
            if use_real_data:
                # Load real leads from file
                real_data_path = Path(__file__).parent.parent / 'real_leads_data.json'
                if real_data_path.exists():
                    self.log_step("Loading real data", f"From: {real_data_path}")
                    with open(real_data_path, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        leads = data.get('leads', [])
                    
                    self.log_step("Lead collection complete", f"Found {len(leads)} real leads")
                    
                    result = {
                        'leads': leads,
                        'count': len(leads),
                        'source': 'real_data_file'
                    }
                    
                    self.log_execution_end(result)
                    return result
            
            # Original Apollo API logic
            # Extract inputs
            icp = inputs.get('icp', {})
            signals = inputs.get('signals', [])
            limit = inputs.get('limit', 50)
            
            self.log_step("Extracting ICP criteria", f"Industry: {icp.get('industry')}, Limit: {limit}")
            
            # Initialize Apollo client
            apollo_config = self.get_tool_config('ApolloAPI')
            apollo_client = ApolloClient(api_key=apollo_config.get('api_key', ''))
            
            # Search for companies
            self.log_step("Searching companies", "Using Apollo API")
            companies = apollo_client.search_companies(
                industry=icp.get('industry'),
                location=icp.get('location'),
                employee_min=icp.get('employee_count', {}).get('min'),
                employee_max=icp.get('employee_count', {}).get('max'),
                revenue_min=icp.get('revenue', {}).get('min'),
                revenue_max=icp.get('revenue', {}).get('max'),
                limit=limit
            )
            
            # Process companies and find contacts
            leads = []
            organizations = companies.get('organizations', [])
            
            self.log_step("Finding contacts", f"Processing {len(organizations)} companies")
            
            for org in organizations[:limit]:
                # Get contacts for this company
                contacts = apollo_client.search_contacts(
                    company_name=org.get('name'),
                    titles=["VP", "Director", "Head", "Chief"],
                    limit=2  # Get top 2 contacts per company
                )
                
                people = contacts.get('people', [])
                
                # Create lead entries
                for person in people[:1]:  # Take first contact
                    lead = {
                        "company": org.get('name'),
                        "contact_name": f"{person.get('first_name', '')} {person.get('last_name', '')}".strip(),
                        "email": person.get('email', ''),
                        "linkedin": person.get('linkedin_url', ''),
                        "title": person.get('title', ''),
                        "signal": signals[0] if signals else "icp_match",
                        "company_size": org.get('estimated_num_employees', 0),
                        "estimated_revenue": org.get('metrics', {}).get('estimatedAnnualRevenue', 0) if isinstance(org.get('metrics'), dict) else 0
                    }
                    
                    # Validate lead
                    is_valid, issues = validate_lead_data(lead)
                    if is_valid:
                        leads.append(lead)
                    else:
                        self.logger.debug(f"Skipping invalid lead: {issues}")
            
            self.log_step("Lead collection complete", f"Found {len(leads)} valid leads")
            
            result = {"leads": leads}
            self.log_execution_end(result, success=True)
            
            return self.format_output(result)
            
        except Exception as e:
            error_result = self.handle_error(e, "prospect search")
            return error_result


if __name__ == "__main__":
    # Test Prospect Search Agent
    print("Testing ProspectSearchAgent\n")
    
    config = {
        "id": "prospect_search",
        "instructions": "Search for prospects",
        "tools": [
            {"name": "ApolloAPI", "config": {"api_key": "test"}}
        ]
    }
    
    agent = ProspectSearchAgent("prospect_search", config)
    
    test_inputs = {
        "icp": {
            "industry": "SaaS",
            "location": "USA",
            "employee_count": {"min": 100, "max": 1000},
            "revenue": {"min": 20000000, "max": 200000000}
        },
        "signals": ["recent_funding"],
        "limit": 5
    }
    
    result = agent.execute(test_inputs)
    
    leads = result.get('data', {}).get('leads', [])
    print(f"\nFound {len(leads)} leads:")
    for i, lead in enumerate(leads[:3], 1):
        print(f"{i}. {lead['contact_name']} at {lead['company']} ({lead['title']})")
    
    print("\n✅ ProspectSearchAgent test complete!")
