PyRadius
========

[PyRadius](https://github.com/jamiesun/PyRadius)是一个使用python开发的AAA认证服务器系统，协议部分使用了[pyrad](https://github.com/wichert/pyrad)模块，服务器使用了[asyncoro](http://asyncoro.sourceforge.net/)分布式协程框架。web管理部分使用了web.py框架

功能特性
========

## 标准Radius功能

* 支持标准RADIUS认证报文分析功能，BAS发起Authentication请求报文到AAA系统认证鉴权。
* Authentication PAP认证：支持标准RADIUS认证报文中采用PAP密码认证方式,NAS发起Authentication请求报文到AAA系统认证鉴权
* Authentication CHAP认证：支持标准RADIUS认证报文中采用CHAP密码认证方式， NAS发起Authentication请求报文到AAA系统认证鉴权
* Authentication授权：在接收NAS Authentication请求报文之后，RADIUS Server根据用户信息资源，对用户授权信息进行封装，通过Authentication响应报文把用户带宽限制、最大时长、IP等信息授权到NAS。
* Accounting-On报文：支持标准RADIUS计费报文分析功能，NAS发起Accounting-On报文，通知RADIUS该BAS启动成功，开始计费。
* Accounting-Off报文：支持标准RADIUS计费报文分析功能，NAS发起Accounting-Off报文，通知RADIUS该BAS结束计费，在线用户统一下线，NAS进入维护或切换状态。
* Accounting-Start报文：支持标准RADIUS计费报文分析功能，NAS发起Accounting-Start报文，通知用户计费开始。
* Accounting-Interium-Update报文：支持标准RADIUS计费报文分析功能，NAS发起Accounting-Start报文，通知用户计费更新。
* Accounting-Stop报文：支持标准RADIUS计费报文分析功能，NAS发起Accounting-Start报文，通知用户计费结束。
