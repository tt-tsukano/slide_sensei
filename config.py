import os
from dotenv import load_dotenv

# 環境変数を読み込み
load_dotenv()

class Config:
    """アプリケーション設定クラス"""
    
    # OpenAI API設定
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    
    # アプリ設定
    REVIEW_MODE = os.getenv("REVIEW_MODE", "all")
    OUTPUT_DIR = os.getenv("OUTPUT_DIR", "output")
    REVIEWS_DIR = os.getenv("REVIEWS_DIR", "reviews")
    
    # モデル設定
    EMBEDDING_MODEL = "text-embedding-3-small"
    LLM_MODEL = "gpt-4o-mini"
    LLM_TEMPERATURE = 0
    
    # ファイル設定
    SUPPORTED_FORMATS = [".pdf", ".pptx"]
    
    @classmethod
    def validate(cls):
        """設定の妥当性をチェック"""
        if not cls.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEYが設定されていません。.envファイルまたは環境変数を確認してください。")
        
        # 必要なディレクトリを作成
        os.makedirs(cls.OUTPUT_DIR, exist_ok=True)
        os.makedirs(cls.REVIEWS_DIR, exist_ok=True)
        
        return True
