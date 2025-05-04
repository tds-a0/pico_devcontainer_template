#!/bin/bash
set -e

# 引数チェック
if [ -z "$1" ]; then
	echo "初期化されたプロジェクトディレクトリ名を指定してください"
	echo "使用例: bash move_pico_project.sh temp_project"
	exit 1
fi

NAME="$1"
SRC="/workspace/$NAME"
DST="/workspace"

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

echo "中身を移動中..."
shopt -s dotglob
mv "$SRC"/* "$DST"/
rm -rf "$SRC"

# パス修正
VSCODE_LAUNCH="$DST/.vscode/launch.json"
if [ -f "$VSCODE_LAUNCH" ]; then
  echo "🛠 launch.json を修正中..."
  sed -i "s|$NAME/||g" "$VSCODE_LAUNCH"
fi

echo "完了しました！"