import pika
import json

conn=pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel=conn.channel()

channel.queue_declare(queue='Q',durable='True')

def callback(ch,method,properties,body):
    data=json.loads(body)
    print(data)
    ch.basic_ack(delivery_tag=method.delivery_tag)

channel.basic_consume(queue='Q',on_message_callback=callback)
channel.start_consuming()