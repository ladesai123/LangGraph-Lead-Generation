"""
Test script for utilities.

Run this to verify all utilities work correctly.
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.logger import get_logger
from utils.config_loader import ConfigLoader
from utils.validators import (
    validate_email, 
    validate_lead_data, 
    validate_score_weights
)

def test_logger():
    """Test logging functionality."""
    print("=" * 50)
    print("Testing Logger")
    print("=" * 50)
    
    logger = get_logger("test_utilities")
    logger.info("✅ Logger is working!")
    logger.warning("⚠️ This is a warning")
    logger.error("❌ This is an error (for testing)")
    
    print("Check logs/ directory for output file")
    print()

def test_config_loader():
    """Test configuration loading."""
    print("=" * 50)
    print("Testing Config Loader")
    print("=" * 50)
    
    try:
        config = ConfigLoader()
        
        print(f"✅ Workflow Name: {config.get_workflow().get('workflow_name')}")
        print(f"✅ Number of Steps: {len(config.get_workflow().get('steps', []))}")
        print(f"✅ Dry Run Mode: {config.is_dry_run()}")
        
        # Test getting a specific step
        step = config.get_step('prospect_search')
        if step:
            print(f"✅ Found step: {step['agent']}")
        
        print()
    except Exception as e:
        print(f"❌ Error: {e}")
        print()

def test_validators():
    """Test validation functions."""
    print("=" * 50)
    print("Testing Validators")
    print("=" * 50)
    
    # Test email validation
    emails = [
        ("john@example.com", True),
        ("invalid@", False),
        ("test+tag@company.co.uk", True)
    ]
    
    print("\nEmail Validation:")
    for email, expected in emails:
        result = validate_email(email)
        status = "✅" if result == expected else "❌"
        print(f"  {status} {email}: {result}")
    
    # Test lead validation
    print("\nLead Validation:")
    test_lead = {
        "company": "Acme Corp",
        "contact_name": "John Doe",
        "email": "john@acme.com",
        "title": "VP Sales"
    }
    is_valid, issues = validate_lead_data(test_lead)
    if is_valid:
        print(f"  ✅ Valid lead structure")
    else:
        print(f"  ❌ Issues: {issues}")
    
    # Test score weights
    print("\nScore Weights Validation:")
    weights = {
        "revenue_fit": 0.3,
        "employee_fit": 0.2,
        "tech_stack": 0.2,
        "growth_signals": 0.3
    }
    is_valid, issues = validate_score_weights(weights)
    if is_valid:
        print(f"  ✅ Valid weights (sum = {sum(weights.values())})")
    else:
        print(f"  ❌ Issues: {issues}")
    
    print()

if __name__ == "__main__":
    print("\n🚀 Testing All Utilities\n")
    
    test_logger()
    test_config_loader()
    test_validators()
    
    print("=" * 50)
    print("✅ All Utility Tests Complete!")
    print("=" * 50)
