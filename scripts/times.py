#
# NopSCADlib Copyright Chris Palmer 2018
# nop.head@gmail.com
# hydraraptor.blogspot.com
#
# This file is part of NopSCADlib.
#
# NopSCADlib is free software: you can redistribute it and/or modify it under the terms of the
# GNU General Public License as published by the Free Software Foundation, either version 3 of
# the License, or (at your option) any later version.
#
# NopSCADlib is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
# without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with NopSCADlib.
# If not, see <https://www.gnu.org/licenses/>.
#

# show execution times and how they have changed.

import json
import time
from colorama import Fore, init

def read_times(dir = '.'):
    global times, last_times, times_fname
    times_fname = dir + '/times.txt'
    init()
    try:
        with open(times_fname) as json_file:
            times = json.load(json_file)
            last_times = dict(times)
    except:
        times = {}
        last_times = {}

def write_times():
    with open(times_fname, 'w') as outfile:
        json.dump(times, outfile, indent = 4)

def got_time(name):
    return name in last_times

def check_have_time(changed, name):
    if not changed and not got_time(name):
        changed = "no previous time"
    return changed

def add_time(name, start):
    times[name] = round(time.time() - start, 3)

def print_times():
    write_times()
    sorted_times = sorted(times.items(), key=lambda kv: kv[1])
    total = 0
    for entry in sorted_times:
        colour = Fore.WHITE
        key = entry[0]
        new = entry[1]
        delta = 0
        if key in last_times:
            old = last_times[key]
            delta = new - old
            if delta > 0.3:
                colour = Fore.RED
            if delta < -0.3:
                colour = Fore.GREEN
        print(colour + "%5.1f %5.1f %s" % (new, delta, key))
        total += new
    if sorted_times:
        print(Fore.WHITE + "%5.1f" % total)
