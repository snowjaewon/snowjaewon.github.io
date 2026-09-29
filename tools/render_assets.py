"""인장 SVG 로 아이콘 PNG 와 링크 미리보기 카드(og.png)를 뽑는다.

먼저 make_seal.py 로 assets/seal.svg · seal-stamp.svg 를 만든 뒤 실행한다.
Edge 헤드리스로 그리고 Pillow 로 줄인다. (Edge 창은 504px 아래로 안 줄어서 크게 그린 뒤 줄인다.)

사용: python tools/render_assets.py
"""
import os
import subprocess
import tempfile

from PIL import Image

EDGE = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
ASSETS = os.path.join(ROOT, "assets")
PAPER = (247, 247, 244, 255)


def shot(url, width, height, out, transparent=False):
    args = [EDGE, "--headless=new", "--disable-gpu", "--hide-scrollbars",
            "--allow-file-access-from-files", "--virtual-time-budget=8000",
            f"--window-size={width},{height}", f"--screenshot={out}"]
    if transparent:
        args.append("--default-background-color=00000000")
    subprocess.run(args + [url], check=True, capture_output=True)


def file_url(path):
    return "file:///" + path.replace("\\", "/")


def save(img, name):
    path = os.path.join(ASSETS, name)
    img.save(path + ".tmp.png")
    os.replace(path + ".tmp.png", path)
    print(name, img.size)


def main():
    tmp = tempfile.mkdtemp()
    page = os.path.join(tmp, "seal.html")
    with open(page, "w", encoding="utf-8") as f:
        f.write('<!doctype html><body style="margin:0;background:transparent">'
                f'<img src="{file_url(os.path.join(ASSETS, "seal.svg"))}" '
                'style="display:block;width:1024px;height:1024px"></body>')
    raw = os.path.join(tmp, "seal.png")
    shot(file_url(page), 1024, 1024, raw, transparent=True)
    seal = Image.open(raw).convert("RGBA").crop((0, 0, 1024, 1024))

    def on_paper(size, ratio):
        canvas = Image.new("RGBA", (size, size), PAPER)
        inner = round(size * ratio)
        mark = seal.resize((inner, inner), Image.LANCZOS)
        off = (size - inner) // 2
        canvas.alpha_composite(mark, (off, off))
        return canvas.convert("RGB")

    save(seal.resize((32, 32), Image.LANCZOS), "favicon-32.png")
    save(on_paper(180, 0.84), "apple-touch-icon.png")
    save(on_paper(192, 0.84), "icon-192.png")
    save(on_paper(512, 0.84), "icon-512.png")
    # 마스커블 아이콘은 가운데 지름 80% 원 안만 보장된다 → 사각 인장은 한 변 56% 이하.
    save(on_paper(512, 0.56), "icon-512-maskable.png")

    og = os.path.join(tmp, "og.png")
    shot(file_url(os.path.join(ROOT, "tools", "og.html")), 1200, 630, og)
    save(Image.open(og).convert("RGB").crop((0, 0, 1200, 630)), "og.png")


if __name__ == "__main__":
    main()
