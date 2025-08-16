from load_presentation import load_presentation

def split_page(documents):
    """
    ページ／スライドごとにチャンク化（= documents をそのまま返す）
    """
    # ここで必要なら前処理（改行や空白の整理）を追加
    return documents

if __name__ == "__main__":
    file_path = "sample.pptx"

    # ファイル読み込み
    documents = load_presentation(file_path)

    # ページ／スライド単位に分割
    chunks = split_page(documents)

    # 確認
    for i, chunk in enumerate(chunks):
        print(f"--- Chunk {i+1} ---")
        print(chunk.page_content[:200]) # 最初の200文字だけ表示
        print()