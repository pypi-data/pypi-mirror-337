from typing import Dict
import threading
import os
import sys
import defix_package_queues
from defix_package_logger import logger


def handler(message_body: Dict, meta: Dict, attributes: Dict):
    logger.info('Message handled')


def start_listening():
    defix_package_queues.start_listening(handler)


def main():
    defix_package_queues.initialize({
        'name': 'test-service'
    })

    defix_package_queues.send_message({
        'status': 'ok'
    }, {'xid': '-'})


if __name__ == '__main__':
    try:
        main()
        t1 = threading.Thread(target=start_listening)
        t1.start()
        t1.join()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            defix_package_queues.destroy()
            sys.exit(130)
        except SystemExit:
            os._exit(130)
