#!/usr/bin/env python
# encoding: utf-8

u"""
tornado测试utils,
get/post for quick/user-friendly http request
yield_get/yield_post used in gen_test func
patcher mock system
dbinit hooks
"""

import mock
from urllib import urlencode
from tornado import gen, ioloop
from tornado.concurrent import Future
from tornado.testing import AsyncHTTPTestCase


def sms(code, mobile):
    return False


class BaseTestCase(AsyncHTTPTestCase):

    def setUp(self):
        super(BaseTestCase, self).setUp()
        self.db = None

        # mock patch
        self.sms_patcher = mock.patch('test_base.sms')
        self.sms_mock = self.request_patcher.start()

        def sms_side(code, mobile):
            future = Future()
            future.set_result(True)
            return future
        self.sms_mock.side_effect = sms_side

        # db clean and init
        self.io_loop.run_sync(self.drop_database)
        if getattr(self, 'fixture_setUp', None):
            self.io_loop.run_sync(self.fixture_setUp)

    def tearDown(self):
        # db clean
        self.io_loop.run_sync(self.drop_database)

        # mock patcher end
        self.patcher.stop()

        super(BaseTestCase, self).tearDown()

    @gen.coroutine
    def drop_database(self):
        # XXX finish your code here
        conn = None
        yield conn.drop_database()

    def get(self, url, data=None, headers=None):
        if data is None:
            return self.fetch(url, method="GET", headers=headers)

        # TODO finish utf8 urlencode error
        data = urlencode(data)
        if '?' in url:
            url += '&amp;%s' % data
        else:
            url += '?%s' % data

        return self.fetch(url, method="GET", headers=headers)

    def post(self, url, data, headers=None):
        if data is not None:
            if isinstance(data, dict):
                data = urlencode(data)

        return self.fetch(url, method='POST', body=data, headers=headers)

    def yield_get(self, url, data=None, headers=None):
        if data is None:
            return self._fetch(url, 'GET', headers=headers)

        if data is not None:
            data = urlencode(data)
        if '?' in url:
            url += '&amp;%s' % data
        else:
            url += '?%s' % data

        return self._fetch(url, 'GET', headers=headers)

    def yield_post(self, url, data, headers=None):
        if data is not None:
            if isinstance(data, dict):
                data = urlencode(data)

        return self._fetch(url, 'POST', data, headers)

    def _fetch(self, url, method, data=None, headers=None):
        url = self.get_url(url)
        return self.http_client.fetch(
            url, method=method, body=data, headers=headers)
