# SlideSensei デスクトップアプリ

SlideSenseiは、LangChainを使用したプレゼン資料レビューAIのデスクトップアプリケーション版です。

## 機能

- **PDF/PPTXファイル読み込み**: プレゼン資料をアップロードして自動解析
- **AIレビュー生成**: OpenAI GPT-4を使用したスライド改善提案
- **2つのレビューモード**:
  - 全スライドレビュー: 全てのスライドを対象
  - 関連スライドレビュー: 特定のクエリに関連するスライドのみ
- **結果保存**: Markdown形式でレビュー結果を保存
- **PDF変換**: レビュー結果をPDFに変換

## セットアップ

### 1. 依存関係のインストール

```bash
# 仮想環境の作成（推奨）
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # macOS/Linux

# 依存関係のインストール
pip install -r requirements.txt
```

### 2. 環境変数の設定

`.env`ファイルを作成し、OpenAI APIキーを設定してください：

```bash
# .envファイルを作成
cp env_example.txt .env
```

`.env`ファイルを編集：
```
OPENAI_API_KEY=your_openai_api_key_here
```

## 使用方法

### 開発環境での実行

```bash
python slide_sensei_app.py
```

### アプリケーションの使い方

1. **ファイル選択**: 「ファイルを選択」ボタンでPDFまたはPPTXファイルをアップロード
2. **レビュー設定**: レビューモードを選択（全スライド or 関連スライド）
3. **レビュー実行**: 「レビューを生成」ボタンをクリック
4. **結果確認**: 生成されたレビュー結果を確認
5. **保存**: 「Markdown保存」でレビューを保存、「PDF変換」でPDFに変換

## ビルド（exe化）

### PyInstallerのインストール

```bash
pip install pyinstaller
```

### exeファイルの作成

```bash
# specファイルを使用してビルド
pyinstaller slide_sensei.spec

# または、直接コマンドでビルド
pyinstaller --onefile --windowed --name SlideSensei slide_sensei_app.py
```

### ビルド後のファイル

- `dist/SlideSensei.exe` - 実行可能ファイル
- このexeファイルは単独で動作し、Python環境は不要です

## ファイル構成

```
slide_sensei/
├── slide_sensei_app.py      # メインGUIアプリケーション
├── review_engine.py          # レビュー処理エンジン
├── pdf_converter.py          # PDF変換機能
├── config.py                 # 設定管理
├── load_presentation.py      # ファイル読み込み（既存）
├── slide_review.py           # 既存のレビュー処理
├── vector_search.py          # 既存のベクトル検索
├── split_documents.py        # 既存のドキュメント分割
├── requirements.txt          # 依存関係
├── slide_sensei.spec        # PyInstaller設定
├── env_example.txt          # 環境変数設定例
├── README.md                # このファイル
└── docs/                    # ドキュメント
    └── SlideSensei_Desktop_Dev_Request.md
```

## 技術仕様

- **言語**: Python 3.12
- **GUIフレームワーク**: Flet
- **AI処理**: LangChain + OpenAI API
- **ベクトル検索**: FAISS
- **ファイル対応**: PDF, PPTX
- **ビルドツール**: PyInstaller

## トラブルシューティング

### よくある問題

1. **OpenAI APIキーエラー**
   - `.env`ファイルに正しいAPIキーが設定されているか確認
   - 環境変数`OPENAI_API_KEY`が設定されているか確認

2. **ファイル読み込みエラー**
   - ファイル形式がPDFまたはPPTXであることを確認
   - ファイルが破損していないか確認

3. **ビルドエラー**
   - 全ての依存関係がインストールされているか確認
   - PyInstallerが最新版か確認

### ログの確認

アプリケーション実行時にエラーが発生した場合、コンソール出力を確認してください。

## ライセンス

このプロジェクトは学習目的で作成されています。

## サポート

問題が発生した場合は、GitHubのIssuesで報告してください。
