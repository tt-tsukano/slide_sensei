import os
import datetime
from load_presentation import load_presentation
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import FAISS

# --- 設定 ---
file_path = "sample.pptx"
review_mode = "all"  # "all" または "related"

# --- 資料読み込み ---
documents = load_presentation(file_path)

# --- ベクトル化（関連モード用） ---
embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
vectorstore = FAISS.from_documents(documents, embeddings)

# --- レビュー依頼 ---
query = "この資料をよりわかりやすくするための改善点を提案して"

# --- スライド抽出 ---
if review_mode == "related":
    results = vectorstore.similarity_search(query, k=3)
else:
    results = documents  # 全スライド

# --- GPT呼び出し ---
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

slide_texts = "\n\n".join(
    [f"[スライド {r.metadata.get('slide_number', '?')}]\n{r.page_content}" for r in results]
)

prompt = f"""
あなたは優秀なプレゼン資料コンサルタントです。
以下のスライド内容を確認し、それぞれのスライドごとに改善提案を日本語で出してください。
スライド番号ごとに区切り、箇条書き形式で短くまとめてください。

{slide_texts}
"""

response = llm.invoke(prompt)

# --- 出力 ---
print("=== 改善提案 ===")
print(response.content)

# --- 保存処理 ---
os.makedirs("reviews", exist_ok=True)
date_str = datetime.datetime.now().strftime("%Y%m%d_%H%M")
base_name = os.path.splitext(os.path.basename(file_path))[0]
save_path = f"reviews/{date_str}_{review_mode}_{base_name}_review.md"

with open(save_path, "w", encoding="utf-8") as f:
    f.write(f"# 改善提案（{base_name}）\n\n")
    f.write(response.content)

print(f"\nレビュー結果を保存しました: {save_path}")
