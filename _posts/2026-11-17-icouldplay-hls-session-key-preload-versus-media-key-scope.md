---
layout: guide
author: Bison
app_id: icouldplay
title: 云映 HLS 密钥标签跟读：会话预加载不替代分片作用域
description: 对读SESSION-KEY与KEY的两份纯文本样本，核相同URI属性、重复组合与METHOD=NONE边界。
permalink: /guides/icouldplay-hls-session-key-preload-versus-media-key-scope/
date: '2026-11-17 00:00:00 +08:00'
modified: '2026-11-17 00:00:00 +08:00'
category: 教程
level: 进阶
series_order: 190
topic: 事件、候选与声明证据
reading_time: 10
---

主清单提前列出密钥资料，不等于它已经替媒体清单指定每个分片的加密状态。本课只阅读原创占位样本，对照SESSION-KEY的预加载用途与KEY的后续作用区间。任务不取得密钥、不下载加密载荷、不执行解密，也不据一个标签承诺云映兼容所有保护系统。

## 两份文本与真实凭据明确分开

在外部建master.m3u8与media/main.m3u8两份阅读文件，原样保存，另记角色和基址。例中example.com只作保留教学域名，所有URI都没有提供实际密钥或媒体，当前不要向它请求资源。自有真实来源若需记录，只写内容身份、标签状态与取得时间，私人令牌和密钥字节不放进公开笔记。本文不要求另建加密服务器，纯文本即可完成作用域账本；播放观察只有自己本来能正常访问的来源才按实际记录，未做的步骤明确未执行。

## 主清单只声明可提前加载的资料

主样本SESSION-KEY列AES-128、一个占位URI、IV及显式identity格式与版本字符串1；末尾变体才引用媒体清单。RFC说明这种会话级标签允许客户端在读媒体清单之前预加载密钥，不表示客户端必然发出请求，也不属于某一指定媒体清单。它是可选标签，不能因有它就认为后续所有分片都已受相同方式保护。CODECS与带宽同样是假定声明，未附载荷。先把主标签放进“可预加载资料”栏，不直接抄进每个分片的当前KEY状态。

```text
#EXTM3U
#EXT-X-VERSION:5
#EXT-X-SESSION-KEY:METHOD=AES-128,URI="https://example.com/hls/keys/key-a.bin",IV=0x0000000000000000000000000000002a,KEYFORMAT="identity",KEYFORMATVERSIONS="1"
#EXT-X-STREAM-INF:BANDWIDTH=1000000,CODECS="avc1.4d401e,mp4a.40.2"
media/main.m3u8
```

## 媒体清单逐段读取KEY到下一KEY

媒体样本首条KEY为AES-128，适用于之后seg42.ts；接着KEY的METHOD=NONE使同一identity格式范围内seg43.ts声明未加密。本例只有这一种KEYFORMAT，不把此简化推广成同时有多个格式时的所有清除行为。两段各四秒，总声明八秒，序号42不是四十二秒。KEY还可作用于其间声明的初始化段，本例没有MAP，不凭空加初始化文件。逐行列当前方法、URI和分片，不因SESSION-KEY仍在主清单就把第二段也记作AES-128；占位文字不证明实际字节真的按这些状态制作。

```text
#EXTM3U
#EXT-X-VERSION:5
#EXT-X-TARGETDURATION:4
#EXT-X-MEDIA-SEQUENCE:42
#EXT-X-KEY:METHOD=AES-128,URI="https://example.com/hls/keys/key-a.bin",IV=0x0000000000000000000000000000002a,KEYFORMAT="identity",KEYFORMATVERSIONS="1"
#EXTINF:4,
seg42.ts
#EXT-X-KEY:METHOD=NONE
#EXTINF:4,
seg43.ts
#EXT-X-ENDLIST
```

## 相同URI核方法与格式版本而非只看文件名

两份样本把占位密钥URI完整写成相同绝对值，避免相对基址差异掩盖本题属性条件。对于相同URI的SESSION-KEY与KEY，METHOD、KEYFORMAT和KEYFORMATVERSIONS必须匹配，本例分别是AES-128、identity与带引号的1。IV也在样本中相同，但这条匹配要求列的是前三项，不能擅自扩成所有属性永远必须逐字相同。记录原值与归属，不因文件名叫key-a.bin就认定响应是合法密钥。实际字节未取得继续留未知，URI是地址，不是密钥内容本身。

## IV只读长度与数值不当作密钥

本例IV在0x后有三十二位十六进制，表示十六字节的初始向量；末尾2a换算十进制42，只是与首段序号相同的原创建议值。已经显式给IV时按该属性读，不能再说所有情况都必须由序号自动生成。IV不是密钥字节，也不是时长、帧率或文件散列，写出它不代表能解密任何资源。当前不进行AES运算或校验真实加密文件，纸面只核格式长度和作用区间。若读者无实际密钥，任务仍可完成文本检查，不要求寻找或猜测缺失内容。

## 用删除预加载标签的副本保持媒体状态

复制主清单只删SESSION-KEY，媒体清单保持不变，再逐行重算seg42和seg43的方法，仍分别是AES-128与NONE。改变的是提前提供资料的机会，不是把首段解密或取消加密。反过来只留主标签却删媒体KEY，不可据预加载标签补造分片作用域；对当前样本这会改变媒体声明，需要重新审核。该对照只在自己的纯文本副本，不试改生产来源绕过访问。云映若对自己来源原本可播，也不能从删除标签的纸面结果推断网络请求次数或播放启动必然更快。

## 审核NONE禁用与重复会话组合

SESSION-KEY的METHOD不得为NONE；媒体KEY可以写METHOD=NONE，但该行不得再带URI、IV等其他属性。另复制主会话行原样重复，会造成METHOD、URI、IV、KEYFORMAT、KEYFORMATVERSIONS五项全相同的重复组合，主清单不允许。先在文本审核发现这些问题，不等待某种固定播放器错误。实际来源失败仍要分清清单、授权资源和解码范围，正常的一条路径不能为其他方法或保护系统背书。故障副本保留唯一改动，修字段不称为成功取得密钥或完成授权。

## 重开交付角色表与不执行范围

重开两份正确文本，确认主会话行一条、媒体KEY两条、两段方法与八秒声明总量，再核三匹配属性和五项去重组合。已有自有来源的播放观察可另附当前入口、实际可见信息与结果，未观察则明确未执行，不把应用无专门密钥界面写成失败。交付原稿、删除对照和故障副本，说明没有请求占位地址、记录密钥字节或执行下载解密。最终成果是能说明预加载与媒体作用域为何不同，不承诺任何DRM、所有加密路径或设备已完成兼容验收。

## 相关教程与资料

[云映 HLS 会话资料核对：数据标识、语言与外部JSON分别记录]({{ '/guides/icouldplay-hls-session-data-id-language-value-uri-record/' | relative_url }})、[云映 HLS 兼容版本核对：按标签组合分别计算最低要求]({{ '/guides/icouldplay-hls-rfc8216-minimum-version-feature-ledger/' | relative_url }})。

方法来源：[RFC8216 §4.3.4.5](https://www.rfc-editor.org/rfc/rfc8216#section-4.3.4.5)、[RFC8216 §4.3.2.4](https://www.rfc-editor.org/rfc/rfc8216#section-4.3.2.4)、[RFC8216 §5.2](https://www.rfc-editor.org/rfc/rfc8216#section-5.2)。

资料核对：2026年11月17日，[云映官方商店](https://apps.apple.com/cn/app/id6755653178)与[Apple公开查询](https://itunes.apple.com/lookup?id=6755653178&country=cn&entity=software&timestamp=20261117-hls)列出1.1.1，最低iOS / iPadOS 15.0。文本与演算在外部手工准备，云映用于自己的已有真实来源选择和播放观察，入口按安装版本实际可见为准。占位地址不提供媒体或密钥。文法审核、假定算例、真实字节资料和观看分别记录，没有执行的步骤明确未执行；未声称完成真机、私人服务器、所有引擎或输出设备逐项兼容测试。
