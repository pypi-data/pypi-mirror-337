from typing import Callable, Dict
from defix_package_logger import get_logger
from ..helpers import sqs_api
from ..helpers.consumer import SimpleConsumer


class BasicQueue():
    def __init__(self, name: str):
        if len(name) == 0:
            raise ValueError('Queue name is empty')

        queue = sqs_api.get_queue(name)
        self.queue = queue

    def start(self, handler: Callable[[Dict, Dict, Dict], None]):
        self.consumer = SimpleConsumer(
            queue_url=self.queue.url, handler=handler)

        get_logger().info(
            'Started listening for the events of %s queue',
            self.queue.url
        )

        self.consumer.start()

    def stop(self):
        if self.consumer == None or not self.consumer._running:
            raise Exception('Queue is not started')

        self.consumer.stop()

    def send_message(self, message_body: Dict, meta: Dict):
        try:
            sqs_api.send_message(self.queue, message_body, meta)
            get_logger().info('Message sent to the queue', extra={
                'queue_url': self.queue.url
            } | meta)
        except:
            get_logger().error('Failed to send a message', extra={
                'queue_url': self.queue.url
            } | meta)
            raise
