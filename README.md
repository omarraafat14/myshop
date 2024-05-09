
[!Note: don't forget to pull RabbitMQ]

`docker pull rabbitmq`


`docker run -it --rm --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:management`
- With this command, we are telling RabbitMQ to run on port 5672, and we are running its web-based \
management user interface on port 15672.


- Running a Celery worker:
`celery -A myshop worker -l info`

- Monitoring Celery with Flower:
`celery -A myshop flower`