import time
import random
import logging

from download_boss.wrapper.AbstractWrapper import AbstractWrapper


class DelayWrapper(AbstractWrapper):

    def __init__(self, client, length=0, maxLength=None):
        super().__init__(client)
        self.length = length
        self.maxLength = maxLength

    def download(self, requestEnvelope):
        delay = self._generateDelayLength()
        logging.info(f'Delaying by {delay}s ... {requestEnvelope}')
        time.sleep(delay)
        
        return self.client.download(requestEnvelope)

    def _generateDelayLength(self):
        if self.maxLength is None:
            return self.length
        else:
            return random.randrange(self.length, self.maxLength+1)
