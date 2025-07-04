#!/bin/bash -e

# 记录脚本开始时间
start_time=$(date +%s)

# 显示开始时间（可选）
echo "脚本开始执行时间: $(date -d @$start_time '+%Y-%m-%d %H:%M:%S')"

# 执行Docker构建
docker build -t ${CNB_DOCKER_REGISTRY}/${CNB_REPO_SLUG_LOWERCASE}:latest . -f .ide/Dockerfile

# 执行Docker推送
docker push ${CNB_DOCKER_REGISTRY}/${CNB_REPO_SLUG_LOWERCASE}:latest

# 记录脚本结束时间
end_time=$(date +%s)

# 计算总用时（秒）
total_time=$((end_time - start_time))

# 转换为更易读的格式
hours=$((total_time / 3600))
minutes=$(( (total_time % 3600) / 60 ))
seconds=$((total_time % 60))

# 输出总用时
echo "===================================="
echo "脚本执行完成"
echo "总用时: ${total_time}秒 (${hours}小时 ${minutes}分钟 ${seconds}秒)"
echo "脚本结束时间: $(date -d @$end_time '+%Y-%m-%d %H:%M:%S')"
echo "===================================="