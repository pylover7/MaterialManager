<h1 style="text-align: center"> MaterialManager </h1>
<div style="text-align: center">

![GitHub commit activity](https://img.shields.io/github/commit-activity/m/pylover7/MaterialManager)
![GitHub License](https://img.shields.io/github/license/pylover7/MaterialManager)
[![wakatime](https://wakatime.com/badge/user/1d39df6a-cef0-41f7-a903-ef4b9dd13fb0/project/018c41f2-4f38-4875-b72b-1a79d2352c7d.svg)](https://wakatime.com/badge/user/1d39df6a-cef0-41f7-a903-ef4b9dd13fb0/project/018c41f2-4f38-4875-b72b-1a79d2352c7d)

</div>

## 介绍

一款适用于企业内部的物资管理平台，特点如下：

- 使用企业内部ldap系统登录
- 单独的权限管理
- 物资的自定义分类
- 区域的自定义划分
- 值班交接班功能
- ...

## 使用

创建 `docker-compose.yaml` 文件

```yaml
configs:
  create_db_sql:
    file: ./create_db.sql

services:
  db:
    image: ghcr.io/pylover7/mysql8
    restart: unless-stopped
    environment:
      MYSQL_ROOT_PASSWORD: mysql
      TZ: Asia/Shanghai
    volumes:
      - ./material-data:/var/lib/mysql:Z
    configs:
      - source: create_db_sql
        target: /docker-entrypoint-initdb.d/create_db.sql
        mode: 0777
    networks:
      material_net:
        aliases:
          - db
  material:
    image: ghcr.io/pylover7/material
    restart: unless-stopped
    environment:
      - DB_HOST=db
      - DB_DRIVER=org.mysql.jdbc.Driver
      - DB_URL=jdbc:mysql://db:3306/material?serverTimezone=Asia/Shanghai
      - DB_USERNAME=root
      - DB_PASSWORD=mysql
      - DEV=false
    volumes:
      - ./material-config:/app/config
      - ./material-logs:/app/logs
    ports:
      - '7001:80'
    depends_on:
      - db
    networks:
      material_net:
        aliases:
          - material

networks:
  material_net:
    driver: bridge
```

使用命令启动容器服务

```bash
docker-compose up -d
```

创建配置文件
在 `./material-config` 目录下添加配置文件 `config.yml`

```yml
app:
  title: MaterialManager
  description: A manager for material
  version: &version 1.0.7
  dev: true

# 启动服务配置信息
server:
  host: 127.0.0.1
  port: 8000
  reload: false
  cors_origins:
  - '*'
  cors_allow_credentials: true
  cors_allow_headers:
  - '*'
  cors_allow_methods:
  - '*'

# 密钥信息
secret:
  secret_key: <secret>
  jwt_algorithm: HS256
  jwt_access_token_expire_min: 30
  jwt_refresh_token_expire_min: 120

# 超级管理员信息
superUser:
  username: admin
  nickname: admin
  employeeID: "00000000"
  mobile: "18888888888"
  email: admin@example.com
  is_superuser: true
  remark: 管理员
  department: 管理员
  company: 管理员

# 数据库配置信息
db:
  start: mysql
  host: localhost
  port: 3306
  username: root
  password: mysql
  database: material

# ldap 服务器IP
ldap:
  host: <ldap IP>
  base: "dc=demo,dc=com"
  username: test
  password: test1234


# 日志配置信息
log:
  version: 1
  disable_existing_loggers: false
  formatters:
    default:
      (): uvicorn.logging.DefaultFormatter
      fmt: '%(levelprefix)s %(message)s'
      use_colors:
    access:
      (): uvicorn.logging.AccessFormatter
      fmt: '%(asctime)s | %(levelprefix)s %(client_addr)s - %(status_code)s - "%(request_line)s"'
  handlers:
    default:
      class: logging.StreamHandler
      formatter: default
      stream: ext://sys.stderr
    access:
      class: logging.StreamHandler
      formatter: access
      stream: ext://sys.stdout
  loggers:
    uvicorn:
      level: INFO
      handlers:
      - default
    uvicorn.error:
      level: INFO
    uvicorn.access:
      level: INFO
      handlers:
      - access
      propagate: false
```

交接班记录文件 `dutyInfo.ini`

```ini
[glb.tool]
dutyperson = 张三
dutypersondepart = xx处xx科
takeovertime = 2025-01-10 22:08:24

[glb.key]
dutyperson = 张三
dutypersondepart = xx处xx科
takeovertime = 2025-01-10 22:13:29

[wk.tool]
dutyperson = admin
dutypersondepart = 管理员
takeovertime = 2024-12-04 11:37:40

[wk.key]
dutyperson = xxx
dutypersondepart = 浙江火电维修处
takeovertime = 2024-11-01 22:37:52

[fk.tool]
dutyperson = admin
dutypersondepart = adminDepart
takeovertime = 2020-01-01 00:00:00

[fk.key]
dutyperson = admin
dutypersondepart = adminDepart
takeovertime = 2020-01-01 00:00:00
```

## 自定义开发

技术栈：

- 前端：
  - Vue3
  - Vite
  - ElementPlus
  - PureAdmin
  - ...
- 后端
  - python3.11
  - fastapi
  - mysql

### 环境搭建

数据库启动

```bash
docker run -itd --name mysql-server -p 3306:3306 -e MYSQL_ROOT_PASSWORD=mysqlroot mysql:latest

# 进入容器
docker exec -it mysql-server bash

# 进入mysql
mysql -uroot -p mysqlroot

# 创建数据库
create database material default character set utf8mb4 collate utf8mb4_unicode_ci;
```

后端

```bash
# 安装依赖 在目录 backend/ 下执行
uv sync

# 启动
uv run run.py
```

安装前端依赖

```bash
# 安装依赖 在目录 frontend/ 下执行
bun i

# 启动
bun dev
```

访问 http://localhost:8001/ 即可

### 代码规范检查

前端

```bash
bun lint
```

后端

```bash
autopep8 --in-place --recursive --aggressive app
```

### docker镜像

构建镜像

```bash
docker build -t material:1.0.9 .
```

保存镜像

```bash
docker save material:1.0.9 -o material109.tar
```

加载镜像

```bash
docker load -i material109.tar
```

## Status

![Alt](https://repobeats.axiom.co/api/embed/f700028c26f06ec181e8a12028e1f01d5e1b782d.svg "Repobeats analytics image")

## Star History

<a href="https://star-history.com/#pylover7/MaterialManager&Date">
 <picture>
   <source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/svg?repos=pylover7/MaterialManager&type=Date&theme=dark" />
   <source media="(prefers-color-scheme: light)" srcset="https://api.star-history.com/svg?repos=pylover7/MaterialManager&type=Date" />
   <img alt="Star History Chart" src="https://api.star-history.com/svg?repos=pylover7/MaterialManager&type=Date" />
 </picture>
</a>
