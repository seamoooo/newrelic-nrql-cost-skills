# New Relic OTelドキュメント監査（2026-11-02）

## 対象と確認方法

New Relic公式の[docs-website](https://github.com/newrelic/docs-website/tree/5bd894835ff800ecebb47e89a8e1fbb5fc96040e/src/content/docs/opentelemetry)を取得。スナップショットは`5bd894835ff800ecebb47e89a8e1fbb5fc96040e`。英語版`/docs/opentelemetry/`以下の**156ページ**を全件列挙し、公式ナビゲーションとも照合した。加えて、配下外にあるOTel API対応、Kubernetes、Lambda、GenAI、Metric型、trace details、NRDOTリリースノートの**73ページ**を対象にした。

**再開分の220ページの本文・表・注意書きの通読を完了した。** 前回の9ページの仕様本文確認と合わせ、棚卸し済みの229ページの文章を確認した。初回は関連箇所の抽出確認に留まっていたため、今回はインストール説明・メトリクス表の各行・リリースノート本文も順番に読んだ。

MDXから本文と表を取り出し、コードブロック、コメント、対話式設定コンポーネントを除いて全51分割を確認。コメント内のコードフェンスで抽出がずれたNGINX host等は、コメントを先に除いた抽出との比較で補完した。対応表のチェックアイコンも元ソースで照合した。これは文章の確認であり、全コードのレビュー・実行、対話式設定の全分岐、画像の視認、リンク先すべての通読ではない。

対象は公開英語ドキュメントの上記スナップショット。翻訳の重複、New Relicサイト全体のOTelへの言及、ブログ、外部リンク先の全マニュアル・全コードを網羅したものではない。公開サイトとソースの反映タイミングも一致を保証しない。実データでの実行とエージェントの判断試験は別。

| 分類 | ページ数 |
|---|---:|
| best-practices | 8 |
| collector-observability | 3 |
| db360 | 65 |
| get-started | 8 |
| integrations | 62 |
| nrdot | 8 |
| overview | 2 |

## 見つかった不足と反映

| 項目 | 修正前の不足 | 対応 |
|---|---|---|
| OTel APIとOTLP | OTelという名前だけでSpan/Transactionを選ぶ可能性 | APIをNew Relicエージェントが取り込む構成を分離。保存後の実スキーマに従う |
| 生成APMメトリクスの単位 | 秒固定のAPM例を流用し得た | 元データのs/ms/nsを引き継ぐ条件を明記 |
| transaction名・生成条件 | Span名とメトリクス名の対応が不明確 | transaction.nameとtransactionName、必要なHTTP/RPC属性、元属性のコピー範囲を確認 |
| Span由来Metric | Metricなら非サンプリングと思う可能性 | messaging・overview・一部DB等の由来を確認 |
| 例外の取得 | SpanEventへの具体的な関連IDが不足 | Span.idとSpanEvent.span.id、trace.idを照合。例外数とエラーSpan数を区別 |
| 非同期トレース | trace.id・親子関係だけでは不足 | span linksによる別traceへの展開と未収集を明記 |
| Metric型と精度 | 型・temporality確認の具体性不足 | count/cumulativeCount/gauge/distribution/summary、加重平均、quantile・exemplar制約を追加 |
| ログとCustom Event | 全OTLP LogをLogとみなしていた | newrelic.event.typeによる分岐と属性優先順位、受信時刻の扱いを追加 |
| 取り込み・属性欠損 | クエリの空結果から未収集を判断し得た | 非同期検証、NrIntegrationError、属性切り詰め、filter/queue/cardinality等を区別 |
| Kubernetes・DBデータ | Metric/Span/Log以外やDBのLog型が不足 | OtlpInfrastructureEvent、DB query_sample/top_queryの取得先を追加 |
| 個別receiver | 全OTelが同じ名前規則と思う可能性 | IBM MQ/Linkerd等のunderscore名・ラベル・enumと変換差分を確認 |
| Collector・ATP・Lambda・GenAI | HTTP server Spanの条件を流用し得た | 内部テレメトリー、フィルタ済みprocess、関数識別、子のLLM/tool Spanを区別 |

反映先：[スキル本体](../skills/newrelic-query-cost/SKILL.md)、[OTel選択手順](../skills/newrelic-query-cost/references/opentelemetry.md)、[データモデル補足](../skills/newrelic-query-cost/references/opentelemetry-data-model.md)。収集設定の変更・計装の導入は実施していない。

## 本文通読で追加した条件

[個別連携の集計条件](../skills/newrelic-query-cost/references/opentelemetry-integrations.md)に、以下を追加した。共通スキル本体は参照先を追加し、対象と無関係なインストール説明や全メトリクス名は読み込ませない。

| 発見 | クエリへの反映 |
|---|---|
| DB query_sampleは繰り返し採取する実行中スナップショット | Log行数をSQL実行数にしない |
| top_queryは上位N件・区間統計 | 確認済み増分と加重平均を使い、DB全体と区別。LIMITで未収集を復元しない |
| query_planは別Logとなる場合がある | DB・instance・query/plan ID・期間で関連付け。実行時actual planと決めつけない |
| PostgreSQLのコメントは最初の呼び出し元で固定され得る | 集約callsをコメントのserviceへ一括帰属させない |
| PostgreSQLのMetricとquery LogでDB対象の設定が違う | databasesだけでLogの範囲まで限定済みとしない |
| receiver・platformで時間/メモリ単位と型が異なる | 名前でなく元の意味を確認。MySQL Log秒とMetric ns等を混ぜない |
| HAProxyのPrometheus rate変換は生涯最大値 | native receiverの現在rateと同等に扱わない |
| Kafkaのp99 gauge、RabbitMQの既存rate、NGINXの現在接続数 | 再percentile・二重rate・累積counterへの誤変換を避ける |
| lag_sum/partition、frontend/backend、proxy/app等の観測階層 | 同じ処理を重複加算しない |
| 複数replicaのscrape、pollより短いscrape | 重複収集を確認。replica数で機械的に割らない |
| Linkerdのservice名、NGINX/ES/Redisの識別属性 | entity統合・分裂と名前違いを確認。Metricだけでtrace収集済みとしない |
| RDS固定0/未対応、Oracleの無制限値、host非収集 | 欠測やsentinelを正常値・通常の分母と扱わない |
| Collectorの別account、LowDataMode・ATPのfilter、Lambda faas.name | 探索先・収集条件を確認して欠測理由を区別 |
| NRDOTの改名・distribution/JMX receiver廃止 | 導入例と利用版を照合。batchをポイント数の集約と扱わない |

## 公式資料自体の不一致・適用時の注意

- APM UI本文で新しいRPCメトリクス名に触れていても、生成元一覧には旧RPC名が掲載されている箇所がある。新しい名前が照会できることだけでAPM生成まで保証しない。
- エージェントのOTel API対応ページは、言語別の説明・対応表・末尾の制約に異なる記載がある（Rubyのspan links/events等）。対応版・信号・実スキーマを確認し、OTLPマッピングを強制しない。
- **前回指摘の訂正：IBM MQのoverviewとraw名の保持は矛盾しない。** 正規化はtargetName/clusterNameの例外で、同ページにもibmmq_*・qmgr・queueを保持する注意がある。全ラベルの改名指示と読まない。
- Linkerdの「Latency p99」の例がhistogramを返す箇所がある。見出しだけでpercentileの結果と判断せず、関数と返却値を検証する。
- GenAIの長い本文に対するSDK側の制限緩和だけでは、New Relic取り込み側の長さ制限を解除できない。未収集・切り詰めをクエリで復元できると説明しない。

追加の公式資料の注意：

- PostgreSQLのCLI/Helm説明は明示DBリストを求める一方、receiver設定表には空リスト時の動作がある。導入経路の制約とreceiver仕様を同一視しない。
- Redisの詳細表・troubleshootingにはnative cluster metricsの説明がある一方、導入ガイドはPrometheus経由が必要とする。対応版と利用receiverを確認し、どちらも普遍的な仕様として断定しない。
- NGINX表のSum分類・累積値の一般説明をconnections_currentへ一律適用しない。現在接続数という意味とmonotonicityを確認する。
- RabbitMQ Kubernetesの「batchでaggregate」という説明から、batchだけでカーディナリティやポイント数が減るとは判断しない。
- ATPのadvanced-featuresとhostの表でdynamic_smoothing_factor・anomaly関連のdefault値が異なる。利用版の実設定を確認する。
- 古いKubernetes設定例には廃止されたNRDOT distribution名や改名前のcomponent名が残る。リリースノートと利用版を優先して照合する。

## 検証と残る限界

`python3 scripts/validate_otel_semantics.py`で合成データの12テストを実行し成功。以前の6件に、Histogramの加重平均、生成APM durationの単位差、SpanEventとSpanの関連IDの反例を追加した。本文通読後に、DBスナップショットと実行数、収集側top N、proxy観測階層の重複加算の3反例も追加した。SQLiteによる意味の検証であり、NRQL構文受理・実アカウントのスキーマ・CCU効果や、スキルに従うエージェントの行動を検証したものではない。

パッケージ・内部リンク・数値台帳検査、skill-creatorの形式検査、git diff --checkも成功。New Relic MCPツールが公開されていないため実環境検証は未実施。コード・画像・外部参照先の詳細や新たな公式改訂は対象外であり、New Relic関連資料すべての抜け漏れゼロとは断定しない。

本文監査後の再検証では、独立エージェントによる静的タスク2件も実施し主要条件を満たした。入力・出力と限界は[再検証記録](otel-revalidation.md)。実NRQL・CCUは未検証。

## 全ページの棚卸し

「仕様本文」は前回の本文・マッピング表確認。「本文通読（コード除外）」は再開後に本文・表・注意書きを通読したもの。どちらも全サンプル実行・画像検証を意味しない。リリースノートindexは本文が空であることを確認した。

| ページ | 確認の深さ |
|---|---|
| [best-practices/opentelemetry-best-practices-logs.mdx](https://docs.newrelic.com/docs/opentelemetry/best-practices/opentelemetry-best-practices-logs/) | 仕様本文 |
| [best-practices/opentelemetry-best-practices-metrics.mdx](https://docs.newrelic.com/docs/opentelemetry/best-practices/opentelemetry-best-practices-metrics/) | 仕様本文 |
| [best-practices/opentelemetry-best-practices-resources.mdx](https://docs.newrelic.com/docs/opentelemetry/best-practices/opentelemetry-best-practices-resources/) | 仕様本文 |
| [best-practices/opentelemetry-best-practices-traces.mdx](https://docs.newrelic.com/docs/opentelemetry/best-practices/opentelemetry-best-practices-traces/) | 仕様本文 |
| [best-practices/opentelemetry-data-overview.mdx](https://docs.newrelic.com/docs/opentelemetry/best-practices/opentelemetry-data-overview/) | 仕様本文 |
| [best-practices/opentelemetry-manage-data-ingest-volume.mdx](https://docs.newrelic.com/docs/opentelemetry/best-practices/opentelemetry-manage-data-ingest-volume/) | 仕様本文 |
| [best-practices/opentelemetry-otlp-troubleshooting.mdx](https://docs.newrelic.com/docs/opentelemetry/best-practices/opentelemetry-otlp-troubleshooting/) | 仕様本文 |
| [best-practices/opentelemetry-otlp.mdx](https://docs.newrelic.com/docs/opentelemetry/best-practices/opentelemetry-otlp/) | 仕様本文 |
| [collector-observability/collector-observability-kpis.mdx](https://docs.newrelic.com/docs/opentelemetry/collector-observability/collector-observability-kpis/) | 本文通読（コード除外） |
| [collector-observability/collector-observability-setup.mdx](https://docs.newrelic.com/docs/opentelemetry/collector-observability/collector-observability-setup/) | 本文通読（コード除外） |
| [collector-observability/collector-observability.mdx](https://docs.newrelic.com/docs/opentelemetry/collector-observability/collector-observability/) | 本文通読（コード除外） |
| [db360/capabilities/db-apm.mdx](https://docs.newrelic.com/docs/opentelemetry/db360/capabilities/db-apm/) | 本文通読（コード除外） |
| [db360/capabilities/sql-query-receiver.mdx](https://docs.newrelic.com/docs/opentelemetry/db360/capabilities/sql-query-receiver/) | 本文通読（コード除外） |
| [db360/introduction.mdx](https://docs.newrelic.com/docs/opentelemetry/db360/introduction/) | 本文通読（コード除外） |
| [db360/mssql/ansible.mdx](https://docs.newrelic.com/docs/opentelemetry/db360/mssql/ansible/) | 本文通読（コード除外） |
| [db360/mssql/chef.mdx](https://docs.newrelic.com/docs/opentelemetry/db360/mssql/chef/) | 本文通読（コード除外） |
| [db360/mssql/cli.mdx](https://docs.newrelic.com/docs/opentelemetry/db360/mssql/cli/) | 本文通読（コード除外） |
| [db360/mssql/cncf.mdx](https://docs.newrelic.com/docs/opentelemetry/db360/mssql/cncf/) | 本文通読（コード除外） |
| [db360/mssql/config-reference.mdx](https://docs.newrelic.com/docs/opentelemetry/db360/mssql/config-reference/) | 本文通読（コード除外） |
| [db360/mssql/docker.mdx](https://docs.newrelic.com/docs/opentelemetry/db360/mssql/docker/) | 本文通読（コード除外） |
| [db360/mssql/helm.mdx](https://docs.newrelic.com/docs/opentelemetry/db360/mssql/helm/) | 本文通読（コード除外） |
| [db360/mssql/introduction.mdx](https://docs.newrelic.com/docs/opentelemetry/db360/mssql/introduction/) | 本文通読（コード除外） |
| [db360/mssql/linux-hosted.mdx](https://docs.newrelic.com/docs/opentelemetry/db360/mssql/linux-hosted/) | 本文通読（コード除外） |
| [db360/mssql/linux-rds.mdx](https://docs.newrelic.com/docs/opentelemetry/db360/mssql/linux-rds/) | 本文通読（コード除外） |
| [db360/mssql/metrics-reference.mdx](https://docs.newrelic.com/docs/opentelemetry/db360/mssql/metrics-reference/) | 本文通読（コード除外） |
| [db360/mssql/multi-receiver.mdx](https://docs.newrelic.com/docs/opentelemetry/db360/mssql/multi-receiver/) | 本文通読（コード除外） |
| [db360/mssql/troubleshooting.mdx](https://docs.newrelic.com/docs/opentelemetry/db360/mssql/troubleshooting/) | 本文通読（コード除外） |
| [db360/mssql/windows-hosted-domain.mdx](https://docs.newrelic.com/docs/opentelemetry/db360/mssql/windows-hosted-domain/) | 本文通読（コード除外） |
| [db360/mssql/windows-hosted-gmsa.mdx](https://docs.newrelic.com/docs/opentelemetry/db360/mssql/windows-hosted-gmsa/) | 本文通読（コード除外） |
| [db360/mssql/windows-hosted-sql.mdx](https://docs.newrelic.com/docs/opentelemetry/db360/mssql/windows-hosted-sql/) | 本文通読（コード除外） |
| [db360/mssql/windows-rds-domain.mdx](https://docs.newrelic.com/docs/opentelemetry/db360/mssql/windows-rds-domain/) | 本文通読（コード除外） |
| [db360/mssql/windows-rds-gmsa.mdx](https://docs.newrelic.com/docs/opentelemetry/db360/mssql/windows-rds-gmsa/) | 本文通読（コード除外） |
| [db360/mssql/windows-rds-sql.mdx](https://docs.newrelic.com/docs/opentelemetry/db360/mssql/windows-rds-sql/) | 本文通読（コード除外） |
| [db360/mysql/ansible.mdx](https://docs.newrelic.com/docs/opentelemetry/db360/mysql/ansible/) | 本文通読（コード除外） |
| [db360/mysql/chef.mdx](https://docs.newrelic.com/docs/opentelemetry/db360/mysql/chef/) | 本文通読（コード除外） |
| [db360/mysql/cli.mdx](https://docs.newrelic.com/docs/opentelemetry/db360/mysql/cli/) | 本文通読（コード除外） |
| [db360/mysql/compatibility.mdx](https://docs.newrelic.com/docs/opentelemetry/db360/mysql/compatibility/) | 本文通読（コード除外） |
| [db360/mysql/config-reference.mdx](https://docs.newrelic.com/docs/opentelemetry/db360/mysql/config-reference/) | 本文通読（コード除外） |
| [db360/mysql/docker.mdx](https://docs.newrelic.com/docs/opentelemetry/db360/mysql/docker/) | 本文通読（コード除外） |
| [db360/mysql/helm.mdx](https://docs.newrelic.com/docs/opentelemetry/db360/mysql/helm/) | 本文通読（コード除外） |
| [db360/mysql/hosted.mdx](https://docs.newrelic.com/docs/opentelemetry/db360/mysql/hosted/) | 本文通読（コード除外） |
| [db360/mysql/introduction.mdx](https://docs.newrelic.com/docs/opentelemetry/db360/mysql/introduction/) | 本文通読（コード除外） |
| [db360/mysql/metrics-reference.mdx](https://docs.newrelic.com/docs/opentelemetry/db360/mysql/metrics-reference/) | 本文通読（コード除外） |
| [db360/mysql/multi-receiver.mdx](https://docs.newrelic.com/docs/opentelemetry/db360/mysql/multi-receiver/) | 本文通読（コード除外） |
| [db360/mysql/optional.mdx](https://docs.newrelic.com/docs/opentelemetry/db360/mysql/optional/) | 本文通読（コード除外） |
| [db360/mysql/rds.mdx](https://docs.newrelic.com/docs/opentelemetry/db360/mysql/rds/) | 本文通読（コード除外） |
| [db360/mysql/troubleshooting.mdx](https://docs.newrelic.com/docs/opentelemetry/db360/mysql/troubleshooting/) | 本文通読（コード除外） |
| [db360/oracle/adb.mdx](https://docs.newrelic.com/docs/opentelemetry/db360/oracle/adb/) | 本文通読（コード除外） |
| [db360/oracle/ansible.mdx](https://docs.newrelic.com/docs/opentelemetry/db360/oracle/ansible/) | 本文通読（コード除外） |
| [db360/oracle/chef.mdx](https://docs.newrelic.com/docs/opentelemetry/db360/oracle/chef/) | 本文通読（コード除外） |
| [db360/oracle/cli.mdx](https://docs.newrelic.com/docs/opentelemetry/db360/oracle/cli/) | 本文通読（コード除外） |
| [db360/oracle/cncf.mdx](https://docs.newrelic.com/docs/opentelemetry/db360/oracle/cncf/) | 本文通読（コード除外） |
| [db360/oracle/config-reference.mdx](https://docs.newrelic.com/docs/opentelemetry/db360/oracle/config-reference/) | 本文通読（コード除外） |
| [db360/oracle/docker.mdx](https://docs.newrelic.com/docs/opentelemetry/db360/oracle/docker/) | 本文通読（コード除外） |
| [db360/oracle/helm.mdx](https://docs.newrelic.com/docs/opentelemetry/db360/oracle/helm/) | 本文通読（コード除外） |
| [db360/oracle/host-cdb.mdx](https://docs.newrelic.com/docs/opentelemetry/db360/oracle/host-cdb/) | 本文通読（コード除外） |
| [db360/oracle/host-pdb.mdx](https://docs.newrelic.com/docs/opentelemetry/db360/oracle/host-pdb/) | 本文通読（コード除外） |
| [db360/oracle/introduction.mdx](https://docs.newrelic.com/docs/opentelemetry/db360/oracle/introduction/) | 本文通読（コード除外） |
| [db360/oracle/metrics-reference.mdx](https://docs.newrelic.com/docs/opentelemetry/db360/oracle/metrics-reference/) | 本文通読（コード除外） |
| [db360/oracle/multi-receiver.mdx](https://docs.newrelic.com/docs/opentelemetry/db360/oracle/multi-receiver/) | 本文通読（コード除外） |
| [db360/oracle/rds.mdx](https://docs.newrelic.com/docs/opentelemetry/db360/oracle/rds/) | 本文通読（コード除外） |
| [db360/oracle/troubleshooting.mdx](https://docs.newrelic.com/docs/opentelemetry/db360/oracle/troubleshooting/) | 本文通読（コード除外） |
| [db360/postgresql/ansible.mdx](https://docs.newrelic.com/docs/opentelemetry/db360/postgresql/ansible/) | 本文通読（コード除外） |
| [db360/postgresql/chef.mdx](https://docs.newrelic.com/docs/opentelemetry/db360/postgresql/chef/) | 本文通読（コード除外） |
| [db360/postgresql/cli.mdx](https://docs.newrelic.com/docs/opentelemetry/db360/postgresql/cli/) | 本文通読（コード除外） |
| [db360/postgresql/compatibility.mdx](https://docs.newrelic.com/docs/opentelemetry/db360/postgresql/compatibility/) | 本文通読（コード除外） |
| [db360/postgresql/config-reference.mdx](https://docs.newrelic.com/docs/opentelemetry/db360/postgresql/config-reference/) | 本文通読（コード除外） |
| [db360/postgresql/docker.mdx](https://docs.newrelic.com/docs/opentelemetry/db360/postgresql/docker/) | 本文通読（コード除外） |
| [db360/postgresql/helm.mdx](https://docs.newrelic.com/docs/opentelemetry/db360/postgresql/helm/) | 本文通読（コード除外） |
| [db360/postgresql/hosted.mdx](https://docs.newrelic.com/docs/opentelemetry/db360/postgresql/hosted/) | 本文通読（コード除外） |
| [db360/postgresql/introduction.mdx](https://docs.newrelic.com/docs/opentelemetry/db360/postgresql/introduction/) | 本文通読（コード除外） |
| [db360/postgresql/metrics-reference.mdx](https://docs.newrelic.com/docs/opentelemetry/db360/postgresql/metrics-reference/) | 本文通読（コード除外） |
| [db360/postgresql/multi-receiver.mdx](https://docs.newrelic.com/docs/opentelemetry/db360/postgresql/multi-receiver/) | 本文通読（コード除外） |
| [db360/postgresql/optional.mdx](https://docs.newrelic.com/docs/opentelemetry/db360/postgresql/optional/) | 本文通読（コード除外） |
| [db360/postgresql/rds.mdx](https://docs.newrelic.com/docs/opentelemetry/db360/postgresql/rds/) | 本文通読（コード除外） |
| [db360/postgresql/troubleshooting.mdx](https://docs.newrelic.com/docs/opentelemetry/db360/postgresql/troubleshooting/) | 本文通読（コード除外） |
| [get-started/apm-monitoring/opentelemetry-apm-intro.mdx](https://docs.newrelic.com/docs/opentelemetry/get-started/apm-monitoring/opentelemetry-apm-intro/) | 本文通読（コード除外） |
| [get-started/apm-monitoring/opentelemetry-apm-ui.mdx](https://docs.newrelic.com/docs/opentelemetry/get-started/apm-monitoring/opentelemetry-apm-ui/) | 仕様本文 |
| [get-started/collector-infra-monitoring/opentelemetry-collector-infra-intro.mdx](https://docs.newrelic.com/docs/opentelemetry/get-started/collector-infra-monitoring/opentelemetry-collector-infra-intro/) | 本文通読（コード除外） |
| [get-started/collector-k8s-monitoring/opentelemetry-collector-k8s-intro.mdx](https://docs.newrelic.com/docs/opentelemetry/get-started/collector-k8s-monitoring/opentelemetry-collector-k8s-intro/) | 本文通読（コード除外） |
| [get-started/collector-processing/opentelemetry-collector-processing-intro.mdx](https://docs.newrelic.com/docs/opentelemetry/get-started/collector-processing/opentelemetry-collector-processing-intro/) | 本文通読（コード除外） |
| [get-started/openlit-llm-observability/openlit-llm-observability-intro.mdx](https://docs.newrelic.com/docs/opentelemetry/get-started/openlit-llm-observability/openlit-llm-observability-intro/) | 本文通読（コード除外） |
| [get-started/opentelemetry-get-started-intro.mdx](https://docs.newrelic.com/docs/opentelemetry/get-started/opentelemetry-get-started-intro/) | 本文通読（コード除外） |
| [get-started/traceloop-llm-observability/traceloop-llm-observability-intro.mdx](https://docs.newrelic.com/docs/opentelemetry/get-started/traceloop-llm-observability/traceloop-llm-observability-intro/) | 本文通読（コード除外） |
| [integrations/docker-monitoring/metrics-reference.mdx](https://docs.newrelic.com/docs/opentelemetry/integrations/docker-monitoring/metrics-reference/) | 本文通読（コード除外） |
| [integrations/docker-monitoring/overview.mdx](https://docs.newrelic.com/docs/opentelemetry/integrations/docker-monitoring/overview/) | 本文通読（コード除外） |
| [integrations/docker-monitoring/self-hosted.mdx](https://docs.newrelic.com/docs/opentelemetry/integrations/docker-monitoring/self-hosted/) | 本文通読（コード除外） |
| [integrations/docker-monitoring/troubleshooting.mdx](https://docs.newrelic.com/docs/opentelemetry/integrations/docker-monitoring/troubleshooting/) | 本文通読（コード除外） |
| [integrations/ecs-monitoring/ecs-ec2.mdx](https://docs.newrelic.com/docs/opentelemetry/integrations/ecs-monitoring/ecs-ec2/) | 本文通読（コード除外） |
| [integrations/ecs-monitoring/ecs-fargate.mdx](https://docs.newrelic.com/docs/opentelemetry/integrations/ecs-monitoring/ecs-fargate/) | 本文通読（コード除外） |
| [integrations/ecs-monitoring/find-and-query-your-data.mdx](https://docs.newrelic.com/docs/opentelemetry/integrations/ecs-monitoring/find-and-query-your-data/) | 本文通読（コード除外） |
| [integrations/ecs-monitoring/overview.mdx](https://docs.newrelic.com/docs/opentelemetry/integrations/ecs-monitoring/overview/) | 本文通読（コード除外） |
| [integrations/elasticsearch/distributed-tracing.mdx](https://docs.newrelic.com/docs/opentelemetry/integrations/elasticsearch/distributed-tracing/) | 本文通読（コード除外） |
| [integrations/elasticsearch/elasticsearch-otel-integration-install.mdx](https://docs.newrelic.com/docs/opentelemetry/integrations/elasticsearch/elasticsearch-otel-integration-install/) | 本文通読（コード除外） |
| [integrations/elasticsearch/elasticsearch-otel-integration-k8-install.mdx](https://docs.newrelic.com/docs/opentelemetry/integrations/elasticsearch/elasticsearch-otel-integration-k8-install/) | 本文通読（コード除外） |
| [integrations/elasticsearch/elasticsearch-otel-integration-overview.mdx](https://docs.newrelic.com/docs/opentelemetry/integrations/elasticsearch/elasticsearch-otel-integration-overview/) | 本文通読（コード除外） |
| [integrations/elasticsearch/find-and-query-data.mdx](https://docs.newrelic.com/docs/opentelemetry/integrations/elasticsearch/find-and-query-data/) | 本文通読（コード除外） |
| [integrations/elasticsearch/metrics-reference.mdx](https://docs.newrelic.com/docs/opentelemetry/integrations/elasticsearch/metrics-reference/) | 本文通読（コード除外） |
| [integrations/elasticsearch/troubleshooting.mdx](https://docs.newrelic.com/docs/opentelemetry/integrations/elasticsearch/troubleshooting/) | 本文通読（コード除外） |
| [integrations/haproxy/distributed-tracing.mdx](https://docs.newrelic.com/docs/opentelemetry/integrations/haproxy/distributed-tracing/) | 本文通読（コード除外） |
| [integrations/haproxy/find-and-query-data.mdx](https://docs.newrelic.com/docs/opentelemetry/integrations/haproxy/find-and-query-data/) | 本文通読（コード除外） |
| [integrations/haproxy/kubernetes.mdx](https://docs.newrelic.com/docs/opentelemetry/integrations/haproxy/kubernetes/) | 本文通読（コード除外） |
| [integrations/haproxy/metrics-reference.mdx](https://docs.newrelic.com/docs/opentelemetry/integrations/haproxy/metrics-reference/) | 本文通読（コード除外） |
| [integrations/haproxy/overview.mdx](https://docs.newrelic.com/docs/opentelemetry/integrations/haproxy/overview/) | 本文通読（コード除外） |
| [integrations/haproxy/self-hosted.mdx](https://docs.newrelic.com/docs/opentelemetry/integrations/haproxy/self-hosted/) | 本文通読（コード除外） |
| [integrations/ibm-mq/host.mdx](https://docs.newrelic.com/docs/opentelemetry/integrations/ibm-mq/host/) | 本文通読（コード除外） |
| [integrations/ibm-mq/kubernetes.mdx](https://docs.newrelic.com/docs/opentelemetry/integrations/ibm-mq/kubernetes/) | 本文通読（コード除外） |
| [integrations/ibm-mq/metrics.mdx](https://docs.newrelic.com/docs/opentelemetry/integrations/ibm-mq/metrics/) | 本文通読（コード除外） |
| [integrations/ibm-mq/overview.mdx](https://docs.newrelic.com/docs/opentelemetry/integrations/ibm-mq/overview/) | 本文通読（コード除外） |
| [integrations/ibm-mq/troubleshooting.mdx](https://docs.newrelic.com/docs/opentelemetry/integrations/ibm-mq/troubleshooting/) | 本文通読（コード除外） |
| [integrations/ibm-mq/view-data.mdx](https://docs.newrelic.com/docs/opentelemetry/integrations/ibm-mq/view-data/) | 本文通読（コード除外） |
| [integrations/kafka/find-and-query-data.mdx](https://docs.newrelic.com/docs/opentelemetry/integrations/kafka/find-and-query-data/) | 本文通読（コード除外） |
| [integrations/kafka/kubernetes-self-managed.mdx](https://docs.newrelic.com/docs/opentelemetry/integrations/kafka/kubernetes-self-managed/) | 本文通読（コード除外） |
| [integrations/kafka/kubernetes-strimzi.mdx](https://docs.newrelic.com/docs/opentelemetry/integrations/kafka/kubernetes-strimzi/) | 本文通読（コード除外） |
| [integrations/kafka/metrics-reference.mdx](https://docs.newrelic.com/docs/opentelemetry/integrations/kafka/metrics-reference/) | 本文通読（コード除外） |
| [integrations/kafka/overview.mdx](https://docs.newrelic.com/docs/opentelemetry/integrations/kafka/overview/) | 本文通読（コード除外） |
| [integrations/kafka/self-hosted.mdx](https://docs.newrelic.com/docs/opentelemetry/integrations/kafka/self-hosted/) | 本文通読（コード除外） |
| [integrations/linkerd/distributed-tracing.mdx](https://docs.newrelic.com/docs/opentelemetry/integrations/linkerd/distributed-tracing/) | 本文通読（コード除外） |
| [integrations/linkerd/find-data.mdx](https://docs.newrelic.com/docs/opentelemetry/integrations/linkerd/find-data/) | 本文通読（コード除外） |
| [integrations/linkerd/introduction.mdx](https://docs.newrelic.com/docs/opentelemetry/integrations/linkerd/introduction/) | 本文通読（コード除外） |
| [integrations/linkerd/metrics-reference.mdx](https://docs.newrelic.com/docs/opentelemetry/integrations/linkerd/metrics-reference/) | 本文通読（コード除外） |
| [integrations/linkerd/nrdot-helm.mdx](https://docs.newrelic.com/docs/opentelemetry/integrations/linkerd/nrdot-helm/) | 本文通読（コード除外） |
| [integrations/linkerd/nrdot-manifest.mdx](https://docs.newrelic.com/docs/opentelemetry/integrations/linkerd/nrdot-manifest/) | 本文通読（コード除外） |
| [integrations/linkerd/otel-helm.mdx](https://docs.newrelic.com/docs/opentelemetry/integrations/linkerd/otel-helm/) | 本文通読（コード除外） |
| [integrations/linkerd/otel-manifest.mdx](https://docs.newrelic.com/docs/opentelemetry/integrations/linkerd/otel-manifest/) | 本文通読（コード除外） |
| [integrations/linkerd/proxy-logs.mdx](https://docs.newrelic.com/docs/opentelemetry/integrations/linkerd/proxy-logs/) | 本文通読（コード除外） |
| [integrations/linkerd/troubleshooting.mdx](https://docs.newrelic.com/docs/opentelemetry/integrations/linkerd/troubleshooting/) | 本文通読（コード除外） |
| [integrations/nginx/find-and-query-your-data.mdx](https://docs.newrelic.com/docs/opentelemetry/integrations/nginx/find-and-query-your-data/) | 本文通読（コード除外） |
| [integrations/nginx/nginx-otel-distributed-tracing.mdx](https://docs.newrelic.com/docs/opentelemetry/integrations/nginx/nginx-otel-distributed-tracing/) | 本文通読（コード除外） |
| [integrations/nginx/nginx-otel-host.mdx](https://docs.newrelic.com/docs/opentelemetry/integrations/nginx/nginx-otel-host/) | 本文通読（コード除外） |
| [integrations/nginx/nginx-otel-kubernetes.mdx](https://docs.newrelic.com/docs/opentelemetry/integrations/nginx/nginx-otel-kubernetes/) | 本文通読（コード除外） |
| [integrations/nginx/nginx-otel-metrics-reference.mdx](https://docs.newrelic.com/docs/opentelemetry/integrations/nginx/nginx-otel-metrics-reference/) | 本文通読（コード除外） |
| [integrations/nginx/nginx-otel-overview.mdx](https://docs.newrelic.com/docs/opentelemetry/integrations/nginx/nginx-otel-overview/) | 本文通読（コード除外） |
| [integrations/nginx-plus/nginx-plus-otel.mdx](https://docs.newrelic.com/docs/opentelemetry/integrations/nginx-plus/nginx-plus-otel/) | 本文通読（コード除外） |
| [integrations/rabbitmq/find-and-query-data.mdx](https://docs.newrelic.com/docs/opentelemetry/integrations/rabbitmq/find-and-query-data/) | 本文通読（コード除外） |
| [integrations/rabbitmq/kubernetes.mdx](https://docs.newrelic.com/docs/opentelemetry/integrations/rabbitmq/kubernetes/) | 本文通読（コード除外） |
| [integrations/rabbitmq/metrics-reference.mdx](https://docs.newrelic.com/docs/opentelemetry/integrations/rabbitmq/metrics-reference/) | 本文通読（コード除外） |
| [integrations/rabbitmq/overview.mdx](https://docs.newrelic.com/docs/opentelemetry/integrations/rabbitmq/overview/) | 本文通読（コード除外） |
| [integrations/rabbitmq/self-hosted.mdx](https://docs.newrelic.com/docs/opentelemetry/integrations/rabbitmq/self-hosted/) | 本文通読（コード除外） |
| [integrations/redis/docker.mdx](https://docs.newrelic.com/docs/opentelemetry/integrations/redis/docker/) | 本文通読（コード除外） |
| [integrations/redis/host.mdx](https://docs.newrelic.com/docs/opentelemetry/integrations/redis/host/) | 本文通読（コード除外） |
| [integrations/redis/kubernetes.mdx](https://docs.newrelic.com/docs/opentelemetry/integrations/redis/kubernetes/) | 本文通読（コード除外） |
| [integrations/redis/metrics.mdx](https://docs.newrelic.com/docs/opentelemetry/integrations/redis/metrics/) | 本文通読（コード除外） |
| [integrations/redis/overview.mdx](https://docs.newrelic.com/docs/opentelemetry/integrations/redis/overview/) | 本文通読（コード除外） |
| [integrations/redis/troubleshooting.mdx](https://docs.newrelic.com/docs/opentelemetry/integrations/redis/troubleshooting/) | 本文通読（コード除外） |
| [integrations/redis/view-data.mdx](https://docs.newrelic.com/docs/opentelemetry/integrations/redis/view-data/) | 本文通読（コード除外） |
| [nrdot/atp/advanced-features.mdx](https://docs.newrelic.com/docs/opentelemetry/nrdot/atp/advanced-features/) | 本文通読（コード除外） |
| [nrdot/atp/host.mdx](https://docs.newrelic.com/docs/opentelemetry/nrdot/atp/host/) | 本文通読（コード除外） |
| [nrdot/atp/k8s.mdx](https://docs.newrelic.com/docs/opentelemetry/nrdot/atp/k8s/) | 本文通読（コード除外） |
| [nrdot/atp/overview.mdx](https://docs.newrelic.com/docs/opentelemetry/nrdot/atp/overview/) | 本文通読（コード除外） |
| [nrdot/atp/query.mdx](https://docs.newrelic.com/docs/opentelemetry/nrdot/atp/query/) | 本文通読（コード除外） |
| [nrdot/atp/troubleshooting.mdx](https://docs.newrelic.com/docs/opentelemetry/nrdot/atp/troubleshooting/) | 本文通読（コード除外） |
| [nrdot/nrdot-collector.mdx](https://docs.newrelic.com/docs/opentelemetry/nrdot/nrdot-collector/) | 本文通読（コード除外） |
| [nrdot/nrdot-intro.mdx](https://docs.newrelic.com/docs/opentelemetry/nrdot/nrdot-intro/) | 本文通読（コード除外） |
| [opentelemetry-integrations-list.mdx](https://docs.newrelic.com/docs/opentelemetry/opentelemetry-integrations-list/) | 本文通読（コード除外） |
| [opentelemetry-introduction.mdx](https://docs.newrelic.com/docs/opentelemetry/opentelemetry-introduction/) | 本文通読（コード除外） |

## 配下外の追加確認

| ページ | 確認の深さ |
|---|---|
| [apm/agents/manage-apm-agents/opentelemetry-api-support.mdx](https://docs.newrelic.com/docs/apm/agents/manage-apm-agents/opentelemetry-api-support/) | 本文通読（コード除外） |
| [ai-monitoring/opentelemetry-ai-monitoring.mdx](https://docs.newrelic.com/docs/ai-monitoring/opentelemetry-ai-monitoring/) | 本文通読（コード除外） |
| [apm/agents/java-agent/configuration/java-agent-configuration-opentelemetry-settings.mdx](https://docs.newrelic.com/docs/apm/agents/java-agent/configuration/java-agent-configuration-opentelemetry-settings/) | 本文通読（コード除外） |
| [distributed-tracing/ui-data/trace-details.mdx](https://docs.newrelic.com/docs/distributed-tracing/ui-data/trace-details/) | 本文通読（コード除外） |
| [data-apis/understand-data/metric-data/metric-data-type.mdx](https://docs.newrelic.com/docs/data-apis/understand-data/metric-data/metric-data-type/) | 本文通読（コード除外） |
| [kubernetes-pixie/k8s-otel/advance-config.mdx](https://docs.newrelic.com/docs/kubernetes-pixie/k8s-otel/advance-config/) | 本文通読（コード除外） |
| [kubernetes-pixie/k8s-otel/install.mdx](https://docs.newrelic.com/docs/kubernetes-pixie/k8s-otel/install/) | 本文通読（コード除外） |
| [kubernetes-pixie/k8s-otel/intro.mdx](https://docs.newrelic.com/docs/kubernetes-pixie/k8s-otel/intro/) | 本文通読（コード除外） |
| [kubernetes-pixie/k8s-otel/troubleshooting.mdx](https://docs.newrelic.com/docs/kubernetes-pixie/k8s-otel/troubleshooting/) | 本文通読（コード除外） |
| [serverless-function-monitoring/aws-lambda-monitoring/opentelemetry/lambda-opentelemetry-dotnet.mdx](https://docs.newrelic.com/docs/serverless-function-monitoring/aws-lambda-monitoring/opentelemetry/lambda-opentelemetry-dotnet/) | 本文通読（コード除外） |
| [serverless-function-monitoring/aws-lambda-monitoring/opentelemetry/lambda-opentelemetry-java.mdx](https://docs.newrelic.com/docs/serverless-function-monitoring/aws-lambda-monitoring/opentelemetry/lambda-opentelemetry-java/) | 本文通読（コード除外） |
| [serverless-function-monitoring/aws-lambda-monitoring/opentelemetry/lambda-opentelemetry-troubleshooting.mdx](https://docs.newrelic.com/docs/serverless-function-monitoring/aws-lambda-monitoring/opentelemetry/lambda-opentelemetry-troubleshooting/) | 本文通読（コード除外） |
| [serverless-function-monitoring/aws-lambda-monitoring/opentelemetry/otel-adot-log-ingestion-serverless.mdx](https://docs.newrelic.com/docs/serverless-function-monitoring/aws-lambda-monitoring/opentelemetry/otel-adot-log-ingestion-serverless/) | 本文通読（コード除外） |
| [serverless-function-monitoring/aws-lambda-monitoring/opentelemetry/otel-service-name-lambda.mdx](https://docs.newrelic.com/docs/serverless-function-monitoring/aws-lambda-monitoring/opentelemetry/otel-service-name-lambda/) | 本文通読（コード除外） |
| [release-notes/nrdot-release-notes/index.mdx](https://docs.newrelic.com/docs/release-notes/nrdot-release-notes/index/) | 本文通読（コード除外） |
| [release-notes/nrdot-release-notes/nrdot-0-8-5.mdx](https://docs.newrelic.com/docs/release-notes/nrdot-release-notes/nrdot-0-8-5/) | 本文通読（コード除外） |
| [release-notes/nrdot-release-notes/nrdot-1-0-0.mdx](https://docs.newrelic.com/docs/release-notes/nrdot-release-notes/nrdot-1-0-0/) | 本文通読（コード除外） |
| [release-notes/nrdot-release-notes/nrdot-1-0-1.mdx](https://docs.newrelic.com/docs/release-notes/nrdot-release-notes/nrdot-1-0-1/) | 本文通読（コード除外） |
| [release-notes/nrdot-release-notes/nrdot-1-0-2.mdx](https://docs.newrelic.com/docs/release-notes/nrdot-release-notes/nrdot-1-0-2/) | 本文通読（コード除外） |
| [release-notes/nrdot-release-notes/nrdot-1-0-3.mdx](https://docs.newrelic.com/docs/release-notes/nrdot-release-notes/nrdot-1-0-3/) | 本文通読（コード除外） |
| [release-notes/nrdot-release-notes/nrdot-1-1-0.mdx](https://docs.newrelic.com/docs/release-notes/nrdot-release-notes/nrdot-1-1-0/) | 本文通読（コード除外） |
| [release-notes/nrdot-release-notes/nrdot-1-10-0.mdx](https://docs.newrelic.com/docs/release-notes/nrdot-release-notes/nrdot-1-10-0/) | 本文通読（コード除外） |
| [release-notes/nrdot-release-notes/nrdot-1-11-0.mdx](https://docs.newrelic.com/docs/release-notes/nrdot-release-notes/nrdot-1-11-0/) | 本文通読（コード除外） |
| [release-notes/nrdot-release-notes/nrdot-1-11-1.mdx](https://docs.newrelic.com/docs/release-notes/nrdot-release-notes/nrdot-1-11-1/) | 本文通読（コード除外） |
| [release-notes/nrdot-release-notes/nrdot-1-12-0.mdx](https://docs.newrelic.com/docs/release-notes/nrdot-release-notes/nrdot-1-12-0/) | 本文通読（コード除外） |
| [release-notes/nrdot-release-notes/nrdot-1-13-0.mdx](https://docs.newrelic.com/docs/release-notes/nrdot-release-notes/nrdot-1-13-0/) | 本文通読（コード除外） |
| [release-notes/nrdot-release-notes/nrdot-1-14-0.mdx](https://docs.newrelic.com/docs/release-notes/nrdot-release-notes/nrdot-1-14-0/) | 本文通読（コード除外） |
| [release-notes/nrdot-release-notes/nrdot-1-15-0.mdx](https://docs.newrelic.com/docs/release-notes/nrdot-release-notes/nrdot-1-15-0/) | 本文通読（コード除外） |
| [release-notes/nrdot-release-notes/nrdot-1-15-1.mdx](https://docs.newrelic.com/docs/release-notes/nrdot-release-notes/nrdot-1-15-1/) | 本文通読（コード除外） |
| [release-notes/nrdot-release-notes/nrdot-1-16-0.mdx](https://docs.newrelic.com/docs/release-notes/nrdot-release-notes/nrdot-1-16-0/) | 本文通読（コード除外） |
| [release-notes/nrdot-release-notes/nrdot-1-17-0.mdx](https://docs.newrelic.com/docs/release-notes/nrdot-release-notes/nrdot-1-17-0/) | 本文通読（コード除外） |
| [release-notes/nrdot-release-notes/nrdot-1-18-0.mdx](https://docs.newrelic.com/docs/release-notes/nrdot-release-notes/nrdot-1-18-0/) | 本文通読（コード除外） |
| [release-notes/nrdot-release-notes/nrdot-1-19-0.mdx](https://docs.newrelic.com/docs/release-notes/nrdot-release-notes/nrdot-1-19-0/) | 本文通読（コード除外） |
| [release-notes/nrdot-release-notes/nrdot-1-2-0.mdx](https://docs.newrelic.com/docs/release-notes/nrdot-release-notes/nrdot-1-2-0/) | 本文通読（コード除外） |
| [release-notes/nrdot-release-notes/nrdot-1-20-0.mdx](https://docs.newrelic.com/docs/release-notes/nrdot-release-notes/nrdot-1-20-0/) | 本文通読（コード除外） |
| [release-notes/nrdot-release-notes/nrdot-1-21-0.mdx](https://docs.newrelic.com/docs/release-notes/nrdot-release-notes/nrdot-1-21-0/) | 本文通読（コード除外） |
| [release-notes/nrdot-release-notes/nrdot-1-21-1.mdx](https://docs.newrelic.com/docs/release-notes/nrdot-release-notes/nrdot-1-21-1/) | 本文通読（コード除外） |
| [release-notes/nrdot-release-notes/nrdot-1-3-0.mdx](https://docs.newrelic.com/docs/release-notes/nrdot-release-notes/nrdot-1-3-0/) | 本文通読（コード除外） |
| [release-notes/nrdot-release-notes/nrdot-1-4-0.mdx](https://docs.newrelic.com/docs/release-notes/nrdot-release-notes/nrdot-1-4-0/) | 本文通読（コード除外） |
| [release-notes/nrdot-release-notes/nrdot-1-5-0.mdx](https://docs.newrelic.com/docs/release-notes/nrdot-release-notes/nrdot-1-5-0/) | 本文通読（コード除外） |
| [release-notes/nrdot-release-notes/nrdot-1-6-0.mdx](https://docs.newrelic.com/docs/release-notes/nrdot-release-notes/nrdot-1-6-0/) | 本文通読（コード除外） |
| [release-notes/nrdot-release-notes/nrdot-1-7-0.mdx](https://docs.newrelic.com/docs/release-notes/nrdot-release-notes/nrdot-1-7-0/) | 本文通読（コード除外） |
| [release-notes/nrdot-release-notes/nrdot-1-8-0.mdx](https://docs.newrelic.com/docs/release-notes/nrdot-release-notes/nrdot-1-8-0/) | 本文通読（コード除外） |
| [release-notes/nrdot-release-notes/nrdot-1-9-0.mdx](https://docs.newrelic.com/docs/release-notes/nrdot-release-notes/nrdot-1-9-0/) | 本文通読（コード除外） |
| [release-notes/nrdot-release-notes/nrdot-2-0-0.mdx](https://docs.newrelic.com/docs/release-notes/nrdot-release-notes/nrdot-2-0-0/) | 本文通読（コード除外） |
| [release-notes/nrdot-release-notes/nrdot-2-1-0.mdx](https://docs.newrelic.com/docs/release-notes/nrdot-release-notes/nrdot-2-1-0/) | 本文通読（コード除外） |
| [release-notes/nrdot-release-notes/nrdot-2-2-0.mdx](https://docs.newrelic.com/docs/release-notes/nrdot-release-notes/nrdot-2-2-0/) | 本文通読（コード除外） |
| [release-notes/nrdot-release-notes/nrdot-2-3-0.mdx](https://docs.newrelic.com/docs/release-notes/nrdot-release-notes/nrdot-2-3-0/) | 本文通読（コード除外） |
| [release-notes/nrdot-release-notes/nrdot-2-4-0.mdx](https://docs.newrelic.com/docs/release-notes/nrdot-release-notes/nrdot-2-4-0/) | 本文通読（コード除外） |
| [release-notes/nrdot-release-notes/nrdot-2-4-1.mdx](https://docs.newrelic.com/docs/release-notes/nrdot-release-notes/nrdot-2-4-1/) | 本文通読（コード除外） |
| [release-notes/nrdot-release-notes/nrdot-2-4-2.mdx](https://docs.newrelic.com/docs/release-notes/nrdot-release-notes/nrdot-2-4-2/) | 本文通読（コード除外） |
| [release-notes/nrdot-release-notes/nrdot-2-4-3.mdx](https://docs.newrelic.com/docs/release-notes/nrdot-release-notes/nrdot-2-4-3/) | 本文通読（コード除外） |
| [release-notes/nrdot-release-notes/nrdot-2-5-0.mdx](https://docs.newrelic.com/docs/release-notes/nrdot-release-notes/nrdot-2-5-0/) | 本文通読（コード除外） |
| [release-notes/nrdot-release-notes/nrdot-2-6-0.mdx](https://docs.newrelic.com/docs/release-notes/nrdot-release-notes/nrdot-2-6-0/) | 本文通読（コード除外） |
| [release-notes/nrdot-release-notes/nrdot-2-7-0.mdx](https://docs.newrelic.com/docs/release-notes/nrdot-release-notes/nrdot-2-7-0/) | 本文通読（コード除外） |
| [release-notes/nrdot-release-notes/nrdot-2-7-1.mdx](https://docs.newrelic.com/docs/release-notes/nrdot-release-notes/nrdot-2-7-1/) | 本文通読（コード除外） |
| [release-notes/nrdot-release-notes/nrdot-2-7-2.mdx](https://docs.newrelic.com/docs/release-notes/nrdot-release-notes/nrdot-2-7-2/) | 本文通読（コード除外） |
| [release-notes/nrdot-release-notes/nrdot-2-7-3.mdx](https://docs.newrelic.com/docs/release-notes/nrdot-release-notes/nrdot-2-7-3/) | 本文通読（コード除外） |
| [release-notes/nrdot-release-notes/nrdot-host-1-12-0.mdx](https://docs.newrelic.com/docs/release-notes/nrdot-release-notes/nrdot-host-1-12-0/) | 本文通読（コード除外） |
| [release-notes/nrdot-release-notes/nrdot-host-1-14-0.mdx](https://docs.newrelic.com/docs/release-notes/nrdot-release-notes/nrdot-host-1-14-0/) | 本文通読（コード除外） |
| [release-notes/nrdot-release-notes/nrdot-host-1-15-1.mdx](https://docs.newrelic.com/docs/release-notes/nrdot-release-notes/nrdot-host-1-15-1/) | 本文通読（コード除外） |
| [release-notes/nrdot-release-notes/nrdot-host-1-17-0.mdx](https://docs.newrelic.com/docs/release-notes/nrdot-release-notes/nrdot-host-1-17-0/) | 本文通読（コード除外） |
| [release-notes/nrdot-release-notes/nrdot-host-1-19-0.mdx](https://docs.newrelic.com/docs/release-notes/nrdot-release-notes/nrdot-host-1-19-0/) | 本文通読（コード除外） |
| [release-notes/nrdot-release-notes/nrdot-host-1-20-0.mdx](https://docs.newrelic.com/docs/release-notes/nrdot-release-notes/nrdot-host-1-20-0/) | 本文通読（コード除外） |
| [release-notes/nrdot-release-notes/nrdot-host-1-21-0.mdx](https://docs.newrelic.com/docs/release-notes/nrdot-release-notes/nrdot-host-1-21-0/) | 本文通読（コード除外） |
| [release-notes/nrdot-release-notes/nrdot-host-2-0-0.mdx](https://docs.newrelic.com/docs/release-notes/nrdot-release-notes/nrdot-host-2-0-0/) | 本文通読（コード除外） |
| [release-notes/nrdot-release-notes/nrdot-host-2-4-1.mdx](https://docs.newrelic.com/docs/release-notes/nrdot-release-notes/nrdot-host-2-4-1/) | 本文通読（コード除外） |
| [release-notes/nrdot-release-notes/nrdot-host-2-4-2.mdx](https://docs.newrelic.com/docs/release-notes/nrdot-release-notes/nrdot-host-2-4-2/) | 本文通読（コード除外） |
| [release-notes/nrdot-release-notes/nrdot-host-2-4-3.mdx](https://docs.newrelic.com/docs/release-notes/nrdot-release-notes/nrdot-host-2-4-3/) | 本文通読（コード除外） |
| [release-notes/nrdot-release-notes/nrdot-host-2-5-0.mdx](https://docs.newrelic.com/docs/release-notes/nrdot-release-notes/nrdot-host-2-5-0/) | 本文通読（コード除外） |
| [release-notes/nrdot-release-notes/nrdot-host-2-6-0.mdx](https://docs.newrelic.com/docs/release-notes/nrdot-release-notes/nrdot-host-2-6-0/) | 本文通読（コード除外） |
| [release-notes/nrdot-release-notes/nrdot-host-2-7-1.mdx](https://docs.newrelic.com/docs/release-notes/nrdot-release-notes/nrdot-host-2-7-1/) | 本文通読（コード除外） |
| [release-notes/nrdot-release-notes/nrdot-host-2-7-3.mdx](https://docs.newrelic.com/docs/release-notes/nrdot-release-notes/nrdot-host-2-7-3/) | 本文通読（コード除外） |

公式ナビゲーションの参照先でスナップショットに存在しないもの：なし。
