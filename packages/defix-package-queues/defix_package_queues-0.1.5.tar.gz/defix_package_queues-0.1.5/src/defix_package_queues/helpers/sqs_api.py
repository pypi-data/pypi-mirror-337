from typing import Dict
import json
import boto3

sqs = boto3.resource("sqs")


def create_queue(name: str, attributes: Dict = None):
    if not attributes:
        attributes = {}

    queue = sqs.create_queue(QueueName=name, Attributes=attributes)
    return queue


def send_message(queue, message_body: Dict, meta: Dict):
    message_body['meta'] = meta

    response = queue.send_message(
        MessageBody=json.dumps(message_body)
    )
    return response


def get_queue(name: str):
    queue = sqs.get_queue_by_name(QueueName=name)
    return queue
