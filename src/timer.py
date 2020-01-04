# timer.py
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

from gi.repository import Gtk, GObject

@Gtk.Template(resource_path='/org/i2002/Planner/timer.ui')
class TimerView(Gtk.Box):
    __gtype_name__ = 'TimerView'

    # Data
    timer = {
        'state': -2, # -2: not connected, -1: idle, 0: work, 1: break
        'pause': False,
        'time': '',
        'info': '',
    }

    # Widgets
    timer_label = Gtk.Template.Child()
    info_label = Gtk.Template.Child()

    toggle_state_button = Gtk.Template.Child()
    toggle_pause_button = Gtk.Template.Child()


    # Setup
    def setup(self, application):
        self.application = application

        # set callbacks
        self.toggle_state_button.connect('clicked', self.on_toggle_state)
        self.toggle_pause_button.connect('clicked', self.on_toggle_pause)


    # Callbacks
    def on_toggle_state(self, button):
        if(self.timer['state'] == -1):
            self.application.socket.send_message('timer_start')
        else:
            self.application.socket.send_message('timer_end')
        self.set_sensitive(False)


    def on_toggle_pause(self, button):
        self.application.socket.send_message('timer_toggle')


    def on_update_ui_state(self, changed):
        # Set label name
        state_label = 'Start' if self.timer['state'] < 0 else 'Stop'
        pause_label = 'Pause' if not self.timer['pause'] else 'Resume'
        timer_label = self.timer['time']
        info_label = self.timer['info']

        # Update labels
        self.toggle_state_button.set_label(state_label)
        self.toggle_pause_button.set_label(pause_label)
        self.timer_label.set_label(timer_label)
        self.info_label.set_label(info_label)

        # Update UI interactivity
        if(changed):
            self.set_sensitive(True)
            self.toggle_pause_button.set_sensitive(self.timer['state'] >= 0)


    # Data methods
    def update_timer(self, data):
        # Mark connected or state changed
        changed = False
        if(data['state'] != self.timer['state']):
            changed = True

        keys = ['state', 'pause', 'time', 'info']
        for key in keys:
            self.timer[key] = data[key]

        self.on_update_ui_state(changed)

