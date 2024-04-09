<h1 align="center"> MaterialManager </h1>

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
