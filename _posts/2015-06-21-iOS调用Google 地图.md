---
layout: post
title: "iOS使用Google地图Api创建的地图显示标注及轨迹回放"
description: "Bison"
category: 地图
headline: Discover the theme elements
tags: [iOS开发地图, Google地图，iOS开发技巧，技术博客]
imagefeature: picture-38.jpg
comments: true
mathjax: true
path: /images
---

>&quot;iOS开发就像搬运工，当搬到一定境界的时候就可以偷懒了&quot;
><small><cite title="Plato">Bison</cite></small>

>![1]({{ page.path }}/zjs.jpg)<br>
>[冰之依韩版女装](http://allluckly.taobao.com/)（程序媛福利）

最近做的项目需要和安卓的地图同步，安卓没有使用百度地图，而是用的Google Map.<br>
说实话有点坑，以前没有和安卓端一起做的时候一般用的苹果自带的地图高德的地图或者百度<br>
对于Google地图基本上没接触过，主要代码如下<br>


 > [更多经验请点击](http://www.allluckly.cn/) 

.h 文件



`@property (strong, nonatomic) GMSMapView *_mapView;`




.m 文件


//创建地图<br>

{% highlight css %}

- (void)creatMap{

    _mapView = [[GMSMapView alloc]initWithFrame:CGRectMake(0, 0, self.view.frame.size.width, self.view.frame.size.height)];
    [self.view addSubview:_mapView];
    [_mapView clear];
    [self initMapView];
}

{% endhighlight %}


就是以下三部分。<br>
{% highlight css %}

- (void)initMapView
{

    GMSCameraPosition *camera = [GMSCameraPosition cameraWithLatitude:-6.13631
    longitude:106.789352
    zoom:ZOOM_LEVEL];
    _mapView.mapType = kGMSTypeNormal;
    _mapView.camera = camera;
    _mapView.delegate = self;
    _geocoder = [[GMSGeocoder alloc] init];

    polyline = [[GMSPolyline alloc] init];
    linepath = [GMSMutablePath path];


    CLLocationCoordinate2D coords;
    coords.latitude = -6.136271;
    coords.longitude = 106.789216;


    _mapView.camera = [GMSCameraPosition cameraWithTarget:coords
    zoom:ZOOM_LEVEL];

    //显示标注
    GMSReverseGeocodeCallback handler = ^(GMSReverseGeocodeResponse *response,
    NSError *error) {
    if (response && response.firstResult) {

        GMSMarker *marker = [[GMSMarker alloc] init];
        marker.position = coords;
        marker.title = response.firstResult.addressLine1;
        marker.snippet = response.firstResult.addressLine2;
        _addressData = response.firstResult.addressLine2;
        [self refreshGpsInfo];
        marker.appearAnimation = kGMSMarkerAnimationNone;
        marker.icon = SETIMAGE(@"deviceannotation.png");
        marker.map = _mapView;
    } else {
        NSLog(@"Could not reverse geocode point (%f,%f): %@",
        coords.latitude, coords.longitude, error);
    }
    };

    [_geocoder reverseGeocodeCoordinate:coords
    completionHandler:handler];
    //画线，轨迹回放
    [linepath removeAllCoordinates];
    [self drawLineWithLocationArray:trackArray];


    /*
    注，trackArray里面的数据格式
    CLLocation *nowLocation = [[CLLocation alloc] initWithLatitude:coords.latitude longitude:coords.longitude];
    [trackArray addObject:nowLocation];

    */

}
{% endhighlight %}


//画线，使用轨迹回放<br>

{% highlight css %}
- (void)drawLineWithLocationArray:(NSArray *)locationArray
{

    if(current_type == _CURRENT_TRACK)
    polyline.strokeColor = [UIColor blueColor];
    else
    polyline.strokeColor = [UIColor redColor];
    polyline.strokeWidth = 6.f;

    // for(int idx = 0; idx < pointStrings.count; idx++)
    for(int idx = 0; idx < locationArray.count; idx++)
    {
    CLLocation *location = [locationArray objectAtIndex:idx];
    CLLocationDegrees latitude  = location.coordinate.latitude;
    CLLocationDegrees longitude = location.coordinate.longitude;

    // create our coordinate and add it to the correct spot in the array
    CLLocationCoordinate2D coordinate = CLLocationCoordinate2DMake(latitude, longitude);
    [linepath addCoordinate:coordinate];
    }
    polyline.path = linepath;
    polyline.map = _mapView;
}
{% endhighlight %}


谷歌Api请到谷歌开发者网站注册，填写相关你自己的app信息自然就有apikey了<br>


> [博主app上线了，赶紧点此来围观吧😄](https://itunes.apple.com/us/app/it-blog-zi-xueios-kai-fa-jin/id1067787090?l=zh&ls=1&mt=8)<br>

