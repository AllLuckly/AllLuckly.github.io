---
layout: app
app_id: pastel
title: Aquarell：iPhone 与 iPad 水彩绘画、插画与手绘画板
description: 了解 Aquarell 的笔刷、图层、色板与导出能力，观看 MCP 绘制 19 层《云山晚渡》的实录，并查看已启用 MCP 构建的 AI 连接说明。
permalink: /apps/aquarell/
modified: '2026-10-26'
---

Aquarell 是一款用于 **iPhone 和 iPad 水彩绘画、插画与手绘创作**的应用。它将笔刷、图层、色板和自定义画布放在一起，适合随手记录灵感，也适合把草图逐步画成完整作品。商店中的产品名称是「Aquarell 水彩绘画与手绘画板」。

## 可以用它做什么

- **画一幅分层插画。** 把草图、颜色和细节放在独立图层，调整不透明度与混合模式，方便分别修改。
- **练习笔触。** 调整笔刷大小、不透明度与间距，比较线稿、涂色和叠色的表现。
- **整理配色。** 选择颜色、保存色板，或从画布取色，把一组颜色用于同一张作品。
- **组合手绘与文字。** 添加文字、导入字体，为插画补充标题或说明。
- **分享和继续编辑。** 导出 PNG、JPEG、PDF、TIFF 或带像素图层的 PSD，也可保留原生作品。

## 从一张小练习开始

建议先用三层完成一张植物或静物练习：第一层画草图，第二层上色，第三层补细节。这样可以熟悉图层与导出流程，不必一开始就调整所有笔刷参数。

[阅读 Aquarell 入门：创建画布、分层绘画与导出 PNG]({{ '/guides/aquarell-getting-started/' | relative_url }})。

## 选择合适的保存方式

PNG 和 JPEG 适合在博客、社交平台或聊天中分享。需要保留可编辑内容时，应同时保存 Aquarell 原生作品。PSD 导出保留像素图层，但不能把它等同于原生文档：可编辑文字和图层分组仍应在原生作品中保留。

Aquarell 适合以笔触和像素图层为中心的绘画；如果目标是编辑 SVG 路径或制作可缩放的 Logo，可以查看 [VectorPaint]({{ '/apps/vectorpaint/' | relative_url }})。

## 通过 MCP 分层绘画

Aquarell MCP（Model Context Protocol，模型上下文协议）让 AI 客户端读取画布与画笔信息，并调用原生画笔、图层、选区、文字、保存与导出能力。笔画在应用中实际渲染，绘画内容保留在像素图层里，适合把构图说明拆成逐层铺染与细节调整。

作品[《云山晚渡》]({{ '/works/aquarell-cloud-mountains-evening-ferry-mcp/' | relative_url }})展示了从淡墨远山到近岸老松、江亭和小舟的一次实际创作。原稿为 1600 × 1100 px、19 层，题款保留原生文字，页面附完整应用界面教程与分层做法。

入门需要能运行 iPad 应用的 **Apple 芯片 Mac、已启用 MCP 的 Aquarell 构建、Python 3.9+ 和支持本地 stdio MCP 的客户端**。先按[Aquarell MCP 中文安装说明](https://github.com/SoBison/Aquarell-mcp/blob/main/README.zh-CN.md)安装桥接并生成个人配置，再在**画廊文件夹菜单或画布图层工具菜单 → AI 控制（MCP）**中检查连接与创作权限。

[Aquarell MCP 集成源码与文档](https://github.com/SoBison/Aquarell-mcp)已公开；当前按预览交付说明，尚未用 App Store / TestFlight 发行包完成验收。请先核对实际构建是否包含 MCP 入口。

## 常见问题

### 可以导出 PSD 吗？

可以导出带像素图层的 PSD。不要将这一能力理解为全部文字、图层分组或其他编辑属性都能在其他应用中无损继续编辑。

### 可以在 iPhone 上画画吗？

可以。Aquarell 面向 iPhone 与 iPad，当前核对的商店版本 1.0.5 最低要求 iOS / iPadOS 15.0。具体兼容情况以下载页面为准。

### 这里的教程是实际操作评测吗？

本页与入门教程根据公开版本说明及项目功能入口整理，没有将代码核对写成真机实测。界面布局可能随设备与后续版本调整。

## 版本与来源

2026 年 10 月 22 日核对：中国区 App Store 版本为 **1.0.5**。功能介绍来自 [Aquarell 官方商店页面](https://apps.apple.com/cn/app/id1591340577)，版本与系统要求通过 [Apple 公共查询接口](https://itunes.apple.com/lookup?id=1591340577&country=cn)核对。
