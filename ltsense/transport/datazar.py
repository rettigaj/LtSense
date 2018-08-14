#!/usr/bin/env python

import requests
import json
import logging
from ltsense.transport import QueuedTransport

class QueuedDatazarTransport(QueuedTransport):
    def __init__(self, token=None, fileId=None,):
	self.fileId = fileId
	self.token = token
        QueuedTransport.__init__(self)

    def _run_transport(self, payload):
            logging.debug('Preparing payload for transport to Datazar')
	    options = {
       		'url':'https://api.datazar.com/files/'+self.fileId,
        	'headers':{
                	'Authorization':'Bearer '+self.token
        	}
	    }
	    requests.patch(options['url'],headers=options['headers'],json=json.loads(payload))
            return True