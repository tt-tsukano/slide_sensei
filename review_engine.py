import os
import datetime
from typing import List, Dict, Any
from langchain.schema import Document
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import FAISS
from load_presentation import load_presentation
from config import Config

class ReviewEngine:
    """スライドレビュー処理エンジン"""
    
    def __init__(self):
        """初期化"""
        self.embeddings = OpenAIEmbeddings(model=Config.EMBEDDING_MODEL)
        self.llm = ChatOpenAI(
            model=Config.LLM_MODEL, 
            temperature=Config.LLM_TEMPERATURE
        )
        self.vectorstore = None
        self.documents = []
        
    def load_file(self, file_path: str) -> List[Document]:
        """ファイルを読み込み"""
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"ファイルが見つかりません: {file_path}")
            
        # ファイル形式チェック
        ext = os.path.splitext(file_path)[1].lower()
        if ext not in Config.SUPPORTED_FORMATS:
            raise ValueError(f"対応していないファイル形式です: {ext}")
            
        # ファイル読み込み
        self.documents = load_presentation(file_path)
        
        # ベクトルストア作成
        self.vectorstore = FAISS.from_documents(self.documents, self.embeddings)
        
        return self.documents
    
    def generate_review(self, review_mode: str = "all", query: str = None) -> Dict[str, Any]:
        """レビューを生成"""
        if not self.documents:
            raise ValueError("ファイルが読み込まれていません")
            
        # レビューモードに応じてスライドを選択
        if review_mode == "related" and query and self.vectorstore:
            results = self.vectorstore.similarity_search(query, k=3)
        else:
            results = self.documents
            
        # スライドテキストを結合
        slide_texts = "\n\n".join(
            [f"[スライド {r.metadata.get('slide_number', '?')}]\n{r.page_content}" 
             for r in results]
        )
        
        # プロンプト作成
        prompt = f"""
あなたは優秀なプレゼン資料コンサルタントです。
以下のスライド内容を確認し、それぞれのスライドごとに改善提案を日本語で出してください。
スライド番号ごとに区切り、箇条書き形式で短くまとめてください。

{slide_texts}
"""
        
        # LLM呼び出し
        response = self.llm.invoke(prompt)
        
        return {
            "content": response.content,
            "slide_count": len(results),
            "mode": review_mode,
            "query": query
        }
    
    def save_review(self, review_data: Dict[str, Any], original_file_path: str) -> str:
        """レビュー結果を保存"""
        # ファイル名生成
        date_str = datetime.datetime.now().strftime("%Y%m%d_%H%M")
        base_name = os.path.splitext(os.path.basename(original_file_path))[0]
        mode = review_data.get("mode", "all")
        
        # Markdown保存
        md_filename = f"{date_str}_{mode}_{base_name}_review.md"
        md_path = os.path.join(Config.REVIEWS_DIR, md_filename)
        
        with open(md_path, "w", encoding="utf-8") as f:
            f.write(f"# 改善提案（{base_name}）\n\n")
            f.write(f"**レビューモード**: {mode}\n")
            if review_data.get("query"):
                f.write(f"**検索クエリ**: {review_data['query']}\n")
            f.write(f"**対象スライド数**: {review_data['slide_count']}\n\n")
            f.write("---\n\n")
            f.write(review_data["content"])
        
        return md_path
