# Python免杀工具



该工具开发完成，用于课程Python渗透测试期末作品  Python-shellcode 免杀工具

该工具支持一键加密shellcode并生成loader，加密loader以及打包

工具使用模块化进行开发



## templates

该模块是基础的loader模板

## encrypt_plugins

该模块用于对shellcode以及loader进行加密

目前支持的加密模块包括

1.ase
2.base64
3.自定义base64
4.des
5.rsa
6.xor

其中ase、des、xor支持自定义密钥

## package

打包模块，该模块用于对最后生成的加密loader进行打包成exe

目前支持的打包方式为

cxfreeze、nuitka、py2exe、PyInstaller

其中nuitka和PyInstaller支持通过记录使用的插件进行动态打包

仅在windows上测试过cxfreeze、nuitka、PyInstaller打包效果

## 使用方法

使用pycharm打开项目，先在shellcode.py里面写入shellcode

形如

```
buf="\xfc\x48\x83\xe4\xf0\xe8\xc0\x00\x00\x00"
```

运行mian.py，选择加密loader的方法，支持多层加密

![image-20250622235657186](https://hongmengshikong.oss-cn-wuhan-lr.aliyuncs.com/img_for_note/202506222357321.png)

可以对生成的loader进行再次加密

![image-20250622235908916](https://hongmengshikong.oss-cn-wuhan-lr.aliyuncs.com/img_for_note/202506222359980.png)

最后可以选择打包方法

![image-20250622235956087](https://hongmengshikong.oss-cn-wuhan-lr.aliyuncs.com/img_for_note/202506222359144.png)

