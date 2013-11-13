# -*- coding: utf-8 -*-
import sublime
import sublime_plugin

_2nd_clipboard = [];

class Clipboard2ndCommand(sublime_plugin.TextCommand):
	def run(self, edit, **args):
		global _2nd_clipboard

		action = args["action"]

		sel = self.view.sel()

		if action == "copy" or action == "cut":
			count = 0
			strings = [];
			for s in sel:
				strings.append(self.view.substr(s))
				count += len(s)

			if count == 0:
				return

			_2nd_clipboard = strings;

			if args["action"] == "cut":
				cmd = "Cut"
				for s in sel:
					self.view.erase(edit, s)
			else:
				cmd = "Copied"

			sublime.status_message(
				str.format("{0} {1} charactor{2} (2nd)",
					cmd,
					count,
					"s" if count == 1 else ""))

		elif action == "paste":
			cnt = len(_2nd_clipboard)
			if cnt == 0:
				return

			if len(sel) == cnt:
				i = 0
				for s in sel:
					self.view.replace(edit, s, _2nd_clipboard[i])
					i += 1
			else:
				text = "\n".join(_2nd_clipboard)
				for s in sel:
					self.view.replace(edit, s, text)

			# change selection
			newSels = []
			for s in sel:
				newSels.append(sublime.Region(s.b, s.b))
			sel.clear()
			sel.add_all(newSels)

	def is_enabled(self, **args):
		action = args["action"]

		if action == "copy" or action == "cut":
			for s in self.view.sel():
				if len(s) > 0:
					return True
		elif action == "paste":
			if len(_2nd_clipboard) > 0:
				return True

		return False