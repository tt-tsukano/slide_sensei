import os
import pypandoc
from typing import Optional
from config import Config

class PDFConverter:
    """MarkdownからPDFへの変換クラス"""
    
    def __init__(self):
        """初期化"""
        self.output_dir = Config.OUTPUT_DIR
    
    def convert_md_to_pdf(self, md_file_path: str, output_filename: Optional[str] = None) -> str:
        """MarkdownファイルをPDFに変換"""
        if not os.path.exists(md_file_path):
            raise FileNotFoundError(f"Markdownファイルが見つかりません: {md_file_path}")
        
        # 出力ファイル名を決定
        if output_filename is None:
            base_name = os.path.splitext(os.path.basename(md_file_path))[0]
            output_filename = f"{base_name}.pdf"
        
        # 出力パスを生成
        output_path = os.path.join(self.output_dir, output_filename)
        
        try:
            # Pandocを使用してPDF変換
            pypandoc.convert_text(
                open(md_file_path, encoding="utf-8").read(),
                to="pdf",
                format="md",
                outputfile=output_path,
                extra_args=["--standalone"]
            )
            
            return output_path
            
        except Exception as e:
            raise RuntimeError(f"PDF変換に失敗しました: {str(e)}")
    
    def convert_review_to_pdf(self, review_md_path: str) -> str:
        """レビューファイルをPDFに変換"""
        return self.convert_md_to_pdf(review_md_path)
