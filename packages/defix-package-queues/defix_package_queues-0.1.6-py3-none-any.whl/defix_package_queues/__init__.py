from typing import Dict, Callable
from defix_package_logger import get_logger
from .utils import get_queue_name
from .helpers import sqs_api
from .queues.basic import BasicQueue

queue: BasicQueue = None


def initialize(opts: Dict):
    global queue

    if queue is not None:
        return

    if opts.get('name') is None:
        raise Exception('Service name is empty')

    queue_name = get_queue_name(opts['name'])

    sqs_api.create_queue(queue_name)

    queue = BasicQueue(queue_name)

    get_logger().info('Queue %s initialized', queue_name)


def start_listening(handler: Callable[[Dict, Dict, Dict], None]):
    if queue is None:
        raise Exception('Queue is not initialized')

    queue.start(handler)


def send_message(message_body: Dict, meta: Dict):
    if queue is None:
        raise Exception('Queue is not initialized')

    queue.send_message(message_body, meta)


def destroy():
    if queue is None:
        raise Exception('Queue is not initialized')

    queue.stop()


__all__ = ['initialize', 'start_listening', 'send_message', 'destroy']
