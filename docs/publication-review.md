# 公開前レビュー（2026-11-02）

対象はリポジトリの作業ツリー（新規・未追跡ファイルを含む）と、ローカルで到達可能なGit履歴7コミット。内容レビューで見つかった以下の記載を修正した。

| 問題 | 対応 |
|---|---|
| READMEのCodex導入先が旧ディレクトリ | 現行公式資料の`~/.agents/skills`へ更新し、根拠リンクを追加 |
| 検証記録の6件・9件・12件や未実施・実施済みが混在 | 現在の12テスト・静的タスク2件を冒頭で一覧化。過去の実測と現在の検証を分離 |
| READMEで対応範囲・実測範囲が分かりにくい | OTel実NRQL・CCUは未検証、Claude Code/Copilotは導入手順照合までと明記 |
| New Relicの公式製品と読み違える余地 | コミュニティ製スキルであることを明記 |
| 参照元をNew Relic資料「のみ」としていた | OTel処理仕様にはOpenTelemetry公式資料も使う説明へ修正 |
| 公開用の検証手順に合成テストが含まれていなかった | READMEと検証記録に実行コマンドとPython要件を追加 |

## 内容・機密情報の確認

- OTelの個別transactionをSpanで調べること、全体指標とサンプリング済みSpanの母集団を分けること、単位・エラー定義・収集経路を確認する指示は維持した。
- 過去の6→2クエリ統合・約66.7%の観測値は、少量データ・各1実行のAPM/Browser比較という制約を維持した。OTelでの削減実測や一般的な削減率とは記載していない。
- 文書監査は固定スナップショット229ページの本文確認。全コード・全画像・全外部資料の検証や、抜け漏れゼロという主張はしていない。
- 現ファイルのパターン検査では、個人の絶対パス・メールアドレス・秘密鍵・主要形式のアクセストークン・長い資格情報代入を検出しなかった。ローカルの履歴7コミット・31個の固有blobにも資格情報パターンの一致はなかった。パターンに一致しない秘密情報や、未取得のリモート履歴まで保証する検査ではない。
- 再検証で使うentity値・サービス名・`pg.*`属性は試験用の仮定であることを明記した。

## 公式資料の照合

- [Codexのスキル保存先と呼び出し](https://learn.chatgpt.com/docs/build-skills#where-codex-loads-local-skills)
- [Claude Codeのスキル保存先](https://code.claude.com/docs/en/skills#choose-where-skills-load)
- [Copilot CLIのスキル導入](https://docs.github.com/en/copilot/how-tos/copilot-cli/customize-copilot/add-skills)
- [NRQLのLIMIT・FACET・TIMESERIES](https://docs.newrelic.com/docs/nrql/nrql-syntax-clauses-functions/)
- [OTel APMのMetric・Spanの使い分け](https://docs.newrelic.com/docs/opentelemetry/get-started/apm-monitoring/opentelemetry-apm-ui/)

## 検証と結論

公開記載として修正が必要だった点は上記へ反映した。形式・内部リンク・計測台帳の検査、合成データ12テスト、skill-creator形式検査、`git diff --check`は成功。OTelの実NRQL・CCUとClaude Code/Copilot上の動作試験が未実施であることを公開文書に残す。

新規のOTel参照資料・テスト・監査記録には未追跡ファイルがあるため、公開するコミットに一式が含まれる必要がある。Gitへの追加・コミット・push・リポジトリの公開設定変更はこのレビューに含めていない。
