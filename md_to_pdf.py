import pypandoc
import os

# --- 設定 ---
input_md = "reviews/20250815_2224_all_sample_review.md"
output_pdf = os.path.splitext(input_md)[0] + ".pdf"

# --- 変換 ---
pypandoc.convert_text(
    open(input_md, encoding="utf-8").read(),
    to="pdf",
    format="md",
    outputfile=output_pdf,
    extra_args=["--standalone"]
)

print(f"PDFを作成しました: {output_pdf}")
