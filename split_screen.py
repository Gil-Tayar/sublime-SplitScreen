"""
SplitScreen v2.0.0
origin by Nick Fisher
https://github.com/spadgos/sublime-SplitScreen
"""
import sublime_plugin
import re


def addUp(lst):
    out = [0.0]
    for i in lst:
        out.append(out[-1] + i)

    return out


class SplitScreenCommand(sublime_plugin.WindowCommand):

    def run(self):
        win = self.window

        # Group check
        if win.num_groups() == 1:
            win.show_input_panel("Split ratios", "60:40", self.splitWindow, None, None)


    def splitWindow(self, inp):
        parts = re.split("\\s*,\\s*", inp)

        horiz = parts[0] or "1"
        vert = parts[1] or "1" if len(parts) > 1 else "1"

        # Python 3 fix        
        vert = list(map(float, re.split(":", vert)))
        horiz = list(map(float, re.split(":", horiz)))

        vertTotal = sum(vert)
        horizTotal = sum(horiz)

        # Python 3 fix
        vert = list(map((lambda x: x / vertTotal), vert))
        horiz = list(map((lambda x: x / horizTotal), horiz))

        cols = addUp(horiz)
        rows = addUp(vert)

        cells = []
        for x, val1 in enumerate(horiz):
            for y, val2 in enumerate(vert):
                cells.append([x, y, x + 1, y + 1])

        # Toggle sidebar
        self.window.run_command('toggle_side_bar')

        # Set layout
        self.window.run_command("set_layout", {
            "cols": cols,
            "rows": rows,
            "cells": cells
        })

        # Leave focus on current group
        self.window.run_command("focus_group", { "group": 0 })