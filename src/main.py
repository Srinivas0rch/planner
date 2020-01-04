# main.py
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

import sys
import gi

gi.require_version('Gtk', '3.0')

from gi.repository import Gtk, Gio, GObject, GLib

from .window import PlannerWindow
from .websocket import WebSocket


class Application(Gtk.Application):
    def __init__(self):
        super().__init__(application_id='org.i2002.Planner',
                         flags=Gio.ApplicationFlags.HANDLES_COMMAND_LINE)
        self.settings = Gio.Settings.new('org.i2002.Planner')
        self.socket = None

        # add CLI options
        self.add_main_option("ip", ord("i"), GLib.OptionFlags.NONE, GLib.OptionArg.STRING, "Time server ip", None)
        self.add_main_option("port", ord("p"), GLib.OptionFlags.NONE, GLib.OptionArg.STRING, "Time server port", None)


    def setup_socket(self):
        socket_ip = self.settings.get_string('socket-ip')
        socket_port = self.settings.get_string('socket-port')
        return WebSocket(self, socket_ip, socket_port)


    # app events
    def do_activate(self):
        self.win = self.props.active_window
        if not self.win:
            self.win = PlannerWindow(application = self, title="Planner")
            self.socket = self.setup_socket()
        self.win.present()


    def do_shutdown(self):
        Gtk.Application.do_shutdown(self)
        if(self.socket):
            self.socket.close_connection()


    def do_command_line(self, command_line):
        options = command_line.get_options_dict()
        options = options.end().unpack()

        # if there are options do not show window
        if(len(options) > 0):
            if "ip" in options:
                self.settings.set_string('socket-ip', options['ip'])
                print('Setted socket IP:', options['ip'])

            if 'port' in options:
                self.settings.set_string('socket-port', options['port'])
                print('Setted socket port:', options['port'])

            print('Restart the app for the changes to take effect')
            return 0

        self.activate()
        return 0


    # socket events
    def on_socket_message(self, type, data):
        if(type == 'init'):
            self.win.on_activate()
            self.win.tasks_view.data_init(data['tasks'])

        elif(type == 'timer'):
            self.props.active_window.timer_view.update_timer(data)

        elif(type == 'task_add'):
            self.win.tasks_view.add_data(data['name'])

        elif(type == 'task_remove'):
            self.win.tasks_view.remove_data(data['name'])


    def on_socket_error(self, error):
        print('Socket error', error)
        self.win.on_deactivate()
        self.win.show_error_dialog(error)


def main(version):
    # set the dark theme by default
    settings = Gtk.Settings.get_default()
    #settings.set_property('gtk-theme-name', 'Adwaita')
    settings.set_property('gtk-application-prefer-dark-theme', True)

    # start the application
    app = Application()
    return app.run(sys.argv)
