---
layout: app
app_id: icouldplay
title: 云映 iCouldPlay：iPhone 与 iPad 视频播放器、NAS 与个人媒体库
description: 了解云映的本地视频、SMB、WebDAV、FTP、媒体服务器、字幕和双引擎播放功能，从 40 篇中文教程中选择自己的使用路线。
permalink: /apps/icouldplay/
modified: 2026-10-27
---

云映的英文名是 **iCouldPlay**。它用来播放和整理自己已有的视频：文件可以保存在手机、相册、NAS，也可以由 Emby、Jellyfin、Plex 或绿联云视频提供。先接好内容来源，再整理海报和字幕，会比一开始就扫描整个硬盘更容易排查问题。

## 从哪一种内容开始

- **手机里的一段视频**：先验证导入、画面方向、声音和续播，熟悉最基本的流程。
- **NAS 中的文件夹**：按服务器实际提供的协议选择 SMB、WebDAV 或 FTP，确认目录可见后再播放一个小文件。
- **已经整理好的媒体服务器**：连接自己的 Emby、Jellyfin、Plex 或绿联云视频，核对账户能访问哪些媒体库。

这些入口需要的视频和服务器由你自己准备。云映的媒体库是在整理这些内容，并不附带影视资源。

## 媒体库和播放器分别解决什么问题

文件名、年份和剧集编号影响媒体信息匹配；匹配到一张海报，只能说明资料找到了，不能据此判断视频已经下载或可以离线播放。播放时还要看文件能否访问、编码是否适合当前引擎，以及所选音轨和字幕是否与这个版本对应。

教程把这些工作分开：先读[本地视频入门]({{ '/guides/icouldplay-getting-started/' | relative_url }})，有 NAS 的可以继续看 [SMB 连接]({{ '/guides/icouldplay-smb-nas/' | relative_url }})；画面正常之后，再处理[外挂字幕]({{ '/guides/icouldplay-external-subtitles/' | relative_url }})。

## 遇到卡顿或黑屏，先留下对照

保留同一份视频，分别观察本地播放与远程播放的结果。只有远程路径出问题时，检查服务器与网络；本地也失败时，再核对文件和播放引擎。每次只改变一个条件，保留原文件和服务器设置记录，便于判断哪一步起了作用。

[40 篇完整教程]({{ '/guides/icouldplay/' | relative_url }})从导入、建库一直写到字幕与兼容排查，可以直接按手头的问题查找。

## 版本与来源

2026 年 10 月 27 日核对，中国区公开版本为 **1.1.0**，最低要求 iOS / iPadOS 13.0。资料依据[云映官方 App Store 页面](https://apps.apple.com/cn/app/id6755653178)、[Apple 版本查询](https://itunes.apple.com/lookup?id=6755653178&country=cn)及对应功能入口整理。不同文件与服务器的实际表现仍需在自己的设备上检查。
