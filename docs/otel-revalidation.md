# OTel対応の再検証（2026-11-02）

対象：2026-11-02の本文監査後の`skills/newrelic-query-cost/`の作業ツリー。読み取りによる検証。NRQL、Collector、計装やアカウントの設定変更は実行していない。

## 結果

| 検証 | 結果と範囲 |
|---|---|
| `python3 scripts/validate_otel_semantics.py` | 12件成功。SQLiteの合成データによる集計の同等性・反例 |
| `scripts/validate.py`（既存検証venv） | パッケージ、ローカルリンク、既存計測台帳の単位・件数・加算が成功。既存台帳は今回のOTel CCU実測ではない |
| skill-creatorの`quick_validate.py` | 形式検査成功 |
| `git diff --check` | 成功 |
| インストール先 | `~/.codex/skills/newrelic-query-cost`はリポジトリ内の対象ディレクトリへのsymlink。SKILL.mdの内容差分なし |
| 独立エージェントによる静的タスク実行 | 下記2ケースで主要な判断条件を満たした。NRQLは実行していない |
| New Relic実接続 | 公開ツール一覧にNew Relicの実行ツールなし。実スキーマ・構文受理・CCU効果は未検証 |

独立評価はCodexのskill-creatorにあるIndependent Forward-Testingの手順に従い実施した。評価者にはスキルのパス、現実的な依頼と既知スキーマ・収集条件を渡した。期待解答・修正案・過去の監査結論は渡さず、監査記録とテストスクリプトの参照も除外した。出力を主担当が評価した。以下の2件の成功は、すべての入力での動作やNRQLエンジンの正しさを保証しない。

以下のサービス名・entity GUID・スキーマは静的試験用の仮定であり、実アカウントから取得した識別情報ではない。

## ケース1：OTLPのtransaction取得と全体集計

依頼：checkoutの直近30分の遅いリクエスト例、全体件数・平均・エラー率を低コストに取得したい。

提示条件：純粋なOTLP、10%のhead sampling、server/client/internal Spanの混在、upstream parentを持つserver、同名の別環境・旧NRエージェント。対象entity.guidとSpanの`duration.ms`、秒単位のHTTP distribution、Metricの`error.type`は既知。元クエリはTransaction/appName、全体案はサービス名だけの全Span集計。

観測した出力：

```sql
FROM Span
SELECT timestamp, id, trace.id, parent.id, duration.ms, otel.status_code
WHERE entity.guid = 'otel-checkout-prod'
  AND span.kind = 'server'
  AND duration.ms > 1000
SINCE 30 minutes ago
LIMIT 50
```

- 個別取得にSpanを選択し、1秒超を1000ms超へ合わせた。parent.idの欠損条件を追加せず、対象entityへ限定した。
- 50件は観測抜粋であり、全件や最遅50件を保証しないと説明した。
- 全体にはMetricの`count(http.server.request.duration)`と`average(...)`を選択。error.typeによるfilterの分子と正常を含む分母を維持した。
- Metricの収集範囲・欠落・重複とerror.typeのエラー定義が適合する場合だけ全体値として採用し、未確認なら件数・平均のみを候補にした。
- 観測Span件数を10倍せず、ERROR statusとMetricのerror.typeの同等性を断定しなかった。
- 未実行・CCU未測定と明示した。

主要条件は合格。依頼は「遅い例」であり、ランキングを保証しないLIMITを最遅一覧と誤表示しなかった。

## ケース2：DB360 PostgreSQLの実行数・加重平均・サービス帰属

依頼：checkoutのSQL実行数と平均時間について、query_sampleのcountとtop_queryの行ごとの平均を1本へ統合できるか。

提示条件：query_sampleはactive queryのscrape、execution_idなし。top_queryは各interval上位20digest。実在が確認済みというfixture属性`pg.calls_delta`・`pg.duration_ms_delta`は区間実行数と総時間。SQL本文コメントは最初のcallerで固定され、複数サービスが同じdigestを実行する。これらの`pg.*`名は試験用の既知スキーマであり、New Relicの標準属性名の主張ではない。

観測した出力：

```sql
FROM Log
SELECT sum(pg.calls_delta) AS collectedTopQueryExecutions,
       sum(pg.duration_ms_delta) / sum(pg.calls_delta)
         AS collectedTopQueryAverageMs
WHERE entity.guid = 'pg-prod'
  AND event.name = 'db.server.top_query'
SINCE 30 minutes ago
```

- query_sampleのcountを実行数とする案を不採用にした。繰り返し採取と、採取の間に完了する処理の欠落を説明した。
- 行ごとの平均の単純平均を不採用とし、総時間/総callsへ変更した。
- SQLコメントのservice GUIDから全callsをcheckoutへ帰属させることを拒否した。
- 代替クエリは「全サービスを含む収集上位20digest/intervalの統計」と明記。checkout限定・DB全体の答えとして代用しなかった。
- 必要なDB範囲・欠測・区間対応・重複・分母0の確認と、サービス帰属が確認できる別データが必要なことを説明した。
- 未実行・CCU未測定と明示した。

主要条件は合格。2ケースで判断上の追加修正を要する失敗は観測しなかった。

## 公式根拠の再照合

公開サイトと前回の固定スナップショットの区別を保って照合した。公開サイトに全詳細が表示されない場合、固定スナップショットに存在することだけを根拠とし、公開サイトの最新版にも一致すると断定しない。

- [OTLP traces](https://docs.newrelic.com/docs/opentelemetry/best-practices/opentelemetry-best-practices-traces/)：Span、duration.ms、id、trace.id、SpanEventの関連先を公開本文で確認。
- [OTel APM UI](https://docs.newrelic.com/docs/opentelemetry/get-started/apm-monitoring/opentelemetry-apm-ui/)：全体傾向でMetric優先、個別transaction traceでSpanを用いることを公開本文で確認。
- [HAProxy metric reference](https://docs.newrelic.com/docs/opentelemetry/integrations/haproxy/metrics-reference/)：native receiverのrateとPrometheus変換によるrate_maxの違いを公開資料と固定ソースで再照合。
- [MySQL metric reference](https://docs.newrelic.com/docs/opentelemetry/db360/mysql/metrics-reference/)：query_sampleのスナップショット、top_queryの区間差分、別query_plan、Logの時間単位を固定ソースで再照合。
- [PostgreSQL metric reference](https://docs.newrelic.com/docs/opentelemetry/db360/postgresql/metrics-reference/)と[multi-receiver](https://docs.newrelic.com/docs/opentelemetry/db360/postgresql/multi-receiver/)：初回callerのコメント、queryid/userid、databasesとquery Log範囲の違いを固定ソースで再照合。
- [OpenTelemetry batch processor](https://github.com/open-telemetry/opentelemetry-collector/blob/main/processor/batchprocessor/README.md)：batchの目的は送信のまとまり・圧縮・接続削減であり、観測の集約による件数削減とは区別することを確認。

固定ソースのcommitは[前回の監査記録](otel-documentation-audit.md)を参照。

## 未検証の範囲

実NRQL構文受理、実アカウントの属性と値、実データでのbefore/after同等性、CCU・料金、Collector構成や全コードの実行は未検証。独立評価も提示したスキーマを前提にした静的タスク実行であり、接続先の発見・ツール操作まで含むend-to-end試験ではない。
