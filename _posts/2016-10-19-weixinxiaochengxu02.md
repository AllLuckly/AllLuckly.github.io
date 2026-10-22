---
layout: post
title: "微信小程序开发教程-从零开始（3）"
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


[微信小程序开发教程-从零开始（1）](http://www.jianshu.com/p/ccf40205300f)

[微信小程序开发教程-从零开始（2）](http://www.jianshu.com/p/bfd8c8d91c7d)

前俩章中我们学会了怎么搭建一个微信小程序的框架以及显示一个文章列表，这篇文章我将讲解列表的网络请求以及网络数据的对接。

首先找到我们的index.js文件，然后看看[微信小程序的网络请求文档](https://mp.weixin.qq.com/debug/wxadoc/dev/api/network-request.html?t=1476197482156)很轻松的就可以找到我们的示例代码：

```
wx.request({
  url: 'test.php',
  data: {
     x: '' ,
     y: ''
  },
  header: {
      'Content-Type': 'application/json'
  },
  success: function(res) {
    console.log(res.data)
  }
})

```

> url为我们需要请求的接口

> data为我们的请求参数

>header为设置请求的 header , header 中不能设置 Referer

> success收到开发者服务成功返回的回调函数，res = {data: '开发者服务器返回的内容'}

>  console.log( res.data )为打印请求下来的数据



默认为get请求，在此我们就用默认的请求方式，具体的代码如下：


```
onLoad: function () {
    console.log('onLoad')
    var that = this
    wx.request( {
      url: 'http://sep9.cn/qt5wix',
      data: {},
      header: {
        'Content-Type': 'application/json'
      },
      success: function( res ) {
        console.log( res.data )
      }
    })
  }
```
运行一下看看我们的请求是否有数据，结果如下图：

![1]({{ site.url }}/images/blog/weixinxiaochengxu/20161019/1.png)<br>

可以看出我们的数据请求已经是成功的，是不是非常的简单啊？😄下面我们再来看看怎么给相应的UI赋值吧。

首先在我们网络成功的地方加上以下代码:
```
success: function( res ) {
        console.log( res.data )
          that.setData( {
            
          })
      }
```

`that.setData( { })`这个方法主要是用来赋值的

然后我们得到的数据为`res.data`通过打印我们可以看出我们的数据结构和原来写死的数据结构是一样的，但是里面的字段确不一样，因此，我们需要把请求下来的值赋值给我们原来的数据源，然后把原有的数据源的字段改成网络请求下来的字段最终的代码如下：
```
//index.js
//获取应用实例
var app = getApp()
Page({
  data: {
    newList:[  
    ]
  },
  //事件处理函数
  bindViewTap: function() {
    wx.navigateTo({
      url: '../logs/logs'
    })
  },
  onLoad: function () {
    console.log('onLoad')
    var that = this
    wx.request( {
      url: 'http://sep9.cn/qt5wix',
      data: {},
      header: {
        'Content-Type': 'application/json'
      },
      success: function( res ) {
        console.log( res.data )
          that.setData( {
            newList: res.data
          })
      }
    })
  }

})
```

再把index.wxml中赋值的字段改成服务器返回相应的字段，运行结果如下图：

![1]({{ site.url }}/images/blog/weixinxiaochengxu/20161019/2.gif)<br>

不知道什么原因，我这接口返回的图片url在微信小程序中无法显示，为了让效果更加的接近我们的效果图，在本地给我们的数据源加了些网络上的图片，代码如下：


```

data: {
    newList:[{fistImg:"http://img0.imgtn.bdimg.com/it/u=1640246403,1832676351&fm=21&gp=0.jpg"} ,
             {fistImg:"http://a.hiphotos.baidu.com/image/pic/item/c8ea15ce36d3d539be4d77b83f87e950352ab05c.jpg"} , 
             {fistImg:"http://h.hiphotos.baidu.com/image/pic/item/8d5494eef01f3a2922e765c99b25bc315c607c8d.jpg"} ,
             {fistImg:"http://c.hiphotos.baidu.com/image/pic/item/3b292df5e0fe9925ae23d95736a85edf8db1718d.jpg"} ,
             {fistImg:"http://g.hiphotos.baidu.com/image/pic/item/faedab64034f78f099a529f47b310a55b3191c0e.jpg"} ,
             {fistImg:"http://g.hiphotos.baidu.com/image/pic/item/bd315c6034a85edf9ba34e244b540923dd54758d.jpg"} ,
             {fistImg:"http://f.hiphotos.baidu.com/image/pic/item/00e93901213fb80e0ee553d034d12f2eb9389484.jpg"} ,
             {fistImg:"http://img1.imgtn.bdimg.com/it/u=2955244448,132069077&fm=21&gp=0.jpg"} ,
             {fistImg:"http://image.tianjimedia.com/uploadImages/2014/127/32/VP974HZ0AXL2.jpg"} ,
             {fistImg:"http://img0.imgtn.bdimg.com/it/u=1640246403,1832676351&fm=21&gp=0.jpg"} ,
             {fistImg:"http://img0.imgtn.bdimg.com/it/u=1640246403,1832676351&fm=21&gp=0.jpg"} ,
             {fistImg:"http://img0.imgtn.bdimg.com/it/u=1640246403,1832676351&fm=21&gp=0.jpg"} ,
             {fistImg:"http://img0.imgtn.bdimg.com/it/u=1640246403,1832676351&fm=21&gp=0.jpg"} ,
             {fistImg:"http://img0.imgtn.bdimg.com/it/u=1640246403,1832676351&fm=21&gp=0.jpg"} ,
             {fistImg:"http://img0.imgtn.bdimg.com/it/u=1640246403,1832676351&fm=21&gp=0.jpg"} ,
             {fistImg:"http://img0.imgtn.bdimg.com/it/u=1640246403,1832676351&fm=21&gp=0.jpg"} 
    ]
  }

```

随便弄几张图了，看看效果如何，😄


![1]({{ site.url }}/images/blog/weixinxiaochengxu/20161019/3.gif)<br>


本来还想做下详情页的，由于接口的详情是H5 ,貌似微信小程序不能直接加载H5，如有知道的朋友也可以给我留言告诉我，本人对于H5也是一窍不通😄。


[demo下载](https://github.com/AllLuckly/IT-Blog_Wechat)


本文为[Bison](https://allluckly.cn/)原创，转载请注明出处，否则将追究法律责任


----------------------------------------------------------



好文推荐：[分分钟解决iOS开发中App启动动画广告的功能](https://allluckly.cn/lblaunchimagead/LBLaunchImageAd)<br>
