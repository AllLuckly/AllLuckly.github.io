---
layout: post
title: "Swift初探之纯代码写tabBar"
description: "Bison"
category: Swift
headline: Discover the theme elements
tags: [Swift纯代码，swift tabBar，iOS开发技巧，swift自学，技术博客]
imagefeature: default_bg7.png
comments: true
featured: 
mathjax: true
path: /images
---

>&quot;充实自我，提升自我的价值；唯有多学&quot;
><small><cite title="Plato">Bison</cite></small>

>![1]({{ site.url }}/images/zjs.jpg)<br>
>[冰之依韩版女装](http://allluckly.taobao.com/)（程序媛福利）

最近的项目新版本基本完成了,闲来无事学习学习新出的语言Swift。
对于有OC基础的人来说学习Swift还是很简单的，下面是我自学写的Tabbar，当<br>
然这并不是自定义的。不过对于一般的需求还是可以满足的。<br>
下面是我仿“折800”写的一个Tabbar，由于图片原因导致有点小小的瑕疵<br>

代码如下<br>

 > [更多经验请点击](http://www.allluckly.cn/)

核心代码


{% highlight css %}

class func CusTomTabBar() ->UITabBarController{

var vc1 = Home_VC()
var vc2 = Class_VC()
var vc3 = Brand_VC()
var vc4 = Shoping_VC()
var vc5 = Personal_VC()
var nvc1:UINavigationController = LBNvc(rootViewController: vc1)
var nvc2:UINavigationController = LBNvc(rootViewController: vc2)
var nvc3:UINavigationController = LBNvc(rootViewController: vc3)
var nvc4:UINavigationController = LBNvc(rootViewController: vc4)
var nvc5:UINavigationController = LBNvc(rootViewController: vc5)
let tabbar1 = UITabBarItem(title: "首页", image: (Public .getImgView("home_tab_home_btn@2x")) , selectedImage: (Public .getImgView("home_tab_home_selected_btn@2x")))
let tabbar2 = UITabBarItem(title: "分类", image: (Public .getImgView("home_tab_saunter_btn@2x")), selectedImage: (Public .getImgView("home_tab_saunter_selected_btn@2x")))
let tabbar3 = UITabBarItem(title: "品牌团", image: (Public .getImgView("home_tab_branc_btn@2x")), selectedImage: (Public .getImgView("home_tab_branc_selected_btn@2x")))
let tabbar4 = UITabBarItem(title: "积分商城", image: (Public .getImgView("home_tab_point_btn@2x")), selectedImage: (Public .getImgView("home_tab_point_selected_btn@2x")))
let tabbar5 = UITabBarItem(title: "个人中心", image: (Public .getImgView("home_tab_personal_btn@2x")), selectedImage: (Public .getImgView("home_tab_personal_selected_btn@2x")))
nvc1.tabBarItem = tabbar1;
nvc2.tabBarItem = tabbar2;
nvc3.tabBarItem = tabbar3;
nvc4.tabBarItem = tabbar4;
nvc5.tabBarItem = tabbar5;
var tc = UITabBarController()

tc.tabBar.tintColor = UIColor .redColor()
//        tc.tabBar.backgroundImage = Public.getImgView("3.png")
tc.viewControllers = [nvc1,nvc2,nvc3,nvc4,nvc5];
return tc;
}
 


{% endhighlight %}

> [博主app上线了，赶紧点此来围观吧😄](https://itunes.apple.com/us/app/it-blog-zi-xueios-kai-fa-jin/id1067787090?l=zh&ls=1&mt=8)<br>

> [点击下载Demo](https://github.com/AllLuckly/LBSwift_TabBar) <br>

![(LBSwift_TabBar)](https://github.com/AllLuckly/LBSwift_TabBar/blob/master/123.gif?raw=true)

