---
layout: guide
author: Bison
app_id: icouldplay
title: 云映 HLS 兼容版本核对：按标签组合分别计算最低要求
description: 用五份独立清单审核RFC8216的3、4、5、6、7要求，不把VERSION当应用版本或当前协议最新版。
permalink: /guides/icouldplay-hls-rfc8216-minimum-version-feature-ledger/
date: '2026-11-16 00:00:00 +08:00'
modified: '2026-11-16 00:00:00 +08:00'
category: 教程
level: 进阶
series_order: 178
topic: 清单声明与播放条件
reading_time: 10
---

写上较大的VERSION，不会让缺失资源自动齐全；把数字调小，也不会让格式变简单。本课以RFC8216第七节为明确范围，用五份独立阅读样本建立最低兼容要求账本。它不是当前HLS全部扩展功能清单，也不依据版本数字承诺云映每条路径都能解码。

## 先确定规范范围与五个独立文件

外部新建甲至戊五份文本卡，每份从自己的EXTM3U开始，不能把五个VERSION连续塞进一份文件。账本列清单角色、用到的特性、各自要求与最终声明，不把应用1.1.1写成HLS兼容级别。RFC8216于二零一七年发布，本轮只核其中列出的规则，数字七不代表今天所有HLS规范都到此为止。五卡没有实际媒体，文件名仅作结构标记；真来源还需要核字节、资源引用与客户端能力，不能凭文本完整把播放栏提前写通过。

## 甲以小数时长核最低三

甲为带结束标记的单片媒体清单，EXTINF写四点五秒，因此按本规范至少声明三。TARGETDURATION为五，和四点五的取整上限相容，但五不是版本要求的来源。把这两种数字分栏，不因目标时长较大就自动把VERSION也写五。若故障副本仅把声明改二而仍留小数特性，要求没有随之消失；修复应依据实际内容与规范，不教修改数字绕过不支持的客户端。当前片名没有媒体字节，正确最低值也不证明文件真的四点五秒或已能播放。

```text
#EXTM3U
#EXT-X-VERSION:3
#EXT-X-TARGETDURATION:5
#EXTINF:4.5,
float-a.ts
#EXT-X-ENDLIST
```

## 乙用字节范围核最低四

乙有两条四秒项，分别取同一资源的零起一千字节与一千起一千字节，使用BYTERANGE要求至少四。两范围分别覆盖零至九百九十九、一千至一千九百九十九，邻接不重叠；此算式是字节位置，不是帧数或时长。先按特性把最低四记进版本栏，再独立核两条时长共八秒。若把完整资源文件名重写两遍而删掉BYTERANGE，就改变了分片引用范围，不是单纯版本降级；本课保留原样本，不以改后缀或减数字代替媒体结构检查。

```text
#EXTM3U
#EXT-X-VERSION:4
#EXT-X-TARGETDURATION:4
#EXTINF:4,
#EXT-X-BYTERANGE:1000@0
media.ts
#EXTINF:4,
#EXT-X-BYTERANGE:1000@1000
media.ts
#EXT-X-ENDLIST
```

## 丙组合关键帧清单与MAP核五

丙声明I-FRAMES-ONLY并引用初始化资源MAP。前者至少四，MAP在这一组合下至少五，最终取这些必要要求中的较高值五。不能把四加五写九，因为版本门槛不是资源数量相加。初始化文件与关键帧分片仍未提供，不从扩展名推断已满足真实容器结构；本课只核标签组合。关键帧间隔四秒也不意味着给出了四秒连续动作，说明这种样本性质有助于把版本核对和实际观看内容保持分开。若误删关键帧标签，接下来的MAP条件也要重新计算。

```text
#EXTM3U
#EXT-X-VERSION:5
#EXT-X-TARGETDURATION:4
#EXT-X-I-FRAMES-ONLY
#EXT-X-MAP:URI="iframe-init.mp4"
#EXTINF:4,
iframe-a.m4s
#EXT-X-ENDLIST
```

## 丁没有关键帧标记时MAP需六

丁也带MAP，但没有I-FRAMES-ONLY，因此按第七节需至少六。先圈这个否定条件，再和丙比较，不把二者都机械归为MAP等于五。MAP指初始化资料，不给它另加EXTINF当作有时长的影片段；真正媒体项才有下面的四秒。将丙的版本五复制给丁是本课要找的错误，单看文件都叫mp4或m4s不能修复。实际格式还可能涉及规范其他要求，五张卡只是选定条件的例子，不等于已经审计所有输出格式或全部标签。

```text
#EXTM3U
#EXT-X-VERSION:6
#EXT-X-TARGETDURATION:4
#EXT-X-MAP:URI="init.mp4"
#EXTINF:4,
fragment-a.m4s
#EXT-X-ENDLIST
```

## 戊的SERVICE编号要求主清单七

戊改为主清单，闭合字幕条目的INSTREAM-ID采用SERVICE3，按本规范需至少七。这里的三是CEA708服务块编号，不能当视频第三片；最低七也不是因为一份主清单天然都要求七。该条目不带URI，字幕资料应在相应媒体中，主清单声明本身不会写入字幕字节。若改成CC1，不能只沿用本节推论断言所有其他条件也降到一，仍须重新查整份主清单和引用资源。代码只为这一兼容条件提供明确例子，不宣称视频含有真实可读的SERVICE3数据。

```text
#EXTM3U
#EXT-X-VERSION:7
#EXT-X-MEDIA:TYPE=CLOSED-CAPTIONS,GROUP-ID="cc-service",NAME="Service three",DEFAULT=NO,AUTOSELECT=NO,INSTREAM-ID="SERVICE3"
#EXT-X-STREAM-INF:BANDWIDTH=900000,CODECS="avc1.4d401e,mp4a.40.2",CLOSED-CAPTIONS="cc-service"
video.m3u8
```

## 在真实来源中核声明与观察两层

对自己的实际清单先确定角色，再逐项列所用条件并取满足它们的最低门槛。更高声明不代表更高画质，客户端若不支持声明版本，RFC要求不尝试播放；本课不把降低标签当通用绕过方案。云映实际能用的路径可另观察启动、顺播和结尾，没有诊断入口就不编造引擎支持版本表。正确版本、资源可取得和媒体可解码分别留结果，任一未知都不由另一项通过代填。失败稿保留原文，不同时转码、改URI和改版本后失去原因线索。

## 重开用三四五六七逐卡验收

重开五份文件，逐卡复述甲小数三、乙范围四、丙MAP加关键帧五、丁无关键帧的MAP六、戊SERVICE主清单七。核每卡只含一个VERSION，主清单不混媒体清单标签，文件间的例子没有被拼成一个错误列表。交付角色、特性、最低值和真实播放或未执行说明，不标成当前协议全部版本大全。以后增加KEYFORMAT等属性或其他扩展，重新查其明确依据，不能只在旧表多抄一个数字。版本声明不是转码、资源补齐或安装应用更新，这些动作各自需要证据。

## 相关教程与资料

[云映 HLS 初始化清单：分开 EXT-X-MAP 与有时长的媒体分片]({{ '/guides/icouldplay-hls-map-initialization-media-segment-ledger/' | relative_url }})、[云映 HLS 关键帧清单跟读：一帧条目不等于四秒连续动作]({{ '/guides/icouldplay-hls-iframe-only-interval-preview-boundary/' | relative_url }})。

方法来源：[RFC8216 §7](https://www.rfc-editor.org/rfc/rfc8216#section-7)、[RFC8216 §4.3.1.2](https://www.rfc-editor.org/rfc/rfc8216#section-4.3.1.2)。

资料核对：2026年11月16日，[云映官方商店](https://apps.apple.com/cn/app/id6755653178)和[Apple公开查询](https://itunes.apple.com/lookup?id=6755653178&country=cn&entity=software&timestamp=20261116)列出1.1.1，最低iOS / iPadOS 15.0。样本在外部用纯文本手工准备，云映用于已有真实来源的选择与播放观察，入口以安装版本实际可见为准。占位URI不提供媒体；文法审核、纸面计算与实际播放分别记录，没有执行的步骤保留未执行。本文不声称完成真机、私人服务器、所有引擎或输出设备逐项兼容测试。
