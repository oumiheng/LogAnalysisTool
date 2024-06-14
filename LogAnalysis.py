#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
实现日志可视化功能
机器人行为分析
机器人充电分析
机器人电量分析
"""

import re
#import logging 
#import matplotlib
import matplotlib.pyplot as plt
from matplotlib import dates as mdates  
from matplotlib.font_manager import FontProperties  
from datetime import datetime

# 设置matplotlib的日志级别为WARNING或更高，以屏蔽DEBUG和INFO级别的消息  
#matplotlib.use('TkAgg')  # 如果你需要设置特定的后端，可以在这里设置  
#matplotlib.rcParams.update({'figure.max_open_warning': 0})  # 关闭最大打开图形数警告（如果需要）  
#logging.getLogger('matplotlib').setLevel(logging.WARNING) 

# 创建一个支持中文的字体对象（这里假设你有一个名为'AdobeSongStd-Light.otf'的宋体细体字文件）
#font = FontProperties(fname='C:\Windows\Fonts\AdobeSongStd-Light.otf', size=12) 
font = FontProperties(fname='.\_internal\Fonts\AdobeSongStd-Light.otf', size=12)  #改为相对路径

phoenix_log_pattern = r'([IWEF])(\d{2})(\d{2})\s+(\d{2}):(\d{2}):(\d{2})\.(\d{6})\s+(\w+)\s+(.*?):(\d+)\]\s+(.*)'  #日志格式正则表达式

# 根据日志规则提取每行的时间
def get_log_time(log_pattern, line):
    #提取时间
    match_time = re.search(log_pattern, line)
    if match_time:
        log_level, month, day, hour, minute, second, microsecond, threadid, filename, line_number, message = match_time.groups()
        log_time_str = f"{hour}:{minute}:{second}" #时分秒
        #log_time = datetime.strptime(log_time_str, "%H:%M:%S")
        return log_time_str

# 机器人行为统计折线图(同时显示充电情况)
def figure_behavior(figure_dict, figure_dict2, title, xlabel, ylabel, ylabel2):
    y_labels = [] #中文标签列表
    y_labels2 = [] #中文标签列表
    times = []
    values = []
    times2 = []
    values2 = []

    #将优先级数值转换成对应的中文任务名称
    for element in figure_dict.values(): #遍历值
        if element == 0:
            y_labels.append("无任务充电")
        elif element == 1:
            y_labels.append("值守")
        elif element == 2:
            y_labels.append("巡逻")
        elif element == 3:
            y_labels.append("动作组充电")
        elif element == 4:
            y_labels.append("跑指定路线")
        elif element == 5:
            y_labels.append("一键/低电量充电")
        elif element == 6:
            y_labels.append("下雨充电")
        elif element == 7:
            y_labels.append("告警联动")
        elif element == 8:
            y_labels.append("手动模式")
        elif element == 9:
            y_labels.append("特定区域做动作")
        elif element == 10:
            y_labels.append("充电屋内取消充电")
        elif element == 11:
            y_labels.append("未初始化")
        elif element == 12:
            y_labels.append("急停")
        elif element == 13:
            y_labels.append("SOS告警")

    for element in figure_dict2.values(): #遍历值
        if element == 0:
            y_labels2.append("未充电")
        elif element == 1:
            y_labels2.append("充电中")

    for key, value in figure_dict.items(): #行为
        times.append(key)
        values.append(value)

    for key, value in figure_dict2.items(): #充电
        times2.append(key)
        values2.append(value)

    # 将 datetime 对象转换为 matplotlib 的数值格式
    #numeric_timestamps = mdates.date2num(times)
    #numeric_timestamps2 = mdates.date2num(times2)
    
    error_msg = 'OK'
    try:
        plt.figure(figsize=(8, 6), dpi=80) # 创建一个图形 
        plt.plot(times, values, marker='.', linestyle='-', color='blue') 
        plt.title(title, fontproperties=font, fontsize=20)
        
        # 设置X轴刻度为所有的时间戳  
        #plt.gca().set_xticks(numeric_timestamps)  # 这将设置X轴刻度为所有时间戳  
        #plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))  # 设置日期格式    
        #plt.gcf().autofmt_xdate() # 自动调整日期的显示格式（这一步可能不是必需的，取决于你的数据）
        plt.xticks(times, rotation=75) #以字符串形式显示X轴刻度并旋转75°
        plt.xlabel(xlabel, fontproperties=font)  
        
        # 设置Y轴刻度为所有的y值
        plt.yticks(values, y_labels, fontproperties=font) 
        plt.ylabel(ylabel, fontproperties=font)

        plt.grid(True)    
        plt.show()
    except ValueError as ve:
        # 处理特定于值错误的异常  
        print(f"Value error occurred: {ve}") 
        error_msg = f'Value error occurred: {ve}'
        return error_msg
    except RuntimeError as re:  
        # 处理运行时错误  
        print(f"Runtime error occurred: {re}")
        error_msg = f'Value error occurred: {re}'  
        return error_msg
    except Exception as e:
       # 如果在绘图过程中发生任何异常，捕获它并打印错误信息  
        print(f"An error occurred: {e}")
        error_msg = f'Value error occurred: {e}'
        return error_msg
    return 'OK'

'''
        # 创建一个新的图形  
        fig, ax1 = plt.subplots()
    
        # 在左边的Y轴上绘制第一条折线，并设置颜色
        ax1.plot(numeric_timestamps, values, 'b-')
        # 设置X轴刻度为所有的时间戳  
        ax1.set_xticks(numeric_timestamps)  # 这将设置X轴刻度为所有时间戳 
        ax1.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))  # 设置日期格式
        # 设置X轴标签
        ax1.set_xlabel(xlabel, fontproperties=font)
        
        # 设置Y1轴刻度内容及颜色
        ax1.set_yticks(values) 
        ax1.set_yticklabels(y_labels, fontproperties=font)  # 将Y1轴刻度转换为中文说明
        ax1.tick_params(axis='y', labelcolor='b')  # 设置Y1轴刻度的颜色为蓝色
        # 设置Y1轴标签内容及颜色为蓝色
        ax1.set_ylabel(ylabel, fontproperties=font, color='b')
        
        # 创建共享同一个X轴但拥有不同Y轴的第二个Axes对象  
        ax2 = ax1.twinx()  
        
        # 在右边的Y轴上绘制第二条折线，并设置颜色
        ax2.plot(numeric_timestamps2, values2, 'r-')
        # 设置X轴刻度为所有的时间戳  
        #ax2.set_xticks(numeric_timestamps2)  # 这将设置X轴刻度为所有时间戳 
        #ax2.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))  # 设置日期格式  
        # 设置Y2轴刻度内容及颜色
        ax2.set_yticks(values2) 
        ax2.set_yticklabels(y_labels2, fontproperties=font)  # 将Y2轴刻度转换为中文说明
        ax2.tick_params(axis='y', labelcolor='r')  # 设置Y2轴刻度的颜色为红色
        # 设置Y2轴标签内容及颜色为红色
        ax2.set_ylabel(ylabel2, fontproperties=font, color='r') 
        
        # 设置标题
        fig.suptitle(title, fontproperties=font, fontsize=20) 

        # 确保X轴刻度旋转以避免重叠  
        plt.xticks(rotation=75)  
        plt.gcf().autofmt_xdate()  

        ax1.grid(True) #显示网格
        plt.show() # 显示图形
'''

# 通用折线统计图
def figure_normal(figure_dict, title, xlabel, ylabel):
    times = []
    values = []

    for key, value in figure_dict.items():
        times.append(key)
        values.append(value)

    # 将 datetime 对象转换为 matplotlib 的数值格式
    #numeric_timestamps = mdates.date2num(times)

    error_msg = 'OK'
    try:
        plt.figure(figsize=(8, 6), dpi=80)  
        plt.plot(times, values, marker='.', linestyle='-', color='blue') 
        plt.title(title, fontproperties=font, fontsize=20) #标题

        # 设置X轴刻度为所有的时间戳  
        #plt.gca().set_xticks(numeric_timestamps)  # 这将设置X轴刻度为所有时间戳  
        #plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))  # 设置日期格式    
        #plt.gcf().autofmt_xdate() # 自动调整日期的显示格式（这一步可能不是必需的，取决于你的数据）
        plt.xticks(times, rotation=75) #以字符串形式显示X轴刻度并旋转75°
        plt.xlabel(xlabel, fontproperties=font) #x轴标签

        # 设置Y轴刻度为所有的y值  
        plt.yticks(values, fontproperties=font)  #y轴刻度       
        plt.ylabel(ylabel, fontproperties=font) #y轴标签

        plt.grid(True) #显示网格        
        plt.show()  
    except ValueError as ve:
        # 处理特定于值错误的异常  
        print(f"Value error occurred: {ve}") 
        error_msg = f'Value error occurred: {ve}'
        return error_msg
    except RuntimeError as re:  
        # 处理运行时错误
        print(f"Runtime error occurred: {re}")
        error_msg = f'Value error occurred: {re}'  
        return error_msg
    except Exception as e:
       # 如果在绘图过程中发生任何异常，捕获它并打印错误信息  
        print(f"An error occurred: {e}")
        error_msg = f'Value error occurred: {e}'
        return error_msg

    return 'OK'

# 根据关键字查找其指代的内容
def create_figure_keyword(log_files, keyword):
    values_container = [] #保存数据跳变时的数据容器
    time_occurs = []  #保存数据跳变时的时刻
    for log_file in log_files:
        with open(log_file, 'r', encoding='utf-8', errors='ignore') as file:
            value_last = -1 #上一次的数值
            time_last = "" #上一次数值的时间点

            for line in file:
                # 判断每一行是否是日志标准格式
                log_msg = ''
                match_log = re.search(phoenix_log_pattern, line)
                if match_log:
                    log_level, month, day, hour, minute, second, microsecond, threadid, filename, line_number, message = match_log.groups()
                    log_msg = f'{message}' #提前日志行的有效信息
                else:
                    continue

                #包含关键字的行
                if keyword in log_msg:
                    pattern = rf'{keyword}(\d+(\.\d+)?)' # 匹配关键字后的浮点数或整数
                    #pattern = rf"{keyword}([^ ]+)"       # 使用正则表达式匹配关键字后面的内容，直到遇到空格
                    match = re.search(pattern, log_msg)
                    if match:
                        # 提取关键词表示的数值并插入到数组中
                        value_cur = float(match.group(1))
                        if value_last == value_cur:  #当前值等于上一次
                            time_last = get_log_time(phoenix_log_pattern, line)
                            continue
                        else:
                            #先插入跳变前的值
                            if value_last != -1 and time_last != "":
                                values_container.append(value_last) #当前值不等于上一次
                                time_occurs.append(time_last)

                            #再插入跳变后的值
                            values_container.append(value_cur) #当前值不等于上一次
                            time_cur = get_log_time(phoenix_log_pattern, line)
                            time_occurs.append(time_cur)

                            #将当前值赋值给上一次
                            value_last = value_cur
                            time_last = time_cur

            #结束搜索后，将最后一次结果存入数组
            if value_last != -1 and time_last != "":
                values_container.append(value_last)
                time_occurs.append(time_last)
    
    figure_dict = dict(zip(time_occurs, values_container)) #将时间戳数组和值数组组合成字典
    return figure_dict

# 查找以数字开头的每一行日志，以字符串存入数组
def search_keyword_num(log_files):
    values_container = [] #保存数据跳变时的数据容器
    time_occurs = []  #保存数据跳变时的时刻
    for log_file in log_files:
        with open(log_file, 'r', encoding='utf-8', errors='ignore') as file:
            value_last = -1 #上一次的数值
            time_last = "" #上一次数值的时间点

            for line in file:
                # 判断每一行是否是日志标准格式
                log_msg = ''
                match_log = re.search(phoenix_log_pattern, line)
                if match_log:
                    log_level, month, day, hour, minute, second, microsecond, threadid, filename, line_number, message = match_log.groups()
                    log_msg = f'{message}' #提前日志行的有效信息
                else:
                    continue

                # 查找日志信息以数字开头的行，并提取出数字（导航状态码）
                pattern = r"^(\d+)" # 正则表达式模式，匹配行首的数字 
                match = re.search(pattern, log_msg)
                if match:
                    # 提取关键词表示的数值并插入到数组中
                    #value_cur = float(match.group(1))
                    value_cur = match.group(1) #导航状态码以字符串表示
                    if value_last == value_cur:  #当前值等于上一次
                        time_last = get_log_time(phoenix_log_pattern, line)
                        continue
                    else:
                        #先插入跳变前的值
                        if value_last != -1 and time_last != "":
                            values_container.append(value_last) #当前值不等于上一次
                            time_occurs.append(time_last)

                        #再插入跳变后的值
                        values_container.append(value_cur) #当前值不等于上一次
                        time_cur = get_log_time(phoenix_log_pattern, line)
                        time_occurs.append(time_cur)

                        #将当前值赋值给上一次
                        value_last = value_cur
                        time_last = time_cur

            #结束搜索后，将最后一次结果存入数组
            if value_last != -1 and time_last != "":
                values_container.append(value_last)
                time_occurs.append(time_last)
    
    figure_dict = dict(zip(time_occurs, values_container))
    return figure_dict

# 根据两个关键字查找其指代的内容
def search_keyword_multiple(log_files, keyword1, keyword2):
    values_container = [] #保存数据跳变时的数据容器
    time_occurs = []  #保存数据跳变时的时刻
    for log_file in log_files:
        with open(log_file, 'r', encoding='utf-8', errors='ignore') as file:
            value_last = -1 #上一次的数值
            time_last = "" #上一次数值的时间点

            for line in file:
                # 判断每一行是否是日志标准格式
                log_msg = ''
                match_log = re.search(phoenix_log_pattern, line)
                if match_log:
                    log_level, month, day, hour, minute, second, microsecond, threadid, filename, line_number, message = match_log.groups()
                    log_msg = f'{message}' #提取日志行的有效信息
                else:
                    continue

                #匹配关键字
                pattern = rf'({keyword1}|{keyword2})\s+(\d+)' # 匹配关键字后的整数，\s+：匹配一个或多个空格
                match = re.search(pattern, log_msg)
                if match:
                    # 提取关键词表示的数值并插入到数组中
                    value_cur = match.group(2)
                    if value_last == value_cur:  #当前值等于上一次
                        time_last = get_log_time(phoenix_log_pattern, line)
                        continue
                    else:
                        #先插入跳变前的值
                        if value_last != -1 and time_last != "":
                            values_container.append(value_last) #当前值不等于上一次
                            time_occurs.append(time_last)

                        #再插入跳变后的值
                        values_container.append(value_cur) #当前值不等于上一次
                        time_cur = get_log_time(phoenix_log_pattern, line)
                        time_occurs.append(time_cur)

                        #将当前值赋值给上一次
                        value_last = value_cur
                        time_last = time_cur

            #结束搜索后，将最后一次结果存入数组
            if value_last != -1 and time_last != "":
                values_container.append(value_last)
                time_occurs.append(time_last)
    
    figure_dict = dict(zip(time_occurs, values_container))
    return figure_dict

###########################################################################################
# 机器人行为分析(手动、自动、巡逻、值守、各种充电、急停、SOS、跑指定路线)
def create_figure_behavior(log_files):
    keyword="设置优先级:"  #所有行为
    my_dict = create_figure_keyword(log_files, keyword)

    keyword2="是否在充电:" #充电情况
    my_dict2 = create_figure_keyword(log_files, keyword2)

    if not my_dict: #没有查到行为
        error_msg = '机器人行为分析-没有查到可用信息!'
        return error_msg
    else:
        strRes = figure_behavior(my_dict, my_dict2, "机器人行为分析", "时间轴", "行为", "充电状态")
        return strRes

#机器人充电状态分析
def create_figure_charge(log_files):
    keyword="是否在充电:"
    my_dict = create_figure_keyword(log_files, keyword)

    if not my_dict: #没有查到
        error_msg = '机器人充电分析-没有查到可用信息!'
        return error_msg
    else:
        #替换value值为中文含义
        for key, value in my_dict.items():
            if value == 1:
                my_dict[key] = '充电中'
            elif value == 0:
                my_dict[key] = '未充电'
            else:
                continue
        strRes = figure_normal(my_dict, "机器人充电分析", "时间轴", "充电状态")
        return strRes

# 机器人告警异常分析
def create_figure_exception(log_files):
    #两个关键字，满足其中任意一个即可
    keyword1='收到异常或告警类型:'
    keyword2='发送异常码:'
    my_dict = search_keyword_multiple(log_files, keyword1, keyword2)

    if not my_dict: #没有查到
        error_msg = '机器人告警异常分析-没有查到可用信息!'
        return error_msg
    else:
        #筛选出需要的告警和异常
        keys_to_remove = []
        for key, value in my_dict.items():
            if value == '428':
                my_dict[key] = '定位丢失'
            elif value == '432':
                my_dict[key] = '长时间滞留'
            elif value == '50100':
                my_dict[key] = '阻挡'
            elif value == '50104':
                my_dict[key] = '巡逻点不可达'
            else:
                keys_to_remove.append(key)

        # 使用列表推导式和dict.copy()来避免在迭代时修改字典  
        for key in keys_to_remove:  # 使用[:]来复制列表，避免在迭代时修改它（虽然在这个特定例子中不是必需的）  
            if key in my_dict:  
                del my_dict[key] 
 
        strRes = figure_normal(my_dict, "机器人本体告警异常分析", "时间轴", "告警类型/异常码")
        return strRes

# 机器人电量变化趋势统计
def create_figure_soc(log_files):
    keyword="机器人当前电量为: "
    my_dict = create_figure_keyword(log_files, keyword)
    if not my_dict: #没有查到
        error_msg = '机器人电量分析-没有查到可用信息!'
        return error_msg
    else:    
        strRes = figure_normal(my_dict, "机器人电量变化趋势", "时间轴", "电量百分比%")
        return strRes

# 机器人导航状态码统计
def create_figure_navi(log_files):
    my_dict = search_keyword_num(log_files)
    if not my_dict: #没有查到
        error_msg = '机器人导航状态分析-没有查到可用信息!'
        return error_msg
    else:
        #筛选出异常的导航状态码
        keys_to_remove = []
        for key, value in my_dict.items():
            if value == '100':
                my_dict[key] = '100(暂停)'
            elif value == '200':
                my_dict[key] = '200(任务被停止)'
            elif value == '300':
                my_dict[key] = '300(路径无效)'
            elif value == '303':
                my_dict[key] = '303(避障等待中)'
            elif value == '304':
                my_dict[key] = '304(避障中)'
            elif value == '305':
                my_dict[key] = '305(路径终点不可达)'
            elif value == '314':
                my_dict[key] = '314(路径起点不可达)'
            elif value == '401':
                my_dict[key] = '401(定位异常)'
            elif value == '402':
                my_dict[key] = '402(目标点不安全)'
            elif value == '403':
                my_dict[key] = '403(前方有障碍物)'
            elif value == '404':
                my_dict[key] = '404(目标点不可达)'
            elif value == '408':
                my_dict[key] = '408(未到达目标点)'
            elif value == '601':
                my_dict[key] = '601(不能转圈)'
            elif value == '603':
                my_dict[key] = '603(转圈失败)'
            elif value == '701':
                my_dict[key] = '701(激光近距离有障碍)' 
            elif value == '1004':
                my_dict[key] = '1004(定位程序异常)' 
            elif value == '1005':
                my_dict[key] = '1005(激光不匹配)' 
            elif value == '1006':
                my_dict[key] = '1006(定位丢失)' 
            else:
                keys_to_remove.append(key)
        
        # 使用列表推导式和dict.copy()来避免在迭代时修改字典  
        for key in keys_to_remove:  # 使用[:]来复制列表，避免在迭代时修改它（虽然在这个特定例子中不是必需的）  
            if key in my_dict:  
                del my_dict[key]

        strRes = figure_normal(my_dict, "导航状态分析", "时间轴", "导航状态码")
        return strRes