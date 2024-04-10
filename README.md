<h1 align="center"> MaterialManager </h1>

[![wakatime](https://wakatime.com/badge/user/1d39df6a-cef0-41f7-a903-ef4b9dd13fb0/project/018c41f2-4f38-4875-b72b-1a79d2352c7d.svg)](https://wakatime.com/badge/user/1d39df6a-cef0-41f7-a903-ef4b9dd13fb0/project/018c41f2-4f38-4875-b72b-1a79d2352c7d)
## 介绍

一款自用的物资管理系统

## 安装

构建镜像

```bash
docker build -t materila-manager:0.0.1 .
```

启动容器

```bash
docker run -d --restart=always --name=material-manager -p 8080:80 material-manager
```

访问 http://localhost:8080/ 即可
