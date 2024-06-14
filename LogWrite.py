import logging  
import os  
from datetime import datetime  
  
# 获取当前日期，用于创建目录  
today = datetime.now().strftime('%Y-%m-%d')  
log_dir = f'logs/{today}'  
  
# 如果目录不存在，则创建它  
if not os.path.exists(log_dir):  
    os.makedirs(log_dir)  
  
# 获取当前详细时间，用于创建日志文件名  
current_time = datetime.now().strftime('%Y%m%d_%H%M%S')  
log_file = f'{log_dir}/LogTool_{current_time}.log'
  
# 配置日志  
logging.basicConfig(filename=log_file, level=logging.INFO,  
                    format='%(asctime)s %(levelname)s %(message)s')  
  
# 创建一个日志记录器  
logger = logging.getLogger(__name__)  
  
# 写入日志  
#logger.debug('这是一条 debug 级别的日志')  
#logger.info('这是一条 info 级别的日志')  
#logger.warning('这是一条 warning 级别的日志')  
#logger.error('这是一条 error 级别的日志')  
#logger.critical('这是一条 critical 级别的日志')

#info级别日志
def write_log_info(info):
    logger.info(info)

#warning级别日志
def write_log_warning(info):
    logger.info(info)

#error级别日志
def write_log_error(info):
    logger.info(info)