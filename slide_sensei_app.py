import flet as ft
import os
import threading
from typing import Optional
from config import Config
from review_engine import ReviewEngine
from pdf_converter import PDFConverter

class SlideSenseiApp:
    """SlideSensei デスクトップアプリケーション"""
    
    def __init__(self):
        """初期化"""
        self.review_engine = ReviewEngine()
        self.pdf_converter = PDFConverter()
        self.current_file_path: Optional[str] = None
        self.current_review_path: Optional[str] = None
        
    def main(self, page: ft.Page):
        """メインアプリケーション"""
        # ページオブジェクトを保存
        self._page = page
        
        # ページ設定
        page.title = "SlideSensei - プレゼン資料レビューAI"
        page.theme_mode = ft.ThemeMode.LIGHT
        page.window.width = 1000
        page.window.height = 800
        page.window.resizable = True
        page.padding = 20
        
        # 設定の検証
        try:
            Config.validate()
        except ValueError as e:
            self.show_error_dialog(page, "設定エラー", str(e))
            return
        
        # UI要素の作成
        self.create_ui(page)
        
        # ページを更新
        page.update()
    
    def create_ui(self, page: ft.Page):
        """UI要素を作成"""
        # ヘッダー
        header = ft.Container(
            content=ft.Text(
                "SlideSensei - プレゼン資料レビューAI",
                size=24,
                weight=ft.FontWeight.BOLD,
                color=ft.Colors.BLUE_700
            ),
            margin=ft.margin.only(bottom=20)
        )
        
        # ファイル選択セクション
        file_section = self.create_file_section(page)
        
        # レビュー設定セクション
        review_section = self.create_review_section(page)
        
        # レビュー実行ボタン
        review_button = ft.ElevatedButton(
            text="レビューを生成",
            icon=ft.Icons.PLAY_ARROW,
            on_click=lambda _: self.run_review(page),
            disabled=True,
            width=200,
            height=50
        )
        self.review_button = review_button
        
        # レビュー結果表示エリア
        self.review_text = ft.TextField(
            label="レビュー結果",
            multiline=True,
            min_lines=10,
            max_lines=20,
            read_only=True,
            border_color=ft.Colors.GREY_400,
            expand=True
        )
        
        # 保存ボタン
        save_section = ft.Row([
            ft.ElevatedButton(
                text="Markdown保存",
                icon=ft.Icons.SAVE,
                on_click=lambda _: self.save_review(page),
                disabled=True
            ),
            ft.ElevatedButton(
                text="PDF変換",
                icon=ft.Icons.PICTURE_AS_PDF,
                on_click=lambda _: self.convert_to_pdf(page),
                disabled=True
            )
        ], spacing=10)
        
        self.save_section = save_section
        
        # ステータス表示
        self.status_text = ft.Text(
            "ファイルを選択してください",
            color=ft.Colors.GREY_600,
            size=14
        )
        
        # レイアウト
        page.add(
            header,
            file_section,
            review_section,
            ft.Container(
                content=review_button,
                alignment=ft.alignment.center,
                margin=ft.margin.only(top=20, bottom=20)
            ),
            ft.Container(
                content=ft.Text("レビュー結果", size=18, weight=ft.FontWeight.BOLD),
                margin=ft.margin.only(bottom=10)
            ),
            self.review_text,
            ft.Container(
                content=save_section,
                margin=ft.margin.only(top=20)
            ),
            ft.Container(
                content=self.status_text,
                margin=ft.margin.only(top=20)
            )
        )
    
    def create_file_section(self, page: ft.Page):
        """ファイル選択セクションを作成"""
        # ファイル選択ボタン
        file_picker = ft.FilePicker(
            on_result=self.on_file_selected
        )
        page.overlay.append(file_picker)
        
        # ファイル選択ボタン
        select_button = ft.ElevatedButton(
            text="ファイルを選択",
            icon=ft.Icons.UPLOAD_FILE,
            on_click=lambda _: file_picker.pick_files(
                allowed_extensions=["pdf", "pptx"],
                allow_multiple=False
            )
        )
        
        # 選択されたファイル名表示
        self.file_name_text = ft.Text(
            "ファイルが選択されていません",
            color=ft.Colors.GREY_600
        )
        
        return ft.Container(
            content=ft.Column([
                ft.Text("1. ファイル選択", size=16, weight=ft.FontWeight.BOLD),
                ft.Row([
                    select_button,
                    self.file_name_text
                ], spacing=20)
            ]),
            padding=20,
            border=ft.border.all(1, ft.Colors.GREY_300),
            border_radius=10,
            margin=ft.margin.only(bottom=20)
        )
    
    def create_review_section(self, page: ft.Page):
        """レビュー設定セクションを作成"""
        # レビューモード選択
        self.review_mode = ft.RadioGroup(
            content=ft.Column([
                ft.Radio(value="all", label="全スライドをレビュー"),
                ft.Radio(value="related", label="関連スライドのみレビュー")
            ]),
            value="all"
        )
        
        # 検索クエリ入力（関連モード用）
        self.query_input = ft.TextField(
            label="検索クエリ（関連モード用）",
            hint_text="例：この資料をよりわかりやすくするための改善点を提案して",
            visible=False,
            expand=True
        )
        
        # モード変更時の処理
        def on_mode_change(e):
            self.query_input.visible = e.control.value == "related"
            page.update()
        
        self.review_mode.on_change = on_mode_change
        
        return ft.Container(
            content=ft.Column([
                ft.Text("2. レビュー設定", size=16, weight=ft.FontWeight.BOLD),
                self.review_mode,
                self.query_input
            ]),
            padding=20,
            border=ft.border.all(1, ft.Colors.GREY_300),
            border_radius=10,
            margin=ft.margin.only(bottom=20)
        )
    
    def on_file_selected(self, e: ft.FilePickerResultEvent):
        """ファイルが選択された時の処理"""
        if e.files:
            file_path = e.files[0].path
            self.current_file_path = file_path
            
            # ファイル名を表示
            file_name = os.path.basename(file_path)
            self.file_name_text.value = f"選択中: {file_name}"
            self.file_name_text.color = ft.Colors.GREEN_700
            
            # レビューボタンを有効化
            self.review_button.disabled = False
            
            # ステータス更新
            self.status_text.value = f"ファイル '{file_name}' が選択されました"
            
            # UI更新
            self.file_name_text.update()
            self.review_button.update()
            self.status_text.update()
    
    def run_review(self, page: ft.Page):
        """レビューを実行"""
        if not self.current_file_path:
            self.show_error_dialog(page, "エラー", "ファイルが選択されていません")
            return
        
        # UI状態を更新
        self.review_button.disabled = True
        self.review_button.text = "レビュー生成中..."
        self.status_text.value = "レビューを生成中です..."
        page.update()
        
        # レビュー実行（同期的に実行）
        try:
            # ファイル読み込み
            documents = self.review_engine.load_file(self.current_file_path)
            
            # レビュー生成
            mode = self.review_mode.value
            query = self.query_input.value if mode == "related" else None
            
            review_data = self.review_engine.generate_review(mode, query)
            
            # UI更新
            self.update_review_result(review_data)
            
        except Exception as e:
            self.show_error_dialog(page, "レビューエラー", str(e))
            self.reset_ui_state()
    
    def update_review_result(self, review_data):
        """レビュー結果をUIに反映"""
        # レビュー結果を表示
        self.review_text.value = review_data["content"]
        
        # 保存ボタンを有効化
        for button in self.save_section.controls:
            button.disabled = False
        
        # ステータス更新
        self.status_text.value = f"レビューが完了しました（{review_data['slide_count']}スライド）"
        
        # UI更新
        self.review_text.update()
        self.save_section.update()
        self.status_text.update()
        self.reset_ui_state()
        
        # ページ全体を更新
        if hasattr(self, '_page'):
            self._page.update()
    
    def reset_ui_state(self):
        """UI状態をリセット"""
        self.review_button.disabled = False
        self.review_button.text = "レビューを生成"
        self.review_button.update()
    
    def save_review(self, page: ft.Page):
        """レビューを保存"""
        try:
            # レビュー保存
            review_path = self.review_engine.save_review(
                {"content": self.review_text.value, "mode": self.review_mode.value},
                self.current_file_path
            )
            
            self.current_review_path = review_path
            
            # 成功メッセージ
            self.show_success_dialog(page, "保存完了", f"レビューを保存しました:\n{review_path}")
            
        except Exception as e:
            self.show_error_dialog(page, "保存エラー", str(e))
    
    def convert_to_pdf(self, page: ft.Page):
        """PDFに変換"""
        if not self.current_review_path:
            self.show_error_dialog(page, "エラー", "レビューファイルが保存されていません")
            return
        
        try:
            # PDF変換
            pdf_path = self.pdf_converter.convert_review_to_pdf(self.current_review_path)
            
            # 成功メッセージ
            self.show_success_dialog(page, "PDF変換完了", f"PDFを作成しました:\n{pdf_path}")
            
        except Exception as e:
            self.show_error_dialog(page, "PDF変換エラー", str(e))
    
    def show_error_dialog(self, page: ft.Page, title: str, message: str):
        """エラーダイアログを表示"""
        page.dialog = ft.AlertDialog(
            title=ft.Text(title),
            content=ft.Text(message),
            actions=[
                ft.TextButton("OK", on_click=lambda _: self.close_dialog(page))
            ]
        )
        page.dialog.open = True
        page.update()
    
    def show_success_dialog(self, page: ft.Page, title: str, message: str):
        """成功ダイアログを表示"""
        page.dialog = ft.AlertDialog(
            title=ft.Text(title),
            content=ft.Text(message),
            actions=[
                ft.TextButton("OK", on_click=lambda _: self.close_dialog(page))
            ]
        )
        page.dialog.open = True
        page.update()
    
    def close_dialog(self, page: ft.Page):
        """ダイアログを閉じる"""
        page.dialog.open = False
        page.update()

def main():
    """メイン関数"""
    app = SlideSenseiApp()
    ft.app(target=app.main)

if __name__ == "__main__":
    main()
