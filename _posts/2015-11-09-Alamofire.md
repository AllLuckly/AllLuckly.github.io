---
layout: post
title: "Swift2.0后Alamofire的使用方法"
description: "Bison"
category: Swift
headline: Discover the theme elements
tags: [Swift2.0，Alamofire，iOS开发，iOS开发技巧，技术博客]
imagefeature: BG.jpg
comments: true
featured: true
mathjax: true
path: /images/blog/Alamofire
---

>&quot;iOS技术分享,iOS开发,iOS开发技巧,iOS开发博客&quot;
><small><cite title="Plato">Bison</cite></small>

>![1]({{ page.path }}/zjs.jpg)<br>
>[冰之依韩版女装](http://allluckly.taobao.com/)（程序媛福利）<br>


<br>


##第一部分，配置项目
在此只讲纯手打拉第三方框架的方法，`Pods`的自行百度哦！不懂`Pods`的可以点击传送
[传送门](http://allluckly.cn/cocoapods/CocoaPods%E5%AE%89%E8%A3%85%E5%8F%8A%E4%BD%BF%E7%94%A8/)
首先我们创建一个工程如下图

![1]({{ page.path }}/1.png)<br>

然后把下载的`Alamofire`解压文件全部放进创建的项目文件夹中，如下图

![2]({{ page.path }}/2.png)<br>

关键时刻到了哦，集中精神，注意！！！

![3]({{ page.path }}/3.png)<br>

这个图以后呢，就是最重要的时候了，请看好红色框框的部分，千万不要选择错了哦！！！

![4]({{ page.path }}/4.jpg)<br>


接着我们要把`Alamofire`的静态库加到工程里面来，具体操作如下图

![5]({{ page.path }}/5.png)<br>

再然后呢，我们导入`Alamofire`的头文件，运行下，看是否报错，不报错呢，我们导入的文件配置工程就是对的！
####PS
告诉大家一个小秘密，Bison发现第三方框架很多都是这个样子导入的哦！例如`HanekeSwift`


##第二部分，Bison教你怎么使用`Alamofire`

{% highlight css %}

import UIKit

import Alamofire

class ViewController: UIViewController {

    let BaiduURL = "http://apis.haoservice.com/lifeservice/cook/query?"

override func viewDidLoad() {
    super.viewDidLoad()
    //网络请求
    self .reloadData()
}

func reloadData(){


    let parameters = [
    "menu": "土豆",
    "pn":  1,
    "rn": "10",
    "key": "2ba215a3f83b4b898d0f6fdca4e16c7c",
    ]


    Alamofire.request(.POST, BaiduURL, parameters:parameters ).responseJSON {response in

    //            debugPrint(response)
    switch response.result {
        case .Success:
            //把得到的JSON数据转为字典
            if let j = response.result.value as? NSDictionary{
                //获取字典里面的key为数组
                let Items = j.valueForKey("result")as! NSArray
            //便利数组得到每一个字典模型
            for dict in Items{

                print(dict)
            }

        }
        case .Failure(let error):

            print(error)
        }


        }

    }

}

{% endhighlight %}

<br>

到此我们的教程就结束了，有什么问题可以留言哦！会抽空解答大家的疑问<br>

> [更多经验请点击](http://www.allluckly.cn/)<br>

好文推荐：[iOS开发内购全套图文教程](http://www.jianshu.com/p/05a3087cd796)<br>

原文在：http://www.allluckly.cn/

<br>
版权归©Bison所有 如需转载请保留原文超链接地址！否则后果自负！






