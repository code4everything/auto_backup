# coding:utf-8
import json
import os
import tarfile
import time
from datetime import datetime

from apscheduler.schedulers.blocking import BlockingScheduler

# MySQL备份命令

dump_cmd = "mysqldump --user={user} --password={password} --skip-lock-tables --host={host} {database} > {file}"
# 读取配置文件
config = json.load(open('config.json', 'r'))['mysql']


def delete_expired():
    """
    删除过期文件
    """
    files = [f for f in os.listdir(config['path'])]
    for file in files:
        full_path = config['path'] + "/" + file
        # 文件是否过期
        is_expired = os.stat(full_path).st_mtime < (time.time() - eval(config['expired']))
        if is_expired:
            # 删除过期文件
            os.remove(full_path)
    print('[%s] delete expired dumped file(s) success' % get_custom_date())


def dump(database="mysql"):
    """
    开始备份数据库
    """
    # 文件名
    filename = "{database}-{date}.sql".format(database=database, date=get_custom_date(config['dateFormat']))
    # 文件绝对路径
    file = "{path}/{filename}".format(path=config['path'], filename=filename)
    # 备份
    os.system(dump_cmd.format(user=config['user'], password=config['password'], host=config['host'],
                              database=database, file=file))
    # 压缩
    tar = tarfile.open(file[0:len(file) - 3] + 'gz', 'w')
    tar.add(file, arcname=filename)
    tar.close()
    # 删除SQL文件
    os.remove(file)


def pre_dump():
    """
    检查配置，准备备份数据库
    """
    dbs = config['database']
    if isinstance(dbs, list):
        for db in dbs:
            dump(db)
    else:
        dump(dbs)
    print('[%s] dump success' % get_custom_date())
    delete_expired()


def get_custom_date(date_format="%Y-%m-%d %H:%M:%S"):
    return datetime.now().strftime(date_format)


if __name__ == "__main__":
    """
    程序入口
    """
    params = config['schedulerParams']
    # 开启定时任务
    scheduler = BlockingScheduler()
    if params['cron']:
        scheduler.add_job(pre_dump, 'cron', day_of_week=params['dayOfWeek'], hour=params['hour'],
                          minute=params['minute'])
    else:
        scheduler.add_job(pre_dump, 'interval', seconds=params['seconds'])
    print('[%s] starting mysql auto backup' % get_custom_date())
    scheduler.start()
