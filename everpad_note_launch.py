#!/usr/bin/env python
#  everpad-note-launch a tool to deploy and socialize Python projects
#   Copyright (C) 2014  Juan Manuel Schillaci
#
#   This program is free software; you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation; either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program; if not, write to the Free Software Foundation,
#   Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301  USA
# Coop version 0.1, Copyright (C) 2013  Juan Manuel Schillaci
#   Coop comes with ABSOLUTELY NO WARRANTY.
#   This is free software, and you are welcome to redistribute it
#   under certain conditions;


import os
from subprocess import Popen, PIPE, STDOUT, call

import dbus
import dbus.mainloop.glib
import gettext
from everpad.basetypes import Note
from everpad.tools import get_provider, resource_filename

path = resource_filename('share/locale/')
gettext.bindtextdomain('everpad', path)
gettext.textdomain('everpad')
dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
provider = get_provider()


SPLIT_CHARACTER = " >>> "

def search_all(search, results):
    for note_struct in provider.find_notes(
        search, dbus.Array([], signature='i'),
        dbus.Array([], signature='i'), 0,
        100, Note.ORDER_TITLE, -1):
        note = Note.from_tuple(note_struct)
        # TODO: Fix so it can return system lang encoding
        tags = ", ".join([tag.title().encode('ascii', errors="replace") for tag in  note.tags])
        results.append(u"%s%s%s%s%s" % (note.id, SPLIT_CHARACTER, tags,
                                        SPLIT_CHARACTER,
                                        note.title.encode('ascii', errors="replace")))

# dmenu constants
DMENU_CACHE = os.path.expanduser('~/.dmenu_cache')
DMENU_COMMAND = [
            'dmenu',
            '-p', 'command:',
            '-sb', '#DD4814',
            '-l', '10',
            '-i',
        ]

# check if local cache exists
if not os.path.exists(DMENU_CACHE):
    os.system('dmenu_path > /dev/null')

# load command cache and combine with our commands
with open(DMENU_CACHE, 'r') as raw_file:
    system_commands = raw_file.read()

output = []

try:
    search_all("", output)
    output.sort(key=lambda note: note.split(SPLIT_CHARACTER)[2].upper())
except Exception, e:
    pass

# create a process
process = Popen(DMENU_COMMAND, stdout=PIPE, stdin=PIPE, stderr=STDOUT)
selection = process.communicate(input='{0}\n{1}'.format('\n'.join(output), system_commands))[0]

# get notes based on selection and open it or create a new one
if selection.strip() != '':
    note_id = selection.split(SPLIT_CHARACTER)[0]
    call(['everpad', '--open', note_id])
