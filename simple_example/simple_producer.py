import pika

# Установка соединения с RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# Создание очереди с ограничением времени жизни сообщений
channel.queue_declare(queue='test_queue')

# Отправка сообщения
channel.basic_publish(
    exchange='', 
    routing_key='test_queue',
    body='Hello World!'
)

# Закрытие соединения
connection.close()

