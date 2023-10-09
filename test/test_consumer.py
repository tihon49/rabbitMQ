import pika
from pika.exchange_type import ExchangeType


def on_message_received(ch, method, properties, body):
    print(f'Analytics - received new message: {body}')


def consume_message(exchange_name='', routing_key=[], queue_name=None):
    connection_parameters = pika.ConnectionParameters('localhost')
    connection = pika.BlockingConnection(connection_parameters)
    channel = connection.channel()

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


if __name__ == '__main__':
    consume_message(
        exchange_name='test',
        routing_key=['test']
    )
