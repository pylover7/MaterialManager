FROM docker.cnb.cool/pylover/docker/python:3.11.12

# 修改镜像源
RUN sed -Ei "s/(deb|security).debian.org/mirrors.cloud.tencent.com/g" /etc/apt/sources.list.d/debian.sources

# 设置时区
RUN ln -sf /share/zoneinfo/Asia/Shanghai /etc/localtime && \
    echo "Asia/Shanghai" > /etc/timezone

# 安装 node
RUN apt install -y gnupg && \
    curl -fsSL https://deb.nodesource.com/setup_22.x | bash - && \
    apt update && apt install -y nodejs

# 安装 bun
RUN curl -fsSL https://bun.sh/install | bash && . /root/.bashrc

# 安装一些常用的工具
RUN apt-get update && \
    apt-get install -y \
    openssh-server curl wget git git-lfs vim tree axel unzip zsh aria2 nload && \
    apt-get -y autoremove

# 安装Oh My Zsh
RUN sh -c "$(curl -fsSL https://raw.githubusercontent.com/robbyrussell/oh-my-zsh/master/tools/install.sh)" -y
# 安装zsh插件
RUN git clone https://github.com/zsh-users/zsh-autosuggestions ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-autosuggestions && \
    git clone https://github.com/zsh-users/zsh-syntax-highlighting.git ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-syntax-highlighting
RUN sed -i 's/plugins=(git)/plugins=(git zsh-autosuggestions zsh-syntax-highlighting)/' ~/.zshrc
# 安装 uv
RUN pip install uv
ENV UV_DEFAULT_INDEX=https://mirrors.cloud.tencent.com/pypi/simple
ENV PATH="/root/.local/bin:$PATH"

# 安装 code-server 和 vscode 常用插件
RUN curl -fsSL https://code-server.dev/install.sh | sh \
    && code-server --install-extension redhat.vscode-yaml \
    && code-server --install-extension waderyan.gitblame \
    && code-server --install-extension ms-ceintl.vscode-language-pack-zh-hans \
    && code-server --install-extension mhutchie.git-graph \
    && code-server --install-extension tencent-cloud.coding-copilot \
    && code-server --install-extension ms-azuretools.vscode-containers \
    && code-server --install-extension cnbcool.cnb-welcome \
    && code-server --install-extension ms-python.python \
    && code-server --install-extension christian-kohler.path-intellisense \
    && code-server --install-extension vscode-icons-team.vscode-icons \
    && code-server --install-extension davidanson.vscode-markdownlint \
    && code-server --install-extension stylelint.vscode-stylelint \
    && code-server --install-extension bradlc.vscode-tailwindcss \
    && code-server --install-extension dbaeumer.vscode-eslint \
    && code-server --install-extension esbenp.prettier-vscode \
    && code-server --install-extension lokalise.i18n-ally \
    && code-server --install-extension csstools.postcss \
    && code-server --install-extension mikestead.dotenv \
    && code-server --install-extension antfu.iconify \
    && code-server --install-extension Vue.volar \
    && code-server --install-extension redjue.git-commit-plugin \
    && code-server --install-extension aaron-bond.better-comments \
    && echo done

# 复制 vscode 自定义到容器中
COPY .ide/settings.json /root/.vscode-server/data/Machine/settings.json
COPY .ide/settings.json /root/.local/share/code-server/Machine/settings.json

# 安装 btop
RUN git clone https://github.com/aristocratos/btop.git /btop
WORKDIR /btop
RUN make && make install && rm -rf /btop

# 设置启动命令
ENV CNB_WELCOME_EXECUTE_COMMAND="zsh"

# 清除 uv 缓存和 pip 缓存
RUN rm -rf ~/.cache/uv && rm -rf ~/.cache/pip

# 指定字符集支持命令行输入中文（根据需要选择字符集）
ENV LANG C.UTF-8
ENV LANGUAGE C.UTF-8

# 安装 WebStorm
RUN wget https://download.jetbrains.com/webstorm/WebStorm-2024.3.6.tar.gz
RUN mkdir -p /ide_cnb && tar -zxvf WebStorm-2024.3.6.tar.gz -C /ide_cnb && rm -rf WebStorm-2024.3.6.tar.gz