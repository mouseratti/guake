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

import logging
import os
import re
import traceback

# pylint: disable=wrong-import-position,wrong-import-order,unused-import
from guake import gi
assert gi  # hack to "use" the import so pep8/pyflakes are happy

from gi.repository import GLib
from gi.repository import Gio
from gi.repository import Gtk
# from gi.repository import Vte
from gi.repository import Keybinder
# pylint: enable=wrong-import-position,wrong-import-order,unused-import

logger = logging.getLogger(__name__)
KEYBINDER_POSTFIX = "-keybinder"
KEYBINDER_PATTERN = re.compile("^.+%s$" % KEYBINDER_POSTFIX)


class GuakeKeybinder(object):

    def __init__(self, giosettings, window):
        self.keybinder = Keybinder
        self.keybinder.init()
        self.keymap = {}
        self._window = window
        giosettings.connect("changed", self.reset_handler)
        self.attach_keys(giosettings)

    @staticmethod
    def is_keybinding(value):
        """Returns True if this dconf key is global keybinding.
            Returns False by default.
        """
        return bool(KEYBINDER_PATTERN.findall(value))

    @staticmethod
    def get_handler_by_setting(obj, setting_name):
        """Returns method with name corrensponded to the given setting_name"""
        method_name = setting_name.replace(KEYBINDER_POSTFIX, '', 1).replace('-', '_')
        return getattr(obj, method_name)

    def attach_keys(self, giosettings, key=None):
        """Bind keys to handlers"""
        self._detach_keys(key)
        keys = [_ for _ in giosettings.list_keys() if self.is_keybinding(_)] if not key else [key,]
        for key in keys:
            try:
                handler = self.get_handler_by_setting(self._window, key)
                keyvalue = giosettings.get_value(key).get_string()
                self.keymap[key] = keyvalue
                self.keybinder.bind(keyvalue, handler, None)
            except Exception as e:
                logger.error("%s can not connect key %s", e, key)
                logger.debug(traceback.format_exc())
        return

    def reset_handler(self, settings, setting_name):
        self.attach_keys(settings, setting_name)
        pass

    def _detach_keys(self, key=None):
        if not self.keymap:
            return
        keys = self.keymap.keys() if not key else [key,]
        for key in keys:
            try:
                self.keybinder.unbind(self.keymap[key])
                self.keymap.pop(key)
            except Exception as e:
                logger.error("%s when _detach_keys %s", e, key)
                logger.debug(traceback.format_exc())
        return
