# -*- coding: utf-8 -*-
# We need this in order to use add-on paths like
# 'plugin://plugin.video.plexkodiconnect.MOVIES' in the Kodi video database
###############################################################################
from __future__ import absolute_import, division, unicode_literals
from logging import getLogger
from sys import argv
import xbmc
import xbmcgui
import xbmcplugin

from resources.lib import pickler, pkc_listitem, utils, loghandler, \
    unicode_paths
###############################################################################
loghandler.config()
LOG = getLogger('PLEX.MOVIES')
###############################################################################

HANDLE = int(argv[1])


def play():
    """
    Start up playback_starter in main Python thread
    """
    LOG.debug('Full sys.argv received: %s', argv)
    request = '%s&handle=%s' % (unicode_paths.decode(argv[2]), HANDLE)
    # Put the request into the 'queue'
    utils.plex_command('PLAY-%s' % request)
    if HANDLE == -1:
        # Handle -1 received, not waiting for main thread
        return
    # Wait for the result
    while not pickler.pickl_window('plex_result'):
        xbmc.sleep(50)
    result = pickler.unpickle_me()
    if result is None:
        LOG.error('Error encountered, aborting')
        xbmcplugin.setResolvedUrl(HANDLE, False, xbmcgui.ListItem())
    elif result.listitem:
        listitem = pkc_listitem.convert_pkc_to_listitem(result.listitem)
        xbmcplugin.setResolvedUrl(HANDLE, True, listitem)


if __name__ == '__main__':
    LOG.info('PKC add-on for movies started')
    play()
    LOG.info('PKC add-on for movies stopped')
