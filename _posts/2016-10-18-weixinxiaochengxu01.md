---
layout: post
title: "微信小程序开发教程-从零开始（2）"
description: "weChat"
category: 微信小程序
headline: Discover the theme elements
tags: [微信小程序, iOS开发, 应用号]
imagefeature: 
comments: true
featured: true
mathjax: 
path: /images
---

![1]({{ site.url }}/images/blog/weixinxiaochengxu/20161017/1.png)<br>

从[微信小程序开发教程-从零开始（1）](http://www.jianshu.com/p/ccf40205300f)

中我们学会了怎么搭建一个微信小程序的框架以及显示一个文章列表，这篇文章我将讲解列表的点击以及UI的优化，达到一个我们预期的一种效果。

 首先我们创建一个详情的界面所需的文件,如下图所示:

![1]({{ site.url }}/images/blog/weixinxiaochengxu/20161018/1.png)<br>

详情页的话，我们暂时随便搭建一下，主要是看下怎么做跳转。

首先我们在详情页面随便写点东西，代码如下：


```
<!--detail.wxml-->
<view class="container">
666666
</view>

```

这样的话在外面的详情页会显示666666这些个字样，然后我们在index.wxml中写跳转的代码，主要代码如下：

```
<navigator url="navigate?title=navigate" hover-class="navigator-hover">
跳转到新页面
</navigator>
```


其中`url`为应用内的跳转链接`title=navigate`为传过去的字段`hover-class`指定点击时的样式类，当hover-class="none"时，没有点击态效果.完整的代码如下图框起来的地方

![1]({{ site.url }}/images/blog/weixinxiaochengxu/20161018/2.png)<br>

运行一下，可以瞧瞧效果如下。

![1]({{ site.url }}/images/blog/weixinxiaochengxu/20161018/3.gif)<br>

由图可以看出跳转的功能已经做好了，下面我们开始优化一下首页的UI
优化UI 的话主要是在`index.wxss`中，根据每个控件的class名来写相应的设置。
首先我们把整个页面做一下设置，代码如下：


```
/**index.wxss**/
.list {
  height: 100%;
  display: flex;
  flex-direction: column;
  padding: 20rpx;
}
```

`padding`为内边框，首页整个的class名为list，所以用.list{}来设置。然后设置一下navigator块，再然后来设置我们的每一个列表，在这里我把它命名为cell，看上去对于iOS开发来说亲切一点。具体代码如下：


```
navigator{ overflow: hidden;}

.cell{
  margin-bottom:  20rpx;
  height: 200rpx;
  position: relative;
}
```

再然后我们设置cell中图片的位置，具体代码如下：

```
.imgs{
  float: right;
}
.imgs image { 
  display: block;
  width: 200rpx;
  height: 200rpx;
}
```
由代码可以看出，我们的图片设置了向右对齐，宽和高分别设置了200rpx，我们运行一下看看效果图片是否已经改变了。

![1]({{ site.url }}/images/blog/weixinxiaochengxu/20161018/4.png)<br>

相对于我们的效果图的图片部分，应该已经差不多就是这个样子了，下面让我们再调一调标题以及其他部分UI 的调试。
我们把其他部分的UI都放在class="infos"; 首先我们先调这一大块的布局，代码如下：

```
.infos {
  float: left; 
  width: 480rpx;
  height: 200rpx;
  padding: 20rpx 0 0 20rpx;
}
```
然后设置里面的每一个小部件，代码如下：

```
.title {font-size: 20px;}

.date {
  padding-top: 50rpx;
  float: right;
  font-size: 16px;
  color: #aaa;
  position: relative;

}
.classification{
  padding-top: 50rpx;
  font-size: 16px;
  color: #aaa;
  position: relative;
}

```

最后我们运行一下看下结果如何：

![1]({{ site.url }}/images/blog/weixinxiaochengxu/20161018/5.gif)<br>

有空的话再写写网络请求方面的，结合这个[demo]()写

本文为[Bison](blog.allluckly.cn)原创，转载请注明出处，否则将追究法律责任


----------------------------------------------------------

> [学习iOS开发的app上线啦，点此来围观吧](https://itunes.apple.com/us/app/it-blog-zi-xueios-kai-fa-jin/id1067787090?l=zh&ls=1&mt=8)<br>

> [更多经验请点击](https://allluckly.cn)<br>

好文推荐：[分分钟解决iOS开发中App启动动画广告的功能](https://allluckly.cn/lblaunchimagead/LBLaunchImageAd)<br>

