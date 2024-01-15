# Disaster Flow Description

The Disaster Flow app is designed to efficiently handle reported disasters through a systematic process. Here's a breakdown of the workflow:

## 1. Alert Reporting by Citizens:

   - Registered citizens can report alerts through the app.
   - Fields to be filled include:
      - `Type`: Represents the type of disaster.
      - `Location`: Specifies the location of the disaster.
      - `Impact`: Describes the impact of the disaster.
      - `Urgency`: Indicates the urgency of the situation.
      - `Image` (optional): Users can attach images related to the disaster.

## 2. Alert Severity Determination:
   - The app calculates the severity of the alert based on the reported `Urgency` and `Impact`.
   - The severity information is used to create an alert with essential details: `Location`, `Image` (optional), and `Type`.

## 3. Alert Transmission via RabbitMQ:
   - An event is sent to `RabbitMQ` using the `alerts` topic and a routing key of `alerts.*`.
   - The event is consumed by the `Emergency Response Service` consumer.

## 4. Emergency Response Handling:
   - The `Emergency Response Service` processes the received alert event and creates an alert with the provided information.
   - Based on the `Type` and `Location` of the alert, the service identifies all available emergency response teams within a `10Km` radius.
   - Notifications are sent to users within a `500m` radius of the reported alert, urging them to take immediate action if they can assist. For example, if the alert type is `Fire`, nearby individuals are notified to help before professional firefighting teams arrive.

## 5. Response by Emergency Teams:
   - Upon receiving the alert, an emergency response team assesses the situation.
   - If available, the team responds to the user who reported the alert and takes necessary actions to handle the disaster.
