# -*- coding: utf-8 -*-
import sys
import requests
import xbmcplugin
import xbmc
from xbmcgui import ListItem
from xbmcaddon import Addon

addon_handle = int(sys.argv[1])
my_addon = Addon('plugin.audio.ilovemusic')
xbmcplugin.setContent(addon_handle, 'albums')

if __name__ == "__main__":
    station_list_response = requests.get('https://api.ilovemusic.team/traffic/')
    
    # Ensure the response was successful
    if station_list_response.status_code == 200:
        station_list = station_list_response.json().get('channels')
        player = xbmc.Player()
        # Stop any existing playback before adding new items
        player.stop()

        for station in station_list:
            item = ListItem(station.get('name'))
            item.setInfo('music', {'title': station.get('name'), 'artist': station.get('artist')})
            item.setArt({
                'thumb': my_addon.getAddonInfo('icon'),
                'fanart': my_addon.getAddonInfo('fanart')
            })
            item.setProperty('isPlayable', 'true')
            xbmcplugin.addDirectoryItem(addon_handle, station['stream_url'], item, False)
        
        xbmcplugin.addSortMethod(addon_handle, 1)
        xbmcplugin.endOfDirectory(addon_handle)
    else:
        xbmcgui.Dialog().ok('Error', 'Failed to fetch station list. Status code: {}'.format(station_list_response.status_code))
