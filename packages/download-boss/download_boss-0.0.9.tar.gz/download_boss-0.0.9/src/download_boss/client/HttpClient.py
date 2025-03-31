import requests
import logging

from download_boss.client.AbstractClient import AbstractClient
from download_boss.error.ClientRetriable import ClientRetriable


class HttpClient(AbstractClient):

    def __init__(self, retriableStatusCodes=None):
        self.retriableStatusCodes = retriableStatusCodes or []
        self.session = requests.Session()

    def download(self, requestEnvelope):
        logging.info(f'Requesting: {requestEnvelope}')

        response = self.session.send(requestEnvelope.request.prepare(), **requestEnvelope.kwargs)

        for statusCodes in self.retriableStatusCodes:
            if ((isinstance(statusCodes, int) and statusCodes == response.status_code) or 
                (isinstance(statusCodes, range) and response.status_code in statusCodes)):
                    raise ClientRetriable(response)

        return response
