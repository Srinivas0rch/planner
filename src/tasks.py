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

from gi.repository import Gtk, GLib, Gdk

@Gtk.Template(resource_path='/org/i2002/Planner/tasks.ui')
class TasksView(Gtk.Box):
    __gtype_name__ = 'TasksView'

    # Data
    store = Gtk.ListStore(str)

    # Widgets
    list = Gtk.Template.Child()
    add_button = Gtk.Template.Child()
    remove_button = Gtk.Template.Child()
    activate_button = Gtk.Template.Child()
    input_entry = Gtk.Template.Child()

    # Setup
    def setup(self, application):
        self.application = application
        self.setup_treeview()

        # set callbacks
        self.input_entry.connect('activate', self.on_add_action)
        self.add_button.connect('clicked', self.on_add_action)
        self.activate_button.connect('clicked', self.on_activate_action)
        self.remove_button.connect('clicked', self.on_remove_action)
        self.list.connect('button-press-event', self.on_list_item_press_event)


    def setup_treeview(self):
        renderer = Gtk.CellRendererText()
        renderer.props.size = 20000

        column = Gtk.TreeViewColumn("Task", renderer, text=0)
        self.list.set_model(self.store)
        self.list.append_column(column)


    # Callbacks
    def on_add_action(self, element):
        input = self.input_entry.get_text()
        self.input_entry.set_text('')
        if(input != ''):
            self.application.socket.send_message('task_add', input)


    def on_remove_action(self, element):
        value = self.get_list_selection()
        if(value):
            self.application.socket.send_message('task_remove', value)


    def on_activate_action(self, element):
        value = self.get_list_selection()
        if(value):
            self.application.socket.send_message('timer_start', value)
            self.application.socket.send_message('timer_change', value)


    def on_list_item_press_event(self, widget, event):
        if event.button == 1 and event.type == Gdk.EventType._2BUTTON_PRESS:
            GLib.idle_add(self.on_activate_action, widget)


    # Data
    def data_init(self, data):
        for task in data:
            self.store.append([ task ])


    def add_data(self, name):
        self.store.append([ name ])


    def remove_data(self, name):
        deliter = self.get_iter(name)

        if(deliter):
            self.store.remove(deliter)


    # Helpers
    def get_list_selection(self):
        selection = self.list.get_selection()
        (model, pathlist) = selection.get_selected_rows()

        # check if any row selected
        if(len(pathlist) == 1):
            tree_iter = model.get_iter(pathlist[0])
            return model.get_value(tree_iter, 0)

        return None


    def get_iter(self, name):
        search = -1
        current = 0

        for row in self.store:
            if(row[0] == name):
                search = current
            current += 1

        # if found
        if(search != -1):
            path = Gtk.TreePath(search)
            return self.store.get_iter(path)

        return None
