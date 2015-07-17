---
layout: post
title: "iOS应用安全防护框架概述"
description: "Security for iOS Mobile Applications"
category: iOS
tags: [iOS应用安全攻防]
imagefeature: pic-2014-09-08.jpg
comments: true
mathjax: null
featured: true
published: true
---


攻易防难，唯有缜密、多层的防护网络才能可靠的保护我们iOS应用程序的安全。那么，一个完善的iOS应用安全防护框架都要写哪些东西呢？
<br>
首先，先梳理一下常见的逆向及攻击工具。  

#iOS应用逆向常用工具
* [Reveal](http://blog.csdn.net/yiyaaixuexi/article/details/18220875)
* [Cycript](http://blog.csdn.net/yiyaaixuexi/article/details/18317819)
* [Class-dump](http://blog.csdn.net/yiyaaixuexi/article/details/18353423)
* [Keychain-Dumper](http://blog.csdn.net/yiyaaixuexi/article/details/18404343)
* [gdb](http://blog.csdn.net/yiyaaixuexi/article/details/18520053)
* [iNalyzer](http://blog.csdn.net/yiyaaixuexi/article/details/18968125)
* [introspy](http://blog.csdn.net/yiyaaixuexi/article/details/18985131)
* [Fishhook](http://blog.csdn.net/yiyaaixuexi/article/details/19094765)
* [removePIE](http://blog.csdn.net/yiyaaixuexi/article/details/20391001)
* [IDA pro](https://www.hex-rays.com/index.shtml) or [Hopper](http://www.hopperapp.com/)
* [snoop-it](https://code.google.com/p/snoop-it/)
* [iDB](https://github.com/dmayer/idb)
* [Charles](http://www.charlesproxy.com/)
* [SSL Kill Switch](https://github.com/iSECPartners/ios-ssl-kill-switch)  

<br>

#裸奔app的安全隐患  
一部越狱的iOS设备，外加上述的逆向工具，给裸奔的iOS应用程序带来哪些威胁呢？ 
 
* 任意读写文件系统数据
* HTTP(S)实时被监测
* 重新打包ipa
* 暴露的函数符号
* 未加密的静态字符
* 篡改程序逻辑控制流
* 拦截系统框架API
* 逆向加密逻辑
* 跟踪函数调用过程（objc_msgSend）
* 可见视图的具体实现
* 伪造设备标识
* 可用的URL schemes
* runtime任意方法调用
* ……

<br>


#iOS应用安全防护开源工具
* ios-class-guard  
[ios-class-guard](https://github.com/Polidea/ios-class-guard)是对抗class-dump的利器，作用是将ObjC类名方法名等重命名为难以理解的字符。  

<br>

#iOS应用安全防护框架概述
针对上述安全隐患，我们的iOS应用安全防护框架需实现的任务大致如下：

##防护  
* ObjC类名方法名等重命名为难以理解的字符
* 加密静态字符串运行时解密
* 混淆代码使其难于反汇编
* 本地存储文件防篡改

##检测  
* 调试状态检测
* 越狱环境检测
* ObjC的Swizzle检测
* 任意函数的hook检测
* 指定区域或数据段的校验和检测

##自修复  
* 自修复被篡改的数据和代码段

<br>
<br>
   
此外，还需要多层的防护，通过高层保护低层的方式来保证整个防护机制不失效。   
参考IBM移动终端安全防护框架解决方案:
<div>
<img src="{{site.url}}/images/1410161600_5555.jpg" alt="test" itemprop="image" class="post-avatar img-responsive"/>
</div>
