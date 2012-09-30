#用Socket发文件
其实这个东西无聊得很，就是用Socket来发文件而已，让死宅之间发文件不必借助QQ！

这个世界上不是只有QQ才能互传文件！

##依赖
* python2
* python-struct
* python-socket

##使用方法
先把它git下来
```bash
git clone https://github.com/zonyitoo/SendBySocket.git
```
然后装依赖，见上。*（其实一般不用装，python都自带了）*

* 接收端

如果你是接收端，就运行`sockrecv.py`
```bash
./sockrecv.py --iface=eth0
```
参数`iface`是你的电脑的网络物理接口名，如`eth0`

运行之后会显示

> Your IP Address is 192.168.1.1

那么你就知道你的IP地址了。不幸的是如果你在家用，有路由器，那么这个子网地址是不行的，去这个[地址](http://www.ip.cn/)看看你的外网IP是多少

然后告诉那个发文件的人。

* 发送端

如果你是发送端，那么就运行`socksend.py`
```bash
./sockrecv.py --address=[RecvIP] --file=[FileName]
```
参数`address`是接收端的IP地址，`file`是要发送的文件名或地址