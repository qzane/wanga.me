## todo:

* 使用的match手段不具备尺度不变性，不可处理不同分辨率的情况

* 
总体结构应该是：
``` python
while(1):
    try:
        on_news()
        pos = getPosition()
        pos.doSth()
    except:
        pass
```
## done
        
* fight 部分
(下一步加入战力比较)

* home部分 
(升级策略还可以改进)

* fight页面右上角定位物体需要修改，why会被战力遮挡
(改用home标志定位)

* 从升级页面到fight页面会卡一下，好像是浏览器卡了
(增加了补兵以后的等待时间就好了)