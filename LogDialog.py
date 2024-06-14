#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
实现日志分析功能的界面功能
"""

import tkinter as tk  
from tkinter import filedialog, scrolledtext

import LogSearch as log_search      #日志关键字查找
import LogAnalysis as log_analysis  #日志分析并生成相应图表
#import LogWrite as log_write        #记录操作过程

log_files = [] #日志文件列表

# 日志查询功能
# 打开日志导入窗口
def open_file_dialog(): 
    global log_files 
    file_paths = filedialog.askopenfilenames(title="选择日志文件", filetypes=[("日志文件", "*.*")])
    log_files = list(file_paths)
    log_text.delete(1.0, tk.END)
    for log_file in log_files:
        #log_label.config(text=f"导入日志: {log_file}")
        log_text.insert(tk.END, f"{log_file}\n")
        #log_write.write_log_info(f"导入日志: {log_file}")

# 清空查询结果
def clear_result():
    #log_write.write_log_info("清空查询结果")
    result_label.config(text="")
    result_text.delete(1.0, tk.END)

# 查找关键字
def search():
    if not log_files:
        result_text.insert(tk.END, "请先导入日志!\n")
        return

    search_count = 0 #匹配次数计数

    keyword = keyword_entry.get().strip()  # 关键字 
    start_time_str = time_start_entry.get().strip() #开始时间
    end_time_str = time_end_entry.get().strip()   #结束时间

    if keyword == "":
        #log_write.write_log_info("查找关键字为空，不进行查找")
        result_text.insert(tk.END, "请输入查找目标!\n")
        return
    else:
        clear_result() # 搜索新的关键字之前清空结果显示框

    # 这里可以添加真正的搜索逻辑
    log_list = log_search.filter_logs(log_files, start_time_str, end_time_str, keyword)  
    for line in log_list:
        search_count += 1
        result_text.insert(tk.END, f"{line}\n")

    # 高亮显示关键字
    search_count -= len(log_files) #总显示次数减去导入日志数量
    log_search.highlight_keyword(result_text, keyword, 'highlight')
    result_label.config(text=f"查找 '{keyword}' 在时间段 '{start_time_str}' 到 '{end_time_str}', 匹配 '{search_count}' 次")
    #log_write.write_log_info(f"查找 '{keyword}' 在时间段 '{start_time_str}' 到 '{end_time_str}', 匹配 '{search_count}' 次")

######################################################################
# 日志分析功能
# 机器人行为分析
def behavior_analysis():
    #log_write.write_log_info("进行机器人行为分析")
    if log_search.validate_log_name(log_files, 'CORE'):
        ret = log_analysis.create_figure_behavior(log_files)
        if ret != 'OK':
            result_text.insert(tk.END, f"{ret}\n")
            #log_write.write_log_info(f'{ret}')
    else:
        result_text.insert(tk.END, "机器人行为分析，请全部导入CORE模块日志!\n")

# 机器人充电分析
def charge_analysis():
    #log_write.write_log_info("进行机器人充电分析")
    if log_search.validate_log_name(log_files, 'CORE'):        
        ret = log_analysis.create_figure_charge(log_files)
        if ret != 'OK':
            result_text.insert(tk.END, f"{ret}\n")
            #log_write.write_log_info(f'{ret}')
    else:
        result_text.insert(tk.END, "机器人充电分析，请导入CORE模块日志!\n")

# 机器人本体告警异常分析(长时间滞留/定位丢失/阻挡/巡逻点不可达)
def exception_analysis():
    #log_write.write_log_info("机器人本体告警异常分析")
    if log_search.validate_log_name(log_files, 'CORE'):        
        ret = log_analysis.create_figure_exception(log_files)
        if ret != 'OK':
            result_text.insert(tk.END, f"{ret}\n")
            #log_write.write_log_info(f'{ret}')
    else:
        result_text.insert(tk.END, "机器人本体告警异常分析，请导入CORE模块日志!\n")

# 机器人电量分析
def soc_analysis():
    #log_write.write_log_info("进行机器人电量分析")
    if log_search.validate_log_name(log_files, 'BOARD'):
        ret = log_analysis.create_figure_soc(log_files)
        if ret != 'OK':
            result_text.insert(tk.END, f"{ret}\n")
            #log_write.write_log_info(f'{ret}')
    else:
        result_text.insert(tk.END, "机器人电量分析，请导入BOARD模块日志!\n")

# 机器人导航状态分析
def navi_analysis():
    #log_write.write_log_info("机器人导航状态分析")
    if log_search.validate_log_name(log_files, 'NAVICOMM'):
        ret = log_analysis.create_figure_navi(log_files)
        if ret != 'OK':
            result_text.insert(tk.END, f"{ret}\n")
            #log_write.write_log_info(f'{ret}')
    else:
        result_text.insert(tk.END, "机器人导航状态分析，请导入NAVICOMM模块日志!\n")

######################################################################
root = tk.Tk()  
root.title("高新兴机器人-Phoenix日志可视化工具v1.0")
root.geometry("960x600+150+15") #打开时大小和位置

# 当前日志路径显示
#log_label = tk.Label(root, text="", width=50) 
#log_label.pack(side=tk.TOP, fill=tk.X, padx=10, pady=(0, 5))
log_text = scrolledtext.ScrolledText(root, wrap=tk.WORD, height=1, width=1)
log_text.pack(side=tk.TOP, fill=tk.BOTH, expand=False, padx=10, pady=5)

# 当前操作提示  
result_label = tk.Label(root, text="", width=50)
result_label.pack(side=tk.TOP, fill=tk.X, padx=10, pady=(0, 5))

# 查找结果显示窗口（使用Text组件支持多行显示和滚动）
result_text = scrolledtext.ScrolledText(root, wrap=tk.WORD)
result_text.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=5)

######################################################################  
# 日志导入按钮  
file_button = tk.Button(root, text="日志导入", command=open_file_dialog)
file_button.pack(side=tk.TOP, fill=tk.X, padx=10, pady=(5, 10))
  
# 查找目标标题  
keyword_label = tk.Label(root, text="查找目标:")
keyword_label.pack(side=tk.TOP, fill=tk.X, padx=10, pady=0)
  
# 查找目标输入框
keyword_entry = tk.Entry(root)
keyword_entry.pack(side=tk.TOP, fill=tk.X, padx=10, pady=0)
  
# 从什么时间
time_range_label = tk.Label(root, text="开始时间")
time_range_label.pack(side=tk.TOP, fill=tk.X, padx=10, pady=0)

# 时间开始输入框
time_start_entry = tk.Entry(root)  #开始时间
time_start_entry.insert(0, "00:00:00")  
time_start_entry.pack(side=tk.TOP, fill=tk.X, padx=10, pady=0)

# 到什么时间
time_range_label2 = tk.Label(root, text="结束时间")
time_range_label2.pack(side=tk.TOP, fill=tk.X, padx=10, pady=0)

# 时间结束输入框
time_end_entry = tk.Entry(root)   #结束时间
time_end_entry.insert(0, "23:59:59")
time_end_entry.pack(side=tk.TOP, fill=tk.X, padx=10, pady=0)
  
# 在当前文件中查找  
search_button = tk.Button(root, text="查找", command=search)
search_button.pack(side=tk.TOP, fill=tk.X, padx=10, pady=5)

# 清空按钮
clear_button = tk.Button(root, text="清空", command=clear_result)
clear_button.pack(side=tk.TOP, fill=tk.X, padx=10, pady=5)

##############################################################
# 机器人行为分析(CORE.INFO)
analysis_button_behavior = tk.Button(root, text="行为分析(CORE)", command=behavior_analysis)
analysis_button_behavior.pack(side=tk.TOP, fill=tk.X, padx=10, pady=(20, 5))

# 机器人充电分析(CORE.INFO)
analysis_button_charge = tk.Button(root, text="充电分析(CORE)", command=charge_analysis)
analysis_button_charge.pack(side=tk.TOP, fill=tk.X, padx=10, pady=5)

# 机器人异常分析(SCOMM.INFO)
analysis_button_exception = tk.Button(root, text="告警异常分析(CORE)", command=exception_analysis)
analysis_button_exception.pack(side=tk.TOP, fill=tk.X, padx=10, pady=5)

# 机器人电量分析(BOARD.INFO)
analysis_button_soc = tk.Button(root, text="电量分析(BOARD)", command=soc_analysis)
analysis_button_soc.pack(side=tk.TOP, fill=tk.X, padx=10, pady=5)

# 机器人导航状态分析(NAVICOMM.INFO)
analysis_button_navi = tk.Button(root, text="导航异常(NAVICOMM)", command=navi_analysis)
analysis_button_navi.pack(side=tk.TOP, fill=tk.X, padx=10, pady=5)

root.mainloop()