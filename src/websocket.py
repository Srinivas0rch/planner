# websocket.py
#
# Copyright 2019 Tudor Butufei
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE X CONSORTIUM BE LIABLE FOR ANY
# CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#
# Except as contained in this notice, the name(s) of the above copyright
# holders shall not be used in advertising or otherwise to promote the sale,
# use or other dealings in this Software without prior written
# authorization.

from gi.repository import GLib
import websocket
import threading
import json

CONFIG = {
    'ip': 'localhost',
    'port': '6789'
}

class WebSocket:
    def __init__(self, application, socket_ip, socket_port):
        CONFIG['ip'] = socket_ip
        CONFIG['port'] = socket_port
        self.socket = None
        self.thread = None
        self.application = application
        self.start_thread()


    def start_thread(self):
        self.thread = threading.Thread(target = self.start_connection)
        self.thread.start()


    def start_connection(self):
        def on_msg(socket, message):
            data = json.loads(message)
            type = data['type']
            GLib.idle_add(self.application.on_socket_message, type, data)

        def on_error(socket, error):
            GLib.idle_add(self.application.on_socket_error, error)

        self.socket = websocket.WebSocketApp(
            'ws://' + CONFIG['ip'] + ':' + CONFIG['port'],
            on_message=on_msg, on_error=on_error)
        self.socket.run_forever()


    def close_connection(self):
        self.socket.close()


    def send_message(self, action, value = ''):
        message = json.dumps({'action': action, 'value': value})
        self.socket.send(message)
