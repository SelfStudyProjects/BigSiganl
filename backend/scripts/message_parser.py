def parse_message(message):
    """
    Parses a message string and returns a dictionary with relevant information.
    
    Args:
        message (str): The message to be parsed.
        
    Returns:
        dict: A dictionary containing parsed information.
    """
    parsed_data = {}
    
    # Example parsing logic (to be customized based on actual message format)
    lines = message.split('\n')
    for line in lines:
        if ':' in line:
            key, value = line.split(':', 1)
            parsed_data[key.strip()] = value.strip()
    
    return parsed_data

def extract_important_info(parsed_data):
    """
    Extracts important information from the parsed data.
    
    Args:
        parsed_data (dict): The parsed message data.
        
    Returns:
        dict: A dictionary containing important information.
    """
    important_info = {}
    
    # Example extraction logic (to be customized based on actual requirements)
    if 'Important Key' in parsed_data:
        important_info['Important Key'] = parsed_data['Important Key']
    
    return important_info

# This file is intentionally left blank.