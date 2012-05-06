import os

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

import logging
import uuid

from tornado.options import define, options

from handlers.main import MainHandler
from handlers.upload import UploadHandler
from handlers.download import RequestHandler, DownloadHandler
from handlers.token import TokenHandler
from handlers.delete import DeleteHandler

import local_environment

define("port", default=8888, help="run on the given port", type=int)
define("storage", default="/tmp/storage", help="FIXME", type=str)
define("desc_min_len", default=15, help="FIXME", type=int)
define("desc_max_len", default=150, help="FIXME", type=int)
define("max_tokens_per_ip", default=3, help="FIXME", type=int)
define("environment", default="development", help="FIXME", type=str)
define("captcha_net_client", default="demo", help="FIXME", type=str)
define("captcha_net_secret", default="secret", help="FIXME", type=str)

#DB settings
define("mysql_host", default=local_environment.DB_HOST, help="blog database host")
define("mysql_database", default=local_environment.DB_NAME, help="uploadr database name")
define("mysql_user", default=local_environment.DB_USER, help="blog database user")
define("mysql_password", default=local_environment.DB_PASSWORD, help="blog database password")

class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/", MainHandler),
            (r"/upload", UploadHandler),
            (r"/token", TokenHandler),
            (r"/request/([0-9abcdef]+)", RequestHandler),
            (r"/download/([0-9abcdef]+)/([^/]+)", DownloadHandler),
            (r"/delete/([0-9abcdef]+)", DeleteHandler),
        ]
        settings = dict(
            cookie_secret="12oETzKXQAGaYdkL5gEmGeJJFuYh7EQnp2XdTP1o/Vo=",
#            login_url="/auth/login",
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
#            xsrf_cookies=True,
#            ui_modules= {"Post": PostModule},
            debug=True,
        )
        tornado.web.Application.__init__(self, handlers, **settings)

        # DB init
        self.db = tornado.database.Connection(
            host=options.mysql_host, database=options.mysql_database,
            user=options.mysql_user, password=options.mysql_password)


def init_environment():
    try:
        os.mkdir(options.storage)
    except OSError, e: # Workaround FIXME
        if e.errno == 17: # File exists
            pass
        else:
            raise e

def main():
    tornado.options.parse_command_line()
    logging.getLogger().setLevel(logging.DEBUG)
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    init_environment()
    tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
    main()
