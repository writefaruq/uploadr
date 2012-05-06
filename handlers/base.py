import tornado.options
import tornado.web

from tornado.options import options
from tornado.database import Connection

import local_environment

class BaseHandler(tornado.web.RequestHandler):
    @property
    def db(self):
        # Todo: Get from config
        if not hasattr(self, "_db"):
            self._db_connection = Connection(host=local_environment.DB_HOST, \
                database=local_environment.DB_NAME,\
                user=local_environment.DB_USER,
                password=local_environment.DB_PASSWORD)

        return self._db_connection
