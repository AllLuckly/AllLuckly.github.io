---
layout: post
title: "iOS开发之诱导用户为自己的App评论"
description: "Bison"
category: ASO
headline: Discover the theme elements
tags: [appstore，评论，aso优化，iOS开发]
imagefeature: 
comments: true
featured: true
mathjax: true
path: /images
---

>&quot;由于我自己的App下载量少，评论也少，出于App的aso优化，想尽办法，而评论是aso里边比较重视的一块，前面的版本都没有诱导用户评论的这一功能，导致有些被动。&quot;

由此自己简单的封装了该功能，下面我们先看看效果图：<br>

![1]({{ page.path }}/blog/1.png)<br>

弹出试图并没有做什么处理，就是系统的8.0以前用的`UIAlertView`8.0以上用的`UIAlertController`<br>


具体的一些算法，都可以看代码，闲话不多说，直接贴码，😄<br>

新建一个NSObject的类命名为`LBToAppStore` 具体代码如下<br>

## .h文件<br>

    #import <Foundation/Foundation.h>

    #import <UIKit/UIKit.h>



    @interface LBToAppStore : NSObject<UIAlertViewDelegate>
    {
        #if __IPHONE_OS_VERSION_MAX_ALLOWED < __IPHONE_8_0

        UIAlertView *alertViewTest;

        #else

        UIAlertController *alertController;

        #endif

    }

    @property (nonatomic,strong) NSString * myAppID;//appID



    - (void)showGotoAppStore:(UIViewController *)VC;

    @end

<br>

## .m文件<br>


    #import "LBToAppStore.h"

    @implementation LBToAppStore


    - (void)showGotoAppStore:(UIViewController *)VC{
        //当前版本号
        NSDictionary *infoDictionary = [[NSBundle mainBundle] infoDictionary];
        float appVersion = [[infoDictionary objectForKey:@"CFBundleShortVersionString"] floatValue];
        //userDefaults里的天数
        NSUserDefaults *userDefaults = [NSUserDefaults standardUserDefaults];
        int udtheDays = [[userDefaults objectForKey:@"theDays"] intValue];
        //userDefaults里的版本号
        float udAppVersion = [[userDefaults objectForKey:@"appVersion"] intValue];
        //userDefaults里用户上次的选项
        int udUserChoose = [[userDefaults objectForKey:@"userOptChoose"] intValue];
        //时间戳的天数
        NSTimeInterval interval = [[NSDate date] timeIntervalSince1970];
        int daySeconds = 24 * 60 * 60;
        NSInteger theDays = interval / daySeconds;

        //版本升级之后的处理,全部规则清空,开始弹窗
        if (udAppVersion && appVersion>udAppVersion) {
            [userDefaults removeObjectForKey:@"theDays"];
            [userDefaults removeObjectForKey:@"appVersion"];
            [userDefaults removeObjectForKey:@"userOptChoose"];
            [self alertUserCommentView:VC];
        }
        //1,从来没弹出过的
        //2,用户选择😓我要吐槽，7天之后再弹出
        //3,用户选择😭残忍拒绝后，7天内，每过1天会弹一次
        //4,用户选择😭残忍拒绝的30天后，才会弹出
        else if (!udUserChoose ||
        (udUserChoose==2 && theDays-udtheDays>7) ||
        (udUserChoose>=3 && theDays-udtheDays<=7 && theDays-udtheDays>udUserChoose-3) ||
        (udUserChoose>=3 && theDays-udtheDays>30))
        {
            [self alertUserCommentView:VC];

        }

    }

    -(void)alertUserCommentView:(UIViewController *)VC{

        if ([[[UIDevice currentDevice] systemVersion] floatValue] >= 8.0) {

        NSUserDefaults *userDefaults = [NSUserDefaults standardUserDefaults];
        //当前时间戳的天数
        NSTimeInterval interval = [[NSDate date] timeIntervalSince1970];
        int daySeconds = 24 * 60 * 60;
        NSInteger theDays = interval / daySeconds;
        //当前版本号
        NSDictionary *infoDictionary = [[NSBundle mainBundle] infoDictionary];
        float appVersion = [[infoDictionary objectForKey:@"CFBundleShortVersionString"] floatValue];
        //userDefaults里版本号
        float udAppVersion = [[userDefaults objectForKey:@"appVersion"] intValue];
        //userDefaults里用户选择项目
        int udUserChoose = [[userDefaults objectForKey:@"userOptChoose"] intValue];
        //userDefaults里用户天数
        int udtheDays = [[userDefaults objectForKey:@"theDays"] intValue];

        //当前版本比userDefaults里版本号高
        if (appVersion>udAppVersion) {
            [userDefaults setObject:[NSString stringWithFormat:@"%f",appVersion] forKey:@"appVersion"];
        }

        alertController = [UIAlertController alertControllerWithTitle:@"致开发者的一封信" message:@"有了您的支持才能更好的为您服务，提供更加优质的，更加适合您的App，当然您也可以直接反馈问题给到我们" preferredStyle:(UIAlertControllerStyleAlert)];

        UIAlertAction *refuseAction = [UIAlertAction actionWithTitle:@"😭残忍拒绝" style:(UIAlertActionStyleDefault) handler:^(UIAlertAction *action) {

        [userDefaults setObject:@"1" forKey:@"userOptChoose"];
        [userDefaults setObject:[NSString stringWithFormat:@"%d",(int)theDays] forKey:@"theDays"];
        }];

        UIAlertAction *okAction = [UIAlertAction actionWithTitle:@"😄好评赞赏" style:(UIAlertActionStyleDefault) handler:^(UIAlertAction *action) {

        [userDefaults setObject:@"2" forKey:@"userOptChoose"];
        [userDefaults setObject:[NSString stringWithFormat:@"%d",(int)theDays] forKey:@"theDays"];

        NSString *str = [NSString stringWithFormat:
        @"https://itunes.apple.com/cn/app/id%@?mt=8",
        self.myAppID ];

        [[UIApplication sharedApplication] openURL:[NSURL URLWithString:str]];

        }];

        UIAlertAction *showAction = [UIAlertAction actionWithTitle:@"😓我要吐槽" style:(UIAlertActionStyleDefault) handler:^(UIAlertAction *action) {

        if (udUserChoose<=3 || theDays-[[userDefaults objectForKey:@"theDays"] intValue]>30) {
        [userDefaults setObject:@"3" forKey:@"userOptChoose"];
        [userDefaults setObject:[NSString stringWithFormat:@"%d",(int)theDays] forKey:@"theDays"];
        }else{
        [userDefaults setObject:[NSString stringWithFormat:@"%d",(int)(theDays-udtheDays+3)] forKey:@"userOptChoose"];
        }
        NSString *str = [NSString stringWithFormat:
        @"https://itunes.apple.com/cn/app/id%@?mt=8",
        self.myAppID ];

        [[UIApplication sharedApplication] openURL:[NSURL URLWithString:str]];
        }];


        [alertController addAction:refuseAction];
        [alertController addAction:okAction];
        [alertController addAction:showAction];

        //        NSLog(@"%@",[userDefaults objectForKey:@"appVersion"]);
        //        NSLog(@"%@",[userDefaults objectForKey:@"userOptChoose"]);
        //        NSLog(@"%@",[userDefaults objectForKey:@"theDays"]);

        [VC presentViewController:alertController animated:YES completion:nil];

        }else{
            #if __IPHONE_OS_VERSION_MAX_ALLOWED < __IPHONE_8_0
            alertViewTest = [[UIAlertView alloc] initWithTitle:@"致开发者的一封信" message:@"有了您的支持才能更好的为您服务，提供更加优质的，更加适合您的App，当然您也可以直接反馈问题给到我们" delegate:self cancelButtonTitle:@"😭残忍拒绝" otherButtonTitles:@"😄好评赞赏",@"😓我要吐槽", nil];
            [alertViewTest show];
            #endif
        }

    }

    #if __IPHONE_OS_VERSION_MAX_ALLOWED < __IPHONE_8_0

    -(void)alertView:(UIAlertView *)alertView clickedButtonAtIndex:(NSInteger)buttonIndex{

        NSUserDefaults *userDefaults = [NSUserDefaults standardUserDefaults];
        //当前时间戳的天数
        NSTimeInterval interval = [[NSDate date] timeIntervalSince1970];
        int daySeconds = 24 * 60 * 60;
        NSInteger theDays = interval / daySeconds;
        //当前版本号
        NSDictionary *infoDictionary = [[NSBundle mainBundle] infoDictionary];
        float appVersion = [[infoDictionary objectForKey:@"CFBundleShortVersionString"] floatValue];
        //userDefaults里版本号
        float udAppVersion = [[userDefaults objectForKey:@"appVersion"] intValue];
        //userDefaults里用户选择项目
        int udUserChoose = [[userDefaults objectForKey:@"userOptChoose"] intValue];
        //userDefaults里用户天数
        int udtheDays = [[userDefaults objectForKey:@"theDays"] intValue];

        //当前版本比userDefaults里版本号高
        if (appVersion>udAppVersion) {
            [userDefaults setObject:[NSString stringWithFormat:@"%f",appVersion] forKey:@"appVersion"];
        }

        switch (buttonIndex) {
            case 0: //残忍的拒绝
            if (udUserChoose<=3 || theDays-[[userDefaults objectForKey:@"theDays"] intValue]>30) {
                [userDefaults setObject:@"3" forKey:@"userOptChoose"];
                [userDefaults setObject:[NSString stringWithFormat:@"%d",(int)theDays] forKey:@"theDays"];
            }else{
                [userDefaults setObject:[NSString stringWithFormat:@"%d",(int)(theDays-udtheDays+3)] forKey:@"userOptChoose"];
            }
            break;
            case 1:{ //好评
                [userDefaults setObject:@"1" forKey:@"userOptChoose"];
                [userDefaults setObject:[NSString stringWithFormat:@"%d",(int)theDays] forKey:@"theDays"];
                NSString *str = [NSString stringWithFormat:
                @"https://itunes.apple.com/cn/app/id%@?mt=8",
                self.myAppID ];

                [[UIApplication sharedApplication] openURL:[NSURL URLWithString:str]];
            }
            break;
            case 2:{ //不好用，我要提意见
                [userDefaults setObject:@"2" forKey:@"userOptChoose"];
                [userDefaults setObject:[NSString stringWithFormat:@"%d",(int)theDays] forKey:@"theDays"];
                NSString *str = [NSString stringWithFormat:
                @"https://itunes.apple.com/cn/app/id%@?mt=8",
                self.myAppID ];

                [[UIApplication sharedApplication] openURL:[NSURL URLWithString:str]];
            }
            break;

            default:
            break;
            }
        //    NSLog(@"%@",[userDefaults objectForKey:@"appVersion"]);
        //    NSLog(@"%@",[userDefaults objectForKey:@"userOptChoose"]);
        //    NSLog(@"%@",[userDefaults objectForKey:@"theDays"]);

    }

    #endif


    @end

<br>

具体使用方法如下：<br>

    #import "ViewController.h"
    #import "LBToAppStore.h"
    @interface ViewController ()

    @end

    @implementation ViewController

    - (void)viewDidLoad {
        [super viewDidLoad];
        // Do any additional setup after loading the view, typically from a nib.
    }

    -(void)viewDidAppear:(BOOL)animated{

        //用户好评系统
        LBToAppStore *toAppStore = [[LBToAppStore alloc]init];
        toAppStore.myAppID = @"1067787090";
        [toAppStore showGotoAppStore:self];

    }


    @end

<br>


[demo下载地址戳我](https://github.com/AllLuckly/LBAppStoreReview)<br>

如对你有帮助，请不要吝惜你的star哦！<br>

----------------------------------------------------------

> [学习iOS开发的app上线啦，点此来围观吧](https://itunes.apple.com/us/app/it-blog-zi-xueios-kai-fa-jin/id1067787090?l=zh&ls=1&mt=8)<br>

> [更多经验请点击](http://allluckly.cn)<br>

好文推荐：[iOS开发之超链接富文本](http://allluckly.cn/投稿/tuogao42)<br>



