import wsgiref.handlers
import tornado.wsgi
import tornado.web
import os
import Handlers
import SystemRequestHandler

def application():
    handlers=[(r"/", Handlers.MainHandler),
            (r"/Login", Handlers.LoginHandler),
            (r"/ViewHistory",Handlers.ViewHistoryHandler),
            (r"/UploadFile", Handlers.UploadHandler),
            (r"/Index", Handlers.IndexHandler),
            (r"/About", Handlers.AboutHandler),
            (r"/Profile", Handlers.ProfileHandler),
            (r"/System", SystemRequestHandler.SystemRequestHandler)]

    settings=dict(template_path=os.path.join(os.path.dirname(__file__), "templates"),
                static_path=os.path.join(os.path.dirname(__file__), "static"),
                debug=True)
    
    return tornado.wsgi.WSGIApplication(handlers, "", **settings)

def main():
    server = wsgiref.handlers.CGIHandler().run(application())

if __name__ == "__main__":
    main()
