## Phoenix日志可视化工具设计

[TOC]

### 总体需求

```
1、日志导入，先实现支持单个日志文件的导入，再支持多个文件的导入；

2、根据时间段和关键字进行查找；

3、配合《Phoenix系统日志分析指南》使用，里面包含关键字；

4、根据常用业务自动统计，具备一定的智能化；
```



### 技术方案

#### 一、采用Python开发Windows桌面程序

界面设计如下：

![image-20240401104225967](C:\Users\liuheng\AppData\Roaming\Typora\typora-user-images\image-20240401104225967.png)



#### 二、功能模块

##### 1、界面交互功能

LogDialog.py

接口：

```
open_file_dialog()        #打开日志导入窗口
clear_result()            #清空日志查找结果
search()                  #查找日志关键字

behavior_analysis()       #机器人行为分析（包括手动、巡逻、值守、充电等状态）
charge_analysis()         #机器人充电分析
exception_analysis()      #机器人本体告警异常分析(长时间滞留/定位丢失/阻挡/巡逻点不可达)
soc_analysis()            #机器人电量分析
navi_analysis()           #机器人导航异常的状态分析
```

##### 2、日志关键字搜索功能

LogSearch.py

接口：

```
validate_log_name()    # 日志名称校验
highlight_keyword()    # 高亮关键字
filter_logs()          #根据时间段和关键字搜索日志，若没有时间段，则全局搜索
```

##### 3、根据日常业务自动分析统计

LogAnalysis.py

接口：

```
get_log_time()       #根据日志规则提取每行的时间
figure_behavior()    #机器人行为统计折线图
figure_normal()      #通用折线统计图

create_figure_keyword()      #根据关键字查找其指代的内容
search_keyword_num()         #查找以数字开头的每一行日志，以字符串存入数组
search_keyword_multiple()    #根据两个关键字查找其指代的内容

create_figure_behavior()    #机器人行为分析(手动、自动、巡逻、值守、各种充电、急停、SOS)
create_figure_charge()      #机器人充电状态分析
create_figure_exception()   #机器人告警异常分析(仅分析定位丢失/长时间滞留/阻挡/巡逻点不可达)
create_figure_soc()         #机器人电量变化趋势统计
create_figure_navi()        #机器人导航状态码统计
```



#### 三、程序打包

##### 1、以管理员身份运行Cmd窗口

##### 2、切换到Python脚本所在的目录

cd C:\Users\liuheng\AppData\Local\Programs\Python\Python310\Scripts

##### 3、执行打包命令

打包成带依赖库的.exe文件（-w 表示打开时不带cmd窗口）

pyinstaller --onedir -w --add-data "C:\Windows\Fonts\AdobeSongStd-Light.otf;Fonts" --name Phoenix日志可视化工具 E:\core\Tools\Tool\LogAnalysisTool\LogDialog.py

最后，生成的exe文件位于以下目录

C:\Users\liuheng\AppData\Local\Programs\Python\Python310\Scripts\dist
