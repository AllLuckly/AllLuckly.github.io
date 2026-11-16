---
layout: guide
author: Bison
app_id: icouldplay
title: 云映 ASS 描边宽度：分别核横向、纵向与统一覆盖
description: 用三条相同文字核xbord、ybord及后置bord，不把描边宽度当字体缩放。
permalink: /guides/icouldplay-ass-directional-border-width-reset-components/
date: '2026-11-16 00:00:00 +08:00'
modified: '2026-11-16 00:00:00 +08:00'
category: 教程
level: 进阶
series_order: 174
topic: 字幕形状与样式计算
reading_time: 10
---

同一句文字的外边缘变厚，可能是描边改变，而非字号或文字被拉伸。本课外部制作横向较宽、纵向较宽与统一复位三条ASS参照，再在云映观察。数值表示指定的样式宽度，实际边缘仍受字形和渲染影响；交付时将源文条件与可见结果分开。

## 固定十四秒片源与可比较字形

选择至少十四秒的自有视频，保留原片与旧字幕。准备同一字体请求、字号三十六和相同的一句英文，让三条参照只改变描边条件。字体名不证明设备实际安装，应在记录里留字体是否可确认、是否明显回退的栏位。固定脚本六百四十乘三百六十，设置描边随脚本分辨率缩放的声明，并保留屏幕方向及适应方式；不要一边改视频比例，一边把边缘变化都记成描边参数的作用。

## 保存三个完整事件与缩放声明

完整保存为UTF-8的border-axis.ass，核Script Info中的ScaledBorderAndShadow为yes。三条分别一至四、五至八和九至十二秒；位置、文字与阴影零值不变。第一条先给横八纵二，第二条横二纵八，第三条在横八纵二之后追加统一bord三。保持标签先后顺序，不能把第三条改成另外的样式名后仍说只测后置覆盖。代码来源是本课自制，不是某台设备已经执行通过的日志。

```text
[Script Info]
ScriptType: v4.00+
PlayResX: 640
PlayResY: 360
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,Arial,36,&H00FFFFFF,&H000000FF,&H00000000,&H00000000,0,0,0,0,100,100,0,0,1,1,0,7,20,20,20,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
Dialogue: 0,0:00:01.00,0:00:04.00,Default,,0,0,0,,{\an5\pos(320,180)\shad0\xbord8\ybord2}Border sample.
Dialogue: 0,0:00:05.00,0:00:08.00,Default,,0,0,0,,{\an5\pos(320,180)\shad0\xbord2\ybord8}Border sample.
Dialogue: 0,0:00:09.00,0:00:12.00,Default,,0,0,0,,{\an5\pos(320,180)\shad0\xbord8\ybord2\bord3}Border sample.
```

## 先读横纵两个宽度的作用对象

xbord作用于横向描边宽度，ybord作用于纵向描边宽度，两者不是给文字横纵比例赋值。把第一条记为横八纵二，第二条横二纵八，不因两个数字相加都等于十就认为外观必定相同。阴影独立固定为零，避免偏向某侧的阴影被误看成较宽描边。白色主字与黑色外边在样式里分开记录；只改变颜色无法验证宽度，必须结合本课数值范围、字形和实际显示来判断。

## 用后置统一bord检查覆盖关系

第三条前面已经写横八纵二，后面的bord三会把两个方向都设为三；不是再各加三，也不是只改原样式字段而忽略覆盖。将最终条件写成横三纵三，再把前三条最终条件并排核对。若把后置bord移到两个方向标签之前，后续的横八纵二又会单独生效，因此顺序属于任务证据。反例应另存文件并记录改动位置，不能在原稿中同时留下两种顺序，导致下一轮难以确定正在比较哪一套设置。

## 用理想轮廓框做外部算例

纸上另设填充轮廓的边界框宽一百、高四十，不把它当实际字体测量。若按两侧各扩展对应宽度的理想模型，横八纵二得到外框一百一十六乘四十四；横二纵八得到一百零四乘五十六；统一三得到一百零六乘四十六。这些数值只检查加两次的边界思路，真实字形拐角、抗锯齿和缩放可能改变可见边缘，不能拿纸面外框的面积宣称某手机多画了多少个像素。还可在纸上比较统一bord零与只设xbord零：前者把两个方向都归零，后者仍保留未改的纵向宽度。本课阴影已为零，因此不以残留阴影冒充纵向描边；主字填充仍属于独立组件，不因描边消失就应一并删除。

## 在云映按顺序观察边缘差异

用当前实际字幕选择路径加载文件，顺播到十二秒之后，逐条记主字是否相同、横纵边缘的可辨变化及空档。可在不改变字体的情况下暂停细看，但不要用不同缩放截图直接比较宽度。若只有普通字可读，描边效果未出现，应分别标明加载结果与样式结果。没有入口或没有观察到的项目写未执行，不把外部编辑器的预览图作为云映已经呈现的证明；输出屏幕尺寸也应随记录保存。

## 把裁剪、字重与描边排查分开

若黑边只在一侧消失，先核是否触到显示边界或另有clip标签，而非立刻认定ybord无效。若主字本身变粗，检查Bold字段和b覆盖；若整句变大，查字号或fsc比例。不要同时调整三类参数，避免把一种问题用另一种效果盖住。每次保留源稿、所选副本和失败现象，再用原始三条参照恢复对比；对某个字体有效也不证明全部字体、全部边界样式和所有渲染路径都一致。

## 重开核最终条件并恢复字幕

重开原片并重新选择原稿，先读三组最终宽度条件，再看对应的三段显示。交付标签顺序、脚本缩放声明、理想外框算例和实际观察，未测的边缘细节不补造。最后选回日常字幕，原视频继续保留。本课完成的标准是能解释横纵参数与统一覆盖之间的关系，并知道为何同一张截图不足以推断字体真实尺寸；它不会将字幕样式烘焙到影片，也没有测量实际打印或投屏设备的像素精度。

## 相关教程与资料

[颜色与组件](/guides/icouldplay-ass-bgr-colour-alpha-component-visibility/)、[裁剪窗口](/guides/icouldplay-ass-clip-iclip-glyph-video-boundaries/)。

方法来源：[Aegisub ASS tags](https://aegisub.org/docs/latest/ass_tags/)。

资料核对：2026年11月16日，[云映官方商店](https://apps.apple.com/cn/app/id6755653178)与[Apple公开查询](https://itunes.apple.com/lookup?id=6755653178&country=cn&entity=software&timestamp=20261116)列出1.1.1，最低iOS / iPadOS15.0。练习材料在外部准备，云映负责实际来源选择和播放观察；以安装版可见入口为准，不声明已执行真机或私人服务器逐项测试。
