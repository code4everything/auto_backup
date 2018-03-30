#### 1. 安装扩展源EPEL

``` shell
yum -y install epel-release
```

#### 2. 安装PIP

``` shell
yum -y install python-pip
```

#### 3. 安装Python第三方扩展库

``` shell
pip install apscheduler
```

#### 4. 上传脚本

``` shell
pscp local_dir user@ip:/remote_dir
# 例：
pscp C:\Users\pantao\Documents\Projects\python\auto_backup\mysql_auto_backup.py root@180.97.80.83:/root/auto_backup
pscp C:\Users\pantao\Documents\Projects\python\auto_backup\config.json root@180.97.80.83:/root/auto_backup
```

> [Putty下载地址（pscp命令）](https://www.chiark.greenend.org.uk/~sgtatham/putty/latest.html)
> [项目地址](https://github.com/zhazhapan/auto_backup)

#### 5. 修改配置文件 `mysql_config.json` （请根据实际情况修改）

``` json
{
    "nodes": [
        {
            "user": "zhazhapan",
            "password": "zhazhapan",
            "host": "127.0.0.1",
            "dbs": [
                "efo"
            ]
        }
    ],
    "mysqldump": "",
    "path": "/Users/pantao/Desktop/backup",
    "dateFormat": "%Y-%m-%d-%H-%M-%S",
    "expired": "60*60*24*100",
    "schedulerParams": {
        "cron": false,
        "dayOfWeek": "0-6",
        "hour": 15,
        "minute": 27,
        "seconds": 10
    }
}
```

> 说明：如果 `mysqldump` 已添加到环境变量（可直接执行 `mysqldump` 命令），则设置配置文件中的 `mysqldump` 值为空；
否则请将 `mysqldump` 值设置 `mysqldump` 所在的路径（并在结尾添加一个文件分隔符），比如 `/usr/local/mysql-5.7.17-macos10.12-x86_64/bin/`

#### 6. 启动脚本，使脚本在后台运行（不受终端影响）

``` shell
cd /root/auto_backup
setsid python mysql_auto_backup.py
# 或者
nohup python mysql_auto_backup.py &
```

#### 7. 检测脚本是否运行

``` shell
ps -ef | grep mysql_auto_backup.py
```

#### 8. 设置开机自启

1. 新建自启脚本

    ``` shell
    vim auto.sh
    ```
    
2. 添加内容

    ``` shell
    #!/usr/bin/env bash
    cd /root/auto_backup
    setsid python mysql_auto_backup.py
    ```
    
3. 在 `/etc/rc.local` 最后一行中添加脚本路径

    ``` shell
    /root/auto_backup/auto.sh
    ```