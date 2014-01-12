everpad-note-launch
===================

Simple command that interacts via DBUS with everpad and provides a list of notes for dmenu

Requirements:
-------------

- An up-to-date version of dmenu (at least 4.5) installed on your system if you are using it on Ubuntu 12.04 you can get the apt package from the i3 `repository <http://i3wm.org/docs/repositories.html>`_

- You need to have `everpad <https://github.com/nvbn/everpad>`_ installed and linked to your evernote account.


Installing it:
--------------
Just put thr everpad_note_launch.py file anywhere on your path, you will need a keybinding to launch it or you could just simple call it from the command line like this:

  ::

    ./everpad_note_launch.py

If you are using i3 you should add the following line to your ~/.i3/config file

  ::

    bindsym $mod+d exec ~/.i3/everpad_note_launch.py


Just replace $mod+d with whatever shortcut you feel comfortable with and of coourse put the right path for everpad_note_launch.py


On launch a list of all of your notes will be displayed, hit enter and everpad will open the note for you.

Enjoy!































