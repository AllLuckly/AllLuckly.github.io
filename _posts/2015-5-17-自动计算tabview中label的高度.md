---
layout: post
published: true
title: iOS开发自动计算tabview中label的高度
mathjax: false
featured: true
comments: true
headline: Making blogging easier for masses
category: UITabView
tags: [iOS开发，UITabView，iOS开发技巧，技术博客]
path: /images
---



>![1]({{ page.path }}/zjs.jpg)<br>
>[冰之依韩版女装](http://allluckly.taobao.com/)（程序媛福利）

自动计算tabview中label的高度的方法

{% highlight css %}
- (UITableViewCell *)tableView:(UITableView *)tableView cellForRowAtIndexPath:(NSIndexPath *)indexPath{
    if(tableView == kindTableView)
    {
        NSInteger section = indexPath.section;

        customCell *cell = (customCell *)[tableView dequeueReusableCellWithIdentifier:customCellView];
        if (cell == nil) {
        [[NSBundle mainBundle] loadNibNamed:@"customCell" owner:self options:nil];
        cell = _customCell;
    }

        FileListItem * item = [cuArray objectAtIndex:indexPath.row];
        cell.textLabel.text = item.name;

        //主要是这里，上面的按平常各自的习惯写
        cell.textLabel.lineBreakMode = NSLineBreakByWordWrapping;
        cell.textLabel.numberOfLines = 0;
        cell.textLabel.font = [UIFont fontWithName:@"Helvetica" size:17.0];
        UIFont *cellFont = [UIFont fontWithName:@"Helvetica" size:17.0];
        CGSize constraintSize = CGSizeMake(280.0f, MAXFLOAT);
        CGSize labelSize = [cell.textLabel.text sizeWithFont:cellFont constrainedToSize:constraintSize lineBreakMode:NSLineBreakByWordWrapping];

        CGRect frame = cell.textLabel.frame;
        cell.textLabel.frame = CGRectMake(frame.origin.x, ((labelSize.height + 20)-frame.size.height)/2, frame.size.width, frame.size.height);

    }
    return cell;

}


//设置cell每行间隔的高度
- (CGFloat)tableView:(UITableView *)tableView heightForRowAtIndexPath:(NSIndexPath *)indexPath{
    NSString *cellText = item.name;
    UIFont *cellFont = [UIFont fontWithName:@"Helvetica" size:17.0];
    CGSize constraintSize = CGSizeMake(280.0f, MAXFLOAT);
    CGSize labelSize = [cellText sizeWithFont:cellFont constrainedToSize:constraintSize lineBreakMode:NSLineBreakByWordWrapping];

    return labelSize.height + 20;
} 

{% endhighlight %}
    


