#!/bin/bash

# .devcontainer/setup_devcontainer.sh
# DevContainer環境でのセットアップスクリプト
# .envファイルを作成し、プロジェクト名を設定します

set -e

# コンテナ内のパスを使用
WORKSPACE_DIR="/workspace"
ENV_FILE="${WORKSPACE_DIR}/.env"

echo "DevContainer セットアップスクリプト"
echo "ワークスペース: ${WORKSPACE_DIR}"

if [ ! -f "$ENV_FILE" ]; then
	echo ".envファイルが存在しないので作成します..."

	# 環境変数PROJECT_NAMEから取得（devcontainer.jsonのremoteEnvで設定済み）
	if [ -n "$PROJECT_NAME" ]; then
		PROJECT_NAME_VALUE="$PROJECT_NAME"
		echo "環境変数からプロジェクト名を取得: $PROJECT_NAME_VALUE"
	else
		# フォールバック: エラーとして扱う
		echo "エラー: 環境変数PROJECT_NAMEが設定されていません"
		echo "devcontainer.jsonのremoteEnvでPROJECT_NAMEが設定されているか確認してください"
		exit 1
	fi

	# .envファイルに書き込み
	{
		echo "PROJECT_NAME=${PROJECT_NAME_VALUE}"
		# 他の環境変数があれば追加
	} >"$ENV_FILE"

	echo
	echo ".envファイルを作成しました"
	echo "ファイル内容:"
	cat "$ENV_FILE"

else
	echo ".envファイルが既に存在します"
	echo "現在の内容:"
	cat "$ENV_FILE"
fi

echo
echo "セットアップ完了"
echo "プロジェクト名: ${PROJECT_NAME:-'未設定'}"

exit 0