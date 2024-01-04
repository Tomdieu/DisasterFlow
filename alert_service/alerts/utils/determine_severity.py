

def determine_severity(impact:str, urgency:str):
    
    severity = "low"

    if impact == "moderate" and urgency == "moderate":
        severity = "moderate"
    elif impact == "high" and urgency == "high":
        severity = "high"
    elif impact == "high" and urgency == "moderate":
        severity = "moderate"
    elif impact == "moderate" and urgency == "high":
        severity = "high"
    elif impact == "high" and urgency == "low":
        severity = "moderate"
    elif impact == "low" and urgency == "high":
        severity = "moderate"
    elif impact == "moderate" and urgency == "low":
        severity = "low"
    elif impact == "low" and urgency == "moderate":
        severity = "low"

    return severity