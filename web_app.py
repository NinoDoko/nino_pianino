import tornado.ioloop
import tornado.web
import tornado.httpserver
import json

import os
import generator, song_generator

class MainHandler(tornado.web.RequestHandler):
    def post(self):
        base_block = json.loads(self.request.body)
        mid = generator.generate(base_block)
        generator.write_mid(mid, 'generated_song', use_soundfont = 'soundfonts/FluidR3_GM.sf2')
        
        buf_size = 4096
        self.set_header('Content Type', 'application/octet-stream')
        self.set_header('Content-Disposition', 'attachment; filename=generated_song.wav')
        with open('generated_song.wav', 'r') as f: 
            while True: 
                data = f.read(buf_size)
                if not data:
                    break
                self.write(data)
        self.finish
        
    def get(self):
        new_song = song_generator.generate_song()
        buf_size = 4096
        self.set_header('Content Type', 'application/octet-stream')
        self.set_header('Content-Disposition', 'attachment; filename=' + new_song )
        with open(new_song, 'r') as f: 
            while True: 
                data = f.read(buf_size)
                if not data:
                    break
                self.write(data)
        self.finish

class IndexHandler(tornado.web.RequestHandler):        
    def get(self):
        self.write('Hello!')

        
        
def make_app():
    return tornado.web.Application([
        (r'/', IndexHandler),
        (r'/generate_song', MainHandler),
    ])
    
    
if __name__ == '__main__':
    app = make_app()
    http_server = tornado.httpserver.HTTPServer(app)
    port = int(os.environ.get("PORT", 5000))
    http_server.listen(port)
    tornado.ioloop.IOLoop.instance().start()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()
