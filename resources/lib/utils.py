#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, unicode_literals
import xbmc
import xbmcgui
###############################################################################
WINDOW = xbmcgui.Window(10000)


def try_encode(input_str, encoding='utf-8'):
    """
    Will try to encode input_str (in unicode) to encoding. This possibly
    fails with e.g. Android TV's Python, which does not accept arguments for
    string.encode()
    """
    if isinstance(input_str, str):
        # already encoded
        return input_str
    try:
        input_str = input_str.encode(encoding, "ignore")
    except TypeError:
        input_str = input_str.encode()
    return input_str


def try_decode(string, encoding='utf-8'):
    """
    Will try to decode string (encoded) using encoding. This possibly
    fails with e.g. Android TV's Python, which does not accept arguments for
    string.encode()
    """
    if isinstance(string, unicode):
        # already decoded
        return string
    try:
        string = string.decode(encoding, "ignore")
    except TypeError:
        string = string.decode()
    return string


def window(prop, value=None, clear=False, windowid=10000):
    """
    Get or set window property - thread safe!

    Returns unicode.

    Property and value may be string or unicode
    """
    if windowid != 10000:
        win = xbmcgui.Window(windowid)
    else:
        win = WINDOW

    if clear:
        win.clearProperty(prop)
    elif value is not None:
        win.setProperty(try_encode(prop), try_encode(value))
    else:
        return try_decode(win.getProperty(prop))


def plex_command(value):
    """
    Used to funnel states between different Python instances. NOT really thread
    safe - let's hope the Kodi user can't click fast enough
    """
    while window('plex_command'):
        xbmc.sleep(20)
    window('plex_command', value=value)


def cast(func, value):
    """
    Cast the specified value to the specified type (returned by func). Currently this
    only support int, float, bool. Should be extended if needed.
    Parameters:
        func (func): Calback function to used cast to type (int, bool, float).
        value (any): value to be cast and returned.
    """
    if value is not None:
        if func == bool:
            return bool(int(value))
        elif func == unicode:
            if isinstance(value, (int, long, float)):
                return unicode(value)
            else:
                return value.decode('utf-8')
        elif func == str:
            if isinstance(value, (int, long, float)):
                return str(value)
            else:
                return value.encode('utf-8')
        elif func in (int, float):
            try:
                return func(value)
            except ValueError:
                return float('nan')
        return func(value)
    return value
