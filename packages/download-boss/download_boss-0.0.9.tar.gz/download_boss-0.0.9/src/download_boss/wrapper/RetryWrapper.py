import time
import logging

from download_boss.wrapper.AbstractWrapper import AbstractWrapper
from download_boss.error.RetriesExhausted import RetriesExhausted
from download_boss.error.ClientRetriable import ClientRetriable


class RetryWrapper(AbstractWrapper):

    def __init__(self, client, count=3):
        super().__init__(client)
        self.count = count

    def download(self, requestEnvelope):
        retriesLeft = self.count

        while True:
            try:
                return self.client.download(requestEnvelope)
            except ClientRetriable as e:
                if retriesLeft == 0:
                    raise RetriesExhausted(e.message)
                
                logging.info(f'Retrying... {requestEnvelope}')
                retriesLeft -= 1
                time.sleep(1)
