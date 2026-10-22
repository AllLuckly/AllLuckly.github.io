---
layout: post
title: "Swift纯代码走进UICollectionView"
description: "Bison"
category: iOS之Swift初探
headline: Discover the theme elements
tags: [Swift，UICollectionView，Swift代码，iOS开发技巧，技术博客]
imagefeature: default_bg.jpg
comments: true
featured: 
mathjax: true
path: /images
---

>&quot;充实自我，提升自我的价值；唯有多学&quot;
><small><cite title="Plato">Bison</cite></small>


`Swift`对于一门新的iOS编程语言，他的崛起是必然的<br>

我们这群老程序员们学习新的技能也是必然的<br>

不接受新技能将被这大群体无情的淘汰<br>

So 我欣然接受这门看似不成熟的语言<br>

下面我们说说`Swift`中比较常见的控件`UICollectionView`<br>

首先我们设置一个全局的`UICollectionView`和一个数据源<br>

`var colltionView : UICollectionView?`<br>
`var dataArr = NSMutableArray()`<br>

然后设置`UICollectionView`的3个代理<br>
`UICollectionViewDelegate,UICollectionViewDataSource,UICollectionViewDelegateFlowLayout`<br>
接下来我们要做的是`override func viewDidLoad()`方法中初始化一些必要的对象<br>

{% highlight css %}

override func viewDidLoad() {
    super.viewDidLoad()
    var layout = UICollectionViewFlowLayout()
    colltionView = UICollectionView(frame: CGRectMake(0, 0, width, height), collectionViewLayout: layout)
    //注册一个cell
    colltionView! .registerClass(Home_Cell.self, forCellWithReuseIdentifier:"cell")
    //注册一个headView
    colltionView! .registerClass(Home_HeadView.self, forSupplementaryViewOfKind:UICollectionElementKindSectionHeader, withReuseIdentifier: "headView")
    colltionView?.delegate = self;
    colltionView?.dataSource = self;

    colltionView?.backgroundColor = UIColor.whiteColor()
    //设置每一个cell的宽高
    layout.itemSize = CGSizeMake((width-30)/2, 250)
    self.view .addSubview(colltionView!)
    self .getData()
}
{% endhighlight %}

然后我们实现`UICollectionView`的代理方法<br>

{% highlight css %}
//返回多少个组
func numberOfSectionsInCollectionView(collectionView: UICollectionView) -> Int {

    return 1
}
//返回多少个cell
func collectionView(collectionView: UICollectionView, numberOfItemsInSection section: Int) -> Int {
    return dataArr.count
}
//返回自定义的cell
func collectionView(collectionView: UICollectionView, cellForItemAtIndexPath indexPath: NSIndexPath) -> UICollectionViewCell {


    let cell = collectionView.dequeueReusableCellWithReuseIdentifier("cell", forIndexPath: indexPath) as! Home_Cell
    var model = GoodsModel()
    model = dataArr[indexPath.row] as! GoodsModel
    let url : NSURL = NSURL(string: model.image_url as String)!
    cell.imgView!.hnk_setImageFromURL(url)
    cell.layer.borderWidth = 0.3;
    cell.layer.borderColor = UIColor.lightGrayColor().CGColor
    cell.titleLabel!.text = model.short_name
    cell.priceLabel!.text = "￥"+model.p_price
    cell.readLabel!.text = "💗"+model.like_count
    return cell
}
//返回HeadView的宽高
func collectionView(collectionView: UICollectionView, layout collectionViewLayout: UICollectionViewLayout, referenceSizeForHeaderInSection section: Int) -> CGSize{

    return CGSize(width: width, height: height/1.6)
}

//返回自定义HeadView或者FootView，我这里以headview为例
func collectionView(collectionView: UICollectionView, viewForSupplementaryElementOfKind kind: String, atIndexPath indexPath: NSIndexPath) -> UICollectionReusableView{
    var v = Home_HeadView()
    if kind == UICollectionElementKindSectionHeader{

    v = colltionView!.dequeueReusableSupplementaryViewOfKind(kind, withReuseIdentifier: "headView", forIndexPath: indexPath) as! Home_HeadView
    }
    return v
}
//返回cell 上下左右的间距
func collectionView(collectionView: UICollectionView, layout collectionViewLayout: UICollectionViewLayout, insetForSectionAtIndex section: Int) -> UIEdgeInsets{
    return UIEdgeInsetsMake(5, 10, 5, 10)
}

{% endhighlight %}

然后我们来获取数据，这里的话我用的是`Alamofire`进行的网络请求，URL不方便透露<br>

{% highlight css %}
//获取数据
func getData(){
    Alamofire.request(.GET, GoodsUrl).responseJSON() { (req, _, JSON, _) -> Void in

        if let j = JSON as? NSDictionary{
            var data = j.valueForKey("data")as! NSArray

            for dict in data{
                var model = GoodsModel()
                model.Analytical(dict as! NSDictionary)
                self.dataArr.addObject(model)
            }

            self.colltionView!.reloadData()
        }
    }
}


{% endhighlight %}

接下来让我们看下cell里面究竟写了些什么玩意<br>

{% highlight css %}

class Home_Cell: UICollectionViewCell {

    let width = UIScreen.mainScreen().bounds.size.width//获取屏幕宽
    var imgView : UIImageView?//cell上的图片
    var titleLabel:UILabel?//cell上title
    var priceLabel:UILabel?//cell上价格
    var readLabel:UILabel?//cell上的阅读量


override init(frame: CGRect) {

    super.init(frame: frame)
    //初始化各种控件
    imgView = UIImageView(frame: CGRectMake(0, -10, (width-30)/2, 200))
    self .addSubview(imgView!)
    titleLabel = UILabel(frame: CGRectMake(5, CGRectGetMaxY(imgView!.frame)-12, (width-40)/2, 50))
    titleLabel?.numberOfLines = 0
    titleLabel?.font = UIFont.boldSystemFontOfSize(14.0)
    titleLabel?.textColor = UIColor.lightGrayColor()
    self .addSubview(titleLabel!)

    priceLabel = UILabel(frame: CGRectMake(5, CGRectGetMaxY(titleLabel!.frame), (width-40)/2/2, 20))
    priceLabel?.numberOfLines = 0
    priceLabel?.font = UIFont.boldSystemFontOfSize(14.0)
    priceLabel?.textColor = UIColor.lightGrayColor()
    self .addSubview(priceLabel!)

    readLabel = UILabel(frame: CGRectMake((width-30)/2/2, CGRectGetMaxY(titleLabel!.frame), (width-40)/2/2, 20))
    readLabel?.numberOfLines = 0
    readLabel?.textAlignment = NSTextAlignment.Right
    readLabel?.font = UIFont.boldSystemFontOfSize(14.0)
    readLabel?.textColor = UIColor.lightGrayColor()
    self .addSubview(readLabel!)


}

required init(coder aDecoder: NSCoder) {
    fatalError("init(coder:) has not been implemented")
}

}


{% endhighlight %}


是不是还觉得缺少点什么？没错，我们的headview是不是还没整啊？<br>
接下来呢，我们看下`UICollectionView`的headview该怎么设置<br>
重点在这里！首先headview要继承`UICollectionReusableView`<br>
然后我们这个.m文件里面并没有看到`override func viewDidLoad()`这样的方法<br>
那我们怎么办呢？<br>
接下来就看我的了<br>
我们点到我们继承的`UICollectionReusableView`里面去看里面有些什么方法<br>
功夫不负有心人，😄终于找到了一个可以让我们用的方法<br>
{% highlight css %}
override func applyLayoutAttributes(layoutAttributes: UICollectionViewLayoutAttributes!){

}
{% endhighlight %}

我们可以把要自定义的UI 请求数据什么的都放这方法里面<br>
也就相当于我们VC里面的`override func viewDidLoad()`这个方法<br>
教程到结束<br>
有任何问题可以留言，定期抽时间回复<br>

版权归©Bison所有 任何转载请标明出处！



<br>
 >最终效果图如下<br>
![UICollectionView 示例效果](/images/blog/Swift_CollTionView.gif)<br><br><br>
