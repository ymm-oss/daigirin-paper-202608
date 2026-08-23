module.exports = {
  title: 'ゆめみ執筆委員会 フリーペーパー',
  author: 'ゆめみ執筆委員会',
  language: 'ja',
  size: 'A4',
  theme: [
    '@mitsuharu/vivliostyle-theme-iosdc-pamphlet@0.3.1',
    '@mitsuharu/vivliostyle-theme-noto-sans-jp',
    'theme/styles',
  ],
  entry: ['index.md'],
  entryContext: './manuscripts',
  output: ['./output/output.pdf'],
  workspaceDir: '.vivliostyle',
  toc: false,
  cover: undefined,
  vfm: {
    hardLineBreaks: false,
    disableFormatHtml: false,
  },
}
