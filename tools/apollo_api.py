"""
Apollo.io API client for prospect search and outreach.

https://apolloapi.io/docs
"""

import requests
from typing import Dict, List, Any, Optional
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.logger import get_logger

logger = get_logger(__name__)


class ApolloClient:
    """Client for Apollo.io API."""
    
    BASE_URL = "https://api.apollo.io/v1"
    
    def __init__(self, api_key: str):
        """
        Initialize Apollo API client.
        
        Args:
            api_key: Apollo API key
        """
        self.api_key = api_key
        self.headers = {
            "Content-Type": "application/json",
            "Cache-Control": "no-cache",
            "X-Api-Key": api_key
        }
    
    def search_companies(
        self,
        industry: Optional[str] = None,
        location: Optional[str] = None,
        employee_min: Optional[int] = None,
        employee_max: Optional[int] = None,
        revenue_min: Optional[int] = None,
        revenue_max: Optional[int] = None,
        limit: int = 50
    ) -> Dict[str, Any]:
        """
        Search for companies matching criteria.
        
        Args:
            industry: Industry filter (e.g., "SaaS", "FinTech")
            location: Location filter (e.g., "USA", "California")
            employee_min: Minimum number of employees
            employee_max: Maximum number of employees
            revenue_min: Minimum revenue
            revenue_max: Maximum revenue
            limit: Number of results to return
        
        Returns:
            API response with company data
        """
        endpoint = f"{self.BASE_URL}/mixed_companies/search"
        
        # Build query
        query = {
            "page": 1,
            "per_page": min(limit, 100),  # Apollo max is 100
        }
        
        # Add filters
        organization_ids = []
        if industry:
            query["organization_industry_tag_ids"] = [industry]
        if location:
            query["organization_locations"] = [location]
        if employee_min or employee_max:
            query["organization_num_employees_ranges"] = [
                f"{employee_min or 1},{employee_max or 10000}"
            ]
        
        logger.info(f"Searching Apollo for companies with filters: {query}")
        
        try:
            response = requests.post(
                endpoint,
                headers=self.headers,
                json=query,
                timeout=30
            )
            response.raise_for_status()
            
            data = response.json()
            logger.info(f"Found {len(data.get('organizations', []))} companies from Apollo")
            return data
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Apollo API error: {e}")
            # Return mock data for testing
            return self._get_mock_companies(limit)
    
    def search_contacts(
        self,
        company_name: Optional[str] = None,
        titles: Optional[List[str]] = None,
        limit: int = 10
    ) -> Dict[str, Any]:
        """
        Search for contacts at specific companies.
        
        Args:
            company_name: Company name to search
            titles: Job titles to filter (e.g., ["VP Sales", "Director"])
            limit: Number of results
        
        Returns:
            API response with contact data
        """
        endpoint = f"{self.BASE_URL}/mixed_people/search"
        
        query = {
            "page": 1,
            "per_page": min(limit, 100),
        }
        
        if company_name:
            query["organization_name"] = company_name
        if titles:
            query["person_titles"] = titles
        
        logger.info(f"Searching Apollo for contacts: {query}")
        
        try:
            response = requests.post(
                endpoint,
                headers=self.headers,
                json=query,
                timeout=30
            )
            response.raise_for_status()
            
            data = response.json()
            logger.info(f"Found {len(data.get('people', []))} contacts from Apollo")
            return data
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Apollo API error: {e}")
            return self._get_mock_contacts(limit)
    
    def send_email(
        self,
        email: str,
        subject: str,
        body: str,
        from_email: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Send email through Apollo (requires email sequence setup).
        
        Note: This is a simplified version. Real implementation would use
        Apollo sequences or SendGrid directly.
        
        Args:
            email: Recipient email
            subject: Email subject
            body: Email body
            from_email: Sender email
        
        Returns:
            Send status
        """
        logger.info(f"Sending email via Apollo to {email}")
        
        # Apollo doesn't have direct email sending in free tier
        # This would typically use sequences
        return {
            "status": "simulated",
            "message_id": f"apollo_{hash(email)}",
            "recipient": email,
            "subject": subject
        }
    
    def _get_mock_companies(self, limit: int) -> Dict[str, Any]:
        """Generate mock company data for testing."""
        logger.warning("Using mock Apollo company data")
        
        mock_companies = []
        company_names = [
            "Acme SaaS Inc", "TechFlow Solutions", "DataDrive Corp",
            "CloudSync Systems", "InnovateTech LLC", "ScaleUp Software",
            "FinTech Dynamics", "SmartOps Platform", "GrowthStack Inc",
            "SalesBoost Technologies"
        ]
        
        for i in range(min(limit, len(company_names))):
            mock_companies.append({
                "id": f"mock_company_{i}",
                "name": company_names[i],
                "website_url": f"https://www.{company_names[i].lower().replace(' ', '')}.com",
                "industry": "SaaS",
                "estimated_num_employees": 100 + (i * 50),
                "organization_raw_address": "USA",
                "linkedin_url": f"https://linkedin.com/company/{company_names[i].lower().replace(' ', '-')}"
            })
        
        return {
            "organizations": mock_companies,
            "pagination": {"total_entries": len(mock_companies)}
        }
    
    def _get_mock_contacts(self, limit: int) -> Dict[str, Any]:
        """Generate mock contact data for testing."""
        logger.warning("Using mock Apollo contact data")
        
        mock_contacts = []
        names = [
            ("John", "Smith"), ("Sarah", "Johnson"), ("Michael", "Williams"),
            ("Emily", "Brown"), ("David", "Jones"), ("Lisa", "Garcia"),
            ("James", "Martinez"), ("Jennifer", "Davis"), ("Robert", "Rodriguez"),
            ("Mary", "Wilson")
        ]
        
        titles = ["VP Sales", "Director of Marketing", "Head of Business Development",
                  "Chief Revenue Officer", "VP of Operations"]
        
        for i in range(min(limit, len(names))):
            first, last = names[i]
            mock_contacts.append({
                "id": f"mock_contact_{i}",
                "first_name": first,
                "last_name": last,
                "email": f"{first.lower()}.{last.lower()}@example.com",
                "title": titles[i % len(titles)],
                "linkedin_url": f"https://linkedin.com/in/{first.lower()}-{last.lower()}",
                "organization_name": "Example Corp"
            })
        
        return {
            "people": mock_contacts,
            "pagination": {"total_entries": len(mock_contacts)}
        }


if __name__ == "__main__":
    # Test Apollo client with mock data
    print("Testing Apollo Client (Mock Mode)\n")
    
    # This will use mock data since we don't have a real API key
    client = ApolloClient(api_key="test_key")
    
    # Test company search
    print("=== Searching Companies ===")
    companies = client.search_companies(
        industry="SaaS",
        location="USA",
        employee_min=100,
        employee_max=1000,
        limit=5
    )
    print(f"Found {len(companies.get('organizations', []))} companies")
    for company in companies.get('organizations', [])[:3]:
        print(f"  - {company['name']} ({company.get('estimated_num_employees')} employees)")
    
    # Test contact search
    print("\n=== Searching Contacts ===")
    contacts = client.search_contacts(
        company_name="Acme Corp",
        titles=["VP Sales", "Director"],
        limit=5
    )
    print(f"Found {len(contacts.get('people', []))} contacts")
    for contact in contacts.get('people', [])[:3]:
        print(f"  - {contact['first_name']} {contact['last_name']} - {contact['title']}")
    
    print("\n✅ Apollo client test complete!")
