# -*- coding: utf-8; -*-
"""
Copyright (C) 2007-2013 Guake authors

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License as
published by the Free Software Foundation; either version 2 of the
License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
General Public License for more details.

You should have received a copy of the GNU General Public
License along with this program; if not, write to the
Free Software Foundation, Inc., 51 Franklin Street, Fifth Floor,
Boston, MA 02110-1301 USA
"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

# pylint: disable=wrong-import-position,wrong-import-order,unused-import
from guake import gi

assert gi  # hack to "use" the import so pep8/pyflakes are happy
from gi.repository import Gio
# pylint: enable=wrong-import-position,wrong-import-order,unused-import
from guake.application.actions import actions as application_actions


class GuakeKeybindingsRepository(Gio.Settings):
    application_actions = application_actions

    def __init__(self, application):
        super().__init__(schema='org.guake.keybindings')
        self.connect('changed', application.change_keybinding_handler)

    def get_application_action(self, key):
        for action_dict in self.application_actions:
            if key == action_dict['key']:
                return action_dict
        return None
