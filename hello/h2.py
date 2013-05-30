import tornado.ioloop
import tornado.web

class MainHander(tornado.web.RequestHandler):
    def get(self):
        self.write('the index xpage')

class StoryHander(tornado.web.RequestHandler):
    def get(self, story_id):
        self.write("you requested the story" + story_id)

class ErrHander(tornado.web.RequestHandler):
    def get(self):
        raise tornado.web.HTTPError(403)

application = tornado.web.Application(
        [
            (r"/", MainHander),
            (r"/story/([0-9]+)", StoryHander),
            (r'/error', ErrHander),
        ],
        debug=True
    )

if __name__ == "__main__":
    application.listen(8000)
    tornado.ioloop.IOLoop.instance().start()
