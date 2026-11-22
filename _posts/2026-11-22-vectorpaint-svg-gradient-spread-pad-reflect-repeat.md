---
layout: guide
author: Bison
app_id: draw_illustration
title: VectorPaint 渐变边界对照：延展、反射和重复的颜色顺序
description: 制作三条相同线性渐变色带，观察端点外的延展方式并检查应用导入。
permalink: /guides/vectorpaint-svg-gradient-spread-pad-reflect-repeat/
date: '2026-11-22 00:00:00 +08:00'
modified: '2026-11-22 00:00:00 +08:00'
category: 教程
level: 进阶
series_order: 276
topic: SVG 渐变边界与色带延展
reading_time: 10
---

制作三条相同线性渐变色带，观察端点外的延展方式并检查应用导入。

## 先确定比较的范围

线性渐变的起点与终点可以位于填充形状内部。SVG 的 spreadMethod 决定渐变两端以外如何填色：pad 延展端点色，reflect 往返反射，repeat 沿原顺序重复。本练习使用相同矩形、渐变方向与色标，只改变延展方式；先写出三种预期，再比较浏览器和 VectorPaint 的实际结果。格式属性不等于软件界面一定提供同名开关。

## 给色带划定三个区间

设三个矩形均从 x=20 到 x=140，宽 120，分别位于 y=15、55、95，高 25。每个渐变使用 userSpaceOnUse，从 x=60 开始到 x=100 结束，颜色从蓝色 #315b8a 到橙色 #dc8538。于是矩形可分为 20–60、60–100 和 100–140 三个等宽区间；中间都是蓝到橙，两侧才体现延展的区别。坐标是示例用户单位，不默认等于手机像素。

## 写下两侧的颜色顺序

pad 行在左区保持蓝色，右区保持橙色。reflect 行从左至右依次是橙到蓝、蓝到橙、橙到蓝；在相接处颜色连续。repeat 行三个区间都从蓝到橙，到了新的周期起点会从橙跳回蓝。端点处与抗锯齿附近的单个像素可能受渲染影响，先看整体色带方向而不是只比较边界上的一个像素。

## 保存完整 SVG 样本

将下方完整样本复制到纯文本编辑器，保存为 gradient-spread.svg 并另存备份。保留 defs、三个唯一渐变 id、两端 stop 和对应矩形的 fill 引用；不要只复制矩形，否则它们找不到渐变。三个渐变的坐标、颜色和 stops 相同，只有 spreadMethod 不同。确认文件后缀不是 svg.txt，不添加来源不明的脚本或覆盖已有作品。

```xml
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 160 135">
  <defs>
    <linearGradient id="gpad" gradientUnits="userSpaceOnUse" x1="60" y1="0" x2="100" y2="0" spreadMethod="pad">
      <stop offset="0" stop-color="#315b8a"/><stop offset="1" stop-color="#dc8538"/>
    </linearGradient>
    <linearGradient id="greflect" gradientUnits="userSpaceOnUse" x1="60" y1="0" x2="100" y2="0" spreadMethod="reflect">
      <stop offset="0" stop-color="#315b8a"/><stop offset="1" stop-color="#dc8538"/>
    </linearGradient>
    <linearGradient id="grepeat" gradientUnits="userSpaceOnUse" x1="60" y1="0" x2="100" y2="0" spreadMethod="repeat">
      <stop offset="0" stop-color="#315b8a"/><stop offset="1" stop-color="#dc8538"/>
    </linearGradient>
  </defs>
  <rect x="20" y="15" width="120" height="25" fill="url(#gpad)"/>
  <rect x="20" y="55" width="120" height="25" fill="url(#greflect)"/>
  <rect x="20" y="95" width="120" height="25" fill="url(#grepeat)"/>
</svg>
```

## 在浏览器建立参照

用支持 SVG 的浏览器打开原稿，自上而下依次观察 pad、reflect、repeat。先用纸遮住中间区，单独比较两端颜色，再看三个中间区是否都是蓝到橙；如果整个矩形只有单一颜色，检查 fill 的 id 是否存在且拼写一致。若三行几乎一样，确认 x1 和 x2 确实位于矩形内部，而不是覆盖了整个宽度。记录结果，不称之为应用实测。

## 用纸面记录颜色接续

在纸上画三条各有三格的长条，每格写起点色和终点色。pad 行写蓝、蓝到橙、橙；reflect 写橙到蓝、蓝到橙、橙到蓝；repeat 则每格均写蓝到橙。把每格连接处画成连续或跳变，随后与浏览器比较。若印刷或屏幕使颜色不易辨别，可在副本中换成对比更明显的两种颜色，但三行必须同时更换，原始样本和记录保留。

## 用端点和中点检查方向

先在草稿上标记 x=20、40、60、80、100、120、140。对于 reflect，x=60 附近接蓝色、x=100 附近接橙色，左右两侧各向相反方向过渡；从中间橙色端点继续向右时颜色逐渐回到蓝色。对于 repeat，每经过一个 40 单位周期就重新从蓝色开始，因此 x=100 附近应出现橙到蓝的突变。pad 两侧则没有进一步的色彩循环。

比较时先检查三个区间的宽度，而不是从颜色看起来相似就认为属性相同。截图如果把色带裁掉一端，应回到原始浏览器画面核对完整矩形。蓝与橙之间的精确中间像素可能因色彩空间、屏幕和渲染方式不同而变化；本练习的检查目标是方向与接续，而不是给所有设备规定相同的中间色值。

## 打开应用工作副本

在安装的 VectorPaint 中寻找当前实际可见的 SVG 打开或导入入口，选择副本；没有入口或不支持此文件时写未完成。先检查三条色带的区间和颜色，再尝试分别选择矩形。若只剩一个平面图像，不把它记成可编辑渐变；若色带外观正确，也不能单凭外观确认 spreadMethod 仍是独立属性。记录应用版本和使用的实际入口。

比较应用显示时，先确认三条矩形的高度与顺序，避免把中间 reflect 误当成底部 repeat。可在外部笔记中写行号，不必修改作为基准的 SVG。若设备启用了影响显示颜色的系统设置，也将其记入条件。

## 另存并区分视觉与结构

通过当前版本可见的分享或导出入口另存，不覆盖源文件。重新打开后检查每条中间渐变及左右接续；如果输出为 SVG，在纯文本编辑器查看 linearGradient、spreadMethod、stop 与 fill 引用是否保留，或者是否转成其他路径、图案或图像。若导出为位图，仅比较可见色带和尺寸，不声称色标仍可编辑。把浏览器、导入和输出结果分开记录。

## 排查颜色或边界异常

渐变显示为纯黑或缺失时，先核对三个 id 与各 fill 引用，再检查 stop-color 和 XML 引号；不要同时重命名所有元素。若 repeat 没有明显跳变，确认渐变端点确在矩形中间，并检查是否打开了正确副本；如果应用与浏览器不同，保留两份结果交由熟悉格式的人比较，不因此断定某种功能一定不受支持。未做的导入、导出或设备步骤写待核，并确认备份可打开。

## 改变重复周期做反证

另存一份副本，仅将底部 repeat 渐变的 x2 从 100 改成 80，x1 仍为 60。重复周期由 40 变成 20 单位，因此原本位于 x=100 的周期交界前还会在 x=80 出现一次交界；上面两行保持不变。浏览器比较前后两份，若三行都变化，先核对改动的渐变编号和引用；不要覆盖基准文件。

## 相关教程与资料

[渐变坐标与对象边界](/guides/vectorpaint-svg-gradient-units-bounds-versus-user-space/)、[SVG 兼容排查](/guides/vectorpaint-svg-compatibility-check/)。

2026年11月22日核对：[Apple 公开版本查询](https://itunes.apple.com/lookup?id=1587272880&country=cn&entity=software)、[MDN：渐变延展方式](https://developer.mozilla.org/en-US/docs/Web/SVG/Reference/Attribute/spreadMethod)。未声称完成真实设备或私人服务器测试。
