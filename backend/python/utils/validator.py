
import re

def detect_html_and_sql_injection(input_string):
    """
    Detect HTML tags and potential SQL injection attempts in an input string.
    
    Args:
        input_string (str): The input string to be checked
    
    Returns:
        dict: A dictionary containing detection results
    """
    # Initialize results dictionary
    detection_results = {
        'has_html_tags': False,
        'has_sql_injection': False,
        'detected_html_tags': [],
        'detected_sql_injection_patterns': []
    }
    
    # HTML Tag Detection
    # This regex matches HTML tags like <tag>, </tag>, <tag attr="value">
    html_tag_pattern = r'<\/?[\w\s="/.:\-]+>'
    html_matches = re.findall(html_tag_pattern, input_string, re.IGNORECASE)
    
    if html_matches:
        detection_results['has_html_tags'] = True
        detection_results['detected_html_tags'] = html_matches
    
    # SQL Injection Detection Patterns
    sql_injection_patterns = [
        # Classic SQL injection patterns
        r'\b(SELECT|INSERT|UPDATE|DELETE|DROP|UNION|ALTER)\b',
        
        # Potential SQL injection keywords and characters
        r'(\s*=\s*|\s*--|\s*\/\*|\*\/|\bOR\b|\bAND\b)',
        
        # Numeric SQL injection attempts
        r'\d+\s*=\s*\d+',
        
        # String-based SQL injection
        r"'(\s*OR\s*'1'='1|;--)",
        
        # Potential database system-specific injections
        r'\b(EXEC|EXECUTE|CONCAT|CHAR|ASCII)\b'
    ]
    
    # Check for SQL injection patterns
    sql_matches = []
    for pattern in sql_injection_patterns:
        matches = re.findall(pattern, input_string, re.IGNORECASE)
        if matches:
            sql_matches.extend(matches)
    
    if sql_matches:
        detection_results['has_sql_injection'] = True
        detection_results['detected_sql_injection_patterns'] = sql_matches
    
    return detection_results

# Example usage and testing
def test_detection():
    # Test cases
    test_inputs = [
        "<script>alert('XSS');</script>",  # HTML tag
        "SELECT * FROM users WHERE username = 'admin'",  # SQL injection
        "1=1 OR 1=1",  # SQL injection
        "Hello, World!",  # Normal input
        "user' OR '1'='1",  # SQL injection
        "<div>Some content</div>",  # HTML tag
        "UNION SELECT password FROM users"  # SQL injection
    ]
    
    for input_str in test_inputs:
        result = detect_html_and_sql_injection(input_str)
        print(result)
        # print(f"\nInput: {input_str}")
        # print(f"HTML Tags Detected: {result['has_html_tags']}")
        # print(f"SQL Injection Detected: {result['has_sql_injection']}")
        
        # if result['has_html_tags']:
        #     print(f"Detected HTML Tags: {result['detected_html_tags']}")
        
        # if result['has_sql_injection']:
        #     print(f"Detected SQL Injection Patterns: {result['detected_sql_injection_patterns']}")
