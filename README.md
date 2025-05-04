# pico_devcontainer_template

Rasberry Pi Picoプロジェクトを作成するためのdevcontainerテンプレート<br>
このテンプレートをコピーして、新しくリポジトリを作成してください。

## 対応プラットフォーム

本テンプレートはLinux(Ubuntu)専用です。
下記の理由によりWindowsやMacOS上でのDocker環境では動作を保証しません。

- ホスト環境のUID/GIDをそのままコンテナに反映する[スクリプト](.devcontainer/setup_devcontainer.sh)を使用しています。
	- ホストとコンテナでファイルの所有者を一致させることで、パーミッションの問題を防止する設計になっています。
	- これはホストの`id -u`、`id -g`を使用して動作します。
