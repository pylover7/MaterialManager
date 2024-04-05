## 物资管理系统

构建镜像

```bash
  docker build -t materila-manager:0.0.1 .
```

启动容器

```bash
  docker run -d --restart=always --name=material-manager -p 8080:80 material-manager
```
