# New Relic OTelドキュメント監査（2026-11-02）

## 確認範囲

New Relic公式の[docs-websiteの固定スナップショット](https://github.com/newrelic/docs-website/tree/5bd894835ff800ecebb47e89a8e1fbb5fc96040e/src/content/docs)を対象に、英語版OTel配下156ページと関連73ページ、計229ページの本文・表・注意書きを確認した。

対象commit：`5bd894835ff800ecebb47e89a8e1fbb5fc96040e`。

関連資料にはOTel API対応、Kubernetes、Lambda、GenAI、Metric型、trace details、NRDOTリリースノートを含む。コード・画像・対話式設定の全分岐・外部リンク先全体は検証対象外。公開サイトと固定ソースの反映時期は異なる場合がある。

## 反映した主な内容

初回12項目と追加14項目の不足を、以下の判断条件へ反映した。個別の公式根拠は各参照資料に記載している。

| 判断条件 | 反映先 |
|---|---|
| OTLPとNew RelicエージェントのOTel API対応を区別。個別transactionはSpan、全体傾向は適合するMetricを選ぶ | [OTel選択手順](../skills/newrelic-query-cost/references/opentelemetry.md) |
| 単位、サンプリング、エラー定義、生成APMメトリクスの条件を照合 | 同上 |
| SpanEventの関連ID、非同期のspan links、Metric型・精度、ログのCustom Event化、取り込み欠損を区別 | [データモデル](../skills/newrelic-query-cost/references/opentelemetry-data-model.md) |
| DBのスナップショット・実行数・上位N件・実行計画・サービス帰属を区別 | [個別連携の集計条件](../skills/newrelic-query-cost/references/opentelemetry-integrations.md) |
| receiver別のrate・percentile・状態値・単位、観測階層と重複scrapeを確認 | 同上 |
| entityの識別、Collector・ATP・Lambda・GenAIの欠測、利用版の違いを確認 | データモデル・個別連携の集計条件 |

## 資料を適用するときの注意

- 本文・表・例で対応範囲や初期値が一致しない箇所がある。RPCの生成条件、エージェントの言語別対応、Redisのcluster対応、ATPの初期値などは利用版と実データで照合する。
- 公式のクエリ例でも、見出しと返却値、Metric型と関数、batchと集約の意味を確認する。SDK側の制限緩和だけでNew Relic側の取り込み制限が解除されるとは扱わない。
- IBM MQのラベル正規化とraw名の保持は矛盾しない。正規化はtargetName/clusterNameの例外であり、全ラベルの改名指示としない。前回の不一致指摘は訂正した。
- 古い導入例のdistribution名・component名は、利用版のリリースノートと照合する。

## 検証と限界

合成データ12テスト、パッケージ・内部リンク・数値台帳・形式検査は成功。独立エージェントの静的タスク2件でも主要条件を満たした。詳細は[検証記録](validation.md)と[再検証記録](otel-revalidation.md)を参照。

実アカウントでのNRQL実行・スキーマ・CCU効果は未検証。この監査は、New RelicのOTel関連資料すべての網羅や、全サンプルの実行成功を保証するものではない。
