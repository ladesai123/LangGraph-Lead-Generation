"""
Data validation utilities for the LangGraph Lead Generation System.

Validates workflow configurations and data structures.
"""

import re
from typing import Dict, Any, List, Optional, Tuple
from jsonschema import validate, ValidationError, Draft7Validator
from .logger import get_logger

logger = get_logger(__name__)


# JSON Schema for workflow.json
WORKFLOW_SCHEMA = {
    "type": "object",
    "required": ["workflow_name", "steps"],
    "properties": {
        "workflow_name": {"type": "string"},
        "description": {"type": "string"},
        "version": {"type": "string"},
        "steps": {
            "type": "array",
            "items": {
                "type": "object",
                "required": ["id", "agent", "instructions"],
                "properties": {
                    "id": {"type": "string"},
                    "agent": {"type": "string"},
                    "description": {"type": "string"},
                    "instructions": {"type": "string"},
                    "inputs": {"type": "object"},
                    "tools": {"type": "array"},
                    "output_schema": {"type": "object"}
                }
            }
        }
    }
}


def validate_workflow(workflow_config: Dict[str, Any]) -> Tuple[bool, Optional[str]]:
    """
    Validate workflow.json structure.
    
    Args:
        workflow_config: Workflow configuration dictionary
    
    Returns:
        Tuple of (is_valid: bool, error_message: str or None)
    """
    try:
        validate(instance=workflow_config, schema=WORKFLOW_SCHEMA)
        logger.info("Workflow configuration is valid")
        return True, None
    except ValidationError as e:
        error_msg = f"Workflow validation error: {e.message}"
        logger.error(error_msg)
        return False, error_msg


def validate_email(email: str) -> bool:
    """
    Validate email address format.
    
    Args:
        email: Email address to validate
    
    Returns:
        True if valid email format
    """
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))


def validate_lead_data(lead: Dict[str, Any]) -> Tuple[bool, List[str]]:
    """
    Validate lead data structure.
    
    Args:
        lead: Lead data dictionary
    
    Returns:
        Tuple of (is_valid: bool, issues: List[str])
    """
    issues = []
    
    # Required fields
    required_fields = ['company', 'contact_name', 'email']
    for field in required_fields:
        if not lead.get(field):
            issues.append(f"Missing required field: {field}")
    
    # Email validation
    if lead.get('email'):
        if not validate_email(lead['email']):
            issues.append(f"Invalid email format: {lead['email']}")
    
    # Optional but recommended fields
    recommended_fields = ['title', 'linkedin']
    for field in recommended_fields:
        if not lead.get(field):
            logger.debug(f"Lead missing recommended field: {field}")
    
    is_valid = len(issues) == 0
    return is_valid, issues


def validate_enriched_lead(lead: Dict[str, Any]) -> Tuple[bool, List[str]]:
    """
    Validate enriched lead data structure.
    
    Args:
        lead: Enriched lead data dictionary
    
    Returns:
        Tuple of (is_valid: bool, issues: List[str])
    """
    issues = []
    
    # Required fields for enriched leads
    required_fields = ['company', 'contact', 'email', 'role']
    for field in required_fields:
        if not lead.get(field):
            issues.append(f"Missing required field: {field}")
    
    # Email validation
    if lead.get('email'):
        if not validate_email(lead['email']):
            issues.append(f"Invalid email format: {lead['email']}")
    
    # Technologies should be a list
    if 'technologies' in lead and not isinstance(lead['technologies'], list):
        issues.append("'technologies' field must be a list")
    
    is_valid = len(issues) == 0
    return is_valid, issues


def validate_scored_lead(lead: Dict[str, Any]) -> Tuple[bool, List[str]]:
    """
    Validate scored lead data structure.
    
    Args:
        lead: Scored lead data dictionary
    
    Returns:
        Tuple of (is_valid: bool, issues: List[str])
    """
    issues = []
    
    # Required fields
    if 'lead' not in lead:
        issues.append("Missing 'lead' object")
    
    if 'score' not in lead:
        issues.append("Missing 'score' field")
    elif not isinstance(lead['score'], (int, float)):
        issues.append("'score' must be a number")
    elif not (0 <= lead['score'] <= 100):
        issues.append("'score' must be between 0 and 100")
    
    # Score breakdown
    if 'score_breakdown' in lead:
        breakdown = lead['score_breakdown']
        if not isinstance(breakdown, dict):
            issues.append("'score_breakdown' must be a dictionary")
    
    is_valid = len(issues) == 0
    return is_valid, issues


def validate_email_message(message: Dict[str, Any]) -> Tuple[bool, List[str]]:
    """
    Validate email message structure.
    
    Args:
        message: Email message dictionary
    
    Returns:
        Tuple of (is_valid: bool, issues: List[str])
    """
    issues = []
    
    # Required fields
    required_fields = ['lead_email', 'subject', 'email_body']
    for field in required_fields:
        if not message.get(field):
            issues.append(f"Missing required field: {field}")
    
    # Email validation
    if message.get('lead_email'):
        if not validate_email(message['lead_email']):
            issues.append(f"Invalid email format: {message['lead_email']}")
    
    # Content validation
    if message.get('subject') and len(message['subject']) > 200:
        issues.append("Subject line too long (max 200 characters)")
    
    if message.get('email_body') and len(message['email_body']) < 50:
        issues.append("Email body too short (min 50 characters)")
    
    is_valid = len(issues) == 0
    return is_valid, issues


def validate_api_response(response: Any, expected_keys: List[str]) -> Tuple[bool, List[str]]:
    """
    Validate API response contains expected keys.
    
    Args:
        response: API response (should be dict)
        expected_keys: List of expected keys in response
    
    Returns:
        Tuple of (is_valid: bool, issues: List[str])
    """
    issues = []
    
    if not isinstance(response, dict):
        issues.append(f"Response is not a dictionary: {type(response)}")
        return False, issues
    
    for key in expected_keys:
        if key not in response:
            issues.append(f"Missing expected key in response: {key}")
    
    is_valid = len(issues) == 0
    return is_valid, issues


def sanitize_text(text: str, max_length: Optional[int] = None) -> str:
    """
    Sanitize text input by removing excessive whitespace and limiting length.
    
    Args:
        text: Text to sanitize
        max_length: Maximum length (optional)
    
    Returns:
        Sanitized text
    """
    if not text:
        return ""
    
    # Remove excessive whitespace
    sanitized = ' '.join(text.split())
    
    # Limit length if specified
    if max_length and len(sanitized) > max_length:
        sanitized = sanitized[:max_length] + "..."
    
    return sanitized


def validate_score_weights(weights: Dict[str, float]) -> Tuple[bool, List[str]]:
    """
    Validate scoring weights sum to 1.0.
    
    Args:
        weights: Dictionary of scoring weights
    
    Returns:
        Tuple of (is_valid: bool, issues: List[str])
    """
    issues = []
    
    # Check all values are numbers between 0 and 1
    for key, value in weights.items():
        if not isinstance(value, (int, float)):
            issues.append(f"Weight '{key}' is not a number: {value}")
        elif not (0 <= value <= 1):
            issues.append(f"Weight '{key}' must be between 0 and 1: {value}")
    
    # Check sum equals 1.0 (with small tolerance for floating point)
    total = sum(weights.values())
    if abs(total - 1.0) > 0.01:
        issues.append(f"Weights must sum to 1.0, got {total:.2f}")
    
    is_valid = len(issues) == 0
    return is_valid, issues


if __name__ == "__main__":
    # Test validators
    print("=== Testing Validators ===\n")
    
    # Test email validation
    print("1. Email Validation:")
    test_emails = [
        "valid@example.com",
        "invalid@",
        "also.valid+test@company.co.uk",
        "not-an-email"
    ]
    for email in test_emails:
        is_valid = validate_email(email)
        print(f"   {email}: {'✅' if is_valid else '❌'}")
    
    # Test lead validation
    print("\n2. Lead Data Validation:")
    test_lead = {
        "company": "Acme Corp",
        "contact_name": "John Doe",
        "email": "john@acme.com",
        "title": "VP Sales"
    }
    is_valid, issues = validate_lead_data(test_lead)
    print(f"   Valid lead: {'✅' if is_valid else '❌'}")
    if issues:
        for issue in issues:
            print(f"   - {issue}")
    
    # Test score weights
    print("\n3. Score Weights Validation:")
    test_weights = {
        "revenue_fit": 0.3,
        "employee_fit": 0.2,
        "tech_stack": 0.2,
        "growth_signals": 0.3
    }
    is_valid, issues = validate_score_weights(test_weights)
    print(f"   Valid weights: {'✅' if is_valid else '❌'}")
    if issues:
        for issue in issues:
            print(f"   - {issue}")
    
    print("\n✅ Validator tests complete!")
