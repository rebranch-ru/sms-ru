# -*- coding: utf8 -*-
import re
import requests
import urlparse

from rebranch_sms_ru.statuses import STATUS_CHOICES


class SMSRuAPI(object):
    _PARAM_MESSAGE_ID = u'id'
    _PARAM_API_ID = u'api_id'
    _PARAM_RECIPIENT = u'to'
    _PARAM_CONTENT = u'text'

    _API_METHOD_SEND = u'/sms/send'
    _API_METHOD_COST = u'/sms/cost'
    _API_METHOD_STATUS = u'/sms/status'

    _content = None
    _api_id = None
    _recipient = None

    @property
    def api_id(self):
        return self._api_id

    @api_id.setter
    def api_id(self, value):
        self._api_id = value


    def _call_api_method(self, url, **params):
        params.update({self._PARAM_API_ID: self.api_id})
        url = urlparse.urljoin(self._api_host, url)
        response = requests.get(url=url, params=params)
        return response

    def __init__(self, api_id, api_host=u'http://sms.ru', debug=False):
        super(SMSRuAPI, self).__init__()
        self._params = {}
        self._debug_mode = debug
        self._api_host = api_host
        self._api_id = api_id

    @staticmethod
    def get_status_description(status):
        return STATUS_CHOICES.get(status, STATUS_CHOICES[u'default'])

    def get_status(self, sms_id):
        params = {
            self._PARAM_MESSAGE_ID: sms_id
        }
        api_response = self._call_api_method(self._API_METHOD_STATUS, **params)
        status = api_response.text.strip()
        result = {
            u'status': status,
        }
        return result

    def get_cost(self, recipient, content):
        params = {
            self._PARAM_RECIPIENT: recipient,
            self._PARAM_CONTENT: content
        }
        api_response = self._call_api_method(self._API_METHOD_COST, **params)
        status, cost, length = (api_response.text.split() + [None, None])[:3]
        result = {
            u'cost': cost,
            u'length': length,
            u'status': status,
        }
        return result

    def send(self, recipient, content):
        params = {
            self._PARAM_RECIPIENT: recipient,
            self._PARAM_CONTENT: content
        }
        api_response = self._call_api_method(self._API_METHOD_SEND, **params)
        status, sms_id, balance = (api_response.text.split() + [None, None])[:3]
        if not status == u'100':
            # в случае неудачи во второй строке идет номер телефона
            sms_id = None
        result = {
            u'balance': balance,
            u'sms_id': sms_id,
            u'status': status,
        }
        return result