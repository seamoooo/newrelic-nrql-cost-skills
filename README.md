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

OTelは公式資料との照合、合成データ12テスト、独立エージェントによる静的タスク2件で確認しています。OTel実環境でのNRQL実行・CCU削減効果は未検証です。検証範囲は[検証記録](docs/validation.md)を参照してください。

## 検証例

あるサイト性能診断で、別々に取得していた6クエリを2クエリへ統合し、結果とサンプル数を維持して重複した処理を減らしました。この診断パターン・各1回の比較に限る観測です。数値と条件は[検証記録](docs/validation.md)に掲載しています。

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

新しいセッションで`$newrelic-query-cost`を指定します。`agents/openai.yaml`はCodex用の表示名・説明・既定プロンプトを持つメタデータです。

保存先・呼び出し方は[公式のスキル説明](https://learn.chatgpt.com/docs/build-skills#where-codex-loads-local-skills)を参照してください。旧保存先に同名スキルがある場合は、重複して読み込まれないよう導入先を確認してください。

### Claude Code

```sh
mkdir -p ~/.claude/skills
cp -R -i skills/newrelic-query-cost ~/.claude/skills/
```

`/newrelic-query-cost`で呼び出します。[公式の導入手順](https://code.claude.com/docs/en/skills#choose-where-skills-load)を参照してください。

### GitHub Copilot

Copilot CLIでは`~/.copilot/skills/`、プロジェクトで共有する場合は対象プロジェクトの`.github/skills/`へ`newrelic-query-cost`フォルダ一式をコピーします。CLIでは`/skills reload`後に`/newrelic-query-cost`、Chatではスキル名を指定します。

導入先は[CLIの公式手順](https://docs.github.com/en/copilot/how-tos/copilot-cli/customize-copilot/add-skills)に従ってください。IDEなどの対応範囲は利用バージョンによります。Claude Code／Copilotについては公式手順を照合しましたが、本スキルを使った製品上の動作試験は未実施です。

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

Python 3.10以上を使います。[検証の現状と過去の観測](docs/validation.md)、[OTel公式ドキュメントの監査範囲と結果](docs/otel-documentation-audit.md)、[独立タスク2件の再検証](docs/otel-revalidation.md)を記録しています。

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements-dev.txt
.venv/bin/python scripts/validate.py
.venv/bin/python scripts/validate_otel_semantics.py
```

オフライン検査はメタデータ・内部リンク・数値台帳と、合成データの集計を確認します。NRQLエンジンやエージェントの判断を自動検証するテストではありません。MCP呼び出しや資格情報の読み取りは行いません。

## ライセンス

[MIT License](LICENSE)
