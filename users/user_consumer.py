import pika

from pika.exchange_type import ExchangeType
from pika.exceptions import AMQPError




def on_message_received(ch, method, properties, body):
    print(f'Payments - received new message: {body}')


def create_channel():
    """Моздает и возвращает канал"""
    try:
        connection_parameters = pika.ConnectionParameters('localhost')
        connection = pika.BlockingConnection(connection_parameters)
        return connection.channel()
    except AMQPError as vonnection_error:
        print(f"Error while connectiong to RabbitMQ: {connection_error}")


def consume_message(exchange_name='', routing_key=[], queue_name=None):
    """Запускаем консюмера"""

    channel = create_channel()
    if not channel:
        return

    try:
        if queue_name:
            channel.queue_declare(queue=queue_name)
            channel.basic_consume(
                queue=queue_name, 
                auto_ack=True,
                on_message_callback=on_message_received
            )

        channel.exchange_declare(
            exchange=exchange_name, 
            exchange_type=ExchangeType.direct
        )
        queue = channel.queue_declare(queue='', exclusive=True)

        for key in routing_key:
            channel.queue_bind(
                exchange=exchange_name, 
                queue=queue.method.queue, 
                routing_key=key
            )

        channel.basic_consume(queue=queue.method.queue, auto_ack=True,
            on_message_callback=on_message_received)

        print('Payments Starting Consuming')
        channel.start_consuming()
    except AMQPError as consume_error:
        print(f'Error while consuming messages: {consume_error}')
    finally:
        if channel.is_open:
            channel.close()


if __name__ == '__main__':
    consume_message(
        exchange_name='routing',
        queue_name='byturn',
        routing_key=['both', 'useronly']
    )

