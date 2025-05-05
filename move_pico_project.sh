#!/bin/bash

# move_pico_project.sh
# これは、projectを移動するためのスクリプトです。
# このスクリプトは、pico-vscode拡張機能を使用して作成されたプロジェクトディレクトリを移動します。
# スクリプトは、.envファイルからPROJECT_NAMEを取得し、CMakeLists.txtのproject名を書き換えます。
# スクリプトは、.gitignoreをマージし、重複を削除します。
# スクリプトは、移動元のディレクトリを削除します。

set -e

# 引数チェック
if [ -z "$1" ]; then
	echo "初期化されたプロジェクトディレクトリ名を指定してください"
	echo "使用例: ./move_pico_project.sh temp_project"
	exit 1
fi

# スクリプトのディレクトリを取得
ROOT_DIR="$(cd "$(dirname "$0")" && pwd)"

NAME="$1"
SRC="${ROOT_DIR}/$NAME"
DST="${ROOT_DIR}"

echo "移動元: $SRC"
echo "展開先: $DST"

# ディレクトリの存在確認
if [ ! -f "$SRC/CMakeLists.txt" ]; then
	echo "$SRC に有効なプロジェクトが見つかりません"
	exit 1
fi

if [ -f "$DST/CMakeLists.txt" ]; then
	echo "$DST には既にプロジェクトがあります。手動で確認してください"
	exit 1
fi

# .env から PROJECT_NAME を取得
if [ -f "$DST/.env" ]; then
	source "$DST/.env"
else
	echo ".env ファイルが見つかりません。プロジェクト名を取得できません。"
	exit 1
fi

# .gitignore マージ処理（重複削除つき）
if [ -f "$SRC/.gitignore" ]; then
	echo ".gitignore をマージ中..."
	touch "$DST/.gitignore"

	# 2つのファイルを結合してソート＆重複削除
	awk 'NF && !seen[$0]++' "$SRC/.gitignore" "$DST/.gitignore" >"$DST/.gitignore.merged"
	mv "$DST/.gitignore.merged" "$DST/.gitignore"

	# 上書き防止のため削除
	rm -f "$SRC/.gitignore"
fi

echo "$SRC/buildディレクトリを削除中..."
rm -rf "$SRC/build"

echo "中身を移動中..."
shopt -s dotglob
mv "$SRC"/* "$DST"/
rm -rf "$SRC"

# CMakeLists.txt の project名を書き換え
CMAKE_FILE="$DST/CMakeLists.txt"
if [ -f "$CMAKE_FILE" ]; then
	echo "CMakeLists.txt のプロジェクト名を ${PROJECT_NAME} に書き換え中..."
	sed -i "s/${NAME}/${PROJECT_NAME}/g" "$CMAKE_FILE"
else
	echo "CMakeLists.txt が見つかりません。処理をスキップします。"
fi

echo ""
echo "スクリプト完了：このままでは CMake が再構成されません。"
echo "[Ctrl+Shift+P] → 'Developer: Reload Window' で VSCode を再読み込みしてください。"
