# 検証範囲

- `scripts/validate.py`：メタデータ、内部リンク、匿名化した数値台帳を検査。
- `scripts/validate_semantics.py`：合成データ4テストで、集計統合、エラーの分母、FACETの上位選出、欠測を検査。
- `scripts/validate_agent_semantics.py`：APM固有の合成データ3テスト。TransactionとMetricの母集団、TransactionErrorの重複、Metric観測数を検査。

依存導入と実行コマンドは[README](../README.md#検証)。SQLiteでの意味の検査であり、NRQLエンジンの構文受理・実データの結果・CCUを検証するものではない。Claude Code／Copilot上の動作も未検証。

[匿名化した旧台帳](evidence/site-performance.json)は、分割前のAPM/Browserクエリ6本を2本へ統合した各1回の過去観測。少量データで、一般的な削減率や今回の実測を示さない。台帳だけでは結果同等性を再計算できず、現在のハーネス経由での再実行も行っていない。
