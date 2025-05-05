#!/bin/bash
set -e

# 引数チェック
if [ -z "$1" ]; then
	echo "初期化されたプロジェクトディレクトリ名を指定してください"
	echo "使用例: ./move_pico_project.sh temp_project"
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

echo "中身を移動中..."
shopt -s dotglob
mv "$SRC"/* "$DST"/
rm -rf "$SRC"

echo "/buildディレクトリを削除中..."
rm -rf "$DST/build"

echo ""
echo "スクリプト完了：このままでは CMake が再構成されません。"
echo "[Ctrl+Shift+P] → 'Developer: Reload Window' で VSCode を再読み込みしてください。"
