#!/bin/bash

# .devcontainer/setup_devcontainer.sh
# これは、pico_devcontainer_templateのセットアップスクリプトです。
# このスクリプトは、.envファイルを作成し、プロジェクト名称とユーザーID、グループIDを設定します。
# スクリプトは、エラーが発生した場合に終了します。
# スクリプトは、.envファイルが存在しない場合にのみ実行されます。
# スクリプトは、.envファイルの内容を表示します

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_ROOT="$(realpath "${SCRIPT_DIR}/..")"
ENV_FILE="${SCRIPT_DIR}/../.env"

if [ ! -f "$ENV_FILE" ]; then
	echo ".envファイルが存在しないので作成します..."

	# UIDとGIDを取得
	USER_ID=$(id -u)
	GROUP_ID=$(id -g)

	# プロジェクトフォルダのパスから名称を取得
	PROJECT_NAME="$(basename "$PROJECT_ROOT")"

	# .envファイルに書き込み
	{
		echo "LOCAL_UID=${USER_ID}"
		echo "LOCAL_GID=${GROUP_ID}"
		echo "PROJECT_NAME=${PROJECT_NAME}"
	} >"$ENV_FILE"

	echo
	echo ".envファイルを作成しました。内容:"
	cat "$ENV_FILE"

else
	echo ".envファイルが存在します。内容:"
	cat "$ENV_FILE"
fi

exit 0
