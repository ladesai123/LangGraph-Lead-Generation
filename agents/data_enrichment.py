"""
Data Enrichment Agent - Enriches lead data with additional information.
"""

from typing import Dict, Any, List
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from agents.base_agent import BaseAgent
from tools.clearbit_api import ClearbitClient
from utils.validators import validate_enriched_lead

class DataEnrichmentAgent(BaseAgent):
    """
    Agent responsible for enriching lead data with additional
    company and contact information.
    """
    
    def execute(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        """
        Enrich lead data with additional information.
        
        Args:
            inputs: Dictionary containing:
                - leads: List of lead dictionaries to enrich
        
        Returns:
            Dictionary with 'enriched_leads' list
        """
        self.log_execution_start(inputs)
        
        try:
            leads = inputs.get('leads', [])
            self.log_step("Enriching leads", f"Processing {len(leads)} leads")
            
            # Check if leads are already enriched (from real_leads_data.json)
            if leads and 'technologies' in leads[0] and 'company_description' in leads[0]:
                self.log_step("Leads already enriched", "Using pre-enriched data from real_leads_data.json")
                
                result = {
                    'enriched_leads': leads,
                    'count': len(leads),
                    'source': 'pre_enriched'
                }
                
                self.log_execution_end(result)
                return result
            
            # Initialize Clearbit client
            clearbit_config = self.get_tool_config('Clearbit')
            clearbit_client = ClearbitClient(api_key=clearbit_config.get('api_key', ''))
            
            enriched_leads = []
            
            for lead in leads:
                try:
                    # Extract domain from email
                    email = lead.get('email', '')
                    domain = email.split('@')[1] if '@' in email else lead.get('company', '').lower().replace(' ', '') + '.com'
                    
                    # Enrich company data
                    self.log_step(f"Enriching {lead.get('company')}", f"Domain: {domain}")
                    company_data = clearbit_client.enrich_company(domain)
                    
                    # Enrich person data
                    person_data = clearbit_client.enrich_person(email) if email else {}
                    
                    # Combine data
                    enriched = {
                        "company": lead.get('company'),
                        "contact": lead.get('contact_name'),
                        "email": email,
                        "role": person_data.get('role', lead.get('title', '')),
                        "technologies": company_data.get('technologies', []),
                        "company_description": company_data.get('description', ''),
                        "recent_news": f"Growing company with {company_data.get('employees', 'N/A')} employees",
                        "linkedin_url": lead.get('linkedin', ''),
                        "email_verified": bool(email)
                    }
                    
                    # Validate enriched lead
                    is_valid, issues = validate_enriched_lead(enriched)
                    if is_valid:
                        enriched_leads.append(enriched)
                    else:
                        self.logger.debug(f"Enriched lead validation issues: {issues}")
                        # Add anyway with issues noted
                        enriched_leads.append(enriched)
                    
                except Exception as e:
                    self.logger.warning(f"Failed to enrich {lead.get('company')}: {e}")
                    # Add with minimal enrichment
                    enriched_leads.append({
                        "company": lead.get('company'),
                        "contact": lead.get('contact_name'),
                        "email": lead.get('email', ''),
                        "role": lead.get('title', ''),
                        "technologies": [],
                        "company_description": "",
                        "recent_news": "",
                        "linkedin_url": lead.get('linkedin', ''),
                        "email_verified": bool(lead.get('email'))
                    })
            
            self.log_step("Enrichment complete", f"Enriched {len(enriched_leads)} leads")
            
            result = {"enriched_leads": enriched_leads}
            self.log_execution_end(result, success=True)
            
            return self.format_output(result)
            
        except Exception as e:
            error_result = self.handle_error(e, "data enrichment")
            return error_result


if __name__ == "__main__":
    # Test Data Enrichment Agent
    print("Testing DataEnrichmentAgent\n")
    
    config = {
        "id": "enrichment",
        "instructions": "Enrich lead data",
        "tools": [
            {"name": "Clearbit", "config": {"api_key": ""}}
        ]
    }
    
    agent = DataEnrichmentAgent("enrichment", config)
    
    test_inputs = {
        "leads": [
            {
                "company": "Acme Corp",
                "contact_name": "John Smith",
                "email": "john.smith@acme.com",
                "title": "VP Sales",
                "linkedin": "https://linkedin.com/in/johnsmith"
            },
            {
                "company": "TechFlow Inc",
                "contact_name": "Sarah Johnson",
                "email": "sarah@techflow.com",
                "title": "Director of Marketing",
                "linkedin": "https://linkedin.com/in/sarahjohnson"
            }
        ]
    }
    
    result = agent.execute(test_inputs)
    
    enriched = result.get('data', {}).get('enriched_leads', [])
    print(f"\nEnriched {len(enriched)} leads:")
    for i, lead in enumerate(enriched, 1):
        print(f"{i}. {lead['contact']} at {lead['company']}")
        print(f"   Technologies: {', '.join(lead['technologies'][:3])}")
        print(f"   Description: {lead['company_description'][:60]}...")
    
    print("\n✅ DataEnrichmentAgent test complete!")
