# pico_devcontainer_template

Rasberry Pi Picoプロジェクトを作成するためのdevcontainerテンプレート<br>
本テンプレートをコピーして、新しくリポジトリを作成してください。

## 対応プラットフォーム

**本テンプレートはLinux(Ubuntu)専用です。**<br>
下記の理由によりWindowsやMacOS上でのDocker環境では動作を保証しません。

- ホスト環境のUID/GIDをそのままコンテナに反映する[スクリプト](.devcontainer/setup_devcontainer.sh)を使用しています。
	- ホストとコンテナでファイルの所有者を一致させることで、パーミッションの問題を防止する設計になっています。
	- これはホストの`id -u`、`id -g`を使用して動作します。

## 使用手順

1. 本テンプレートを任意の場所にコピーし、VScodeで開いてください。
2. VScodeでコマンドパレットを開き`Dev Containers: Reopen in Container`を選択してDevcontainerを起動します。
3. DevContainer内で、Raspberry Pi Pico拡張機能を使ってプロジェクトを初期化してください。
	- 初期化先のディレクトリは`/workspace/temp_project`など、一時的な名前にしてください。
	- このディレクトリは後の工程で削除されます。
4. 初期化後、ターミナルで以下のスクリプトを実行してプロジェクトの中身を`workspace/`に展開します。

	```bash
	$ ./move_pico_project.sh temp_project
	```

	- 初期化ディレクトリ名を変更した場合は、`temp_project` をその名前に置き換えてください。

5. スクリプトは以下の処理を自動で行います
	- 初期化されたプロジェクトのファイル（`temp_project`内の`.vscode/`, `src/`, `CMakeLists.txt`など）を `workspace/` に移動
	- 一時ディレクトリ `temp_project/` の削除

6. これにより、`workspace/` 直下に初期化されたPicoプロジェクトの構成が展開され、ホストで初期化された構成と同様になります

7. VScodeのウィンドウを再読込してください。
	- スクリプトにより `build/` ディレクトリが削除されたため、再読み込みによりCMakeが自動的に再構成されます。
	- 再読み込み手順：
		- `Ctrl + Shift + P` を押してコマンドパレットを開く
		- 「**Developer: Reload Window**」と入力して選択
