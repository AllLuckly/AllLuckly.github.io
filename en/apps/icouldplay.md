---
layout: app
app_id: icouldplay
title: 'iCouldPlay: Video Player for iPhone and iPad'
description: Learn about iCouldPlay local videos, SMB, WebDAV, FTP, media servers, subtitles and playback engines through
  40 practical tutorials.
permalink: /en/apps/icouldplay/
modified: 2026-10-27
lang: en
source_url: /apps/icouldplay/
---

iCouldPlay, called 云映 in Chinese, plays and organises videos you already have. Files may live on your phone, in Photos or on a NAS, or be served by Emby, Jellyfin, Plex or UGREEN. Connect a source before organising posters and subtitles; a small working example is easier to troubleshoot than a scan of an entire drive.

## Choose your first source

- **A video on your phone:** check import, picture orientation, sound and resume playback to learn the basic flow.
- **A NAS folder:** choose SMB, WebDAV or FTP to match the server. Once the folder is visible, play one small file.
- **An existing media server:** connect your Emby, Jellyfin, Plex or UGREEN service and check which libraries the account can access.

You supply the videos and servers for these sources. The media library organises your content; it does not come with films or series.

## The library and the player do different jobs

Filenames, years and episode numbers affect metadata matching. Finding a poster means metadata was found; it does not establish that the video is downloaded or playable offline. Playback also depends on file access, the codec and current engine, and whether the selected audio track or subtitles match this edition.

The tutorials address these tasks separately. Begin with [a local video]({{ '/en/guides/icouldplay-getting-started/' | relative_url }}), then try an [SMB connection]({{ '/en/guides/icouldplay-smb-nas/' | relative_url }}) if you have a NAS. Once picture and sound work, add [external subtitles]({{ '/en/guides/icouldplay-external-subtitles/' | relative_url }}).

## Keep a comparison for stutters or a black screen

Use the same video to compare local and remote playback. If only the remote path fails, inspect the server and network. If local playback fails too, check the file and engine next. Change one condition at a time, keeping the original file and a record of server settings so you can see what helped.

The [40-tutorial learning path]({{ '/en/guides/icouldplay/' | relative_url }}) runs from importing and library setup to subtitles and compatibility checks. You can also choose the article that matches your current problem.

## Version and sources

Checked on 27 October 2026: the China App Store listed **1.1.0**, requiring iOS or iPadOS 13.0 or later. This introduction uses the [iCouldPlay App Store page](https://apps.apple.com/cn/app/id6755653178), [Apple’s lookup API](https://itunes.apple.com/lookup?id=6755653178&country=cn) and feature entry points. Check your own files and servers on your device to confirm their behaviour.
