---
layout: post
title: "Bison眼中的iOS开发多线程是这样的（三）"
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




前面在《[Bison眼中的iOS开发多线程是这样的（二）](http://allluckly.cn/多线程/duoxiancheng02/)》一文中讲完了多线程的`NSThread`，不难发现这种方式的多线程实现起来非常的复杂，为了简化多线程的开发，iOS提供了GCD来实现多线程。GCD有俩个核心的概念:<br>

> 队列:队列负责管理开发者提交的任务，GCD队列始终以先进先出的方式来处理任务，但由于任务的执行时间并不相同，因此先处理的任务并不一定先结束。队列既可是串行队列，也可是并发队列，串行队列每次只处理一个任务，必须前一任务完成后，才会执行下一任务；并放队列则可同时处理多个任务，So将会有多个任务并发执行。队列底层会维护一个线程池来处理用户提交的任务，线程池的作用就是执行队列管理的任务。串行队列底层的线程池只要维护一个线程即可，并发队列则想反。<br>

> 任务:任务则为用户提交给队列的工作单元，这些任务将会提交给队列底层维护的线程池执行，因此这些任务会以多线程的方式执行。<br>

综上所述，不难发现，使用GCD只需俩步即可。<br>

1.创建队列。<br>
2.将任务提交给队列。<br>

接下来我让我们详细的玩一玩这GCD把😄<br>

> 首先咱先创建队列<br>

```
//获取当前执行代码所在的队列（已废弃）
dispatch_get_current_queue(void);

/*根据制定优先级、额外的旗标来获取系统的全局并发队列，第一个参数指定dispatch queue的优先级，取值可以是DISPATCH_QUEUE_PRIORITY_HIGHT、DISPATCH_QUEUE_PRIORITY_DEFAULT、DISPATCH_QUEUE_PRIORITY_LOW或DISPATCH_QUEUE_PRIORITY_BACKGROUND（iOS 5.0加入的）; 第二个参数，目前只能为0或NULL
*/
dispatch_get_global_queue(long identifier, unsigned long flags);

//获取主线程相关联的串行队列
dispatch_get_main_queue(void)

/*
    根据指定字符串标签创建队列。第二个参数可控制创建串行队列还是并发队列，如果将第二个参数设置为“DISPATCH_QUEUE_SERIAL”,则为串行
    设为“DISPATCH_QUEUE_CONCURRENT”为并发队列。在没有启动ARC机制的情况下，通常这种方式创建的队列需要调用dispatch_release()释放引用计数
*/
dispatch_queue_create(const char *label, dispatch_queue_attr_t attr);

//获取指定队列的字符串标签，dispatch_queue_t代表一个队列
dispatch_queue_get_label(dispatch_queue_t queue);

```
根据上面的方法，可以创建如下几种队列<br>

1.获取系统默认的全局并发队列<br>

```
dispatch_queue_t queue = dispatch_get_global_queue(DISPATCH_QUEUE_PRIORITY_DEFAULT, 0);

```

2.获取系统主线程关联的串行队列<br>

```
dispatch_queue_t queue = dispatch_get_main_queue();

```

3.创建串行队列<br>

```
dispatch_queue_t queue = dispatch_queue_create("Bison", DISPATCH_QUEUE_SERIAL);

```

4.创建并发队列<br>

```
dispatch_queue_t queue = dispatch_queue_create("Bison", DISPATCH_QUEUE_CONCURRENT);

```

### 异步提交任务<br>

iOS提供了如下函数来向队列提交任务。下面这些函数很多都有俩个版本:一个接收代码块作为参数的版本，一个接收函数作为参数的版本；其中接收函数的函数名最多多了_f后缀，而且会多一个参数，用于向函数传入应用程序定义的上下文。<br>

```
//将代码块以异步方式提交给指定队列，该队列底层的线程池将负责执行该代码块
dispatch_async(dispatch_queue_t queue, dispatch_block_t block);

//将函数以异步方式提交给指定队列，该队列底层的线程池将负责执行该函数
dispatch_async_f(dispatch_queue_t queue,void *context,dispatch_function_t work);

//将代码块以同步方式提交给指定队列，该队列底层的线程池将负责执行该代码块
dispatch_sync(dispatch_queue_t queue, dispatch_block_t block);

//将函数以同步方式提交给指定队列，该队列底层的线程池将负责执行该函数
dispatch_sync_f(dispatch_queue_t queue,void *context,dispatch_function_t work);

//将代码块以异步方式提交给指定的队列，该队列底层的线程池将负责在when指定的时间点执行该代码块
dispatch_after(dispatch_time_t when,dispatch_queue_t queue,dispatch_block_t block);

//将函数以异步方式提交给指定的队列，该队列底层的线程池将负责在when指定的时间点执行该函数
dispatch_after_f(dispatch_time_t when,dispatch_queue_t queue,void *context,dispatch_function_t work);

//将代码块以异步方式提交给指定的队列，该队列底层的线程池将多次重复执行该代码块
dispatch_apply(size_t iterations, dispatch_queue_t queue,void (^block)(size_t));

//将函数以异步方式提交给指定的队列，该队列底层的线程池将多次重复执行该函数
dispatch_apply_f(size_t iterations, dispatch_queue_t queue,void *context,void (*work)(void *, size_t));


//将代码块提交给指定队列，该队列底层的线程池控制在应用的某个生命周期内仅执行一次。predicate 是指向dispatch_once_t变量的指针，判断是否已经执行过，runtime中很常用
dispatch_once(dispatch_once_t *predicate, dispatch_block_t block);


```

下面是简单的几个案例<br>

    // 定义2个队列
    dispatch_queue_t serialQueue;
    dispatch_queue_t concurrentQueue;
    - (void)viewDidLoad
    {
        [super viewDidLoad];
        // 创建串行队列
        serialQueue = dispatch_queue_create("fkjava.queue", DISPATCH_QUEUE_SERIAL);
        // 创建并发队列
        concurrentQueue = dispatch_queue_create("fkjava.queue"
        , DISPATCH_QUEUE_CONCURRENT);
    }
    - (IBAction)serial:(id)sender
    {
        // 依次将2个代码块提交给串行队列
        // 必须等到第1个代码块完成后，才能执行第2个代码块。
        dispatch_async(serialQueue, ^(void)
        {
            for (int i = 0 ; i < 100; i ++)
            {
                NSLog(@"%@===……-……==%d"  , [NSThread currentThread] , i);
            }
        });
        dispatch_async(serialQueue, ^(void)
        {
            for (int i = 0 ; i < 100; i ++)
            {
                NSLog(@"%@------%d" , [NSThread currentThread] , i);
            }
        });
    }

    - (IBAction)concurrent:(id)sender
    {
        // 依次将2个代码块提交给并发队列
        // 两个代码块可以并发执行
        dispatch_async(concurrentQueue, ^(void)
        {
            for (int i = 0 ; i < 100; i ++)
            {
                NSLog(@"%@===……-……==%d"  , [NSThread currentThread] , i);
            }
        });
        dispatch_async(concurrentQueue, ^(void)
        {
            for (int i = 0 ; i < 100; i ++)
            {
                NSLog(@"%@------%d" , [NSThread currentThread] , i);
            }
        });


    }

<br>

编译执行不难看出，第一个是串行队列，第二个是并行队列。<br>

下面我们将简单的举个异步下载图片的例子<br>

代码如下：<br>

    // 将代码块提交给系统的全局并发队列
    dispatch_async(dispatch_get_global_queue(DISPATCH_QUEUE_PRIORITY_HIGH, 0),
    ^(void){
        NSString* url = @"http://allluckly.cn/images/blog/applepay/6.png";
        // 从网络获取数据
        NSData *data = [[NSData alloc]
        initWithContentsOfURL:[NSURL URLWithString:url]];
        // 将网络数据初始化为UIImage对象
        UIImage *image = [[UIImage alloc]initWithData:data];
        if(image != nil)
        {
            // 将代码块提交给主线程关联的队列，该代码块将会由主线程完成
            dispatch_async(dispatch_get_main_queue(), ^{
                self.iv.image = image;
            }); // ①
        }
        else
        {
            NSLog(@"---下载图片出现错误---");
        }
    });

<br>
这里值的注意的是我们的图片是http的，xcode7以上必须设置下info.plist文件设置下网络，否则无法成功！
不难看出上面的送上面的例子中通过创建全局并发队列，该代码块负责从网络下载图片，下载完成后交给主线程执行。

### 同步提交任务<br>

dispatch_async()函数则会以同步方式提交代码块，该函数必须等到代码块执行结束才会返回。如果程序使用该函数先后提交了俩个代码块（并发队列），也必须等第一个任务执行完后才会执行第二个任务。如下🌰<br>

    - (IBAction)clicked:(id)sender
    {
        // 以同步方式先后提交2个代码块
        dispatch_sync(dispatch_get_global_queue(DISPATCH_QUEUE_PRIORITY_DEFAULT, 0)
        , ^(void){
            for (int i = 0 ; i < 100; i ++)
            {
                NSLog(@"%@=====%d"  , [NSThread currentThread] , i);
                [NSThread sleepForTimeInterval:0.1];
            }
        });
        // 必须等第一次提交的代码块执行完成后，dispatch_sync()函数才会返回，
        // 程序才会执行到这里，才能提交第二个代码块。
        dispatch_sync(dispatch_get_global_queue(DISPATCH_QUEUE_PRIORITY_DEFAULT, 0)
        , ^(void){
            for (int i = 0 ; i < 100; i ++)
            {
                NSLog(@"%@-----%d"  , [NSThread currentThread] , i);
                [NSThread sleepForTimeInterval:0.1];
            }
        });
    }

<br>

### 多次执行任务<br>

dispatch_apply()函数将代码块多次重复执行，如果该代码块被提交给并发队列，系统可以使用多个线程并发执行同一个代码块。下面我们简单的看个🌰.<br>

    - (IBAction)clicked:(id)sender
    {
        // 控制代码块执行5次
        dispatch_apply(5
        , dispatch_get_global_queue(DISPATCH_QUEUE_PRIORITY_DEFAULT, 0)
        // time形参代表当前正在执行第几次
        , ^(size_t time)
        {
            NSLog(@"===执行【%lu】次===%@" , time, [NSThread currentThread]);
        });
    }

<br>

### 只执行一次任务<br>

dispatch_once()将代码块提交给指定队列，该队列底层的线程池控制在应用的某个生命周期内仅执行一次。predicate 是指向dispatch_once_t变量的指针，判断是否已经执行过，runtime中很常用。系统直接用主线程执行该函数提交的代码块。下面我们简单的看个🌰.<br>

    - (IBAction)clicked:(id)sender
    {	
        static dispatch_once_t onceToken;
        dispatch_once(&onceToken, ^{
            NSLog(@"==执行代码块==");
            // 线程暂停3秒
            [NSThread sleepForTimeInterval:3];
        });
    }

<br>


今天暂时写到这！<br>
预告：（四）主讲NSOperationQueue多线程！<br>

----------------------------------------------------------

> [博主app上线啦，快点此来围观吧](https://itunes.apple.com/us/app/it-blog-zi-xueios-kai-fa-jin/id1067787090?l=zh&ls=1&mt=8)<br>

> 原文地址：[http://allluckly.cn](http://allluckly.cn)<br>

好文推荐：[详解持久化Core Data框架的原理以及使用](http://allluckly.cn/持久化/chijiuhua01/)<br>

版权归©Bison所有 如需转载请保留原文超链接地址！否则后果自负！





