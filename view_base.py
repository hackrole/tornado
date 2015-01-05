#!/usr/bin/env python
# encoding: utf-8

u"""
view base.py
"""

import tornado.web
from tornado import gen


class BaseHandler(tornado.web.RequestHandler):

    def get_current_user(self):
        return None

    def raise_gen_error(self, code, msg=None):
        output = {"code": code, "msg": msg}
        self.finish(output)
        raise gen.Return()

    def raise_gen_ok(self, data=None, code=200, msg=None):
        output = {"data": data, "code": code, "msg": msg}
        self.finish(output)
        raise gen.Return()
