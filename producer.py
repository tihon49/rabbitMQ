import pika

from pika.exceptions import AMQPError
from pika.exchange_type import ExchangeType



def create_channel():
    """ Создает и возвращает канал """
    try:
        connection_parameters = pika.ConnectionParameters('localhost')
        connection = pika.BlockingConnection(connection_parameters)
        return connection.channel()
    except AMQPError as connection_error:
        print(f'Error while connecting to RabbitMQ: {connection_error}')
        return None


def publish_message(
        exchange_name='', 
        queue_name=None, 
        routing_key='', 
        message=''
    ) -> None:
    """ Публикует сообщение """

    channel = create_channel()
    if not channel:
        return
    try:
        if queue_name:
            channel.queue_declare(queue=queue_name)
            channel.basic_publish(
                exchange=exchange_name, 
                routing_key=routing_key, 
                body=message
            )
        else:
            channel.exchange_declare(exchange=exchange_name, exchange_type=ExchangeType.direct)
            channel.basic_publish(exchange=exchange_name, routing_key=routing_key, body=message)

    except AMQPError as publish_error:
        print(f'Error while publishing message: {publish_error}')
    finally:
        if channel.is_open:
            channel.close()


def main():
    publish_message(exchange_name='routing', routing_key='both', message='This message needs to be routed')
    publish_message(exchange_name='routing', routing_key='paymentsonly', message='Message for payments consumer')
    publish_message(queue_name='byturn', routing_key='byturn', message='Hello Mazafaka!!!!')

    publish_message(exchange_name='test', routing_key='test', message='Nu privet, zasranec')



if __name__ == '__main__':
    main()

