# 公式ドキュメントと判断基準

New Relicの仕様はNew Relicの公開公式ドキュメントを参照する。OpenTelemetry自体の処理仕様は同プロジェクトの公式資料も参照する。以下の運用上の提案は、公開仕様を踏まえたクエリ削減のノウハウであり、内部の実行計画・課金計算式を説明するものではない。公式仕様は利用時にも確認する。

| 参照先 | 確認する仕様と実務での使い方 |
|---|---|
| [時間範囲](https://docs.newrelic.com/docs/nrql/using-nrql/query-time-range/) | 通常NRQLの既定は直近1時間。時間ピッカーによる上書きを含めて実効範囲を把握し、目的に必要な期間へ絞る。 |
| [NRQL仕様](https://docs.newrelic.com/docs/nrql/nrql-syntax-clauses-functions/) | WHERE、filter()、FACET、TIMESERIES等の意味を確認する。改善で母集団や分母を変えない。LIMITは結果数を制御するために使い、CCUの上限とは扱わない。 |
| [NRQLアラート](https://docs.newrelic.com/docs/alerts/create-alert/create-alert-condition/create-nrql-alert-conditions/) | ストリーミングアラートへSINCE/UNTIL/TIMESERIES/LIMITを追加しない。必要な検出時間と集約設定を照合する。 |
| [クエリのレート制限](https://docs.newrelic.com/docs/nrql/using-nrql/rate-limits-nrql-queries/) | 複雑なクエリの同時実行と不要な反復を避ける。回数制限やタイムアウトを料金算定式とは混同しない。 |
| [利用量のクエリ](https://docs.newrelic.com/docs/accounts/accounts-billing/new-relic-one-pricing-billing/usage-queries-alerts/) | Core/Advancedの利用量を区分して追跡する。利用量データは概算であり、請求確定値と同一視しない。 |
| [NrComputeUsageの公開辞書](https://docs.newrelic.com/attribute-dictionary/?event=NrComputeUsage) | 公開されているイベント・属性の定義を確認する。実アカウントのスキーマと照合し、観測できない値を推測しない。 |
| [イベントからメトリクスへの変換](https://docs.newrelic.com/docs/data-apis/convert-to-metrics/analyze-monitor-data-trends-metrics/) | 定期的な同種のイベント集計に対する設計候補。集計定義とディメンションが目的に合うかを確認し、作成が必要なものは改善案として提示する。 |

## 実利用で補う確認先

- [NRQL仕様](https://docs.newrelic.com/docs/nrql/nrql-syntax-clauses-functions/)：LIMIT MAXの上限、FACETの既定件数・選出基準、TIMESERIESのバケット上限。全件性や集計統合の同等性を判断する。
- [時間範囲](https://docs.newrelic.com/docs/nrql/using-nrql/query-time-range/)：Metric・TIMESERIESの時間範囲の丸め。比較時は実効期間も確認する。
- [NerdGraphでNRQLを実行](https://docs.newrelic.com/docs/apis/nerdgraph/examples/nerdgraph-nrql-tutorial/)：複数アカウント・非同期実行。MCPが公開する機能を確認し、非同期IDがある場合は状態確認を再送より優先する。
- [Consumption Management](https://docs.newrelic.com/docs/accounts/accounts-billing/new-relic-one-pricing-billing/consumption-management/)：適用プランと利用量の内訳。アカウント全体の値を単一クエリへ帰属させない。

- [NrdbQueryの公開辞書](https://docs.newrelic.com/attribute-dictionary/?event=NrdbQuery)：クエリ文字列・実行時間・検査イベント数。CCUの直接測定と区別し、実アカウントのスキーマと照合する。

## 削減案の評価

- 必要なサービス・アカウント・期間を特定して対象を絞る。
- 同じ母集団への複数集計をまとめ、取得済み結果や安定したメタデータを再利用する。
- 必要な属性と結果件数を指定し、転送量とトークン量を抑える。
- FACETと時系列は必要な分析粒度に合わせる。
- 大量イベントの反復集計には、同じ答えが得られる既存MetricやE2Mを検討する。
- 効果は同条件の実測で確認する。スキャン・CCU・料金の固定倍率や内部インデックスの挙動を根拠なく断定しない。

## OpenTelemetryの確認先

OTLP取り込みの仕様と適用条件は[opentelemetry.md](opentelemetry.md)で使う。2026-11-02確認。

- [OTel APM UI](https://docs.newrelic.com/docs/opentelemetry/get-started/apm-monitoring/opentelemetry-apm-ui/)：APMメトリクスの生成元、メトリクスとSpanの優先順位、エラーの定義。
- [OTel metrics](https://docs.newrelic.com/docs/opentelemetry/best-practices/opentelemetry-best-practices-metrics/)：Metricへの変換、単位、Histogramとtemporality。
- [OTel traces](https://docs.newrelic.com/docs/opentelemetry/best-practices/opentelemetry-best-practices-traces/)：Spanの属性、所要時間とIDのマッピング。
- [OTel logs](https://docs.newrelic.com/docs/opentelemetry/best-practices/opentelemetry-best-practices-logs/)：Logのseverity属性、サービス・トレースとの関連。

追加の型・関連ID・取り込み制約と連携別の確認先は[opentelemetry-data-model.md](opentelemetry-data-model.md)。APM生成メトリクスの単位はAPM UIの **APM Service Metrics** の表を参照する。OTel APIとネイティブOTLP送信を区別する際は[APMエージェントのOTel API対応](https://docs.newrelic.com/docs/apm/agents/manage-apm-agents/opentelemetry-api-support/)を確認する。公式資料内でも新旧説明・例・対応表が一致しない場合があるため、矛盾する例をそのまま実行せず、信号別仕様と実データで確認する。

DB360・receiver・Prometheus経由の意味の違いと個別公式資料は[opentelemetry-integrations.md](opentelemetry-integrations.md)。上位N件・スナップショット・計算済みrate/percentileは、通常の実行イベントや分布へ置換しない。
