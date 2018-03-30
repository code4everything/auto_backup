# coding:utf-8
import json
import os
import tarfile
import time
from datetime import datetime

from apscheduler.schedulers.blocking import BlockingScheduler

# MySQL备份命令

dump_cmd = "{prefix}mysqldump --user={user} --password={password} --skip-lock-tables --host={host} {database} > {file}"
# 读取配置文件
config = json.load(open('mysql_config.json', 'r'))


def check_folder(path):
    """
    检查路径是否存在
    """
    if not os.path.exists(path):
        os.makedirs(path)


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


def dump(database="mysql", node=None):
    """
    开始备份数据库
    """
    # 文件名
    if node is None:
        node = {}
    filename = "{database}-{date}.sql".format(database=database, date=get_custom_date(config['dateFormat']))
    # 文件绝对路径
    path = config['path']
    check_folder(path)
    file = "{path}/{filename}".format(path=path, filename=filename)
    # 备份
    os.system(
        dump_cmd.format(prefix=config['mysqldump'], user=node['user'], password=node['password'], host=node['host'],
                        database=database, file=file))
    # 压缩
    tar = tarfile.open(file[0:len(file) - 3] + 'gz', 'w')
    tar.add(file, arcname=filename)
    tar.close()
    # 删除SQL文件
    os.remove(file)


def parse_node(node):
    """
    解析节点数据
    """
    dbs = node['dbs']
    if isinstance(dbs, list):
        for db in dbs:
            dump(db, node)
    else:
        dump(dbs, node)


def pre_dump():
    """
    检查配置，准备备份数据库
    """
    global config
    config = json.load(open('mysql_config.json', 'r'))
    nodes = config['nodes']
    if isinstance(nodes, list):
        for node in nodes:
            parse_node(node)
    else:
        parse_node(nodes)
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
