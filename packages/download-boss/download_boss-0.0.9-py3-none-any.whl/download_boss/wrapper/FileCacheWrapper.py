import os
import re
import time
import hashlib
import requests
import logging
import traceback
import json

from download_boss.wrapper.AbstractWrapper import AbstractWrapper
from download_boss.error.CachedFileNotFound import CachedFileNotFound
from download_boss.error.CachedFileExpired import CachedFileExpired
from download_boss.client.request.Boto3LogsRequestEnvelope import Boto3LogsRequestEnvelope


class FileCacheWrapper(AbstractWrapper):

    def __init__(self, client, cacheFolderPath, cacheLength=None):
        super().__init__(client)
        self.cacheFolderPath = cacheFolderPath
        self.cacheLength = cacheLength

    def download(self, requestEnvelope):
        try:
            return self._getCache(requestEnvelope)
        except Exception as e:
            if not isinstance(e, CachedFileNotFound) and not isinstance(e, CachedFileExpired):
                traceback.print_exc()
                raise e
            
            response = self.client.download(requestEnvelope)
            self._setCache(requestEnvelope, response)
            return response

    def _setCache(self, requestEnvelope, response):
        cacheKey = requestEnvelope.getCacheKey()
        cacheKeyPath = os.path.join(self.cacheFolderPath, cacheKey)

        if isinstance(requestEnvelope, Boto3LogsRequestEnvelope):
            cacheValue = json.dumps(response)
        else:
            cacheValue = response.text

        with open(cacheKeyPath, 'w') as f:
            f.write(cacheValue)

    def _getCache(self, requestEnvelope):
        cacheKey = requestEnvelope.getCacheKey()
        cacheKeyPath = os.path.join(self.cacheFolderPath, cacheKey)
        
        if not os.path.isfile(cacheKeyPath):
            logging.info(f'Cache miss: {requestEnvelope}')
            raise CachedFileNotFound(cacheKeyPath)
        
        currentTime = time.time()
        fileTime = os.path.getmtime(cacheKeyPath)

        if self.cacheLength is not None and fileTime + self.cacheLength < currentTime:
            logging.info(f'Cache expired: {requestEnvelope}')
            raise CachedFileExpired(cacheKeyPath)
        
        with open(cacheKeyPath) as f:
            logging.info(f'Cache found: {requestEnvelope}')

            if isinstance(requestEnvelope, Boto3LogsRequestEnvelope):
                response = json.load(f)
            else:
                response = requests.Response()
                response._content = f.read().encode('utf-8')
            
            return response

    def removeCache(self, requestEnvelope):
        cacheKey = requestEnvelope.getCacheKey()
        cacheKeyPath = os.path.join(self.cacheFolderPath, cacheKey)
        
        if os.path.isfile(cacheKeyPath):
            os.remove(cacheKeyPath)
