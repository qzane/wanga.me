todo: 从升级页面到fight页面会卡一下，好像是浏览器卡了

todo: 使用的match手段不具备尺度不变性，不可移植

todo:
总体结构应该是：
while(1):
    try:
        on_news()
        pos = getPosition()
        pos.doSth()
    except:
        pass
        
        
done: fight 部分（下一步加入战力比较）

done: home部分 (升级策略还可以改进)

done: fight页面右上角定位物体需要修改，why会被战力遮挡