# APMエージェントのデータ選択

[APMイベント](https://docs.newrelic.com/docs/data-apis/understand-data/event-data/events-reported-apm/)と[transactionの定義](https://docs.newrelic.com/docs/apm/transactions/intro-transactions/transactions-new-relic-apm/)に従い、実スキーマと収集設定を確認する。例は未実行の構文案。

| 目的 | データと注意 |
|---|---|
| 個別のリクエスト・カスタム属性 | Transaction。durationは秒、対象appNameやentityとtransactionTypeを照合。件数はイベントで観測した件数 |
| エラーの詳細 | TransactionError。例外数・エラーイベント数とエラーtransaction数を同一視しない |
| 分散トレースの経路 | Span。保存後のtrace ID・親子IDで限定し、サンプリングと取得上限を確認 |
| 定期的な全体指標 | 適合する既存APM Metric。Transaction集計との同等性を自動的に仮定しない |

## 個別transaction

```sql
FROM Transaction
SELECT timestamp, name, duration, error
WHERE appName = 'checkout' AND duration > 1
SINCE 30 minutes ago
LIMIT 50
```

1秒超の観測例。全件や最遅50件ではない。同名アプリや環境が混ざる場合は実在するentity・環境属性で限定する。非Web処理へWeb条件を流用しない。

## Transaction上の集計をまとめる

```sql
FROM Transaction
SELECT count(*) AS observedTransactions,
       average(duration) AS latencySeconds,
       percentage(count(*), WHERE error IS true) AS observedErrorPercent
WHERE appName = 'checkout'
SINCE 1 hour ago
```

これはTransactionイベント上の集計。イベントの制限・サンプリングでMetricと件数や平均が異なり得る。TransactionError件数を分子へ置き換えると、エラー定義・収集条件・重複により同等とは限らない。

## 定期集計に既存APMメトリクスを使う

アプリ全体の応答時間・処理量・エラー傾向を定期的に確認するなら、対象アプリに既存のAPMメトリクスがあるか調べる。例のアプリ名と期間は実際の対象に合わせる。

```sql
FROM Metric
SELECT count(apm.service.transaction.duration) AS requests,
       rate(count(apm.service.transaction.duration), 1 minute) AS rpm,
       average(apm.service.transaction.duration) AS latencySeconds,
       100 * count(apm.service.error.count)
         / count(apm.service.transaction.duration) AS errorPercent
WHERE appName = '<対象アプリ名>'
  AND transactionType = 'Web'
SINCE 1 hour ago
TIMESERIES 5 minutes
```

`requests`は期間内の処理件数、`rpm`は1分あたりの処理件数、`latencySeconds`は秒単位、`errorPercent`は百分率。処理件数と毎分の処理件数を取り違えない。分母が0の区間や値がない区間を、正常な0%として補完しない。

同じ対象と期間の複数指標は、FACETの選出や各指標の条件が変わらないなら1本にまとめる。時系列を比較するときは、各バケットの開始・終了時刻と値を照合する。

Transactionイベントを使った集計とメトリクス集計は、同じアプリ名でも件数や平均値が一致するとは限らない。収集・サンプリング・エラーの扱い・境界時刻・利用可能な属性を照合し、元の目的に合うものを選ぶ。個別リクエストやカスタム属性が必要な調査はイベントを使う。

`apm.service.transaction.overview`は処理時間の内訳を見るためのものなので、アプリの応答時間を知る目的で使っていないか確認する。内訳が必要な調査をdurationメトリクスだけへ置き換えない。
