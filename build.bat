@echo off
echo SlideSensei ビルド開始...

REM 仮想環境の有効化
if exist venv\Scripts\activate.bat (
    echo 仮想環境を有効化中...
    call venv\Scripts\activate.bat
) else (
    echo 仮想環境が見つかりません。venv\Scripts\activate.bat を確認してください。
    pause
    exit /b 1
)

REM 依存関係のインストール
echo 依存関係をインストール中...
pip install -r requirements.txt
if errorlevel 1 (
    echo 依存関係のインストールに失敗しました。
    pause
    exit /b 1
)

REM PyInstallerのインストール
echo PyInstallerをインストール中...
pip install pyinstaller
if errorlevel 1 (
    echo PyInstallerのインストールに失敗しました。
    pause
    exit /b 1
)

REM ビルド実行
echo ビルドを開始します...
pyinstaller slide_sensei.spec
if errorlevel 1 (
    echo ビルドに失敗しました。
    pause
    exit /b 1
)

echo.
echo ビルドが完了しました！
echo 実行ファイル: dist\SlideSensei.exe
echo.
pause
