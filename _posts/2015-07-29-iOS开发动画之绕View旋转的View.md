---
layout: post
title: "iOS开发动画之绕View旋转的View"
description: "Bison"
category: iOS动画
headline: Discover the theme elements
tags: [iOS动画，iOS开发技巧，iOS开发，技术博客]
imagefeature: picture-35.jpg
comments: true
featured: 
mathjax: true
path: /images
---

>&quot;身体是革命的本钱，多锻炼才是王道&quot;
><small><cite title="Plato">Bison</cite></small>

>![1]({{ page.path }}/zjs.jpg)<br>
>[冰之依韩版女装](http://allluckly.taobao.com/)（程序媛福利）

最近项目中出现了个动画，找了很多相关资料<br>
发现并没有适合的，于是自定义了一个<br>
主要的原理是根据改变三角形的正弦定理 <br>
余弦定理来实现view绕图片中心点运行的动画。<br>

下面请看代码<br>

 > [更多经验请点击](http://www.allluckly.cn/) 

核心代码
{% highlight css %}

self.center = CGPointMake(_radius * cosf(_angle) + imgView.center.x, _radius * sinf(_angle) + imgView.center.y);

_timer = [NSTimer scheduledTimerWithTimeInterval:_time target:self selector:@selector(moveView) userInfo:nil repeats:YES];

{% endhighlight %}

> [点击下载Demo](https://github.com/AllLuckly/RadiusOperation) <br>

![(RadiusOperation)](https://github.com/AllLuckly/RadiusOperation/blob/master/123.gif?raw=true)

