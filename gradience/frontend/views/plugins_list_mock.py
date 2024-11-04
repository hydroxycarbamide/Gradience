# plugins_list.py
#
# Change the look of Adwaita, with ease
# Copyright (C) 2022-2023, Gradience Team
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.

import os

from gi.repository import Adw

from gradience.backend.globals import user_plugin_dir

from gradience.backend.logger import Logger

logging = Logger()


class GradiencePluginsList:
    """Represent the plugin group in Advanced"""

    def __init__(self, win):

        self.win = win
        self.app = self.win.get_application()
        self.enabled_plugins = set(
            self.app.settings.get_value("enabled-plugins").unpack()
        )
        self.rows = {}

    def reload(self):
        return

    def save_enabled_plugins(self):
        return

    def enable_plugin(self, plugin_id):
        return

    def disable_plugin(self, plugin_id):
        return

    @staticmethod
    def check_if_plugin_dir_exists():
        """Check if the plugin directory exists, if not, create it"""
        if not os.path.exists(user_plugin_dir):
            os.makedirs(user_plugin_dir)
            return False
        return True

    def to_group(self):
        group = Adw.PreferencesGroup()
        group.set_title(_("Plugins"))
        group.set_description(
            _(
                "Plugins add additional features to Gradience, plugins are "
                "made by Gradience community and can cause issues."
            )
        )
        row = Adw.ActionRow()
        row.set_title(_("No Plugins Found."))
        group.add(row)
        return group

    def save(self):
        saved = {}
        return saved

    def validate(self):
        errors = []
        return errors

    def apply(self):
        return
