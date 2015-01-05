#!/usr/bin/env python
# encoding: utf-8

u"""
tornado webapp的一个比较重要的策略就是最好把
app.run 单独写成一个启动脚本或是函数.
配置文件,数据库链接等也应该在此时传入,这样以来方便程序的扩展和变更,
也能方便测试代码书写, 便于根据环境启动不同的配置,
之后可以配置supervisor做监控和进程管理
"""

import logging
import tornado.web
import tornado.ioloop
from tornado.options import define, options, parse_command_line


define('port', default='8000', help="default port to run server")


def main():
    parse_command_line()
    urls = []
    settings = {
        'debug': True,
        'db_conn': None,
    }

    application = tornado.web.Application(urls, **settings)
    logging.info("start application on port %s" % options.port)
    application.listen(options.port)

    ioloop = tornado.ioloop.IOLoop.instance()
    ioloop.start()


if __name__ == "__main__":
    main()
