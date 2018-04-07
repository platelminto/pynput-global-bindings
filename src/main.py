import sys

import os

from pynput.keyboard import Key, KeyCode, Listener

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

bindings_file = 'bindings.txt'

method_keys_delimiter = '='
key_to_key_delimiter = '+'
multiple_keycodes_delimiter = ','
ignore_after_char = '#'

currently_pressed_keys = list()
looking_for = {}


def on_press(key):
    currently_pressed_keys.append(key)

    for key_tuple, methods in looking_for.items():
        if currently_pressed_keys == list(key_tuple):

            for method in methods:
                if method == 'print1':
                    print('1')
                elif method == 'print2':
                    print('2')
                else:
                    print('binding has no link')

                # Alternatively, set your python method names to be the same, and run:
                # getattr(your_class, method)()

            currently_pressed_keys.pop(-1)


def on_release(key):
    try:
        currently_pressed_keys.remove(key)
    except ValueError:
        pass


def get_key_from_string(key_str):

    try:
        return getattr(Key, key_str)
    except AttributeError:
        return KeyCode.from_char(key_str)


with open(bindings_file) as file:

    for line in file:

        method_and_keycodes = line.split(method_keys_delimiter)

        method = method_and_keycodes[0]
        rest_of_line = method_and_keycodes[1]

        if ignore_after_char in rest_of_line:

            rest_of_line = rest_of_line[:rest_of_line.index(ignore_after_char)]

        bindings = rest_of_line.rstrip()

        if bindings is not '':
            for binding in bindings.split(multiple_keycodes_delimiter):
                keys = list()
                for single_key in binding.split(key_to_key_delimiter):
                    keys.append(get_key_from_string(single_key.strip()))

                keys_tuple = tuple(keys)

                if keys_tuple not in looking_for.keys():
                    looking_for[keys_tuple] = []

                looking_for[keys_tuple].append(method)


with Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()
