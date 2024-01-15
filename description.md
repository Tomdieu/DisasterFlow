# Disaster Flow Description

This is what happens when a disaster is reported

1. A Citizen that register to the app can report an alert in the system by filling the different fields which are `type`(which represent the type of the disaster),`location`,`impact`, `urgency` and `image`(optional).

2. From the `urgency` and `impact` of the reported disaster we are going to determine the `severity` of the alert.After the severity obtain we know create the alert with some informations from the reported disaster which are `location`,`image`(optional) and `type`.

3. After the alert created in the `Alert Service` we now send and event to `RabbitMQ` through the topic `alerts` with routing key `alerts.*` which is been consume by the consumer of the `Emergency Response Service` Which now create an Alert with the information of the alert recieve from the event.

4. After the alert created in the `Emergency Response Service` from the `type` and `location` of the `alert` we now get all the different emergency response team that can handle that kind of disaster located in a radius of `10Km` from the alert location. An also a notification is send to all the different users that are located in the radius of `500m` from the reported alert for them to see if they can also do something. eg If the alert type is `Fire` all the people located in a radius of `500m` will recieve the notification and can go to help put off the fire before a Firefighting can arrive.

5. When an emergency response team recieve the alert if there are free they can respond to the user who reported and the alert and can take an action to handle the disaster.
