---
layout: app
app_id: man_yue
title: 'ManYue: local comics, offline reading and NAS libraries'
description: Learn about ManYue comic imports, offline reading, WebDAV, SMB and personal comic servers, then choose a tutorial
  for your library.
permalink: /en/apps/manyue/
modified: 2026-10-23
lang: en
source_url: /apps/manyue/
---

ManYue is a **comic reader and personal library app for iPhone and iPad**. Read imported files, add your own sources or connect a NAS or comic server. Its English App Store title is “ManYue: Manga & Comic Reader”; it is called 漫阅+ in Chinese.

**You add the comic files and sources yourself.** ManYue supplies reading and organisation tools. Available content depends on your files, sources and servers.

## Start where your comics are

| Where your content lives | A suitable starting point |
| --- | --- |
| The Files app on iPhone or iPad | Import CBZ, CBR, CB7, ZIP, RAR, 7z, PDF or another supported comic file |
| Already imported or downloaded to the device | Read from the local library while offline |
| A personal NAS or cloud drive | Connect through WebDAV or SMB |
| Your own comic server | Connect Suwayomi / Tachidesk, Komga, Kavita, LANraragi or another supported service |
| A source you have chosen | Import a JS / .ManYue source file or add a source URL |

For a first test, use one local file you own or are authorised to read: [import a local comic and check offline reading]({{ '/en/guides/manyue-getting-started/' | relative_url }}).

## Reading and organisation

ManYue offers single- and double-page layouts, portrait and landscape reading, image zoom and light or dark themes. Shelf groups, reading history, bookmarks and a to-read list help organise a collection and return to your place.

Reading history, favourites and app settings can sync through iCloud or WebDAV. This does not mean every comic file is copied to the other device. For offline reading, confirm that the content has been imported or downloaded on the device you will use.

## NAS, servers and membership

The store description lists iCloud / WebDAV sync, cloud-storage import and SMB among Pro benefits. Server libraries, image enhancement and batch operations are listed among Ultra benefits. Check the current in-app purchase screen and your regional store for benefits and pricing.

OPDS-PSE supports reading page by page. A regular OPDS entry that supplies only a whole-file download does not provide that same experience. Before connecting, check the interface your server actually exposes rather than treating all OPDS support as identical.

## Common questions

### Does ManYue include comics?

No. You add comic files, sources or a personal server. Content and availability vary by source.

### Can I read offline?

Yes, for content already imported or downloaded to the device. An item appearing in a remote catalogue is not proof that its file is saved locally.

### Can it read CBZ, CBR and PDF?

The public description lists these formats, as well as CB7, ZIP, RAR and 7z. The compression method, file integrity and contents still matter; this is not a guarantee for every encrypted or unusual archive.

### Can it connect to Komga or Kavita?

Yes. Public information lists Komga, Kavita, Suwayomi / Tachidesk, LANraragi and OPDS / Ubooquity libraries. You need an accessible server and the relevant account. Some capabilities require Ultra.

## Version and sources

Checked on 22 October 2026: the China App Store listed **2.0.2**, requiring iOS or iPadOS 15.0 or later. This introduction uses the [ManYue App Store page](https://apps.apple.com/cn/app/id6753895889), [Apple’s public lookup API](https://itunes.apple.com/lookup?id=6753895889&country=cn) and feature entry points. It does not claim physical-device testing.
