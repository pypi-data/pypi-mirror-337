from typing import Callable, Dict
import json
from datetime import datetime
from aws_sqs_consumer import Consumer
from defix_package_logger import logger
from . import sqs_api
from .. import constants


class SimpleConsumer(Consumer):
    def __init__(self, queue_url: str, handler: Callable[[Dict, Dict, Dict], None]):
        super().__init__(queue_url, sqs_client=sqs_api.sqs.meta.client,
                         attribute_names=[
                             'ApproximateReceiveCount', 'SentTimestamp'],
                         wait_time_seconds=constants.DEFAULT_RECEIVE_MESSAGE_WAIT_TIME)

        self.handler = handler

    def handle_message(self, message):
        parsedMessage = json.loads(message.Body)
        meta = parsedMessage['meta']

        attributes = {
            'approximate_receive_count': int(message.Attributes['ApproximateReceiveCount']),
            'sent_at': datetime.fromtimestamp(float(message.Attributes['SentTimestamp'])/1000)
        }

        try:
            self.handler(parsedMessage, meta, attributes)
        except:
            logger.error('Failed to handle message', extra={
                'queue_url': self.queue_url,
                'msg_code': constants.MESSAGE_HANDLING_FAILED_MSG_CODE
            } | meta)
            raise
