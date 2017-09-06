#!/usr/bin/env python

# Copyright (C) 2017 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


from __future__ import print_function

import argparse
import os.path
import json

import google.oauth2.credentials

from google.assistant.library import Assistant
from google.assistant.library.event import EventType
from google.assistant.library.file_helpers import existing_file

from blinkt import set_clear_on_exit, set_pixel, show, set_brightness, set_all
import colorsys
import time
import random
import threading

try:
    import numpy as np
except ImportError:
    exit("This script requires the numpy module\nInstall with: sudo pip install numpy")

global talking

# These are the colors I defined to randomly flash during talking
colors = [[247, 90, 0],[2, 103, 193],[242, 35, 31],[255, 211, 38],[51, 173, 38]]

# Lights pulse on when hotword is detected
def pulse():
    clear()
    set_brightness(0.05)
    set_pixel(3, 2, 103, 193)
    set_pixel(4, 2, 103, 193)
    show()
    time.sleep(0.05)
    set_pixel(3, 2, 103, 193)
    set_pixel(4, 2, 103, 193)
    set_pixel(2, 2, 103, 193)
    set_pixel(5, 2, 103, 193)
    show()
    time.sleep(0.05)
    set_pixel(3, 2, 103, 193)
    set_pixel(4, 2, 103, 193)
    set_pixel(2, 2, 103, 193)
    set_pixel(5, 2, 103, 193)
    set_pixel(1, 2, 103, 193)
    set_pixel(6, 2, 103, 193)
    show()
    time.sleep(0.05)
    set_pixel(3, 2, 103, 193)
    set_pixel(4, 2, 103, 193)
    set_pixel(2, 2, 103, 193)
    set_pixel(5, 2, 103, 193)
    set_pixel(1, 2, 103, 193)
    set_pixel(6, 2, 103, 193)
    set_pixel(0, 2, 103, 193)
    set_pixel(7, 2, 103, 193)
    show()

# Random light flashes in predefined colors while the assistant talks
def talk():
    set_brightness(0.05)

    while True:
        for i in range(8):
            color = random.choice(colors)
            set_pixel(i, color[0], color[1], color[2])
        show()
        time.sleep(0.1)
        if talking == 0:
        	clear()
        	break

# Clear Blinkt LEDs
def clear():
    set_all(0,0,0)
    show()

# Process assistant events
def process_event(event):
    global talking

    print(event)
    if event.type == EventType.ON_CONVERSATION_TURN_STARTED:
        print()
        flashing_thread = threading.Thread(target=pulse)
        flashing_thread.start()

    if event.type == EventType.ON_CONVERSATION_TURN_FINISHED:
        talking = 0
        clear()

    if event.type == EventType.ON_START_FINISHED:
        set_brightness(0.05)
        set_pixel(0, 2, 103, 193)
        show()
        time.sleep(0.05)
        set_pixel(1, 2, 103, 193)
        show()
        time.sleep(0.05)
        set_pixel(2, 2, 103, 193)
        show()
        time.sleep(0.05)
        set_pixel(3, 2, 103, 193)
        show()
        time.sleep(0.05)
        set_pixel(4, 2, 103, 193)
        show()
        time.sleep(0.05)
        set_pixel(5, 2, 103, 193)
        show()
        time.sleep(0.05)
        set_pixel(6, 2, 103, 193)
        show()
        time.sleep(0.05)
        set_pixel(7, 2, 103, 193)
        show()
        clear()

    if event.type == EventType.ON_RESPONDING_STARTED:
        talking = 1
        flashing_thread = threading.Thread(target=talk)
        flashing_thread.start()

    if (event.type == EventType.ON_CONVERSATION_TURN_FINISHED and
            event.args and not event.args['with_follow_on_turn']):
        print()

def main():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('--credentials', type=existing_file,
                        metavar='OAUTH2_CREDENTIALS_FILE',
                        default=os.path.join(
                            os.path.expanduser('~/.config'),
                            'google-oauthlib-tool',
                            'credentials.json'
                        ),
                        help='Path to store and read OAuth2 credentials')
    args = parser.parse_args()
    with open(args.credentials, 'r') as f:
        credentials = google.oauth2.credentials.Credentials(token=None,
                                                            **json.load(f))

    with Assistant(credentials) as assistant:
        for event in assistant.start():
            process_event(event)


if __name__ == '__main__':
    main()
