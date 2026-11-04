# New Relic APM Agent NRQL Cost Optimization

New Relic APMエージェント向けに、必要な結果を保ちながらNRQLの対象・集計・実行回数を見直すAgent Skill。コミュニティ製で、New Relicの公式製品ではない。

スキル名：`newrelic-query-cost`。データ選択は[判断手順](skills/newrelic-query-cost/references/agent.md)を参照。

## 対象

New Relic APMエージェントが収集するTransaction・TransactionError・Span・Metric・Log。

共通のNRQL最適化・計測・NerdGraph・運用知識も一式を保持し、他リポジトリやサブモジュールへの実行時依存はありません。

## 導入

macOS／Linuxの例。既存の同名スキルを確認してからコピーする。

```sh
git clone https://github.com/seamoooo/newrelic-nrql-cost-skills.git
cd newrelic-nrql-cost-skills
mkdir -p ~/.agents/skills
cp -R -i skills/newrelic-query-cost ~/.agents/skills/
```

Codexで`$newrelic-query-cost`を指定する。Claude Codeでは`~/.claude/skills/`へコピーして`/newrelic-query-cost`、Copilot CLIでは`~/.copilot/skills/`へコピーし`/skills reload`後に`/newrelic-query-cost`を指定する。

## 依頼例

```text
newrelic-query-costで次のNRQLをレビューして。実行は不要です。
目的・対象サービス・必要期間を維持し、改善案と検証条件を示してください。
```

レビューはMCP接続不要。実行にはハーネスに公開されたNew Relic MCPツールと対象アカウントの権限が必要。資格情報を探索して直接接続する方法は使わない。

## 検証

Python 3.10以上。

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements-dev.txt
.venv/bin/python scripts/validate.py
.venv/bin/python scripts/validate_semantics.py
.venv/bin/python scripts/validate_agent_semantics.py
```

検証はパッケージ・内部リンク・合成データの集計を対象とする。実環境のNRQL・CCU、Claude Code／Copilot上の動作は未検証。[検証範囲](docs/validation.md)を参照。

## ライセンス

[MIT License](LICENSE)。
