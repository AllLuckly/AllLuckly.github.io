---
layout: post
title: "Bison眼中的iOS开发多线程是这样的（一）"
description: "Bison"
category: 多线程
headline: Discover the theme elements
tags: [多线程，NSThread，NSOperationQueue，GCD，技术博客]
imagefeature: BG2.jpg
comments: true
featured: 
mathjax: true
path: /images
---


>&quot;对于单线程的应用而言，整个应用只是一个顺序执行流，当执行到某个耗时操作时，主线程就会被阻塞，应用就卡在那无法继续执行，因此单线程的应用体验度很低，总感觉像手机卡似得，就像一条小河北阻塞了，只有打通了才能继续有水流到下一个地方放一样。而多线程则更像一条河有无数的分支，这条阻塞了还有其他的分支在运行，影响不到大局。&quot;



不知道大家面试iOS软件工程师的时候有没有遇到问多线程的？反正我遇到的还是蛮多的。下面是我面试时候的一个小场景！有点不堪🙈，看完不许笑啊.....<br>

面试官：你平常在开发中有用到多线程吗？<br>

我：有！<br>

面试官：那你说说你在开发的时候都有哪些场景用到多线程啊？<br>

我：很多场景...（气氛瞬间有点不对劲了😓）<br>

面试官：那你说说多线程都有哪些框架？<br>

我：`NSThread`、`NSOperationQueue`、`GCD`（很洋气的用英语讲出来😄）<br>

面试官：说说你理解的三者的优缺点（气氛稍稍有点缓解）<br>

我：（网上看到过就背下来了，心里有点小得意，滔滔不绝的说完如下话语）<br>
1.NSThread:<br>

> 使用NSThread对象建立一个线程非常方便;

<br>

> 但是要使用NSThread管理多个线程非常困难,不推荐使用;

<br>

> 技巧!使用[NSThread currentThread]跟踪任务所在线程,适用于这三种技术.

<br>

2.NSOperation/NSOperationQueue:<br>

> 是使用GCD实现的一套Objective-C的API;<br>

<br>

> 是面向对象的多线程技术;

<br>

> 提供了一些在GCD中不容易实现的特性,如:限制最大并发数量,操作之间的依赖关系.

3.GCD---Grand Central Dispatch:

> 是基于C语言的底层API;<br>

<br>

> 用Block定义任务,使用起来非常灵活便捷;<br>

<br>

> 提供了更多的控制能力以及操作队列中所不能使用的底层函数.<br>

面试官：面无表情的说，回去等通知.....（结果..........大家懂的😂）<br>
这就是Bison刚出道时眼中的多线程😄<br>
这种局面，究根结底，是自己对底层的东西不够透彻只停留在怎么去使用它，而不知道底层是怎么实现的。下面让我很严肃的和大家说说多线程到底是一个什么样子的！

对于单线程的应用而言，整个应用只是一个顺序执行流，当执行到某个耗时操作时，主线程就会被阻塞，应用就卡在那无法继续执行，因此单线程的应用体验度很低，总感觉像手机卡似得，就像一条小河北阻塞了，只有打通了才能继续有水流到下一个地方放一样。而多线程则更像一条河有无数的分支，这条阻塞了还有其他的分支在运行，影响不到大局。希望我的比喻够恰当啊.......😄
iOS开发平台提供了非常优秀的多线程支持，程序可以通过很简单的方式来开启多线程，提供了我上述场景所说的多线程编程。总之iOS已经降低了开发多线程应用的繁琐，让开发者能轻松、简单的开发多线程应用。
几乎所有的操作系统都支持同时运行多个任务，一个任务通常就是一个程序，每个运行的程序就是一个进程。当一个程序运行时，内部可能包含了多个顺序执行流，每个执行流就是一个线程。在此就不得不说下进程和线程有什么区别了，很早以前我还是会混淆的哦😂。下面是我的理解....
仅供参考

> 当一个程序进入内存运行后，即变成了一个进程。进程是处于运行过程中的程序，并且具有一定的独立功能，是系统进行资源分配和调度的一个独立单位。

<br>

> 线程是进程的组成部分，一个进程可以拥有多个线程，而一个线程必须拥有一个父进程，线程可以拥有自己的堆栈、自己的程序计数器和自己的局部变量，但不再拥有系统资源，与父进程中的其他线程共享该进程所拥有的全部资源。也因此多线程编程更加的方便；值得注意的是确保每个线程不会妨碍该进程的其他线程。

通过上面的啰嗦，我想大家对多线程都有一定的了解了。在此总结一下多线程编程的几个优点，如有遗漏，欢迎留言补充：

- 进程间不能共享内存，但线程之间共享内存非常容易。
- 系统创建进程需要为该进程重新分配系统资源，但创建线程则代价小的多，因此使用多线程来实现多任务并发比多进程的效率高。
- iOS提供了多种多线程实现方式，从而简化了iOS的多线程编程。

接下来Bison将分别讲解iOS开发多线程中的用法

##NSThread

iOS使用`NSThread `类代表线程，创建新线程也就是创建`NSThread `对象。
创建`NSThread `有俩种方式。



{% highlight css %}
//创建一个新线程对象
- (instancetype)initWithTarget:(id)target selector:(SEL)selector object:(nullable id)argument NS_AVAILABLE(10_5, 2_0);
//创建并启动新线程
+ (void)detachNewThreadSelector:(SEL)selector toTarget:(id)target withObject:(nullable id)argument;
{% endhighlight %}

上面俩种方式的本质都是将`target`对象的`selector`方法转换为线程执行体，其中`selector`方法最多可以接收一个参数，而`argument`就代表传给`selector`方法的参数。
这俩种创建新线程的方式并没有明显的区别，只是第一种方式是一个实例化方法，该方法返回一个`NSThread `对象，必须调用 `start`方法启动线程：另一种不会返回`NSThread `对象，因此这种方法会直接创建并启动新线程。
下面我们随便举个栗子，代码如下



{% highlight css %}
- (void)viewDidLoad
{
    [super viewDidLoad];
    for(int i = 0 ; i < 100 ; i++)
    {
        NSLog(@"===%@===%d" , [NSThread currentThread].name , i);
    if(i == 7)
    {
        // 创建线程对象
        NSThread *thread = [[NSThread alloc]initWithTarget:self
        selector:@selector(run) object:nil];
        // 启动新线程
        [thread start];
        // 创建并启动新线程
        //			[NSThread detachNewThreadSelector:@selector(run) toTarget:self
        //				withObject:nil];
        }
    }
}
- (void)run
{
    for(int i = 0 ; i < 100 ; i++)
    {
        NSLog(@"-----%@----%d" , [NSThread currentThread].name, i);
    }
}
{% endhighlight %}
运行一下，打印日志如下：



{% highlight css %}
//主线程正在运行
2016-01-12 14:30:46.400 NSThreadTest[7498:104912] ======0
2016-01-12 14:30:46.401 NSThreadTest[7498:104912] ======1
2016-01-12 14:30:46.401 NSThreadTest[7498:104912] ======2
2016-01-12 14:30:46.401 NSThreadTest[7498:104912] ======3
2016-01-12 14:30:46.401 NSThreadTest[7498:104912] ======4
2016-01-12 14:30:46.401 NSThreadTest[7498:104912] ======5
2016-01-12 14:30:46.401 NSThreadTest[7498:104912] ======6
2016-01-12 14:30:46.402 NSThreadTest[7498:104912] ======7
2016-01-12 14:30:46.402 NSThreadTest[7498:104912] ======8
//新线程开始运行
2016-01-12 14:30:46.402 NSThreadTest[7498:104956] ---------0
2016-01-12 14:30:46.402 NSThreadTest[7498:104912] ======9
2016-01-12 14:30:46.402 NSThreadTest[7498:104956] ---------1
2016-01-12 14:30:46.402 NSThreadTest[7498:104912] ======10
2016-01-12 14:30:46.402 NSThreadTest[7498:104956] ---------2
2016-01-12 14:30:46.402 NSThreadTest[7498:104912] ======11
2016-01-12 14:30:46.402 NSThreadTest[7498:104912] ======12
2016-01-12 14:30:46.402 NSThreadTest[7498:104956] ---------3
................
{% endhighlight %}
由上不难看出，这是俩个线程并发执行的效果。除此之外上面的🌰还用到了
`+ (NSThread *)currentThread;`方法，该方法总是返回当前正在执行的线程对象。

当线程被创建并启动以后，它既不是一启动就进入了执行状态，也不是一直处于执行状态。即使线程开始运行以后，它也不可能一直“霸占”着CPU独自运行，所以CPU需要再多个线程之间切换，于是线程状态也会多次在运行、就绪状态之间的切换。
当程序创建了一个线程之后，该线程就处于新建状态，此时它和其他Objective-C对象一样，仅仅由系统为其分配了内存，并初始化了其他成员变量的值。此时的线程对象没有表现出任何线程的动态特征，程序也不会执行线程的线程执行体。
当线程对象调用了`start`方法之后，该线程处于就绪状态，系统会为其创建方法调用栈和程序计数器，处于这种状态中的线程并没有开始运行，它只是表示该线程可以运行了。至于该线程何时运行，取决于系统的调度。

####终止子线程

线程会以如下3中方式之一结束，结束后就处于死亡状态。

> 线程执行体方法执行完成，线程正常结束。

<br>

> 线程执行过程中出现了错误。

<br>

>直接调用`NSThread `类的exit方法来终止当前正在执行的线程。


为了测试木个线程是否正在运行，可以调用线程对象的`isExecuting`、`isFinished`方法，当线程正处于执行过程中时，调用`isExecuting`方法会返回YES,当线程执行完后，调用`isFinished`方法也返回YES。
如果希望在UI线程中终止子线程，`NSThread `并没有提供方法来终止某个子线程，虽然提供了`cancel`方法，但该方法仅仅只是改变该线程的状态，导致该线程的isCancelled方法返回NO，而不是真正终止该线程。
为了在UI线程中终止子线程，可以向子线程发送一个信号，然后在子线程的线程执行体方法中进行判断，如果子线程收到过终止信号，程序应该调用`exit`方法来终止当前正在执行的循环。下面举个🌰，代码如下：


{% highlight css %}
NSThread* thread;
- (void)viewDidLoad
{
    [super viewDidLoad];
    // 创建新线程对象
    thread = [[NSThread alloc] initWithTarget:self selector:@selector(run)
    object:nil];
    // 启动新线程
    [thread start];
}
- (void)run
{
    for(int i = 0 ; i < 100 ; i++)
    {
        if([NSThread currentThread].isCancelled)
    {
        // 终止当前正在执行的线程
        [NSThread exit];
    }
    NSLog(@"-----%@----%d" , [NSThread currentThread].name, i);
    // 每执行一次，线程暂停0.5秒
    [NSThread sleepForTimeInterval:0.5];
}
}
- (IBAction)cancelThread:(id)sender
{
    // 取消thread线程，调用该方法后，thread的isCancelled方法将会返回NO
    [thread cancel]; 
}
{% endhighlight %}
如果需要让当前正在执行的线程暂停一段时间，并进入阻塞状态，则可以通过调用如下方法。


{% highlight css %}
//  让当前正在执行的线程暂停到date代表的时间，并进入阻塞状态。
+ (void)sleepUntilDate:(NSDate *)date;
//  让当前正在执行的线程暂停到ti秒，并进入阻塞状态。
+ (void)sleepForTimeInterval:(NSTimeInterval)ti;
{% endhighlight %}

每个线程执行时都具有一定的优先级，优先级高的线程获得较多的执行机会，而优先级的则反之。每个子线程默认的优先级是0.5.
`NSThread `通过如下代码演示优先级。
<br>


{% highlight css %}
- (void)viewDidLoad
{
    [super viewDidLoad];
    NSLog(@"UI线程的优先级为：%g" , [NSThread threadPriority]);
    // 创建第一个线程对象
    NSThread* thread1 = [[NSThread alloc]
    initWithTarget:self selector:@selector(run) object:nil];
    // 设置第一个线程对象的名字
    thread1.name = @"线程A";
    NSLog(@"线程A的优先级为：%g" , thread1.threadPriority);
    // 设置使用最低优先级
    thread1.threadPriority = 0.0;
    // 创建第二个线程对象
    NSThread* thread2 = [[NSThread alloc]
    initWithTarget:self selector:@selector(run) object:nil];
    // 设置第二个线程对象的名字
    thread2.name = @"线程B";
    NSLog(@"线程B的优先级为：%g" , thread2.threadPriority);
    // 设置使用最高优先级
    thread2.threadPriority = 1.0;
    // 启动2个线程
    [thread1 start];
    [thread2 start];
}
- (void)run
{
    for(int i = 0 ; i < 100 ; i++)
    {
        NSLog(@"-----%@----%d" , [NSThread currentThread].name, i);
    }
}
{% endhighlight %}

运行所得日志如下

{% highlight css %}
2016-01-12 16:26:26.451 PriorityTest[10135:150983] UI线程的优先级为：0.5
//新线程默认优先级
2016-01-12 16:26:26.452 PriorityTest[10135:150983] 线程A的优先级为：0.5
2016-01-12 16:26:26.452 PriorityTest[10135:150983] 线程B的优先级为：0.5
//改变优先级后，优先级高的线程，获取更多的执行机会
2016-01-12 16:26:26.453 PriorityTest[10135:151058] -----线程B----0
2016-01-12 16:26:26.453 PriorityTest[10135:151058] -----线程B----1
2016-01-12 16:26:26.453 PriorityTest[10135:151058] -----线程B----2
2016-01-12 16:26:26.454 PriorityTest[10135:151058] -----线程B----3
2016-01-12 16:26:26.454 PriorityTest[10135:151058] -----线程B----4
2016-01-12 16:26:26.454 PriorityTest[10135:151058] -----线程B----5
2016-01-12 16:26:26.454 PriorityTest[10135:151058] -----线程B----6
2016-01-12 16:26:26.465 PriorityTest[10135:151056] -----线程A----0
{% endhighlight %}
今天暂时写到这吧....，有点长了😄

> [Bison眼中的iOS开发多线程是这样的（二）](http://allluckly.cn/多线程/duoxiancheng02)

----------------------------------------------------------

> [博主app上线啦，快点此来围观吧](https://itunes.apple.com/us/app/it-blog-zi-xueios-kai-fa-jin/id1067787090?l=zh&ls=1&mt=8)<br>

> 原文地址：[http://allluckly.cn](http://allluckly.cn)<br>

好文推荐：[详解持久化Core Data框架的原理以及使用](http://allluckly.cn/持久化/chijiuhua01)<br>

版权归©Bison所有 如需转载请保留原文超链接地址！否则后果自负！





