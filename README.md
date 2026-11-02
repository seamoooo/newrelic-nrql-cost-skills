# New Relic NRQL Cost Optimization Skills

New RelicのNRQL実行コストを下げるためのAgent Skillsです。必要な結果を保ちながら、クエリの処理量と実行回数を見直します。

コミュニティが作成したスキルで、New Relicの公式製品ではありません。

## newrelic-query-cost

- New Relic APMエージェント／OpenTelemetry（OTel）／混在環境向けの判断手順を提供
- 対象・期間・検索条件・カーディナリティ・反復・応答量を評価
- 判定 → 理由 → 改善案 → 検証状況の順で回答
- 静的レビューに対応。実行時はハーネスに公開された登録済みMCPツールのみ使用
- NerdGraphはNRQLの実行経路として扱い、汎用GraphQL最適化や設定変更は対象外

[スキル本体](skills/newrelic-query-cost/SKILL.md)に判断手順、参照ファイルにクエリ例と運用ノウハウをまとめています。

## 導入

```sh
git clone https://github.com/seamoooo/newrelic-nrql-cost-skills.git
cd newrelic-nrql-cost-skills
```

使用するエージェントのスキルディレクトリへ一式をコピーします。既存の同名スキルがある場合は内容を確認してから更新してください。以下の`-i`は既存ファイルの上書き時に確認します。コマンド例はmacOS／Linux向けです。

### Codex

```sh
mkdir -p ~/.agents/skills
cp -R -i skills/newrelic-query-cost ~/.agents/skills/
```

新しいセッションで`$newrelic-query-cost`を指定します。

保存先・呼び出し方は[公式のスキル説明](https://learn.chatgpt.com/docs/build-skills#where-codex-loads-local-skills)を参照してください。同名スキルの重複に注意してください。

### Claude Code

```sh
mkdir -p ~/.claude/skills
cp -R -i skills/newrelic-query-cost ~/.claude/skills/
```

`/newrelic-query-cost`で呼び出します。[公式の導入手順](https://code.claude.com/docs/en/skills#choose-where-skills-load)を参照してください。

### GitHub Copilot

Copilot CLIでは`~/.copilot/skills/`、プロジェクトで共有する場合は対象プロジェクトの`.github/skills/`へ`newrelic-query-cost`フォルダ一式をコピーします。CLIでは`/skills reload`後に`/newrelic-query-cost`、Chatではスキル名を指定します。

導入先・対応範囲は[CLIの公式手順](https://docs.github.com/en/copilot/how-tos/copilot-cli/customize-copilot/add-skills)で確認してください。

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

OTelの場合は収集元も指定できます。例：「OTelで収集したcheckoutのHTTPサーバーメトリクスを使い、応答時間と件数の定期集計を見直して。Spanのサンプリングとエラー定義も確認して」。[OTel対応の判断手順と例](skills/newrelic-query-cost/references/opentelemetry.md)に公式資料と適用条件を記載しています。

レビューだけならMCP接続は不要です。実行には、ハーネス側のNew Relic MCP接続・公開済みツール・対象アカウントへの権限が必要です。ツールがない場合は静的評価を返し、ユーザーへ接続を案内します。

## 検証

Python 3.10以上を使います。検証範囲は[検証記録](docs/validation.md)を参照してください。

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements-dev.txt
.venv/bin/python scripts/validate.py
.venv/bin/python scripts/validate_otel_semantics.py
```

オフライン検査はメタデータ・内部リンク・数値台帳と合成データの集計を確認します。OTel実環境のNRQL・CCUと、Claude Code／Copilot上の動作は未検証です。

## ライセンス

[MIT License](LICENSE)
