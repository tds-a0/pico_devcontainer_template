#!/usr/bin/env python3
"""
move_pico_project.py
DevContainer環境でPicoプロジェクトを移動するためのPythonスクリプト
環境変数PROJECT_NAMEを使用してプロジェクト名を取得します
"""

import sys
import os
import re
import shutil
from pathlib import Path
from typing import Optional, List
from datetime import datetime


class PicoProjectMover:
    # Picoプロジェクト移動を管理するクラス
    
    def __init__(self, root_dir: Path = None):
        self.root_dir = root_dir or Path(__file__).parent.absolute()
        self.project_name = self._get_project_name()
        
    def _get_project_name(self) -> str:
        # 環境変数またはディレクトリ名からプロジェクト名を取得
        project_name = os.environ.get('PROJECT_NAME')
        if not project_name:
            print("警告: PROJECT_NAME環境変数が設定されていません")
            print("フォルダ名から自動取得します...")
            project_name = self.root_dir.name
        return project_name
    
    def _print_header(self):
        # ヘッダー情報を表示
        print("=" * 50)
        print("プロジェクト移動用スクリプト")
        print("=" * 50)
        print(f"プロジェクト名: {self.project_name}")
        print(f"ルートディレクトリ: {self.root_dir}")
        print()
    
    def validate_arguments(self, args: List[str]) -> str:
        # コマンドライン引数を検証
        if len(args) < 2:
            print("エラー: 初期化されたプロジェクトディレクトリ名を指定してください")
            print("使用例: ./move_pico_project.py temp_project")
            sys.exit(1)
        return args[1]
    
    def validate_directories(self, init_dir: str) -> tuple[Path, Path]:
        # ディレクトリの存在と状態を検証
        src_dir = self.root_dir / init_dir
        dst_dir = self.root_dir
        
        print(f"移動元: {src_dir}")
        print(f"展開先: {dst_dir}")
        print()
        
        # CMakeLists.txtの存在確認
        cmake_file = src_dir / "CMakeLists.txt"
        if not cmake_file.exists():
            print(f"エラー: {src_dir} に有効なPicoプロジェクトが見つかりません")
            print("CMakeLists.txt が存在しません")
            sys.exit(1)
        
        # 既存プロジェクトの確認
        existing_cmake = dst_dir / "CMakeLists.txt"
        if existing_cmake.exists():
            print(f"エラー: {dst_dir} には既にプロジェクトが存在します")
            print("既存のプロジェクトを削除してから実行してください")
            sys.exit(1)
        
        return src_dir, dst_dir
    
    def create_env_file(self) -> None:
        # 環境変数ファイルを作成
        env_file = self.root_dir / ".env"
        try:
            with open(env_file, 'w', encoding='utf-8') as f:
                f.write(f"PROJECT_NAME={self.project_name}\n")
            print(f".env ファイルを作成しました")
        except IOError as e:
            print(f"警告: .envファイルの作成に失敗しました: {e}")
    
    def merge_gitignore(self, src_dir: Path) -> None:
        # gitignoreファイルをマージ（重複削除
        src_gitignore = src_dir / ".gitignore"
        dst_gitignore = self.root_dir / ".gitignore"
        
        if not src_gitignore.exists():
            return
        
        print(".gitignore をマージ中...")
        
        # 既存の.gitignoreの内容を読み込み
        existing_lines = set()
        if dst_gitignore.exists():
            try:
                with open(dst_gitignore, 'r', encoding='utf-8') as f:
                    existing_lines = {line.strip() for line in f if line.strip()}
            except IOError as e:
                print(f"警告: 既存の.gitignoreの読み込みに失敗: {e}")
        
        # 新しい.gitignoreの内容を読み込み
        try:
            with open(src_gitignore, 'r', encoding='utf-8') as f:
                new_lines = {line.strip() for line in f if line.strip()}
        except IOError as e:
            print(f"警告: 移動元の.gitignoreの読み込みに失敗: {e}")
            return
        
        # マージして重複削除
        merged_lines = sorted(existing_lines | new_lines)
        
        # 書き込み
        try:
            with open(dst_gitignore, 'w', encoding='utf-8') as f:
                for line in merged_lines:
                    f.write(f"{line}\n")
            print(".gitignore のマージが完了しました")
        except IOError as e:
            print(f"警告: .gitignoreのマージに失敗: {e}")
        
        # 移動元のgitignoreを削除
        try:
            src_gitignore.unlink()
        except OSError as e:
            print(f"警告: 移動元.gitignoreの削除に失敗: {e}")
    
    def cleanup_build_directory(self, src_dir: Path) -> None:
        # ビルドディレクトリを削除
        build_dir = src_dir / "build"
        if build_dir.exists():
            print(f"{build_dir} ディレクトリを削除中...")
            try:
                shutil.rmtree(build_dir)
                print("ビルドディレクトリを削除しました")
            except OSError as e:
                print(f"警告: ビルドディレクトリの削除に失敗: {e}")
    
    def move_project_files(self, src_dir: Path, dst_dir: Path, init_dir: str) -> None:
        # プロジェクトファイルを移動
        print("プロジェクトファイルを移動中...")
        
        moved_count = 0
        for item in src_dir.iterdir():
            if item.name == ".gitignore":
                continue  # 既にマージ済み
            
            dst_item = dst_dir / item.name
            try:
                if item.is_dir():
                    shutil.move(str(item), str(dst_item))
                else:
                    shutil.move(str(item), str(dst_item))
                moved_count += 1
            except OSError as e:
                print(f"警告: {item.name} の移動に失敗: {e}")
        
        print(f"{moved_count} 個のファイル/ディレクトリを移動しました")
        
        # 移動元ディレクトリを削除
        try:
            src_dir.rmdir()
            print(f"移動元ディレクトリ {init_dir} を削除しました")
        except OSError as e:
            print(f"警告: 移動元ディレクトリの削除に失敗: {e}")
    
    def update_cmake_project_name(self, init_dir: str) -> None:
        # CMakeLists.txtのプロジェクト名と実行可能ファイル名を更新
        cmake_file = self.root_dir / "CMakeLists.txt"
        
        if not cmake_file.exists():
            print("警告: CMakeLists.txt が見つかりません。プロジェクト名の書き換えをスキップします。")
            return
        
        print(f"CMakeLists.txt のプロジェクト名を {self.project_name} に変更中...")
        
        try:
            # ファイルを読み込み
            with open(cmake_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 1. project()行のプロジェクト名を置換
            project_pattern = rf'^(\s*project\s*\(\s*){re.escape(init_dir)}(\s+.*?)$'
            project_replacement = rf'\1{self.project_name}\2'
            
            updated_content, project_count = re.subn(
                project_pattern, 
                project_replacement, 
                content, 
                flags=re.MULTILINE
            )
            
            # 2. add_executable()行の実行可能ファイル名を置換
            # 一般的なパターン: add_executable(old_name ...)
            executable_pattern = rf'^(\s*add_executable\s*\(\s*){re.escape(init_dir)}(\s+.*?)$'
            executable_replacement = rf'\1{self.project_name}\2'
            
            updated_content, executable_count = re.subn(
                executable_pattern,
                executable_replacement,
                updated_content,
                flags=re.MULTILINE
            )
            
            # 3. pico_set_program_name()行を置換
            program_name_pattern = rf'^(\s*pico_set_program_name\s*\(\s*){re.escape(init_dir)}(\s+.*?)$'
            program_name_replacement = rf'\1{self.project_name}\2'
            
            updated_content, program_name_count = re.subn(
                program_name_pattern,
                program_name_replacement,
                updated_content,
                flags=re.MULTILINE
            )
            
            # 4. その他のターゲット参照も置換（target_link_libraries等）
            other_target_pattern = rf'\b{re.escape(init_dir)}\b'
            updated_content, other_count = re.subn(
                other_target_pattern,
                self.project_name,
                updated_content
            )
            
            total_changes = project_count + executable_count + program_name_count + other_count
            
            if total_changes > 0:
                # ファイルに書き戻し
                with open(cmake_file, 'w', encoding='utf-8') as f:
                    f.write(updated_content)
                
                print(f"CMakeLists.txt を更新しました")
                print(f"更新箇所: project({project_count}) executable({executable_count}) program_name({program_name_count}) other({other_count})")
                
                # 更新された重要な行を表示
                for line in updated_content.split('\n'):
                    line_stripped = line.strip()
                    if (line_stripped.startswith('project(') or 
                        line_stripped.startswith('add_executable(') or
                        line_stripped.startswith('pico_set_program_name(')):
                        print(f"更新行: {line_stripped}")
            else:
                print("警告: 置換対象が見つかりませんでした")
                print(f"検索対象: '{init_dir}' → '{self.project_name}'")
                
        except IOError as e:
            print(f"エラー: CMakeLists.txt の更新に失敗: {e}")
        except re.error as e:
            print(f"エラー: 正規表現エラー: {e}")
    
    def cleanup_build_artifacts(self) -> None:
        # 最終的なビルド成果物のクリーンアップ
        build_dir = self.root_dir / "build"
        if build_dir.exists():
            print("既存のbuildディレクトリを削除...")
            try:
                shutil.rmtree(build_dir)
                print("buildディレクトリを削除しました")
            except OSError as e:
                print(f"警告: buildディレクトリの削除に失敗: {e}")
    
    def print_completion_message(self) -> None:
        # 完了メッセージを表示
        print()
        print("=" * 50)
        print("スクリプト完了")
        print("=" * 50)
        print()
        print("次の手順:")
        print("1. [Ctrl+Shift+P] でコマンドパレットを開く")
        print("2. 'Developer: Reload Window' を選択してVSCodeを再読み込み")
        print("3. CMakeが自動的に再構成されることを確認")
        print()
        print(f"プロジェクト名: {self.project_name}")
        print("環境変数 PROJECT_NAME が設定されています")
        print("=" * 50)
    
    def move_project(self, init_dir: str) -> None:
        # プロジェクト移動のメイン処理
        try:
            # ディレクトリ検証
            src_dir, dst_dir = self.validate_directories(init_dir)
            
            # .envファイル作成
            self.create_env_file()
            
            # .gitignoreマージ
            self.merge_gitignore(src_dir)
            
            # ビルドディレクトリクリーンアップ
            self.cleanup_build_directory(src_dir)
            
            # プロジェクトファイル移動
            self.move_project_files(src_dir, dst_dir, init_dir)
            
            # CMakeLists.txtのプロジェクト名更新
            self.update_cmake_project_name(init_dir)
            
            # 最終クリーンアップ
            self.cleanup_build_artifacts()
            
            # 完了メッセージ
            self.print_completion_message()
            
        except KeyboardInterrupt:
            print("\n処理が中断されました")
            sys.exit(1)
        except Exception as e:
            print(f"\n予期しないエラーが発生しました: {e}")
            print("詳細なエラー情報:")
            import traceback
            traceback.print_exc()
            sys.exit(1)


def main():
    # メイン関数
    # 実行時引数チェック
    if len(sys.argv) < 2:
        print("エラー: 初期化されたプロジェクトディレクトリ名を指定してください")
        print("使用例: ./move_pico_project.py temp_project")
        sys.exit(1)
    
    # PicoProjectMoverのインスタンス作成
    mover = PicoProjectMover()
    
    # ヘッダー表示
    mover._print_header()
    
    # 引数検証
    init_dir = mover.validate_arguments(sys.argv)
    
    # プロジェクト移動実行
    mover.move_project(init_dir)


if __name__ == "__main__":
    main()