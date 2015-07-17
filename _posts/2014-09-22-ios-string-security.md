---
layout: post
title: "iOS字符串安全"
description: "Security for strings in iOS"
category: iOS
tags: [iOS应用安全攻防]
imagefeature: blog/bg.jpg
comments: true
mathjax: null
featured: false
published: true
---


一个编译成功的可执行程序，其中已初始化的字符串都是完整可见的。
<br>
针对于iOS的Mach-O二进制通常可获得以下几种字符串信息：  

* 资源文件名  
* 可见的函数符号名  
* SQL语句
* format
* 通知名
* 对称加密算法的key

<br>

##攻击者如何利用字符串

资源文件名通常用来快速定位逆向分析的入口点。  
想要知道判断购买金币成功与否的代码位置？只要确定购买成功时播放的音频文件名字或者背景图名字就可以顺藤摸瓜了。  

kLoginSuccessNotification类似这种通知名称格外炸眼，利用Cycript发个此通知试试，也许会有什么意外收获。  

拿到对称加密算法的key是件很幸福的事情。

……

<br>


##字符串异或加解密

是的，字符串需要加密处理，但只需要对高度敏感字符数据做加密，比如对称加密算法的key。  
其他的，需要提高编程安全意识来弥补。  

常规办法是通过异或来加解密，来写个sample code：  

{% highlight Objective-C %}
static unsigned char XOR_KEY = 0xBB;

void xorString(unsigned char *str, unsigned char key)
{
    unsigned char *p = str;
    while( ((*p) ^=  key) != '\0')  p++;
}

- (void)testFunction
{
    unsigned char str[] = {(XOR_KEY ^ 'h'),
                           (XOR_KEY ^ 'e'),
                           (XOR_KEY ^ 'l'),
                           (XOR_KEY ^ 'l'),
                           (XOR_KEY ^ 'o'),
                           (XOR_KEY ^ '\0')};
    xorString(str, XOR_KEY);
    static unsigned char result[6];
    memcpy(result, str, 6);
    NSLog(@"%s",result);      //output: hello
}
{% endhighlight %}


这样就无法从二进制中直接分析得到字符串“hello”了。   
扔进IDA里分析一下，发现效果不好，连续存储的'h'、'e'等字符还是暴露了可读的"hello"。  

<div>
<img src="{{ site.url }}/images/blog/20140922-strings1.png" alt="test" itemprop="image" class="post-avatar img-responsive"/>
</div>

改进一下，取消`XOR_KEY`独立变量的身份，改为宏，作为数据直接插入。  

{% highlight Objective-C %}
#define XOR_KEY 0xBB

void xorString(unsigned char *str, unsigned char key)
{
    unsigned char *p = str;
    while( ((*p) ^=  key) != '\0')  p++;
}

- (void)testFunction
{
    unsigned char str[] = {(XOR_KEY ^ 'h'),
                           (XOR_KEY ^ 'e'),
                           (XOR_KEY ^ 'l'),
                           (XOR_KEY ^ 'l'),
                           (XOR_KEY ^ 'o'),
                           (XOR_KEY ^ '\0')};
    xorString(str, XOR_KEY);
    static unsigned char result[6];
    memcpy(result, str, 6);
    NSLog(@"%s",result);      //output: hello
}
{% endhighlight %}  

<div>
<img src="{{ site.url }}/images/blog/20140922-strings2.png" alt="test" itemprop="image" class="post-avatar img-responsive"/>
</div>

嗯这下好多了。


<br>
<br>
 

