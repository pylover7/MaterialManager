FROM node:18.8.0-alpine3.16 as frontend

WORKDIR /app
COPY /frontend ./frontend
RUN cd /app/frontend \
    && corepack enable corepack prepare pnpm@8.15.6 --activate \
    && npm config set registry https://registry.npmmirror.com \
    && pnpm install --frozen-lockfile && pnpm build


FROM python:3.11-slim

WORKDIR /app
COPY /backend .
COPY entrypoint.sh .

RUN sed -i s@/deb.debian.org/@/mirrors.aliyun.com/@g /etc/apt/sources.list.d/debian.sources \
    && sed -i s@/security.debian.org/@/mirrors.aliyun.com/@g /etc/apt/sources.list.d/debian.sources

RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc python3-dev bash nginx vim curl procps net-tools\
    && ln -sf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime

RUN cd /app/backend && pip install poetry -i https://pypi.tuna.tsinghua.edu.cn/simple\
    && poetry config virtualenvs.create false \
    && poetry install

COPY --from=frontend /app/frontend/dist /app/frontend
ADD /deploy/web.conf /etc/nginx/sites-available/web.conf
RUN rm -f /etc/nginx/sites-enabled/default \ 
    && ln -s /etc/nginx/sites-available/web.conf /etc/nginx/sites-enabled/ 

ENV LANG=zh_CN.UTF-8
EXPOSE 80

ENTRYPOINT [ "sh", "entrypoint.sh" ]