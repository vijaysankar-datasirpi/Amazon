import pika, json
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import User
from .Serialize import serialize

@swagger_auto_schema(
    method='post',
    operation_summary='Insert to DB and call RabbitMQ',
    request_body=serialize,
    responses={
        200: openapi.Response(
            description='Success',
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'message': openapi.Schema(type=openapi.TYPE_STRING)
                }
            )
        )
    }
)
@api_view(['POST'])
def Post(request):
    data = request.data
    serial = serialize(data=data)

    if serial.is_valid():
        serial.save()

        connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        channel = connection.channel()

        channel.queue_declare(queue='email_queue', durable=True)

        channel.basic_publish(
            exchange='',
            routing_key='Q',
            body=json.dumps(data),
            properties=pika.BasicProperties(
                delivery_mode=2,
            )
        )

        connection.close()

        return Response({'message': 'User added and message sent to queue'}, status=201)

    return Response(serial.errors, status=400)


def forms(request):
    return render(request,'f.html')