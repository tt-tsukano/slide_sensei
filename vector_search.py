import os
from load_presentation import load_presentation
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS

# 1. スライドを読み込み
file_path = "sample.pptx"
documents = load_presentation(file_path)

# 2. OpenAIの埋め込みモデルを準備
embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

# 3. FAISSを使ってベクトルストアを作成（メモリ上）
vectorstore = FAISS.from_documents(documents, embeddings)

# 4. 質問を投げて検索
query = "LangChainでできることを説明して"
results = vectorstore.similarity_search(query, k=2) # 上位2件を取得

# 5. 検索結果を表示
for i, res in enumerate(results):
    print(f"--- 検索結果 {i+1} ---")
    print(f"[metadata] {res.metadata}")
    print(res.page_content)
    print()