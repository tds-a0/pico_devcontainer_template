# pico_devcontainer_template

Raspberry Pi Pico公式VSCode拡張機能と組み合わせて使用するDevContainerテンプレート<br>
[Raspberry Pi Pico VSCode Extension](https://marketplace.visualstudio.com/items?itemName=raspberry-pi.raspberry-pi-pico)を使用したPico開発環境をDevContainer内で構築できます。


## 対応プラットフォーム

**本テンプレートはLinux(Ubuntu)専用です。**<br>
DevContainer Featuresとautomatic UID/GID mappingを使用しており、LinuxのDocker環境で最適化されています。

## 特徴

- **Raspberry Pi Pico公式拡張機能対応**: 拡張機能のすべての機能をDevContainer内で使用可能
- **自動環境構築**: DevContainer起動時に開発環境を自動セットアップ
- **ツールチェーン完備**: ARM GCC、CMake、デバッグツール等を事前インストール
- **USB デバイスサポート**: Picoの書き込み・デバッグが可能な権限設定
- **統一開発環境**: チーム全体で一貫した開発環境を共有

## 含まれるツール

- **GCC ARM Toolchain**: ARM Cortex-M開発用
- **CMake & Ninja**: ビルドシステム
- **Pico SDK**: VSCode拡張機能によって自動管理
- **Unity**: C言語用テストフレームワーク
- **picotool**: VSCode拡張機能によって自動管理
- **clang-format**: コードフォーマッター
- **GDB**: デバッガー
- **Python環境**: プロジェクト管理スクリプト用

## 使用手順

1. 本テンプレートを任意の場所にコピーし、VScodeで開いてください。
2. VScodeでコマンドパレットを開き`Dev Containers: Reopen in Container`を選択してDevContainerを起動します。
3. DevContainer内で、Raspberry Pi Pico拡張機能を使ってプロジェクトを初期化してください。
	- 初期化先時のプロジェクト名はtemp_project`など、一時的な名前にしてください。
	- 初期化時に拡張機能によって作成されるディレクトリは後の工程で削除されます。
4. 初期化後、ターミナルで以下のスクリプトを実行してプロジェクトの中身を`workspace/`に展開します。

	```bash
	$ ./move_pico_project.py temp_project
	```

	- 初期化ディレクトリ名を変更した場合は、`temp_project` をその名前に置き換えてください。

5. スクリプトは以下の処理を自動で行います
	- 初期化されたプロジェクトのファイル（`temp_project/`内の`.vscode/`, `src/`, `CMakeLists.txt`など）を `workspace/` に移動。
	- `.env` ファイルの内容（`PROJECT_NAME`）を元に、`CMakeLists.txt` 内のプロジェクト名が正しく書き換え。
		- たとえば、初期化時に `project(temp_project ...)` のように書かれていたものが、`.env` に記録された `PROJECT_NAME` に自動的に置き換わります。
	- 一時プロジェクトディレクトリ `temp_project/` の削除。

6. これにより、`workspace/` 直下に初期化されたPicoプロジェクトの構成が展開され、ホストで初期化された構成と同様になります。

7. VScodeのウィンドウを再読込してください。
	- スクリプトにより `build/` ディレクトリが削除されたため、再読み込みによりCMakeが自動的に再構成されます。
	- 再読み込み手順：
		- `Ctrl + Shift + P` を押してコマンドパレットを開く。
		- 「**Developer: Reload Window**」と入力して選択。
