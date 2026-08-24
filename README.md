# ゆめみ執筆委員会 フリーペーパー

ゆめみ執筆委員会の活動紹介フリーペーパーの原稿とビルド構成です。Markdown で書いた原稿を [Vivliostyle](https://vivliostyle.org/) で組版し、PDF を出力します。

[mitsuharu/iosdc-pamphlet-template](https://github.com/mitsuharu/iosdc-pamphlet-template) を元に作成しました。

## 出力の前提

**A4 仕上がり・中央 2 つ折りのパンフレット**を想定しています。判型は `vivliostyle.config.js` の `size: 'A4'` で指定しています。

Vivliostyle の出力は **A4 単ページの連なり**です。折ったときの面の並びは次のようになるため、PDF のページ順と紙面上の配置は一致しません。

| PDF ページ | 面 |
|:--|:--|
| 1 | 表紙 |
| 2 | 中面（左） |
| 3 | 中面（右） |
| 4 | 裏表紙 |

折って冊子にする前提なので、**ページ数は偶数**である必要があります。原稿を増減させるときは偶数を保ってください。

A4 の出力を A3 の紙面 2 枚に組み直すには `scripts/impose.py` を使います（「面付け」を参照）。

なお元テンプレートは綴じ本を想定しており、テーマが `@page :left` / `@page :right` でノド側を避けた左右非対称の余白を持ちます。2 つ折りには綴じがなく、ノドを避ける必要がないため、`theme/styles/styles.css` で左右対称に上書きしています。

## リポジトリ構成

| パス | 内容 |
|:--|:--|
| `manuscripts/index.md` | 原稿。本文と独自クラスの HTML ブロック |
| `manuscripts/images/` | 原稿で使う画像 |
| `theme/styles/styles.css` | 本ペーパー独自のスタイル |
| `vivliostyle.config.js` | 判型・テーマ・出力先の設定 |
| `prh-rules/` | textlint の表記ゆれ辞書 |
| `scripts/impose.py` | A4 の出力を A3 見開きに面付けする |
| `output/` | 生成物（Git 管理外） |

## セットアップ

```shell
corepack enable
```

```shell
yarn
```

## PDF の作成

`output/output.pdf` に出力されます。

```shell
yarn pdf
```

PDF を開く。

```shell
yarn open
```

作成と表示を同時に行う。

```shell
yarn start
```

### press-ready 版

`output/press.pdf` に出力されます。Docker で実行する場合は `yarn press`、ローカルで実行する場合は `yarn press-local`。

```shell
yarn press
```

## 面付け

A4 4 ページの出力を、A3 見開き 2 ページに組み直します。`output/press_a3.pdf` に出力されます。

```shell
uv run --with pypdf python scripts/impose.py
```

面付けは 4 ページ折の標準どおりです。

```text
A3 表面 = [ 表4（裏表紙） | 表1（表紙） ]
A3 裏面 = [ 表2（中面左） | 表3（中面右） ]
```

A3 の 1 ページが紙の片面に対応します。表と裏を 1 ページに混ぜてはいけません。

## 文章校正

```shell
yarn lint
```

## 原稿で使える独自クラス

`theme/styles/styles.css` で定義しています。

### `.book` — 表紙とテキストを横並びにする書籍紹介

```html
<section class="book">
    <div class="container">
        <div class="cover"><img src="…" alt="…" /></div>
        <div class="detail">
            <h3>書名</h3>
            <p>紹介文</p>
        </div>
    </div>
</section>
```

表紙幅は実寸で固定しています。flex 比率にすると紙面幅に応じて表紙の高さが変わり、ブロックが入りきらず面の下部に余白が出ます。

### `.book-gallery` — 表紙だけを並べる

```html
<section class="book-gallery">
    <div class="gallery-item">
        <img src="…" alt="…" />
        <div class="caption">書名</div>
    </div>
</section>
```

3 列固定です。`calc()` で gap を差し引いてから割っているので、紙面幅が変わっても列数は崩れません。

### `.text-image` — テキストと画像を横並びにする

```html
<section class="text-image">
    <div class="container">
        <div class="text">…</div>
        <div class="image"><img src="…" /></div>
    </div>
</section>
```

### `hr.page-break` — 明示的な改ページ

```html
<hr class="page-break" />
```

## テンプレートからの変更点

- ページ余白を左右対称に上書きしています（理由は「出力の前提」を参照）
- 上記の独自クラスを追加しています

## 過去の版

- [ymm-oss/daigirin-paper-202504](https://github.com/ymm-oss/daigirin-paper-202504) — 本リポジトリの前身
