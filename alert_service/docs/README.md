# Alerting Microservice

Responsible for managing the generation and distribution of alerts for various types of disasters, including fires.

## Entities

1. Alert:

    - Represents an alert message that contains information about a specific incident.
    - Attributes
        - `alert_id` (Primary Key)
        - `type` : The type of the alert
        - `title` : A brief title or headline for the alert.
        - `description` : Detailed information about the alert, including the nature of the incident.
        - `severity` : Indicates the severity level of the alert (e.g., Low, Moderate, High, Critical).
        - `location` : Specifies the geographical area affected by the alert (latitude, longitude, or descriptive location).
        - `timestamp` : The timestamp indicating when the alert was generated.
        - `created_by` : The entity or user responsible for creating the alert (e.g., Citizen, Emergency Responder, Administrator).
2. User Report:

    - Represents a user-initiated report of an incident, including fire incidents.
    - Attributes
        - `report_id` (Primary Key)
        - `user_id` The identifier of the user who reported the incident.
        