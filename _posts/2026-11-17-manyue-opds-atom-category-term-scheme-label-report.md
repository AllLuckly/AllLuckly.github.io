---
layout: guide
author: Bison
app_id: man_yue
title: 漫阅+ OPDS分类报告跟读：term、scheme与显示标签各留一栏
description: 比较三条分类记录，核同一分类换显示名与不同体系共用标签，不把目录标签当正文身份。
permalink: /guides/manyue-opds-atom-category-term-scheme-label-report/
date: '2026-11-17 00:00:00 +08:00'
modified: '2026-11-17 00:00:00 +08:00'
category: 教程
level: 进阶
series_order: 225
topic: 文件报告的结构与语义
reading_time: 10
---

目录里两个相同标签未必指同一分类，同一分类也可能换一种人类可读名称。本课把Atom格式的分类片段做成PDF报告，在漫阅逐项核term、scheme和label。材料只解释OPDS所用Atom字段，不承诺应用有原始XML检查器、按这些字段筛选的界面或自动合并分类功能。

## 先把三条记录做成可核的样本

在外部文本工具保存下方三条片段，按出现次序编号A、B、C。scheme使用example.invalid占位地址，只是分类体系标识示例，不要求访问，也不包含自己的服务器资料。另做报告PDF第一页放原片段，第二页放三栏表，第三页放一条原创漫画条目与观察栏；给三页加P1到P3角标。片段没有完整feed和entry的必需字段，不能当成可直接连接的OPDS服务。导入漫阅前先确认PDF能正常显示引号和完整地址，避免报告本身截断证据。

```xml
<category xmlns="http://www.w3.org/2005/Atom" term="river" scheme="https://example.invalid/subjects" label="Rivers"/>
<category xmlns="http://www.w3.org/2005/Atom" term="river" scheme="https://example.invalid/subjects" label="Waterways"/>
<category xmlns="http://www.w3.org/2005/Atom" term="river" scheme="https://example.invalid/collections" label="Rivers"/>
```

## 先抄必需的term不按标签猜值

在三栏表第一栏逐条写river，确认三条都有term。Atom规定category必须带term，它是标识所属分类的字符串，不是要显示给用户的唯一一句标题。缺少term是结构问题，不能因为label看起来很完整就默认为它补同值。反过来，term的词形恰好是英语单词，也不说明用户一定会在界面看到这个词。保留原始字符，不擅自翻译标识值或把复数改成单数。报告的表头与实际字段名分开排，防止把说明文字也抄进值里。

## 把scheme当分类体系标识

第二栏完整抄scheme：A与B是subjects，C是collections；这里只用末段简称便于讨论，证据栏仍保留完整IRI。scheme是可选的体系标识，不是漫画下载链接、封面位置或必须能打开的网页。不能点不开占位地址就判分类无效，也不拿它替代服务器基础地址去登录。比较时先核是否存在，再核实际字符；缺失scheme应写未声明，而非自动继承旁边另一条记录的值。本课不建立复杂IRI归一化规则，只对明确给定的字符串做对照。

## label提供人类可读名称而非唯一键

第三栏读出Rivers、Waterways、Rivers。label可选，用于面向用户的显示名称，且具有语言范围；没有它不等于没有category。A和B的term与scheme都相同，只换显示标签，所以在本练习的分类身份账中归到同一项；C虽然也写Rivers，但体系不同，应另留一项。三条记录于是有两组明确的体系与术语组合，显示字符串也有两种，但两种二并非由同一个规则得来。不要直接按屏幕看起来相同就合并漫画文件或删除条目。

若将A的显示标签改成中文河流，而term与scheme不动，原始分类组合仍相同；语言敏感的显示名可以变化，不是强迫把标识也翻译。另把C的label删去，它仍有term与scheme，不能在分类账里消失。至于实际客户端缺标签时显示术语、空白还是其他回退，本课不替未知界面作承诺。

## 用实体转义核实际显示文字

在P3另加一个小例：label写Maps后接转义的与号再接Rivers。XML里的amp实体代表字符与号，不是把后面一段变成标签；人类可读结果为Maps & Rivers。原始串与解码文本分别留栏，不能把浏览器已经解码的文本再当原始XML复制回去。用尖括号的转义也同理，不因此执行标记。阅读PDF时只看报告展示的原文与预期，若实际字样变成实体名，先核外部导出是否又转义一次，不立即归因于漫阅处理了OPDS。

```xml
<category xmlns="http://www.w3.org/2005/Atom" term="maps" label="Maps &amp; Rivers"/>
```

## 在实际目录只记录看见的内容

先把报告PDF在漫阅读完并给对照表加书签。若已有自己有权访问的OPDS书库，可另选一个已知条目，记录当前实际显示的标签、书名、作者与封面，不要求服务端立刻改样本。可见标签只是观察，不能单凭它还原scheme或断定服务器删除了原始term。没有原始响应报告就将那些字段记未知；普通OPDS整包获取与OPDS-PSE逐页阅读仍按公开能力分开，不能因为分类显示成功就认定正文可以直接阅读。没有自己的目录时只做PDF任务也完整。

## 用三类错例追溯误合并

若A和B被当不同体系，查是否误把Waterways当scheme；若A和C被合并，查是否只比较Rivers；若缺term的例子被自动补成Rivers，查是否混淆必需字段与可选显示名。修正报告只改一栏并保留旧值，不去批量改自己的服务器标签。目录实际显示与报告不同，也可能来自不同条目、不同语言或服务端输出，先核身份与时间再推测。把分类身份与书籍身份分开：同一分类能容纳多书，一本书也可能有多分类，分类条数不是漫画页数。

还可把这三条category都归到同一份原创条目下，用一句话写书籍一条、分类记录三条、明确组合两组。这样复查者可发现把类别数量当书籍数量的错位。报告未给排序规则时不从字母先后推受欢迎程度，标签出现两次也不证明它拥有两本作品。

## 重开交付原文身份与显示三层

重开报告书签，遮住表格先读A、B、C的term与完整scheme，再指出两个Rivers为何仍不能直接合并。返回P3核与号解码，不把原始amp实体漏掉。验收要保留三条原记录、两组组合、两种显示串和未观察字段，缺少任一层就无法解释同名问题。PDF重开或目录抽查没执行时照实待做，交付原稿与记录即可。换目录服务后重新核响应，不承诺不同OPDS服务用同一分类体系，也不把本次手工账本说成App自动去重结果。

## 相关教程与资料

[OPDS链接用途](/guides/manyue-opds-cover-sample-acquisition-links/)、[LANraragi标签查询](/guides/manyue-lanraragi-tag-lookup/)。

方法依据：[RFC4287 §4.2.2 Atom分类](https://www.rfc-editor.org/rfc/rfc4287.html#section-4.2.2)、[OPDS1.2目录规范](https://specs.opds.io/opds-1.2)。本课图、报告数据、错例及记录表均为原创练习。

版本核对：2026年11月17日，[Apple公开查询](https://itunes.apple.com/lookup?id=6753895889&country=cn&entity=software&timestamp=20261117)显示漫阅+2.0.5，最低iOS / iPadOS 15.0；公开能力见[官方App Store](https://apps.apple.com/cn/app/id6753895889)。本课使用自制PDF或受支持的漫画图片阅读，具体入口依安装版本可见范围。外部制作与纸面预期不等于已做真机观察，未执行项目照实留空。
