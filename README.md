# 渠道打包脚本

## 配置信息

### 渠道信息
#### 工程文件信息
主要是info.plist，配置系统设置

#### 渠道代码中相关配置信息
主要是xxx.h文件三方库key等的配置

#### 渠道图片
包括渠道icon，启动图替换
需要把图片复制到单独文件下

替换方式：
key：工程文件目录
value:需要替换的图片目录
> 注意：必须保证两个目录下的图片名一致

### 打包证书配置
#### 工程配置

| 参数      | 功能         |
| ------- | ---------- |
| userCocoaPods   | 是否使用cocoaPods:1-是 0-不是    |
| project_name | 项目工程文件名字 |
| scheme_name | 项目scheme名字（一般和项目名称一致） |
| configuration | 归档类型：Release版或者Debug版 |


#### 打包证书配置
ProvisioningProfile: 证书的名字

#### 打包目录配置：
targetIPA_path：最后打包完成放到的目录

## 使用方法

终端 cd到channelbuild.py的目录

执行 python channelbuild.py

