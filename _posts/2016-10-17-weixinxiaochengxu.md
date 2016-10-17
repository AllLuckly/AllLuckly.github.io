---
layout: post
title: "微信小程序开发教程-从零开始（1）"
description: "Swift"
category: 投稿
headline: Discover the theme elements
tags: [微信小程序, iOS开发, 应用号]
imagefeature: 
comments: true
featured: true
mathjax: 
path: /images
---

![1]({{ site.url }}/images/blog/weixinxiaochengxu/20161017/1.png)<br>


## 前言

微信小程序暂时处于内测期间，公司大的版本刚好上线了，闲来无事，看看微信小程序的文档，顺便学习学习，在此希望和大家一起共勉，发现自己越来越懒惰了，越活越没上进心了，有点危险，给自己敲下警钟吧。废话不多说，开始记录下这些天学习到的一些知识，希望对正在阅读的你有所帮助！
本文为iOS开发者[Bison](blog.allluckly.cn)自学微信小程序所写，所以很多东西都和iOS进行了一下对比。

## 开搞

> 创建项目在此滤过，相信大家看着官方文档就可以搞定

### 首先我们先把整个app的架构搭起来

一般市面上的app都已tabbar展示的方式为主，今天我就仿原生的[IT Blog](https://itunes.apple.com/cn/app/it-blog-ios-kai-fa-zhe-wen/id1067787090?mt=8)下面让我们看下[IT blog](https://itunes.apple.com/cn/app/it-blog-ios-kai-fa-zhe-wen/id1067787090?mt=8)长什么样吧！<br>

![1]({{ site.url }}/images/blog/weixinxiaochengxu/20161017/2.jpg)<br>

#### 首先是tabbar
下面我将简单的介绍一下微信小程序一些不可缺的目录结构。
![1]({{ site.url }}/images/blog/weixinxiaochengxu/20161017/3.png)<br>

- 下面借用官方的解释

##### WXSS(WeiXin Style Sheets)是一套样式语言，用于描述 WXML 的组件样式。

WXSS 用来决定 WXML 的组件应该怎么显示。为了适应广大的前端开发者，我们的 WXSS 具有 CSS 大部分特性。 同时为了更适合开发微信小程序，我们对 CSS 进行了扩充以及修改。

#### app.json 文件来对微信小程序进行全局配置，决定页面文件的路径、窗口表现、设置网络超时时间、设置多 tab 等。

文件来对微信小程序进行全局配置，决定页面文件的路径、窗口表现、设置网络超时时间、设置多 tab 等。相当于iOS开发中的AppDelegate

#### app.js 是小程序逻辑部分

根据上面的目录结构的解释不难看出，我们的tabbar是写在哪的，没错就是app.json，下面让我们看下代码

```
{
  "pages":[
    "pages/index/index",
    "pages/logs/logs"
  ],
  "window":{
    "backgroundTextStyle":"light",
    "navigationBarBackgroundColor": "#fff",
    "navigationBarTitleText": "WeChat",
    "navigationBarTextStyle":"black"
  },
  "tabBar": {
    "backgroundColor":"#000000",
    "list": [{
      "iconPath":"image/icon_API.png",
      "selectedIconPath":"image/icon_API_HL.png",
      "pagePath": "pages/index/index",
      "text": "首页"
    }, {
      "iconPath":"image/icon_component.png",
      "selectedIconPath":"image/icon_component_HL.png",
      "pagePath": "pages/about/about",
      "text": "我的"
    }]
  }
}
```

![1]({{ site.url }}/images/blog/weixinxiaochengxu/20161017/4.png)<br>

上图框出来的地方就是我们的tabbar，tabbar里面可以传一个数组list，想显示多少个tab就到这里加就行，当然个数是有限制的最多5个，一个的话就没必要了。这点和iOS开发里面颇为相似。
下面我们按下com + s 再 编译一下，就可以看到如下结果了


![1]({{ site.url }}/images/blog/weixinxiaochengxu/20161017/5.png)<br>

iconPath为默认图片路径，selectedIconPath为点击时的图片路径，text的话我想不说大家也已经猜到了，对，没错就是图片下面显示的title了。

我们这暂时只写了俩个Tab，在此主要也就是实现我们的首页效果。
由我们的效果图可以看出，iOS开发中我们的布局主要用的是tabview，而在微信小程序中类似tabviewCell的布局又是怎么写的呢？下面我们先写贴下代码再做下解说。

```
<!--文章列表模板 begin-->
<template name="itmes">
     <view class="imgs"><image src="{{imgURL}}" class="in-img" background-size="cover" model="scaleToFill"></image></view>
    <view class="infos">
      <view class="title">{{title}}</view>
      <view class="date">{{time}}</view>
       <view class="classification">{{classification}}</view>
    </view>
</template>
<!--文章列表模板 begin-->
```

在这段代码中`<template name="items">`...`</template>`是微信小程序中的模板，那什么是模板呢？官方文档是这样解释的。

#### 模板

WXML提供模板（template），可以在模板中定义代码片段，然后在不同的地方调用。

我的理解这个相当于iOS开发中的cell，cell有了的话， 那就只缺少一个数据源了，下面我们暂时做一个本地的数据源。

数据主要是写在js代码当中的，下面来看下代码

```
//index.js
//获取应用实例
var app = getApp()
Page({
  data: {
    newList:[{url:"baidu.com",title:"sdsadsadasdas",classification:"ss",time:"2016-10-17",imgURL:"../../image/wechatHL.png"},
             {url:"baidu.com",title:"sdsadsadasdassss",classification:"ss",time:"2016-10-17",imgURL:"../../image/wechatHL.png"},
             {url:"baidu.com",title:"sdsadsadasdas",classification:"12",time:"2016-10-17",imgURL:"../../image/wechatHL.png"},
             {url:"baidu.com",title:"sdsadsadasdas",classification:"333",time:"2016-10-17",imgURL:"../../image/wechatHL.png"},
             {url:"baidu.com",title:"sdsadsadasdas",classification:"44",time:"2016-10-17",imgURL:"../../image/wechatHL.png"},
             {url:"baidu.com",title:"sdsadsadasdas",classification:"44",time:"2016-10-17",imgURL:"../../image/wechatHL.png"},
             {url:"baidu.com",title:"sdsadsadasdas",classification:"32",time:"2016-10-17",imgURL:"../../image/wechatHL.png"},
             {url:"baidu.com",title:"sdsadsadasdas",classification:"123",time:"2016-10-17",imgURL:"../../image/wechatHL.png"},
             {url:"baidu.com",title:"sdsadsadasdas",classification:"456",time:"2016-10-17",imgURL:"../../image/wechatHL.png"},
             {url:"baidu.com",title:"sdsadsadasdas",classification:"454",time:"2016-10-17",imgURL:"../../image/wechatHL.png"}
    ]
  },
  //事件处理函数
  bindViewTap: function() {
    wx.navigateTo({
      url: '../logs/logs'
    })
  }

})

```

其中的`newList`为我们的数据源,数组里面包含多个字典，字典里面有我们所需要的5个字段。
cell 和数据源都有了，那就只差一个显示了， 显示在微信小程序当中用的是`列表渲染`

#### 列表渲染

在组件上使用wx:for控制属性绑定一个数组，即可使用数组中各项的数据重复渲染该组件。
默认数组的当前项的下标变量名默认为index，数组当前项的变量名默认为item

下面我们来看看这个列表渲染是怎么做的,首先切换到index.wxml中，代码如下。

```
<!--循环渲染列表 begin-->
<block wx:for="{{newList}}">
  <template is="itmes" data="{{...item}}" />
</block>
<!--循环渲染列表 end-->
```

com + s 再 编译一下可以看到如下的效果

![1]({{ site.url }}/images/blog/weixinxiaochengxu/20161017/6.gif)<br>

到此微信小程序的列表功能已经做完了，当然我们看到的布局都是很乱的，下一篇我们将优化UI让他和我们的效果图一样。

本文为[Bison](blog.allluckly.cn)原创，转载请注明出处，否则将追究法律责任

----------------------------------------------------------

> [学习iOS开发的app上线啦，点此来围观吧](https://itunes.apple.com/us/app/it-blog-zi-xueios-kai-fa-jin/id1067787090?l=zh&ls=1&mt=8)<br>

> [更多经验请点击](https://allluckly.cn)<br>

好文推荐：[分分钟解决iOS开发中App启动动画广告的功能](https://allluckly.cn/lblaunchimagead/LBLaunchImageAd)<br>

