# 検証範囲

## オフライン検査

Python 3.10以上で実行する。依存関係の導入は[README](../README.md#検証)を参照。

```sh
.venv/bin/python scripts/validate.py
.venv/bin/python scripts/validate_otel_semantics.py
```

- `validate.py`：スキルのメタデータ・内部リンク・数値台帳の単位と集計を確認する。
- `validate_otel_semantics.py`：SQLiteの合成データ12テストで、集計統合、分母、加重平均、単位、関連ID、サンプリング、欠測、DBスナップショット、top N、重複計上の反例を確認する。

通信・MCP接続は行わない。NRQLエンジンの構文受理や実データの結果を検証するものではない。

## 確認済みの範囲

2026-11-02時点で、オフライン検査は成功。Codex環境の独立エージェントによる静的タスク2件では、次の判断を確認した。

- OTel HTTP：個別transactionはserver Span、全体傾向は適合するMetricを選び、単位・対象entity・sampling・エラーの分母を維持する。
- PostgreSQL DB360：query_sampleの行数を実行数にせず、top_queryは加重平均を使う。初回callerのSQLコメントだけで全callsを特定サービスへ帰属させない。

OTelの仕様は公式資料と照合した。実環境のNRQL・CCU、Claude Code／Copilot上の動作は未検証。

公開候補を別ディレクトリへ展開し、新しい仮想環境で依存導入・12テスト・形式と内部リンクの検査が成功した。READMEのコピー手順でもスキル全ファイルの一致を確認した。ファイルのコピー検査は各製品による読込・実行の検証とは別。

整理後のスキルでも独立エージェントの静的タスク4件を確認し、OTLPのSpan/Metric選択、エージェントのOTel API対応、FACETランキングの維持、MCP未接続時の静的評価について主要な条件を満たした。

## 過去のCCU観測

同じサービスの固定1時間について、BrowserとAPMの6クエリを2本へ統合した単発比較。匿名化した台帳は[evidence/site-performance.json](evidence/site-performance.json)。

| 指標 | 個別6本の合計 | 統合2本の合計 |
|---|---:|---:|
| 検査イベント数 | 297 | 99 |
| 記録Core CCU | 0.000279738984 | 0.000093246328 |

結果とサンプル数は過去の照合で一致したが、各クエリ1回の少量データの観測であり、一般的な削減率やOTelの効果を示すものではない。台帳だけでは結果同等性を再計算できない。比較値には探索・計測用クエリを含まない。

この過去の観測は直接MCP接続によるもので、現在のスキルが使うハーネス経由の経路ではない。現在の経路での再実行は行っていない。
