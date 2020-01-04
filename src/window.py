# window.py
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

from gi.repository import Gtk
from .websocket import WebSocket
from .timer import TimerView
from .tasks import TasksView


@Gtk.Template(resource_path='/org/i2002/Planner/window.ui')
class PlannerWindow(Gtk.ApplicationWindow):
    __gtype_name__ = 'PlannerWindow'

    timer_view = Gtk.Template.Child()
    tasks_view = Gtk.Template.Child()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # init components
        application = kwargs['application']
        self.timer_view.setup(application)
        self.tasks_view.setup(application)


    def on_activate(self):
        self.timer_view.set_sensitive(True)
        self.tasks_view.set_sensitive(True)


    def on_deactivate(self):
        self.timer_view.set_sensitive(False)
        self.tasks_view.set_sensitive(False)


    def show_error_dialog(self, error):
        # setup data
        title = "Connection error"
        content = (
            'A socket connection error has occured:\n'
            '<tt><i>' + error.__str__() + '</i></tt>\n'
            'Please restart the app to try again.')

        # setup dialog
        dialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.ERROR, Gtk.ButtonsType.OK, title)
        dialog.format_secondary_markup(content)
        dialog.run()
        dialog.destroy()

