FROM node:20.12.1 as frontend

WORKDIR /app
COPY /frontend /app/frontend
RUN cd /app/frontend \
    && npm i -g pnpm --registry=https://registry.npmmirror.com \
    && pnpm i && pnpm build


FROM python:3.11-slim

WORKDIR /app
COPY /backend .
COPY entrypoint.sh .

RUN sed -i s@/deb.debian.org/@/mirrors.aliyun.com/@g /etc/apt/sources.list.d/debian.sources \
    && sed -i s@/security.debian.org/@/mirrors.aliyun.com/@g /etc/apt/sources.list.d/debian.sources \
    && sed -i 's/\r$//' ./entrypoint.sh


RUN apt-get update \
    # && apt-get install -y --no-install-recommends gcc python3-dev bash nginx vim curl procps net-tools\
    && apt-get install -y --no-install-recommends nginx\
    && ln -sf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime

RUN pip install poetry -i https://pypi.tuna.tsinghua.edu.cn/simple\
    && poetry config virtualenvs.create false \
    && poetry install

COPY --from=frontend /app/frontend/dist /app/frontend
ADD mm.conf /etc/nginx/sites-available/mm.conf
RUN rm -f /etc/nginx/sites-enabled/default \
    && ln -s /etc/nginx/sites-available/mm.conf /etc/nginx/sites-enabled/ 

ENV LANG=zh_CN.UTF-8
EXPOSE 80

ENTRYPOINT [ "bash", "entrypoint.sh" ]