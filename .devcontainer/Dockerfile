FROM ubuntu:22.04

ARG USERNAME=vscode
ARG USER_ID
ARG GROUP_ID

# 対話的なインストールを避けるために、環境変数を設定
ARG DEBIAN_FRONTEND=noninteractive

# ホストから渡されたUIDとGIDをリモートに設定
RUN set -eux; \
	EXISTING_GROUP=$(getent group ${GROUP_ID} | cut -d: -f1 || true); \
	if [ -z "$EXISTING_GROUP" ]; then \
	groupadd --gid ${GROUP_ID} ${USERNAME}; \
	GROUP_NAME=${USERNAME}; \
	else \
	GROUP_NAME=$EXISTING_GROUP; \
	fi && \
	useradd --uid ${USER_ID} --gid ${GROUP_ID} -ms /bin/bash ${USERNAME} && \
	mkdir -p /etc/sudoers.d && \
	echo "${USERNAME} ALL=(ALL) NOPASSWD:ALL" > /etc/sudoers.d/${USERNAME}

RUN apt-get update && apt-get install -y \
	git \
	cmake \
	ninja-build \
	python3 \
	python3-pip \
	tar \
	libnewlib-arm-none-eabi \
	libhidapi-hidraw0 \
	libftdi1-2 \
	clang-format \
	&& apt-get clean && rm -rf /var/lib/apt/lists/*

# Unityをクローン
RUN git clone https://github.com/ThrowTheSwitch/Unity.git /opt/Unity

# Unityの環境変数を通す
ENV UNITY_PATH=/opt/Unity

# コンテナにマウントするディレクトリ
WORKDIR /workspace

# devcontainerの仕様上、何もしないでも生きているコンテナを作らないと落ちるためプロセスを永続化
CMD [ "sleep", "infinity" ]