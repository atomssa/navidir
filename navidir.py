import sublime, sublime_plugin
import os, stat

navi_dir_active = False;

def unset_navi_dir_active():
	global navi_dir_active
	navi_dir_active = False

def set_navi_dir_active():
	global navi_dir_active
	navi_dir_active = True

class ViewWatcher(sublime_plugin.EventListener):
	def __init__(self, *args, **kwargs):
		super(ViewWatcher, self).__init__(*args, **kwargs)

	def on_query_context(self, view, key, operator, operand, match_all):
		if key == "navi_dir_active":
			return navi_dir_active

	def on_activated_async(self, view):
		def perm_sub_str(perm,_r,_w,_x):
			sub_str = "r" if perm & _r else "-"
			sub_str += "w" if perm & _w else "-"
			sub_str += "x" if perm & _x else "-"
			return sub_str

		def perm_str(perm):
			mode_line = perm_sub_str(perm,stat.S_IRUSR,stat.S_IWUSR,stat.S_IXUSR)
			mode_line += perm_sub_str(perm,stat.S_IRGRP,stat.S_IWGRP,stat.S_IXGRP)
			mode_line += perm_sub_str(perm,stat.S_IROTH,stat.S_IWOTH,stat.S_IXOTH)
			return mode_line

		def format_line(line):
			return " -:- " + line + " -:- "

		full_path = view.file_name()
		if full_path is None:
			_filename = format_line("Unsaved buffer")
		else:
			if os.path.exists(full_path):
				filename = os.path.split(full_path)[1]
				mode_line = perm_str(os.stat(view.file_name()).st_mode)
				_filename = format_line(mode_line + "  " + filename)
			else:
				_filename = format_line("Off-disk WTF buffer")
			view.set_status('_filename', _filename)

class NaviDirCommand(sublime_plugin.WindowCommand):
	content = []
	curent_dir = ""
	current_highlight = ""

	def run(self, running=False, move_up=False):
		def has_read_perm(path):
			return os.stat(path).st_mode & stat.S_IRUSR;

		def format_content(basename):
			path = "%s/%s" % (self.curent_dir,basename)
			cat = ""
			if os.path.isdir(path):
				cat += "/"
			if not has_read_perm(path):
				cat += "(no read permission)";
			return "%s%s" % (basename,cat)

		def on_select(index):
			if index != -1:
				path = "%s/%s" % (self.curent_dir,self.content[index])
				if (self.content[index] == "../"):
					self.curent_dir = os.path.abspath(os.path.join(self.curent_dir, os.pardir))
					display_contents(on_select,on_highlight,True)
				elif os.path.isdir(path):
					self.curent_dir = path
					display_contents(on_select,on_highlight, True)
				else:
					self.window.open_file(path)
					unset_navi_dir_active()
			else:
				unset_navi_dir_active()

		def on_highlight(index):
			if index != -1:
				self.current_highlight = self.content[index]
				path = "%s/%s" % (self.curent_dir,self.current_highlight)
				if not os.path.isdir(path):
					self.window.open_file(path, sublime.TRANSIENT)

		def display_contents(sel, high, timeout=False):
			set_navi_dir_active()
			self.content = [ format_content(x) for x in [".."] + os.listdir(self.curent_dir) if x != ".DS_Store" ]
			if (timeout):
				sublime.set_timeout(lambda:
					self.window.show_quick_panel(self.content, sel, sublime.MONOSPACE_FONT, 0, high))
			else:
				self.window.show_quick_panel(self.content, sel, sublime.MONOSPACE_FONT, 0, high)

		def update_display(path):
			self.window.run_command("hide_overlay")
			self.curent_dir = path
			display_contents(on_select,on_highlight,True)

		def new_dir(dest):
			return os.path.abspath(os.path.join(self.curent_dir, dest))

		if running:
			if move_up:
				update_display(new_dir(os.pardir))
			else:
				path = new_dir(self.current_highlight)
				if os.path.isdir(path):
					update_display(path)
				else:
					self.window.open_file(path)
					unset_navi_dir_active()
					self.window.run_command("hide_overlay")
		else:
			set_navi_dir_active()
			filename = self.window.active_view().file_name()
			if filename is not None and os.path.exists(filename):
				self.curent_dir = os.path.dirname(filename)
			else:
				self.curent_dir = os.path.expanduser("~")
			display_contents(on_select,on_highlight)







