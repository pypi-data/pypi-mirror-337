#!/usr/bin/env python3
# coding: utf-8
import sys
# Copyright 2024 by BurnoutDV, <development@burnoutdv.com>
#
# This file is part of EpisodeNames.
#
# EpisodeNames is free software: you can redistribute
# it and/or modify it under the terms of the GNU General Public
# License as published by the Free Software Foundation, either
# version 3 of the License, or (at your option) any later version.
#
# EpisodeNames is distributed in the hope that it will
# be useful, but WITHOUT ANY WARRANTY; without even the implied warranty
# of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# @license GPL-3.0-only <https://www.gnu.org/licenses/gpl-3.0.en.html>

import time
from typing import Iterable

from rich.console import RenderableType
from textual.app import App, ComposeResult, SystemCommand
from textual.binding import Binding
from textual.containers import Vertical
from textual.widgets import Footer, RichLog
from textual.screen import ModalScreen, Screen

from episode_names.Modals.DialogueModals import YesNoBox
from episode_names.Screens import EpisodeScreen, TemplateScreen, SettingsScreen
from episode_names.Utility import MenuProvider, i18n, user_setup
from episode_names.__init__ import __version__

__author__ = "Bruno DeVries"
__license__ = "GPL-3"
__appname__ = "episode_names"
__appauthor__ = "BurnoutDV" # my preferred name so to speak
__folder_version__ = "1.1" # in case of breaking changes, change this


class DebugLog(ModalScreen[bool]):
    """
    Sad Excuse for a quick debug log functionality, I am totally aware that there is a way with Textual
    to achieve the same thing without this.
    """
    BINDINGS = [
        ("escape", "back", i18n['Cancel']),
        ("ctrl+c", "quit", i18n['Quit']),
    ]
    def __init__(self, log: RichLog):
        self.debug = log
        super().__init__()

    def compose(self) -> ComposeResult:
        with Vertical(id="log_overlay"):
            yield self.debug
            yield Footer()

    def _action_back(self):
        self.dismiss(True)


class EpisodeNames(App):
    CSS_PATH = 'app_design.tcss'
    COMMANDS = {MenuProvider}
    COMMAND_PALETTE_BINDING = "circumflex_accent"

    BINDINGS = [
        Binding(key="escape", action="quit_dial", description=i18n['Quit'], show=False),
        Binding(key="f4", action="open_debug", description="Debug", show=False),
        Binding(key="f1", action="switch_mode('episodes')", description=i18n['Episode']),
        Binding(key="f2", action="switch_mode('templates')", description=i18n['Templates']),
        Binding(key="f3", action="switch_mode('settings')", description=i18n['Settings']),
    ]

    MODES = {
        "episodes": EpisodeScreen,
        "templates": TemplateScreen,
        "settings": SettingsScreen,
        #"help": HelpScreen,
    }

    def __init__(self):
        self.hour_zero = time.time_ns()/1000000
        self.dummy_log = RichLog(id="dummy_log")
        self.debug_open = False
        self.console_title = f"Episode Names - v{__version__}, DB Version: {__folder_version__}"
        # ? at least for Konsole the set_window_title does not work
        sys.stderr.write(f"\x1b]2;{self.console_title}\x07")
        sys.stderr.flush()
        self.redraw_after_import = False, False
        super().__init__()

    def on_mount(self) -> None:
        self.theme = "flexoki"
        self.console.set_window_title(self.console_title)
        self.app.switch_mode("episodes")

    def get_system_commands(self, screen: Screen) -> Iterable[SystemCommand]:
        yield from super().get_system_commands(screen)
        # hide default commands
        pass

    def write_raw_log(self, this: RenderableType, additional_text=""):
        self.write_log(f"Raw Object: {additional_text}")
        self.dummy_log.write(this)

    def write_log(self, text):
        delta_time = round(time.time_ns()/1000000 - self.hour_zero,2)
        self.dummy_log.write(f"{delta_time} - {text}")

    def _action_show_templates(self):
        self.app.switch_mode('templates')

    def _action_open_debug(self):
        if self.debug_open:
            return

        def handle_debug(diss: bool):
            self.debug_open = False

        self.debug_open = True
        self.app.push_screen(DebugLog(self.dummy_log), handle_debug)

    def action_quit_dial(self):
        def handle_quit_message(dec: bool):
            if dec:
                self.exit(message=i18n["Thanks for choosing EpisodNames"])
        self.app.push_screen(YesNoBox(i18n["Do you want to quit?"]), handle_quit_message)

def run_main():
    print("Running App")
    user_setup(__appname__, __appauthor__, __folder_version__)
    app = EpisodeNames()
    app.run()

if __name__ == "__main__":
    run_main()
