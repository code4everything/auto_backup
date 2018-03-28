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
pscp C:\Users\pantao\Documents\Projects\python\auto_backup\mysql.py root@180.97.80.83:/root/auto_backup
pscp C:\Users\pantao\Documents\Projects\python\auto_backup\config.json root@180.97.80.83:/root/auto_backup
```

> [Putty下载地址（pscp命令）](https://www.chiark.greenend.org.uk/~sgtatham/putty/latest.html)
> [项目地址](https://github.com/zhazhapan/auto_backup)

#### 5. 修改配置文件 `config.json`

``` json
{
    "mysql": {
        "user": "root",
        "password": "root",
        "host": "127.0.0.1",
        "database": "sego",
        "path": "/root/auto_backup/dumps",
        "dateFormat": "%Y-%m-%d-%H-%M-%S",
        "expired": "60*60*24*7",
        "schedulerParams": {
            "cron": true,
            "dayOfWeek": "0-6",
            "hour": 0,
            "minute": 0,
            "seconds": 10
        }
    }
}
```

#### 6. 启动脚本，使脚本在后台运行（不受终端影响）

``` shell
cd /root/auto_backup
setsid python mysql.py
# 或者
nohup python mysql.py &
```

#### 7. 检测脚本是否运行

``` shell
ps -ef | grep mysql.py
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
    setsid python mysql.py
    ```
    
3. 在 `/etc/rc.local` 最后一行中添加脚本路径

    ``` shell
    /root/auto_backup/auto.sh
    ```