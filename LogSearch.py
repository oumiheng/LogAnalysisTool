#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
实现日志关键字查找功能
不区分大小写
不进行全词匹配
"""

import re  
import os 
import tkinter as tk
from datetime import datetime

phoenix_log_pattern = r'([IWEF])(\d{2})(\d{2})\s+(\d{2}):(\d{2}):(\d{2})\.(\d{6})\s+(\w+)\s+(.*?):(\d+)\]\s+(.*)'  #日志格式正则表达式

# 日志名称校验
def validate_log_name(log_files, log_type):  
    # 提取文件名
    for log_file in log_files:  
        log_name = os.path.basename(log_file) 
        # 构建正则表达式
        pattern = rf'^{re.escape(log_type)}\.(INFO|DEBUG|ERROR|WARNING)_(\d{{8}}-\d{{6}})\.\d+$' 
        # 匹配文件名 
        match = re.match(pattern, log_name)

        if match is None:
            return False
    return True 

# 高亮关键字
def highlight_keyword(text_widget, keyword, tag_name):  
    # 清除之前的高亮  
    text_widget.tag_remove(tag_name, "1.0", tk.END)  
  
    # 配置标签的样式  
    text_widget.tag_config(tag_name, background="yellow", foreground="red", font=("Courler new", 10))
  
    # 使用正则表达式查找关键字并高亮  
    start_pos = '1.0'  
    while True:  
        start_pos = text_widget.search(keyword, start_pos, nocase=True, stopindex=tk.END)  
        if not start_pos:  
            break  
        end_pos = f'{start_pos}+{len(keyword)}c'  
        text_widget.tag_add(tag_name, start_pos, end_pos)  
        start_pos = end_pos

# 根据时间段和关键字搜索日志，若没有时间段，则全局搜索
def filter_logs(log_files, start_time_str, end_time_str, keyword):  
    if start_time_str == "":
        start_time = ""
    else:
        start_time = datetime.strptime(start_time_str, "%H:%M:%S")  # 将日志中的时间字符串解析为datetime对象 

    if end_time_str == "":
        end_time = ""
    else:
        end_time = datetime.strptime(end_time_str, "%H:%M:%S")  # 将日志中的时间字符串解析为datetime对象

    log_list = []

    keyword = keyword.lower()  # 将关键字转换为小写
    
    # 循环读取日志每一行
    for log_file in log_files:
        with open(log_file, 'r', encoding='utf-8', errors='ignore') as f:
            log_list.append(os.path.basename(log_file)) #首先将日志名导入
            for line in f:
                lower_line = line.lower()  # 将每行内容转换为小写
                match = re.search(phoenix_log_pattern, line)
                if match:  
                    log_level, month, day, hour, minute, second, microsecond, threadid, filename, line_number, message = match.groups()  
                    log_time_str = f"{hour}:{minute}:{second}"
                    log_time = datetime.strptime(log_time_str, "%H:%M:%S") # 将日志中的时间字符串解析为datetime对象

                    if start_time == "" or end_time == "":
                        if keyword in lower_line:
                            log_list.append(line.strip())
                    else:
                        if start_time <= log_time <= end_time and keyword in lower_line:
                            log_list.append(line.strip())
                else: #不满足日志标准格式的打印,这里就不判断时间了
                    if keyword in lower_line:
                        log_list.append(line.strip())
    return log_list