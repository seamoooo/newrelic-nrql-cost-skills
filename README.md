# New Relic NRQL Cost Skills

収集経路ごとにリポジトリとスキルを分割しました。新しく導入する場合は、対象のデータに合うものを選んでください。

| 収集経路 | リポジトリ | スキル名 |
|---|---|---|
| New Relic APMエージェント、同エージェントのOTel API対応 | [Agent版](https://github.com/seamoooo/newrelic-agent-nrql-cost-skills) | `newrelic-agent-query-cost` |
| OpenTelemetry SDK・Collector・NRDOTからのOTLP送信 | [OTel版](https://github.com/seamoooo/newrelic-otel-nrql-cost-skills) | `newrelic-otel-query-cost` |

共通のNRQL最適化・計測・NerdGraph・運用知識は、両リポジトリに同じ内容を保持しています。各スキルは単独で利用でき、混在環境では収集元ごとに選べます。導入手順は各リポジトリのREADMEを参照してください。

このリポジトリは移行用に旧統合版を保持しています。新しいスキルへの移行後は、同じ依頼に旧`newrelic-query-cost`が重複して適用されないよう読込を解除してください。

コミュニティ製で、New Relicの公式製品ではありません。

## 検証

旧統合版の検証はPython 3.10以上で実行できます。新しい版の検証は各リポジトリの手順を使ってください。

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements-dev.txt
.venv/bin/python scripts/validate.py
.venv/bin/python scripts/validate_otel_semantics.py
```

実環境のNRQL・CCU、Claude Code／Copilot上の動作は未検証です。

## ライセンス

[MIT License](LICENSE)
