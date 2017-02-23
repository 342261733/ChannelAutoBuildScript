#coding: utf-8
import os
import traceback
import sys
import time
import hashlib
import requests
import subprocess

# ==============================================配置渠道信息=============================================================

# 配置工程的根目录
PROJECT_PATH = '/Users/xxx/Documents/work/test'

# 工程配置信息plist文件
PLIST_FILE = ['/Test/Info.plist']
PLIST_CONFIG= {
    '/Test/Info.plist': {
        'CFBundleDisplayName': 'xxx',
        'CFBundleName': 'xxx',
        'CFBundleShortVersionString': '1.0.0',
        'CFBundleVersion': '010000'
    },
}

# 渠道代码相关信息配置,没有代码配置可以忽略
H_FILE = ['/Test/xxx.h']
H_CONFIG = {
    '/Test/xxx.h': {
        'UMengKey': 'xxxxx',
    },
}

# 图片信息配置：key:工程文件目录，value:需要替换的图片目录，注意：必须保证两个目录图片名一致，这里没有兼容不同名字的处理
ICON_CONFIG= {
    '/Test/Images.xcassets/AppIcon.appiconset': './ConfigImage/IconImage',
    '/Test/Images.xcassets/LaunchImage.launchimage': './ConfigImage/LaunchImage',
}

# ==============================================配置打包信息=============================================================

# 项目是否使用cocoaPods:1-是 0-不是
userCocoaPods = 1
# 项目工程文件名字
project_name = "Test"
# 项目scheme名字（一般和项目名称一致）
scheme_name = "Test"
# 归档类型：Release版或者Debug版
configuration = "Release"
# 证书概要文件：
ProvisioningProfile = "com.profile"
#===============================================
# 项目根目录:xcodebuild命令必须进入的项目目录   绝对目录
project_path = PROJECT_PATH
# 编译后项目的app根目录：即build的.app所在的根目录
build_root_path = project_path
# 编译成功后.app所在目录
build_app_path = "%s/build/Build/Products/Release-iphoneos/%s.app" %(build_root_path,scheme_name)
# 指定项目下编译目录
build_path = "%s/build" %(build_root_path)
#===============================================
# 打包后ipa存储目录
targetIPA_path = "/Users/xxx/Desktop/IPA"











# ==============================================方法实现=============================================================

# 替换工程配置信息
def replaceConfigFile():
    try:
        FLAG = False
        # plist
        for plist in PLIST_FILE:
            p_dict = PLIST_CONFIG[plist]
            plist = PROJECT_PATH + plist
            for k, v in p_dict.items():
                with open(plist, 'r') as fr:
                    lines = fr.readlines()
                
                with open(plist, 'w') as fw:
                    for line in lines:
                        if line.count(k):
                            fw.write(line)
                            v_line = line[0:line.index('<key>')] + '<string>' + v + '</string>' + '\n'
                            fw.write(v_line)
                            FLAG = True
                        else:
                            if not FLAG:
                                fw.write(line)
                            else:
                                FLAG = False
    
        # .h
        for h in H_FILE:
            h_dict = H_CONFIG[h]
            h = PROJECT_PATH + h
            for k, v in h_dict.items():
                with open(h, 'r') as fr:
                    lines = fr.readlines()
                
                with open(h, 'w') as fw:
                    for line in lines:
                        if line.count(k):
                            new_line = line[0:(line.index(k) + len(k) + 1)] + v + '\n'
                            fw.write(new_line)
                        else:
                            fw.write(line)

        FLAG = False
        # icon
        for k, v in ICON_CONFIG.items():
            k = PROJECT_PATH + k
            pro_files = os.listdir(k)
            replace_files = os.listdir(v)
            for pro_file in pro_files:
                for replace_file in replace_files:
                    if pro_file == replace_file:
                        os.system("rm %s" % os.path.join(k, pro_file))
                        os.system('cp %s %s' % (os.path.join(v, replace_file), k))
                        FLAG = True
        if not FLAG:
            print '\n\n ** Replace image failure, reason: replace file has no common image ** \n\n'
            os._exit(0)

        print '\n\n************ Replace file success *************\n\n'
    except:
        print traceback.format_exc()
        exit()


# 清理项目 创建build目录
def clean_project_mkdir_build():
    if userCocoaPods == 1 :#使用cocoaPods，才需要创建目录
        os.system('cd %s;xcodebuild clean -workspace %s.xcworkspace -configuration %s -target %s' % (project_path,project_name,configuration,scheme_name)) # clean 项目
        os.system('cd %s;mkdir build' % project_path) # 创建build目录
    else:
        #xcodebuild clean -project ${PROJECT_NAME}.xcodeproj -configuration ${CONFIGURATION} -alltargets
        os.system('cd %s;xcodebuild clean -project %s.xcodeproj -configuration %s  -target %s' % (project_path,project_name,configuration,scheme_name)) # clean 项目

# 编译工程为.app或者.xcarchive
def build_project():
    print("build %s start"%(configuration))
    os.system ('xcodebuild -list')
    
    if userCocoaPods == 1 :#使用cocoaPods
        #        build_string = "cd %s;xcodebuild -workspace %s.xcworkspace  -scheme %s -configuration %s -derivedDataPath %s ONLY_ACTIVE_ARCH=NO || exit" % (project_path,project_name,scheme_name,configuration,build_path)
        build_string = "cd %s;xcodebuild -workspace %s.xcworkspace -scheme %s -configuration %s -archivePath build/%s.xcarchive archive" % (project_path,project_name,scheme_name,configuration,scheme_name)
        print("使用cocoaPods：编译命令：%s" %(build_string));
        os.system (build_string)
    else:#使用非cocoaPods
        #        build_string = "cd %s;xcodebuild -project %s.xcodeproj  -scheme %s -configuration %s -derivedDataPath %s ONLY_ACTIVE_ARCH=NO || exit" % (project_path,project_name,scheme_name,configuration,build_path)
        build_string = "cd %s;xcodebuild  -scheme %s -configuration %s -archivePath build/%s.xcarchive archive" % (project_path,scheme_name,configuration,scheme_name)
        print("不使用cocoaPods：编译命令：%s" %(build_string));
        os.system (build_string)

# 打包ipa 并且保存在桌面
def build_ipa():
    global ipa_filename
    ipaName = scheme_name;
    ipa_filename = ipaName + "_" + configuration + time.strftime('_%Y-%m-%d-%H-%M-%S.ipa',time.localtime(time.time()))
    #    os.system ('xcrun -sdk iphoneos PackageApplication -v %s -o %s/%s'%(build_app_path,targetIPA_path,ipa_filename))
    #    os.system ('xcrun -sdk iphoneos xcodebuild -exportArchive  %s  %s/%s'%(build_app_path,targetIPA_path,ipa_filename))
    
    build_ipa_string = "xcodebuild  -exportArchive -exportFormat IPA -archivePath %s/%s.xcarchive -exportPath %s/%s -exportProvisioningProfile %s" % (build_path,scheme_name,targetIPA_path,ipa_filename,ProvisioningProfile)
    print("编译ipa包命令：%s" %(build_ipa_string));
    os.system (build_ipa_string)


if __name__ == '__main__':
    # 替换渠道信息文件
    replaceConfigFile()
    # 清理并创建build目录
    clean_project_mkdir_build()
    # 编译coocaPods项目文件并 执行编译目录
    build_project()
    # 打包ipa 并制定到桌面
    build_ipa()



