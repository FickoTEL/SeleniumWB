#! /bin/sh
proc_name="weibojs.py"
log_name="/root/crontab_log.log"

# 计算进程数
proc_num()
{
	num=`ps -ef | grep $proc_name | grep -v grep | wc -l`
	return $(($num))
}

proc_num
number=$?

if [ $number -eq 0 ]
then
    # 执行重启
	. ./reboot_jobs.sh
else
    echo 'weibojs.py is running. Current time: ' `date` >> $log_name
fi