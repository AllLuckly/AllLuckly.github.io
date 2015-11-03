---
layout: post
title: iOS开发CocoaPods安装及使用
description: "Bison"
headline: ""
categories: CocoaPods
tags: [CocoaPods，iOS开发，iOS开发技巧，技术博客]
imagefeature: ""
imagecredit: 
imagecreditlink: ""
comments: true
mathjax: null
featured: true
published: true
path: /images
---

>&quot;The beginning is the most important part of the work.&quot;
><small><cite title="Plato">Plato</cite></small>
>![1]({{ page.path }}/zjs.jpg)<br>
>[冰之依韩版女装](http://allluckly.taobao.com/)（程序媛福利）
1.安装Brew

`ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"`  
2.更新Ruby

`brew install ruby`

3.安装CocoaPods

首先： `sudo gem install cocoapods`   
如果没反应  `gem sources --remove https://rubygems.org/`     
//等有反应之后再敲入以下命令
`gem sources -a http://ruby.taobao.org/`
为了验证你的Ruby镜像是并且仅是taobao，可以用以下命令查看：

`gem sources -l`

只有在终端中出现下面文字才表明你上面的命令是成功的：
*** CURRENT SOURCES ***

http://ruby.taobao.org/
这时候，你再次在终端中运行：`sudo gem install cocoapods`

等待十几秒
然后：`pod setup`

4.使用Search命令来看看你需要的第三方库是否存在!

`pod search SDWebImage `

5.创建Podfile

`cd` +项目的路径 然后再创建

`touch Podfile`

6. 然后在Podfile文件中输入以下文字：
`platform :ios, '7.0'
pod "SDWebImage", "~> 2.0"  `

7.最后 `esc  :wq`

8. 运行 `pod install `

如果需要再加第三方框架到CocoaPods中时 需要`pod search` 第三方框架名  选择最新的版本加到 Podfile 文件中！然后 `pod install`。

注意最后一句话，意思是：以后打开项目就用 .xcworkspace 打开，而不是之前的.xcodeproj文件。

使用`CocoaPods` 导入第三方库头文件不自动补齐时解决方法

选择`Target -> Build Settings` 菜单，找到`\”User Header Search Paths\”`设置项
新增一个值`"${SRCROOT}"`，并且选择`\”Recursive\”`，这样xcode就会在项目目录中递归搜索文件
自动补齐功能马上就好使了。

你也许会郁闷，为什么会出现.xcworkspace文件呢。这正是你刚刚运行`$ pod install`命令产生的新文件。除了这个文件，你会发现还多了另外一个文件“Podfile.lock”和一个文件夹“Pods”。




