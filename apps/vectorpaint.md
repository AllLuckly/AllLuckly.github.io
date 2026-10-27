---
layout: app
app_id: draw_illustration
title: VectorPaint：iPhone 与 iPad 矢量绘图、Logo 设计与 SVG 编辑
description: 了解 VectorPaint 在 iPhone 与 iPad 上的矢量绘图、Logo 设计、SVG 编辑与图片矢量化，从形状和节点教程开始，按用途导出 SVG、PNG 或 PDF。
permalink: /apps/vectorpaint/
modified: 2026-10-27
---

VectorPaint 是用于 **iPhone 和 iPad 矢量绘图与 SVG 编辑**的应用。用钢笔、形状、可编辑路径、图层和文字制作 Logo、图标、插画与海报。商店名称是「VectorPaint-矢量绘图与Logo设计」。

## 适合的创作场景

- **几何图标与 Logo。** 从简单形状开始，通过填充、描边、对齐和分布整理结构。
- **SVG 路径编辑。** 导入已有 SVG，使用贝塞尔节点调整曲线、路径和轮廓。
- **插画与版式。** 用图层和分组管理对象，将渐变、蒙版、文字与图案组合在一起。
- **图片描摹。** 导入图片，检查矢量化预览，再生成可以编辑的路径。
- **准备交付文件。** 按用途导出 SVG、PDF 或 PNG，并保留可编辑的 VectorPaint 原稿。

第一次使用可以先做一个由圆形和矩形组成的小图标：[VectorPaint 入门：用形状制作图标并导出 SVG]({{ '/guides/vectorpaint-getting-started/' | relative_url }})。

## 矢量化与导出并不等同

导入一张照片后直接导出 SVG，照片仍可能作为位图包含在文件中。要得到可编辑路径，需要使用图片矢量化并检查结果。线稿、标志和平涂图通常更适合作为描摹素材；照片会按选择的颜色数进行量化，结果取决于原图。

SVG 和 PDF 也可以同时包含矢量路径与位图元素。交付时应按实际内容说明文件组成，不能仅凭扩展名承诺「全矢量」。PNG 是像素图片，可选择透明背景。

## 在设备上整理作品

绘图与作品管理以本地文件为基础，可以离线进行。可以为作品添加分组、标签与收藏，使用撤销、重做、版本、最近删除和备份功能管理创作过程。用于继续修改的原稿，应与用于分享的成品文件一起保留。

## 用 MCP 把场景计划变成可编辑对象

VectorPaint 的 MCP（Model Context Protocol）接口让 AI 客户端通过绘图工具创建和修改应用原生对象，包括路径、形状、文字、图层和渐变。适合把一段构图说明拆成多个可以继续调整的部分，也适合在已有作品里精确修改对象。

作品 [《午夜兰花》]({{ '/works/vectorpaint-midnight-orchid-mcp/' | relative_url }}) 展示了一次实际创作：六朵兰花围着夜色玻璃温室，背景星月、水面倒影和前景叶片分在 14 个图层中，花瓣与玻璃保留可编辑路径和渐变，并由应用导出 PNG。页面附真实画布视频与分层做法。

入门需要**已启用 MCP 的 VectorPaint 构建**，并且能看到 **设置 → AI 控制**。公开文档提供同一台 Apple 芯片 Mac 上运行 iPad 版本时的本机 HTTP 连接流程，以及 Codex 和 VS Code 配置示例；先开启本机连接，复制个人客户端配置，再按需开启「允许修改作品」。

连接与工具说明见 [VectorPaint MCP 公开源码](https://github.com/AllLuckly/VectorPaint-mcp)和[中文入门文档](https://github.com/AllLuckly/VectorPaint-mcp/blob/main/README.zh-CN.md)。当前 App Store 包是否包含 MCP 入口尚未确认，请先核对实际安装版本。

## 常见问题

### VectorPaint 能做什么？

它适合矢量插画、Logo / 图标设计、SVG 编辑和图形排版。以画笔笔触、水彩和像素图层为主的创作，也可以查看 [Aquarell]({{ '/apps/aquarell/' | relative_url }})。

### 可以导出透明背景 PNG 吗？

可以。导出 PNG 时选择透明背景，并确认画布中没有覆盖整页的实色背景对象。透明背景设置不会自动删除你画出的背景图形。

### 导出 SVG 后所有内容都是矢量吗？

不一定。SVG 可以保留作品中的位图元素，导出不会自动把每张图片都转换成路径。

### 可以离线使用吗？

绘图与本地作品管理可以离线进行。将结果发送到在线服务或从网络获取素材，需要对应的网络连接。

## 版本与来源

2026 年 10 月 27 日核对：中国区 App Store 版本为 **1.0.8**，最低要求 iOS / iPadOS 17.0。本文根据 [VectorPaint 官方商店页面](https://apps.apple.com/cn/app/id1587272880)、[Apple 公共查询接口](https://itunes.apple.com/lookup?id=1587272880&country=cn)与项目功能入口整理，未作真机实测声明。
