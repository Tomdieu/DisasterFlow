

def determine_severity(nature:str, impact:str, urgency:str):
    
    if nature == 'Fire':
        # Custom logic for fire incidents
        if impact == 'High' and urgency == 'Immediate':
            return 'Critical'
        elif impact == 'High':
            return 'High'
        else:
            return 'Moderate'
    else:
        # Default severity determination for other incident types
        # Custom logic can be added for different incident types
        return 'Moderate'