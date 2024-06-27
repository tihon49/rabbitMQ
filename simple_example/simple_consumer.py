import pika

def callback(ch, method, properties, body):
    print(f"Получено сообщение: {body}")
    ch.basic_ack(delivery_tag=method.delivery_tag)

# Установка соединения с RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# Создание очереди
channel.queue_declare(queue='test_queue')

# Подписка на очередь с подтверждением сообщений
channel.basic_consume(
    queue='test_queue', 
    on_message_callback=callback, 
    auto_ack=False
)

print('Ожидание сообщений. Нажмите Ctrl+C для выхода')
channel.start_consuming()

