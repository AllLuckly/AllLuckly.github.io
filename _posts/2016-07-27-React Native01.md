---
layout: post
title: "React Native在Mac上部署iOS开发环境"
description: "Bison"
category: React Native
headline: Discover the theme elements
tags: [React Native, iOS开发, 部署环境]
imagefeature: 
comments: true
featured: true
mathjax: 
path: /images
---

1.如果Mac上没有安装[Homebrew](http://brew.sh/)请按如下步骤安装

- 打开终端输入如下代码

```

ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"

```

- 更新Ruby(版本过低部分组件无法安装)

`brew install ruby`

2.安装[Node.js](https://nodejs.org/)

在这里我使用的是直接下载安装[Node.js](https://nodejs.org/)： [https://nodejs.org/en/download/](https://nodejs.org/en/download/)
简单方便。

3.安装 [watchman](https://facebook.github.io/watchman/docs/install.html) 和 [flow](http://www.flowtype.org/)操作分别执行以下俩代码

```
brew install watchman

brew install flow
```
3.安装 React-Native

```
sudo  npm install -g react-native-cli
```
然后输入开机密码，如果成功会有如下提示


![1]({{ site.url }}/images/blog/React Native/1.png)<br>

到此环境配置完毕，我们创建一个项目试试看，通过如下代码创建

```
react-native init testProject
```

testProject 为项目名，可随意，等待 **一段时间之后**（具体视网络情况而定），项目初始化完成。如果成功则有如下提示

![1]({{ site.url }}/images/blog/React Native/2.png)<br>

4.进入项目

`cd testProject `

可以看到如下目录

```
golddeMac-mini: testProject gold$ ls -l
total 24
drwxr-xr-x  10 gold  staff   340  7 27 10:46 android
-rw-r--r--   1 gold  staff  1103  7 27 10:46 index.android.js
-rw-r--r--   1 gold  staff  1069  7 27 10:46 index.ios.js
drwxr-xr-x   5 gold  staff   170  7 27 10:46 ios
drwxr-xr-x   5 gold  staff   170  7 27 10:46 node_modules
-rw-r--r--   1 gold  staff   238  7 27 10:46 package.json

```

![1]({{ site.url }}/images/blog/React Native/3.png)<br>

其中 android 和 ios 中分别为两个平台的项目文件。index.android.js 和 index.ios.js 为两个页面对应的 js 文件。

5.运行项目

iOS 还是非常简单，XCode 打开项目，点击运行就好。修改 index.ios.js, 在模拟器中 ⌘ + R 重新载入 js 即可看到相应的变化。

iOS 真机调试也简单，修改HTTP地址即可。

```
jsCodeLocation = [NSURL URLWithString:@"http://localhost:8081/index.ios.bundle"];

```
运行成功的效果图如下

![1]({{ site.url }}/images/blog/React Native/4.png)<br>

参考文档:[react-native官方文档]([https://facebook.github.io/react-native/docs/getting-started.html#content](https://facebook.github.io/react-native/docs/getting-started.html#content))

有问题欢迎留言，对你有帮助随手点喜欢。后续如果有时间的话，会一直更新学习React Native的一些心得与体会。
