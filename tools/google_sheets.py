"""
Google Sheets API client for feedback tracking and recommendations.

https://developers.google.com/sheets/api
"""

import gspread
from google.oauth2.service_account import Credentials
from typing import Dict, List, Any, Optional
from datetime import datetime
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.logger import get_logger

logger = get_logger(__name__)


class GoogleSheetsClient:
    """Client for Google Sheets API."""
    
    SCOPES = [
        'https://www.googleapis.com/auth/spreadsheets',
        'https://www.googleapis.com/auth/drive'
    ]
    
    def __init__(self, credentials_path: Optional[str] = None, sheet_id: Optional[str] = None):
        """
        Initialize Google Sheets client.
        
        Args:
            credentials_path: Path to Google service account credentials JSON
            sheet_id: Google Sheet ID to work with
        """
        self.credentials_path = credentials_path
        self.sheet_id = sheet_id
        self.client = None
        self.sheet = None
        
        if credentials_path and Path(credentials_path).exists():
            try:
                creds = Credentials.from_service_account_file(
                    credentials_path,
                    scopes=self.SCOPES
                )
                self.client = gspread.authorize(creds)
                
                if sheet_id:
                    self.sheet = self.client.open_by_key(sheet_id)
                
                logger.info("Google Sheets client initialized successfully")
            except Exception as e:
                logger.error(f"Failed to initialize Google Sheets client: {e}")
        else:
            logger.warning("Google Sheets client initialized without credentials - will use mock mode")
    
    def write_recommendations(
        self,
        recommendations: List[Dict[str, Any]],
        worksheet_name: str = "Recommendations"
    ) -> bool:
        """
        Write campaign recommendations to Google Sheet.
        
        Args:
            recommendations: List of recommendation dictionaries
            worksheet_name: Name of the worksheet to write to
        
        Returns:
            True if successful
        """
        if not self.client or not self.sheet:
            return self._mock_write_recommendations(recommendations, worksheet_name)
        
        try:
            # Get or create worksheet
            try:
                worksheet = self.sheet.worksheet(worksheet_name)
            except gspread.WorksheetNotFound:
                worksheet = self.sheet.add_worksheet(
                    title=worksheet_name,
                    rows=100,
                    cols=10
                )
            
            # Prepare headers
            headers = [
                "Timestamp",
                "Category",
                "Current Value",
                "Suggested Value",
                "Rationale",
                "Expected Impact",
                "Confidence",
                "Status"
            ]
            
            # Write headers if sheet is empty
            if worksheet.row_count == 0 or worksheet.cell(1, 1).value == "":
                worksheet.append_row(headers)
            
            # Write recommendations
            for rec in recommendations:
                row = [
                    datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    rec.get("category", ""),
                    rec.get("current_value", ""),
                    rec.get("suggested_value", ""),
                    rec.get("rationale", ""),
                    rec.get("expected_impact", ""),
                    rec.get("confidence", ""),
                    "Pending Approval"
                ]
                worksheet.append_row(row)
            
            logger.info(f"Wrote {len(recommendations)} recommendations to Google Sheets")
            return True
            
        except Exception as e:
            logger.error(f"Error writing to Google Sheets: {e}")
            return False
    
    def write_campaign_results(
        self,
        campaign_id: str,
        metrics: Dict[str, Any],
        worksheet_name: str = "Campaigns"
    ) -> bool:
        """
        Write campaign results to Google Sheet.
        
        Args:
            campaign_id: Campaign identifier
            metrics: Campaign metrics dictionary
            worksheet_name: Name of the worksheet
        
        Returns:
            True if successful
        """
        if not self.client or not self.sheet:
            return self._mock_write_campaign(campaign_id, metrics, worksheet_name)
        
        try:
            # Get or create worksheet
            try:
                worksheet = self.sheet.worksheet(worksheet_name)
            except gspread.WorksheetNotFound:
                worksheet = self.sheet.add_worksheet(
                    title=worksheet_name,
                    rows=100,
                    cols=10
                )
            
            # Prepare headers
            headers = [
                "Timestamp",
                "Campaign ID",
                "Total Sent",
                "Open Rate",
                "Click Rate",
                "Reply Rate",
                "Meeting Rate"
            ]
            
            # Write headers if needed
            if worksheet.row_count == 0 or worksheet.cell(1, 1).value == "":
                worksheet.append_row(headers)
            
            # Write campaign data
            row = [
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                campaign_id,
                metrics.get("total_sent", 0),
                f"{metrics.get('open_rate', 0) * 100:.1f}%",
                f"{metrics.get('click_rate', 0) * 100:.1f}%",
                f"{metrics.get('reply_rate', 0) * 100:.1f}%",
                f"{metrics.get('meeting_rate', 0) * 100:.1f}%"
            ]
            worksheet.append_row(row)
            
            logger.info(f"Wrote campaign {campaign_id} results to Google Sheets")
            return True
            
        except Exception as e:
            logger.error(f"Error writing to Google Sheets: {e}")
            return False
    
    def read_approved_recommendations(
        self,
        worksheet_name: str = "Recommendations"
    ) -> List[Dict[str, Any]]:
        """
        Read approved recommendations from Google Sheet.
        
        Args:
            worksheet_name: Name of the worksheet
        
        Returns:
            List of approved recommendation dictionaries
        """
        if not self.client or not self.sheet:
            return []
        
        try:
            worksheet = self.sheet.worksheet(worksheet_name)
            records = worksheet.get_all_records()
            
            approved = [
                rec for rec in records
                if rec.get("Status", "").lower() == "approved"
            ]
            
            logger.info(f"Found {len(approved)} approved recommendations")
            return approved
            
        except Exception as e:
            logger.error(f"Error reading from Google Sheets: {e}")
            return []
    
    def _mock_write_recommendations(
        self,
        recommendations: List[Dict[str, Any]],
        worksheet_name: str
    ) -> bool:
        """Mock writing recommendations."""
        logger.warning(f"[MOCK] Would write {len(recommendations)} recommendations to '{worksheet_name}'")
        
        for i, rec in enumerate(recommendations[:3], 1):  # Show first 3
            logger.info(
                f"  {i}. {rec.get('category')}: "
                f"{rec.get('suggested_value')} "
                f"(confidence: {rec.get('confidence', 0):.0%})"
            )
        
        return True
    
    def _mock_write_campaign(
        self,
        campaign_id: str,
        metrics: Dict[str, Any],
        worksheet_name: str
    ) -> bool:
        """Mock writing campaign data."""
        logger.warning(f"[MOCK] Would write campaign {campaign_id} to '{worksheet_name}'")
        logger.info(
            f"  Metrics: Open {metrics.get('open_rate', 0):.1%}, "
            f"Reply {metrics.get('reply_rate', 0):.1%}"
        )
        return True


if __name__ == "__main__":
    # Test Google Sheets client (mock mode)
    print("Testing Google Sheets Client (Mock Mode)\n")
    
    client = GoogleSheetsClient()
    
    # Test writing recommendations
    print("=== Writing Recommendations ===")
    test_recommendations = [
        {
            "category": "ICP_REFINEMENT",
            "current_value": "industry: SaaS",
            "suggested_value": "industry: SaaS, must_have_signal: recent_funding",
            "rationale": "Funded companies have 3x better conversion",
            "expected_impact": "Increase reply rate from 12% to 18%",
            "confidence": 0.85
        },
        {
            "category": "MESSAGING",
            "current_value": "Generic subject lines",
            "suggested_value": "Mention specific funding round",
            "rationale": "Personalized intros get 40% more opens",
            "expected_impact": "Increase open rate from 53% to 65%",
            "confidence": 0.78
        }
    ]
    
    success = client.write_recommendations(test_recommendations)
    print(f"Write successful: {success}\n")
    
    # Test writing campaign results
    print("=== Writing Campaign Results ===")
    test_metrics = {
        "total_sent": 50,
        "open_rate": 0.45,
        "click_rate": 0.12,
        "reply_rate": 0.08,
        "meeting_rate": 0.03
    }
    
    success = client.write_campaign_results("campaign_001", test_metrics)
    print(f"Write successful: {success}")
    
    print("\n✅ Google Sheets client test complete!")
