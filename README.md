# 재원 랩

설재원의 포트폴리오 사이트 「돌아가는 것들의 기록」. https://snowjaewon.github.io

빌드 도구 없는 정적 페이지다. `main` 에 push 하면 GitHub Pages 가 그대로 띄운다.

| 파일 | 내용 |
|---|---|
| `index.html` | 본문 전체 (대장 카드, 지표, 활동, 연표) |
| `assets/style.css` | 디자인 토큰과 레이아웃, 인쇄(PDF)용 스타일 |
| `assets/main.js` | 제목 글자 애니메이션, 스크롤 흐름, 카드 쌓기 순서 |
| `jaewon-lab-portfolio.pdf` | 같은 페이지를 인쇄 스타일로 뽑은 제출용 PDF |

## 갱신할 때

1. `index.html` 의 숫자와 문장을 고친다. 숫자는 실측값만 넣는다.
2. 푸터의 갱신 날짜를 바꾼다.
3. PDF 를 다시 뽑는다.

   ```sh
   "/c/Program Files (x86)/Microsoft/Edge/Application/msedge.exe" --headless=new --disable-gpu \
     --no-pdf-header-footer --virtual-time-budget=6000 \
     --print-to-pdf="C:\\Users\\설재원\\jaewon-lab\\jaewon-lab-portfolio.pdf" \
     "file:///C:/Users/설재원/jaewon-lab/index.html"
   ```

4. 커밋하고 push 한다.

## 원본

처음 사이트는 Higgsfield 웹사이트 빌더로 만들어 https://jaewon-lab.higgsfield.app 에 올렸다.
그 라이브 결과물(HTML 과 자산 40개)을 태그 `higgsfield-original` 에 그대로 보존했다.

```sh
git checkout higgsfield-original -- legacy-higgsfield
```
