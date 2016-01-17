#!/usr/bin/env python
"""
The module for IO-DATA HVL-A2.0

## Tested Environments
- Python 3.4.3 on Windows 8.1
- HVL-A2.0 (Firmware 2.03)
  - http://www.iodata.jp/product/hdd/rokuga/hvl-a/

Copyright (c) 2016 @kaito834

This software is released under the MIT License.
http://opensource.org/licenses/mit-license.php
"""

__author__  = '@kaito834'
__version__ = '0.1'

import urllib.request
import urllib.error
import urllib.parse
import socket
import json

class myHvlA():
    """
    The wrappper class for APIs of IO-DATA HVL-A2.0
    - http://www.iodata.jp/product/hdd/rokuga/hvl-a/ (in Japanese)
    This class supports the APIs below: browse, remove and rename
    """
    __apiPath = '/dms/transfer_tool/api/'

    def __init__(self, host='192.168.0.220', port='55247'):
        self.host = host
        self.port = port
        self.url = 'http://' + host + ':' + port

    def browse(self, id, index='0', count='20', sort='+dc:title'):
        """
        Retrieve the list of items from HVL-A2.0
        Call browse API: http://<HVL-A URL>/dms/transfer_tool/api/browse

        Arguments:
            id: Item ID(string). Ex: FS-4
            index: starting_index(string)
            count: requested_count(string)
            sort: sort_criteria(string)
        Return:
            JSON object(dict)
        """
        params = {
            'id': id,
            'starting_index': index,
            'requested_count': count,
            'sort_criteria': sort
        }

        queryString = ''
        for key in params:
            if queryString != '':
                queryString = queryString + '&' + '='.join([key, urllib.parse.quote_plus(params[key])])
            else:
                queryString = '='.join([key, urllib.parse.quote_plus(params[key])])
        req_url=self.url + self.__apiPath + 'browse?' + queryString

        with urllib.request.urlopen(req_url, timeout=90) as res:
            j = json.loads(res.read().decode('utf-8'))

        return j

    def remove(self, id):
        """
        Delete item on HVL-A2.0
        Call remove API: http://<HVL-A URL>/dms/transfer_tool/api/remove

        Arguments:
            id: Item ID(string). Ex: FS-4
        Return:
            Result value(integer)
            - 0: SUCCESS
            - 1: UNKNOWN (whether SUCCESS/FAILED)
            - 2,3: FAILED
        """
        req_url = self.url + self.__apiPath + 'remove'
        req_body = '='.join(['id', urllib.parse.quote_plus(id)])
        req_obj = urllib.request.Request(req_url, data=req_body.encode('utf-8'), method='POST')

        try:
            res = urllib.request.urlopen(req_obj, timeout=30)
            httpStatus = res.status
            httpReason = res.reason
        except socket.timeout as e:
            # Ref. http://stackoverflow.com/questions/8072597/skip-url-if-timeout
            print("[!] {0}".format(e))
            return 1
        except urllib.error.HTTPError as e:
            print('[!] {0}'.format(e))
            return 2
        except urllib.error.URLError as e:
            print('[!] {0}'.format(e))
            return 3

        if httpStatus == 200:
            return 0
        else:
            # Maybe this condition is catched on urllib.error.HTTPError
            return 2

    def rename(self, id, newname):
        """
        Rename item on HVL-A2.0
        Call remove API: http://<HVL-A URL/dms/transfer_tool/api/rename

        Arguments:
            id: Item ID(string). Ex: FS-4
            newname: new_name(string)
        Return:
            Result value(integer)
            - 0: SUCCESS
            - 1: UNKNOWN (whether SUCCESS/FAILED)
            - 2,3: FAILED
        """
        req_url = self.url + self.__apiPath + 'rename'
        req_body = '='.join(['id', urllib.parse.quote_plus(id)])
        req_body = req_body + '&' + '='.join(['new_name', urllib.parse.quote_plus(newname)])
        req_obj = urllib.request.Request(req_url, data=req_body.encode('utf-8'), method='POST')

        try:
            res = urllib.request.urlopen(req_obj, timeout=30)
            httpStatus = res.status
            httpReason = res.reason
        except socket.timeout as e:
            print("[!] {0}".format(e))
            return 1
        except urllib.error.HTTPError as e:
            print('[!] {0}'.format(e))
            return 2
        except urllib.error.URLError as e:
            print('[!] {0}'.format(e))
            return 3

        if httpStatus == 200:
            return 0
        else:
            # Maybe this condition is catched on urllib.error.HTTPError
            return 2
