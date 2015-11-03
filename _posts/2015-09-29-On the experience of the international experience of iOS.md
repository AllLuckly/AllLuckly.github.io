---
layout: post
title: "iOS开发之多国语言国际化经验浅谈"
description: "Bison"
category: iOS之国际化
headline: Discover the theme elements
tags: [iOS开发国际化，iOS开发本地化，iOS开发技巧，iOS开发，技术博客]
imagefeature: default_bg.jpg
comments: true
featured: 
mathjax: true
path: /images
---

>&quot;努力、努力、再努力，今天的付出，乃明天的收获&quot;
><small><cite title="Plato">Bison</cite></small>

>![1]({{ page.path }}/zjs.jpg)<br>
>[冰之依韩版女装](http://allluckly.taobao.com/)（程序媛福利）<br>


<br>



iOS多国语言国际化由于我个人也是第一次做，所以遇到了很多问题，<br>
在此我把我所遇到的一些问题分享给大家。<br>
最基础的怎么进行多国语言国际化在此就不老生常谈了，有兴趣的朋友可自行百度。<br>
<br>
1.首先我们说下翻译的格式：`"你好" = "hello"`;<br>
我们可以把需要翻译的文档制作成`"你好" = "";`这种Word文档<br>
每一种语言一个Word文档，这样你会发现，你做国际化的时候会快很多，<br>
不必到处找啊找的，我们这次搞得就是表格样式的，坑死人了，放翻译文档放的手都软了；<br>
<br>
2.我们尽量把同一个`VC`的词语翻译成差不多长的其他语言。<br>
大家可以想象一下如果你的一个布局里面有一排按钮，等分排练的，<br>
然后翻译的`title`一个好长一个非常短的，我们该这么去适配呢？而我们
最简单的做法是<br>
`btn.titleLabel.adjustsFontSizeToFitWidth = YES;`
想象一下当时我是有多痛苦了吗？所以说，当你看到这篇文章的时候说明你很庆幸，<br>
至少下次你遇到这样的需求你可以及时的和翻译说。<br>
<br>
3.由于某些国家的语言有很多种不同的系列，导致测试的时候会出现，这种语言缺失，<br>
其实不然，只是你在选择语言的时候少选了他的语种，就像中文一样，有简体和繁体中文。<br>
我这里最常见的有这么几种：<br>
西班牙语（最坑爹，我选了3个才搞定）<br>
丹麦语<br>
俄语<br>
葡萄牙语<br>
意大利语<br>

4.当初做项目的时候没管那么多，直接是只考虑了中文，然而国际版我们的项目需要<br>
减少一个`tabBarItem`所以通过判断是否为中文来判断的具体写法是写了个单例的类然<br>
后写的方法：<br>

{% highlight css %}
//判断是否为中文简体
- (BOOL)isSimpleChinese
{
    NSString *language = [[NSLocale preferredLanguages] firstObject];
    if ([language isEqualToString:@"zh-Hans"]) {
          return 1;
    }else{
        return 0;
    }
}
{% endhighlight %}
然而我们的运气貌似有点差，刚好碰上的iOS9升级，失效了，打开代码断点看看，<br>
原来是苹果IOS9增加了语言后面的地区代码，原来的`zh-Hanz`变成了`zh-Hanz-CN`<br>
能怎么办呢？当然是改代码咯。。。。下面是改过的代码<br>

{% highlight css %}
//判断是否为中文简体
- (BOOL)isSimpleChinese
{
    NSString *language = [[NSLocale preferredLanguages] firstObject];
    if ([language hasPrefix:@"zh-Hans"]) {
            return 1;
        }else {
            return 0;
        }
}
{% endhighlight %}

仔细的你是否发现了代码的不同之处啊？<br>

5.国际化一些有图片的地方，我们需要特别注意下取名哦，比如：<br>
`hello_en@2x.png`（英语）<br>
这样做的好处就是我们替换图片的时候只要判断下后缀是否是`en`<br>
就可以判断当前语言所需的图片下面我截个图给大家瞧瞧<br>

![屏幕快照 2015-09-29 上午9.40.17.png](http://upload-images.jianshu.io/upload_images/671504-cc907a133a676790.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)<br>
记得叫美工改好名字哦，我们用起来的时候就会方便快捷！<br>

暂时就发现这么多，大家有什么需要补充的也可以邮箱给我。<br>

版权归©Bison所有 任何转载请标明出处！<br>


 > [更多经验请点击](http://www.allluckly.cn/)

