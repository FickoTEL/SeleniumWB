#! /bin/sh
host_dir=`echo ~`
proc_name=/root/weibojs.py"
log_name="/root/crontab_log.log"

# 杀掉进程
kill -9 `ps -ef | grep -e 'phantomjs' -e 'weibojs' | grep -v grep | awk '{print $2}' | xargs`
# 重启进程
cd $host_dir
nohup /usr/local/bin/python3.6 ${proc_name}&
# 写入log文件
echo 'weibojs.py Reboot time: ' `date` >> $log_name
