import pika
from pika.exchange_type import ExchangeType

connection_parameters = pika.ConnectionParameters('localhost')
connection = pika.BlockingConnection(connection_parameters)
channel = connection.channel()

channel.exchange_declare(exchange='routing', exchange_type=ExchangeType.direct)

message = 'This message needs to be routed'
message_for_payment = 'Message for payments consumer'
message_mazafaka = 'Hello, mazafaka!!!'


channel.basic_publish(exchange='routing', routing_key='both', body=message)
channel.basic_publish(exchange='routing', routing_key='paymentsonly', body=message_for_payment)

print(f'sent message: {message}')
print(f'sent message: {message_for_payment}')

####
channel.queue_declare(queue='byturn')
channel.basic_publish(exchange='', routing_key='byturn', body=message_mazafaka)
print(f'sent message: {message_mazafaka}')
####

connection.close()

