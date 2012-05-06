import tornado.options
import tornado.web

from handlers.base import BaseHandler
from status import UPLOAD_STATUS as us
import tools

class MainHandler(BaseHandler):
    @property
    def db(self):
        return self.application.db

    def get_current_user(self):
        user_id = self.get_secure_cookie("user")
        if not user_id: return None
        return self.db.get("SELECT * FROM authors WHERE id = %s", int(user_id))

    def get(self):
        service = tools.obtain_captcha_service()
        captcha_random = service.random()
        captcha_image = service.image()
        hosted_files = self._count_hosted_files()

        self.render("uploadform.html",
            hosted_files=hosted_files,
            captcha_random=captcha_random,
            captcha_image=captcha_image)

    def post(self):
        raise tornado.web.HTTPError(403)

    def _count_hosted_files(self):
        row = self.db.get("SELECT COUNT(*) as c \
                        FROM uploads WHERE \
                        uploads.status = %u" % us['ONLINE'])
        if row is not None:
            row = row['c']
        return row
