---
layout: guide
author: Bison
app_id: icouldplay
title: 云映 HLS 会话资料核对：数据标识、语言与外部JSON分别记录
description: 读取三条SESSION-DATA，检查唯一组合、二选一载体与JSON引用，不把节目资料当字幕。
permalink: /guides/icouldplay-hls-session-data-id-language-value-uri-record/
date: '2026-11-16 00:00:00 +08:00'
modified: '2026-11-16 00:00:00 +08:00'
category: 教程
level: 进阶
series_order: 176
topic: 清单声明与播放条件
reading_time: 10
---

主清单里的标题文字不一定会出现在影片画面中。本课用三条自制会话资料建立字段卡，把数据身份、语言、直接值与外部JSON分开核对，再到云映观察自己真实来源的播放。练习不假定应用提供会话资料编辑器，也不把看见文字清单当成已经加载可见字幕。

## 先给主清单和资料卡保留身份

在外部纯文本工具准备练习文件，另为自己的实际HLS来源记录主清单地址、取得时间与所选视频入口。没有真实来源也可完成字段任务，播放栏写未执行，不向样本URI索要不存在的影片。把主清单和JSON卡分别命名，保留未经修改原稿；它们是两份资料，不是把JSON接在M3U8末尾的一整份文件。来源是否可访问、文字语法是否符合样本、界面是否展示资料应分栏记录，不能只因主清单能打开就同时把后三项都勾为通过。

## 逐条读取三种资料行

把下方全文作为一个主清单阅读样本，前三条资料分别是英文标题、法文标题和外部资料卡。两标题共用DATA-ID而LANGUAGE不同，第三条有另一个标识与URI；末尾变体才引用视频媒体清单。DATA-ID应按建议采用不易碰撞的反向域名式命名，本例org.example只是教学命名空间，不证明任何注册归属。代码中的编码与带宽也是假定声明，没有附带媒体字节，不能将文法完整误写为已经建立服务器、编码完成或可直接观看。

```text
#EXTM3U
#EXT-X-SESSION-DATA:DATA-ID="org.example.lesson.title",LANGUAGE="en",VALUE="Harbor notes"
#EXT-X-SESSION-DATA:DATA-ID="org.example.lesson.title",LANGUAGE="fr",VALUE="Notes du port"
#EXT-X-SESSION-DATA:DATA-ID="org.example.lesson.card",URI="session-card.json"
#EXT-X-STREAM-INF:BANDWIDTH=900000,CODECS="avc1.4d401e,mp4a.40.2"
lesson.m3u8
```

## 按标识与语言组合查重复

给三条资料各填DATA-ID、LANGUAGE、载体和值四栏。前两条的组合分别是标题加en、标题加fr，因此不是重复键；若复制英文行只改VALUE而仍保留同一DATA-ID与en，就产生应修正的重复组合。不能靠把第二行挪到文件末尾解决，也不把两个不同语言值自动拼成一条双语字幕。未写LANGUAGE的资料另记未声明，不凭播放器系统语言补填。本课只核当前主清单中的组合，名称能避免本地冲突并不等于全球已有中央机构为它登记唯一性。

## 外部资料必须按JSON单独审核

第三行URI指向独立JSON资源，其内容可用下方原创小卡。先核花括号、双引号与数组边界，再登记exercise、edition和两个章节名称；这些自定义键只是卡片数据，不会自动生成HLS章节或字幕时间。URI按包含它的清单地址还原，文件扩展名叫json也不保证响应实际就是JSON。若取得的是登录网页，保留返回类型和访问结果，不把网页标题抄进卡片当解析成功。这里的JSON可独立读懂，但没有实际请求时仍不能声称已经取得远端资料。

```text
{
  "exercise": "harbor-card",
  "edition": 2,
  "chapters": ["arrival", "departure"]
}
```

## 用二选一规则检查故障副本

复制第一条，在同一SESSION-DATA行同时加入VALUE和URI，其他属性不变。这份故障稿违反每条必须二选一的要求，不能解释成先读VALUE、失败再回退URI。修复时选一种资料载体，恢复正确稿再核三行组合；只有DATA-ID却两种载体都没有也不合要求。LANGUAGE说明直接值的语言，不会翻译英语句子，也不是字幕轨道的LANGUAGE入口。若把语言改成de却保留法文文字，应另记内容语言待核，不能说字段变动已自动得到德语资料。

## 在云映只记录实际可见的结果

有真实完整来源时，从正常入口打开影片，记录启动、顺播以及界面实际可见的节目文字。若应用没有显示会话标题，把播放通过与资料展示未知或未显示分别写，不据此宣布媒体缺失；反过来，标题出现也不能证明三条资料都解析。保持同一来源与安装版本，不为得到期望标题同时改文件名、刮削信息和会话值。需要播放对照时使用自己的可恢复测试来源，清单审核留在外部，不编造云映里的JSON查看器或自动字幕生成按钮。

## 把访问、文法与显示异常逐层定位

资料不见时先核是否读到正确主清单，再查外部URI还原和JSON实际内容；不要先把文字加进分片地址里试运气。重复资料先查DATA-ID加LANGUAGE，不只比VALUE看起来像不像；载体冲突先恢复二选一，不修改视频编码掩盖文字问题。记录每一处失败属于主清单、资料资源还是客户端展示，三者可能给出不同结果。保存故障副本与唯一变动说明，无法判断的字段写未知，不能用另一条标题能显示为失败资料作全部兼容保证。

## 重开核三行组合与资料边界

重开正确主清单与JSON卡，重新列两种标题语言和一份外部资料，核没有重复键、没有双载体，JSON的edition仍为二。再进入自己的影片，只有实际做过才补播放观察；未做就交付纯阅读成果。最终交付主清单、资料卡、字段账本和当前路径结果，注明会话元数据不等于字幕轨、时间提示或媒体分片。下次换清单地址或资料版本需重新还原URI并核内容，不能沿用旧标题就声称视频身份、媒体完整性和字幕加载状态都没变。

## 相关教程与资料

[云映 HLS 多版本清单：分开主清单、变体与媒体分片]({{ '/guides/icouldplay-hls-master-variant-media-map/' | relative_url }})、[云映 HLS 地址对照：逐条还原相对分片位置]({{ '/guides/icouldplay-hls-relative-uri-resolution-sheet/' | relative_url }})。

方法来源：[RFC8216 §4.3.4.4](https://www.rfc-editor.org/rfc/rfc8216#section-4.3.4.4)。

资料核对：2026年11月16日，[云映官方商店](https://apps.apple.com/cn/app/id6755653178)和[Apple公开查询](https://itunes.apple.com/lookup?id=6755653178&country=cn&entity=software&timestamp=20261116)列出1.1.1，最低iOS / iPadOS 15.0。样本在外部用纯文本手工准备，云映用于已有真实来源的选择与播放观察，入口以安装版本实际可见为准。占位URI不提供媒体；文法审核、纸面计算与实际播放分别记录，没有执行的步骤保留未执行。本文不声称完成真机、私人服务器、所有引擎或输出设备逐项兼容测试。
