#!/usr/bin/env python3
"""A4 4 ページの PDF を A3 見開き 2 ページに面付けする。

センター2つ折りの折パンフレット用。印刷所は「展開した状態の見開きデータ」を
求めるため、A4 単ページの出力をこのスクリプトで A3 の紙面 2 枚に組み直す。

面付けは 4 ページ折の標準どおり。
    表面 = [ 表4（裏表紙） | 表1（表紙） ]
    裏面 = [ 表2（中面左） | 表3（中面右） ]

表と裏を 1 ページに混ぜてはいけない（印刷所の指示）。A3 の 1 ページが
紙の片面に対応する。

使い方:
    uv run --with pypdf python scripts/impose.py [入力PDF] [出力PDF]

既定は output/output.pdf -> output/press_a3.pdf。
"""

from pypdf import PdfReader, PdfWriter, PageObject, Transformation
import pathlib
import sys

MM = 72 / 25.4
A4_W, A4_H = 210 * MM, 297 * MM
A3_W, A3_H = 420 * MM, 297 * MM
TOLERANCE = 1.0  # pt

# (ラベル, 左に置くページの索引, 右に置くページの索引) 0 始まり
SHEETS = [
    ("表面", 3, 0),
    ("裏面", 1, 2),
]


def main() -> int:
    root = pathlib.Path(__file__).resolve().parent.parent
    src = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else root / "output/output.pdf"
    dst = pathlib.Path(sys.argv[2]) if len(sys.argv) > 2 else root / "output/press_a3.pdf"

    if not src.exists():
        print(f"入力が見つかりません: {src}", file=sys.stderr)
        print("先に `yarn pdf` を実行してください。", file=sys.stderr)
        return 1

    reader = PdfReader(src)

    if len(reader.pages) != 4:
        print(f"4 ページを想定していますが {len(reader.pages)} ページです。", file=sys.stderr)
        print("折パンフレットはページ数が偶数（4 面）である必要があります。", file=sys.stderr)
        return 1

    for i, page in enumerate(reader.pages, 1):
        w, h = float(page.mediabox.width), float(page.mediabox.height)
        if abs(w - A4_W) > TOLERANCE or abs(h - A4_H) > TOLERANCE:
            print(f"p{i} が A4 縦ではありません: {w / MM:.1f} x {h / MM:.1f} mm", file=sys.stderr)
            return 1

    writer = PdfWriter()
    for label, left, right in SHEETS:
        sheet = PageObject.create_blank_page(width=A3_W, height=A3_H)
        sheet.merge_transformed_page(reader.pages[left], Transformation())
        sheet.merge_transformed_page(
            reader.pages[right], Transformation().translate(A4_W, 0)
        )
        writer.add_page(sheet)
        print(f"{label}: 左 = p{left + 1}, 右 = p{right + 1}")

    dst.parent.mkdir(parents=True, exist_ok=True)
    with dst.open("wb") as f:
        writer.write(f)

    print(f"\n{dst.relative_to(root)} を作成しました（{dst.stat().st_size / 1024 / 1024:.2f} MB）")
    return 0


if __name__ == "__main__":
    sys.exit(main())
