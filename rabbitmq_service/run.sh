docker run -d --name my_rabbitmq_container -p 5672:5672 -p 15672:15672 rabbitmq:latest
docker run --rm -it -p 15672:15672 -p 5672:5672 rabbitmq:3.10-management-alpine