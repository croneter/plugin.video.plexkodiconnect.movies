# -*- coding: utf-8 -*-
###############################################################################
import cPickle

from xbmcgui import Window
from xbmc import log, LOGDEBUG

import utils

###############################################################################
WINDOW = Window(10000)
PREFIX = 'PLEX.MOVIES.%s: ' % __name__
###############################################################################


def pickl_window(property, value=None, clear=False):
    """
    Get or set window property - thread safe! For use with Pickle
    Property and value must be string.

    Returns string.
    """
    if clear:
        WINDOW.clearProperty(property)
    elif value is not None:
        WINDOW.setProperty(property, value)
    else:
        return utils.try_encode(WINDOW.getProperty(property))


def pickle_me(obj, window_var='plex_result'):
    """
    Pickles the obj to the window variable. Use to transfer Python
    objects between different PKC python instances (e.g. if default.py is
    called and you'd want to use the service.py instance)

    obj can be pretty much any Python object. However, classes and
    functions won't work. See the Pickle documentation
    """
    log('%sStart pickling' % PREFIX, level=LOGDEBUG)
    pickl_window(window_var, value=cPickle.dumps(obj))
    log('%sSuccessfully pickled' % PREFIX, level=LOGDEBUG)


def unpickle_me(window_var='plex_result'):
    """
    Unpickles a Python object from the window variable window_var.
    Will then clear the window variable!
    """
    result = pickl_window(window_var)
    pickl_window(window_var, clear=True)
    log('%sStart unpickling' % PREFIX, level=LOGDEBUG)
    obj = cPickle.loads(result)
    log('%sSuccessfully unpickled' % PREFIX, level=LOGDEBUG)
    return obj


class Playback_Successful(object):
    """
    Used to communicate with another PKC Python instance
    """
    listitem = None
