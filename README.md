## Directory Navigation for Sublime Text
Sublime Text go-to-everything is a very handy tool, but sometimes falls
short when looking for files outside the workspace directory. This plugin
supplies that functionality by using the quick panel.

***

### Note
* First commit, not thoroughly debugged yet
* Tested only on OS X with Sublime Text Version 3

***

### Installation
Clone this repository in Packages directory

***
### Usage

Default launch keybinding (ctrl+x, ctrl+f) opens a quick pannel overlay with a listing of the contents the foreground buffer's directory

* If the buffer in foreground hasn't been saved yet or can not be saved
because it is being previewed from an archive, the list shows contents of
home directory
* List can be narrowed and navigated using native fuzzy-matching from Sublime Text
* A preivew of the highlited item is shown if it is a file with read permission
* At any moment, to move up one directory, use key binding (ctrl+l)
* Once an item has been highlighted, possible actions are
	* To open a file, hit enter
	* To enter directories hit either tab or enter. The directory listing will be refreshed with the contents
* The current file's name is shown in the status bar with the linux acess permissions

***
### To Do
* Add option to disable preview while navigating directory listing
* Add option to disable showing filename in status bar