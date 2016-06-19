# -*- coding: utf-8 -*-

#################################################################################################

import os
import sys
import urlparse

import xbmc
import xbmcaddon

#################################################################################################

_addon = xbmcaddon.Addon(id='plugin.video.plexkodiconnect')
addon_path = _addon.getAddonInfo('path').decode('utf-8')
base_resource = xbmc.translatePath(os.path.join(addon_path, 'resources', 'lib')).decode('utf-8')
sys.path.append(base_resource)

#################################################################################################

import entrypoint

# Parse parameters
base_url = sys.argv[0]
addon_handle = int(sys.argv[1])
params = urlparse.parse_qs(sys.argv[2][1:])
xbmc.log("PlexKodiConnect Parameter string: %s" % sys.argv[2])

try:
    mode = params['mode'][0]
    itemid = params['id'][0]
    dbid = params['dbid'][0]

except (KeyError, IndexError):
    if "extrafanart" in sys.argv[0]:
        plexpath = sys.argv[2][1:]
        plexid = params.get('id', [""])[0]
        entrypoint.getExtraFanArt(plexid, plexpath)

else:
    if "play" in mode:
        # plugin.video.emby entrypoint
        xbmc.log("mode: %s, itemid: %s, dbid: %s" % (mode, itemid, dbid))
        entrypoint.doPlayback(itemid, dbid)