---
layout: post
title: "App Extension的脱壳办法"
description: "Dumps decrypted mach-o files from encrypted app extensions to a file"
category: iOS
tags: [iOS应用安全攻防]
imagefeature: blog/bg.jpg
comments: true
mathjax: null
featured: false
published: true
---


从app store下载的app和app extension是加过密的，可以通过otool查看:
`$ otool -l binary_name | grep crypt`  
{% highlight C %}
cryptoff  16384
cryptsize 294912
cryptid   1
{% endhighlight %}

<br>


## iPhone applications的解密办法  
[dumpdecrypted](https://github.com/stefanesser/dumpdecrypted) 是个出色的app脱壳开源工具，它的原理是：将应用程序运行起来（iOS系统会先解密程序再启动），然后将内存中的解密结果dump写入文件中，得到一个新的可执行程序。


<br>



## iPhone app extensions的特别之处
* app extension虽是独立进程，但不可独立运行   
* app extension的进程中，写权限被严格控制  

基于以上两点，[dumpdecrypted](https://github.com/stefanesser/dumpdecrypted) 无法实现对iPhone app extensions的脱壳。


<br>



## iPhone app extensions的解密办法
通过对[dumpdecrypted](https://github.com/stefanesser/dumpdecrypted)稍作修改，更改其写入dump结果的path，变通启动方式就可实现对app extension的解密，详见：[Carina's dumpdecrypted](https://github.com/CarinaTT/dumpdecrypted)

使用方法很简单，用微信的Share Extension为例    
1）本地编译好 dumpdecrypted.dylib   
2）指定作用的Extension Bundle  
{% highlight xml %}
{
	Filter = {
		Bundles = ("com.tencent.xin.sharetimeline");
	};
}
{% endhighlight %}
3）将 `dumpdecrypted.plist` 和 `dumpdecrypted.dylib` 拷贝至越狱机的 `/Library/MobileSubstrate/DynamicLibraries/` 下  
4）利用系统相册启动微信的Share Extension

当微信的Share Extension被启动时，解密插件自动工作。值得注意的是，如果你的越狱机是armv7架构，那么也就只dump armv7那部分；如果越狱机是arm64架构，那么也就只dump arm64那部分。So，最后你需要:  
`$ lipo -thin armv7 xxx.decrypted -output xxx_armv7.decrypted`  或   
`$ lipo -thin armv64 xxx.decrypted -output xxx_arm64.decrypted` 来得到干净的dump结果 

<br>


 
