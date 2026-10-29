# New Relic MCP Skills

NRQLのquery cost・CCU・実行計画を見直し、必要な答えを保てる改善案を返すAgent Skillです。

## newrelic-query-cost

- 対象・期間・検索条件・カーディナリティ・反復・応答量を評価
- 判定 → 理由 → 改善案 → 検証状況の順で回答
- 静的レビューに対応。実行時はハーネスに公開された登録済みMCPツールのみ使用
- NerdGraphはNRQLの実行経路として扱い、汎用GraphQL最適化や設定変更は対象外

[スキル本体](skills/newrelic-query-cost/SKILL.md)に判断手順、参照ファイルにクエリ例と運用ノウハウをまとめています。

## 検証例

あるサイト性能診断で、別々に取得していた6クエリを2クエリへ統合し、結果とサンプル数を維持して重複した処理を減らしました。この診断パターン・各1回の比較に限る観測です。数値と条件は[検証記録](docs/validation.md)に掲載しています。

## 導入

```sh
git clone https://github.com/seamoooo/newrelic-mcp-skills.git
cd newrelic-mcp-skills
```

使用するエージェントのスキルディレクトリへ一式をコピーします。既存の同名スキルがある場合は内容を確認してから更新してください。以下の`-i`は既存ファイルの上書き時に確認します。

### Codex

```sh
mkdir -p ~/.codex/skills
cp -R -i skills/newrelic-query-cost ~/.codex/skills/
```

新しいセッションで`$newrelic-query-cost`を指定します。`agents/openai.yaml`はCodex用の表示名・説明・既定プロンプトを持つメタデータです。

### Claude Code

```sh
mkdir -p ~/.claude/skills
cp -R -i skills/newrelic-query-cost ~/.claude/skills/
```

`/newrelic-query-cost`で呼び出します。

### GitHub Copilot

Copilot CLIでは`~/.copilot/skills/`、プロジェクトで共有する場合は対象プロジェクトの`.github/skills/`へ`newrelic-query-cost`フォルダ一式をコピーします。CLIでは`/skills reload`後に`/newrelic-query-cost`、Chatではスキル名を指定します。

## 依頼例

```text
newrelic-query-costで次のNRQLをレビューして。実行は不要です。
FROM Log SELECT * SINCE 7 days ago LIMIT MAX
目的はcheckoutの直近30分のエラーログ確認です。
```

```text
Review and optimize the NRQL query cost for this MCP investigation.
Preserve the requested time range and explain how you will verify equivalent results.
```

レビューだけならMCP接続は不要です。実行には、ハーネス側のNew Relic MCP接続・公開済みツール・対象アカウントへの権限が必要です。ツールがない場合は静的評価を返し、ユーザーへ接続を案内します。

## 検証

[手動レビューと過去の観測](docs/validation.md)と、オフライン検査を分けています。

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements-dev.txt
.venv/bin/python scripts/validate.py
```

オフライン検査はメタデータ・内部リンク・数値台帳の集計を確認します。MCP呼び出しや資格情報の読み取りは行いません。

## ライセンス

[MIT License](LICENSE)
