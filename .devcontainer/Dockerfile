FROM mcr.microsoft.com/devcontainers/base:ubuntu-22.04

# 対話的なインストールを避けるために、環境変数を設定
ARG DEBIAN_FRONTEND=noninteractive

# 基本パッケージのインストール
RUN apt-get update && apt-get install -y \
	build-essential \
	cmake \
	ninja-build \
	gcc-arm-none-eabi \
	libnewlib-arm-none-eabi \
	libstdc++-arm-none-eabi-newlib \
	gdb-multiarch \
	libhidapi-hidraw0 \
	libftdi1-2 \
	udev \
	clang-format \
	curl \
	wget \
	unzip \
	tar \
	# 削除とクリーンアップ
	&& apt-get clean \
	&& rm -rf /var/lib/apt/lists/*

# Unityをクローン
RUN git clone https://github.com/ThrowTheSwitch/Unity.git /opt/Unity

# Unityの環境変数を通す
ENV UNITY_PATH=/opt/Unity

# コンテナにマウントするディレクトリ
WORKDIR /workspace

# devcontainerの仕様上、何もしないでも生きているコンテナを作らないと落ちるためプロセスを永続化
CMD [ "sleep", "infinity" ]