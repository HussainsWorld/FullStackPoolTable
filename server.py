import sys
import os
import cgi
import phylib
import Physics
import math
import helper
import json

from http.server import HTTPServer, BaseHTTPRequestHandler;
from urllib.parse import urlparse, parse_qsl;
from urllib import parse


#grab port based on input
PORT = 50000 + (int(sys.argv[1][-4:]))

class MyHandler(BaseHTTPRequestHandler):
    player_names = {}
    def do_GET(self):
        parsed = urlparse(self.path)
        if parsed.path == '/intro.html':
            # Handle request for the introduction page
            with open('.' + self.path, 'r') as fp:
                content = fp.read()
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.send_header("Content-length", len(content))
                self.end_headers()
                self.wfile.write(bytes(content, "utf-8"))
        elif parsed.path == '/game.html':
            # Extract player names from query parameters
            # query_params = dict(parse_qsl(parsed.query))
            # player1_name = query_params.get('player1', '')
            # player2_name = query_params.get('player2', '')

            # Read content of game.html
            with open('./game.html', 'r') as fp:
                content = fp.read()

            # Replace placeholders in game.html with player names
            # content = content.replace('${player1}', player1_name)
            # content = content.replace('${player2}', player2_name)

            # Send modified game.html to client
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.send_header("Content-length", len(content))
            self.end_headers()
            self.wfile.write(bytes(content, "utf-8"))

        elif parsed.path == '/intro.js':
            # Handle request for the game page
            with open('.' + self.path, 'r') as fp:
                content = fp.read()
                self.send_response(200)
                self.send_header("Content-type", "application/javascript")
                self.send_header("Content-length", len(content))
                self.end_headers()
                self.wfile.write(bytes(content, "utf-8"))
        elif parsed.path == '/game.js':
            # Handle request for the game page
            with open('.' + self.path, 'r') as fp:
                content = fp.read()
                self.send_response(200)
                self.send_header("Content-type", "application/javascript")
                self.send_header("Content-length", len(content))
                self.end_headers()
                self.wfile.write(bytes(content, "utf-8"))
        elif parsed.path == '/style.css':
            # Handle request for the game page
            with open('.' + self.path, 'r') as fp:
                content = fp.read()
                self.send_response(200)
                self.send_header("Content-type", "text/css")
                self.send_header("Content-length", len(content))
                self.end_headers()
                self.wfile.write(bytes(content, "utf-8"))
        else:
            # Handle requests for other resources (like images, CSS, etc.)
            if parsed.path.startswith('/table-') and parsed.path.endswith('.svg'):
                # Handle request for SVG files
                filePath = '.' + self.path
                if os.path.exists(filePath):
                    with open(filePath, 'r') as fp:
                        content = fp.read()
                    self.send_response(200)
                    self.send_header("Content-type", "image/svg+xml")
                    self.send_header("Content-length", len(content))
                    self.end_headers()
                    self.wfile.write(bytes(content, "utf-8"))
                else:
                    # Generate 404 error code if file not found
                    self.send_response(404)
                    self.end_headers()
                    self.wfile.write(bytes("404: %s not found" % self.path, "utf-8"))
            else:
                # Generate 404 error code for other requests
                self.send_response(404)
                self.end_headers()
                self.wfile.write(bytes("404: %s not found" % self.path, "utf-8"))

    def do_POST(self):
        if self.path == '/get_svg_content':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            form_data = parse.parse_qs(post_data.decode('utf-8'))
            print('hi')
            playerName1 = self.player_names.get('playerName1', None)
            playerName2 = self.player_names.get('playerName2', None)
            
            # db = Physics.Database()
            print(playerName1)
            print(playerName2)
            # game = Physics.Database.setGame(gameName="Game01", playerName1=playerName1, playerName2=playerName2)
            firstTable = helper.init_table()
            Physics.Game(gameName = 'Game01', player1Name = playerName1, player2Name = playerName2)
            
            # Generate the SVG content of the table
            svg_content = firstTable.svg()
            # print(svg_content)

            # Serve game.html with the SVG content embedded in it
            with open('game.html', 'r') as file:
                content = file.read().replace('${svg_content}', svg_content)
                content = content.replace('${playerName1}', playerName1)
                content = content.replace('${playerName2}', playerName2)
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.send_header("Content-length", len(content))
                self.end_headers()
                self.wfile.write(bytes(content, "utf-8"))
        elif self.path == '/set_player_names':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            form_data = parse.parse_qs(post_data.decode('utf-8'))
            playerName1 = form_data.get('playerName1', [None])[0]
            playerName2 = form_data.get('playerName2', [None])[0]
            
            # Store player names in server memory
            self.player_names['playerName1'] = playerName1
            self.player_names['playerName2'] = playerName2

            self.send_response(200)
            self.end_headers()
        elif self.path == '/submit_shot':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            
            dx = data.get('dx')
            dy = data.get('dy')
            
            db = Physics.Database()
            preShotID = db.getLastTableID() - 1
            game = Physics.Game(gameID = 1)
            game.shoot("Game01", "Hello", db.readTable(preShotID), dx, dy)
            postShotID = db.getLastTableID() - 1
            
            frames_data = {
                "frames": []
            }
            
            i = preShotID
            while (i < postShotID):
                table = db.readTable(i)
                frame_info = {
                    "svg": table.svg().strip(), 
                    "time": table.time
                }
                frames_data["frames"].append(frame_info)
                i += 1
            
            print("Number of frames:", len(frames_data["frames"]))
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            jsonResponse = json.dumps(frames_data) 
            self.send_header('Content-Length', str(len(jsonResponse)))
            self.end_headers()
            self.wfile.write(jsonResponse.encode('utf-8'))



if __name__ == "__main__":
    httpd = HTTPServer( ( 'localhost', PORT ), MyHandler );
    print( "Server listing in port:  ", PORT );
    httpd.serve_forever();
