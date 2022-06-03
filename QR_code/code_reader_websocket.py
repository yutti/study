import os.path
import json
import sqlite3
import webbrowser
import cv2
import winsound
import threading
from pyzbar.pyzbar import decode
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from websocket_server import WebsocketServer

class OrenoServer:

    def __init__(self):
        self.HOST = 'localhost'
        self.HTTP_PORT = 8080
        self.WS_PORT = 8081
        self.client = None     
        self.wss = WebsocketServer(host=self.HOST, port=self.WS_PORT)
        self.wss.set_fn_new_client(self.new_client)
        self.https = ThreadingHTTPServer((self.HOST, self.HTTP_PORT), HttpHandler)
        self.codes = []

    def start(self):
        threading.Thread(target=self.wss.run_forever).start()
        threading.Thread(target=self.https.serve_forever).start()
        webbrowser.open(f'http://{self.HOST}:{str(self.HTTP_PORT)}')

    def shutdown(self):
        self.wss.shutdown()
        self.https.shutdown()

    def new_client(self, client, server):
        if self.client is None:
            self.client = client
            threading.Thread(target=self.cam_capture).start()

    def cam_capture(self):
        cap = cv2.VideoCapture(0)
        font = cv2.FONT_HERSHEY_SIMPLEX
        while cap.isOpened():
            ret, frame = cap.read()

            if ret:
                d = decode(frame)

                if d:
                    for barcode in d:
                        barcode_data = barcode.data.decode('utf-8')

                        if barcode_data not in self.codes:
                            self.codes.append(barcode_data)
                            winsound.Beep(2000, 50)
                            font_color = (0, 0, 255)
                            self.wss.send_message(self.client, barcode_data)
                        else:
                            font_color = (0, 154, 87)

                        x, y, w, h = barcode.rect
                        cv2.rectangle(frame, (x, y), (x + w, y + h), font_color, 2)
                        frame = cv2.putText(frame, barcode_data, (x, y - 10), 
                                            font, .5, font_color, 2, cv2.LINE_AA)

            cv2.imshow('QRCODE READER  press q -> exit', frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                db = OrenoDataBase()
                db.set(self.codes)
                db.close()
                self.shutdown()
                break


class OrenoDataBase:

    def __init__(self):
        self.conn = sqlite3.connect(r"./book_list.db", check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        self.cur = self.conn.cursor()

    def get(self):
        self.cur.execute('SELECT * FROM bookitems ORDER BY code')
        rows = []

        for r in self.cur.fetchall():
            rows.append({'name': r['name'], 'code': r['code'], 'status': r['status']})

        return rows

    def set(self, codes):
        place_holder = ','.join('?'*len(codes))
        values = tuple(codes)
        self.cur.execute(
            f'UPDATE bookitems SET status = TRUE WHERE code in ({place_holder})', values)
        self.conn.commit()

    def close(self):
        self.cur.close()
        self.conn.close()


class HttpHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        with open(r"./template.html", mode='r', encoding='utf-8') as html:
            response_body = html.read()
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(response_body.encode('utf-8'))

    def do_POST(self):
        db = OrenoDataBase()
        rows = db.get()
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        response_body = json.dumps(rows)
        self.wfile.write(response_body.encode('utf-8'))
        db.close()


server = OrenoServer()
server.start()