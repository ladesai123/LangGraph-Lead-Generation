"""
Clearbit API client for data enrichment.

https://clearbit.com/docs
"""

import requests
from typing import Dict, Any, Optional
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.logger import get_logger

logger = get_logger(__name__)


class ClearbitClient:
    """Client for Clearbit Enrichment API."""
    
    BASE_URL = "https://company.clearbit.com/v2/companies/find"
    
    def __init__(self, api_key: str):
        """
        Initialize Clearbit client.
        
        Args:
            api_key: Clearbit API key
        """
        self.api_key = api_key
        self.headers = {
            "Authorization": f"Bearer {api_key}"
        } if api_key else {}
    
    def enrich_company(self, domain: str) -> Dict[str, Any]:
        """
        Enrich company data using domain.
        
        Args:
            domain: Company domain (e.g., "stripe.com")
        
        Returns:
            Enriched company data
        """
        if not self.api_key:
            return self._get_mock_company_data(domain)
        
        try:
            logger.info(f"Enriching company data for {domain}")
            
            response = requests.get(
                self.BASE_URL,
                headers=self.headers,
                params={"domain": domain},
                timeout=10
            )
            response.raise_for_status()
            
            data = response.json()
            logger.info(f"Successfully enriched data for {domain}")
            
            return self._format_company_data(data)
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Clearbit API error: {e}")
            return self._get_mock_company_data(domain)
    
    def enrich_person(self, email: str) -> Dict[str, Any]:
        """
        Enrich person data using email.
        
        Args:
            email: Person's email address
        
        Returns:
            Enriched person data
        """
        if not self.api_key:
            return self._get_mock_person_data(email)
        
        try:
            logger.info(f"Enriching person data for {email}")
            
            response = requests.get(
                "https://person.clearbit.com/v2/people/find",
                headers=self.headers,
                params={"email": email},
                timeout=10
            )
            response.raise_for_status()
            
            data = response.json()
            logger.info(f"Successfully enriched data for {email}")
            
            return self._format_person_data(data)
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Clearbit API error: {e}")
            return self._get_mock_person_data(email)
    
    def _format_company_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Format Clearbit company data to our schema."""
        return {
            "name": data.get("name"),
            "domain": data.get("domain"),
            "description": data.get("description"),
            "industry": data.get("category", {}).get("industry"),
            "employees": data.get("metrics", {}).get("employees"),
            "revenue": data.get("metrics", {}).get("estimatedAnnualRevenue"),
            "technologies": data.get("tech", []),
            "linkedin": data.get("linkedin", {}).get("handle")
        }
    
    def _format_person_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Format Clearbit person data to our schema."""
        return {
            "name": data.get("name", {}).get("fullName"),
            "title": data.get("employment", {}).get("title"),
            "role": data.get("employment", {}).get("role"),
            "seniority": data.get("employment", {}).get("seniority"),
            "company": data.get("employment", {}).get("name"),
            "linkedin": data.get("linkedin", {}).get("handle"),
            "twitter": data.get("twitter", {}).get("handle")
        }
    
    def _get_mock_company_data(self, domain: str) -> Dict[str, Any]:
        """Generate mock company enrichment data."""
        logger.warning(f"Using mock Clearbit company data for {domain}")
        
        company_name = domain.split('.')[0].title()
        
        return {
            "name": f"{company_name} Inc",
            "domain": domain,
            "description": f"{company_name} is a leading SaaS company providing innovative solutions.",
            "industry": "SaaS",
            "employees": 250,
            "revenue": 50000000,
            "technologies": ["Salesforce", "AWS", "React", "PostgreSQL"],
            "linkedin": f"company/{company_name.lower()}"
        }
    
    def _get_mock_person_data(self, email: str) -> Dict[str, Any]:
        """Generate mock person enrichment data."""
        logger.warning(f"Using mock Clearbit person data for {email}")
        
        name_parts = email.split('@')[0].split('.')
        first_name = name_parts[0].title() if len(name_parts) > 0 else "John"
        last_name = name_parts[1].title() if len(name_parts) > 1 else "Doe"
        
        return {
            "name": f"{first_name} {last_name}",
            "title": "VP of Sales",
            "role": "sales",
            "seniority": "executive",
            "company": "Example Corp",
            "linkedin": f"{first_name.lower()}-{last_name.lower()}",
            "twitter": None
        }


if __name__ == "__main__":
    # Test Clearbit client (mock mode)
    print("Testing Clearbit Client (Mock Mode)\n")
    
    client = ClearbitClient(api_key=None)
    
    # Test company enrichment
    print("=== Enriching Company Data ===")
    company_data = client.enrich_company("stripe.com")
    print(f"Company: {company_data['name']}")
    print(f"Industry: {company_data['industry']}")
    print(f"Employees: {company_data['employees']}")
    print(f"Technologies: {', '.join(company_data['technologies'])}\n")
    
    # Test person enrichment
    print("=== Enriching Person Data ===")
    person_data = client.enrich_person("john.doe@example.com")
    print(f"Name: {person_data['name']}")
    print(f"Title: {person_data['title']}")
    print(f"Company: {person_data['company']}")
    print(f"LinkedIn: {person_data['linkedin']}")
    
    print("\n✅ Clearbit client test complete!")
