# New Relic MCP Skills

New Relic MCPでの調査に使うAgent Skillsです。

## newrelic-query-cost

[スキル本体](skills/newrelic-query-cost/SKILL.md)は、NRQL・NerdGraphのクエリや実行計画をコスト効率の観点で評価し、意味を保った改善案を返します。

- 対象範囲、時間範囲、反復回数、FACET・時系列の粒度、応答量を評価
- 静的評価と実測を区別し、未確認のCCU・料金・削減率を作らない
- MCPでの実行も依頼された場合は、必要な読み取りだけで検証
- [New Relic公式ドキュメント](skills/newrelic-query-cost/references/official-docs.md)に基づく判断基準を使用

参照元はNew Relicの公開公式ドキュメントです。クエリの範囲・反復・返却量を減らすノウハウと、効果を正しく検証する手順をまとめています。

## 実測効果

サイト性能の初期診断で、同じ対象・固定期間の取得結果を維持して比較しました。

- NRQL実行数：**6本 → 2本（66.7%減）**
- 検査イベント数：**297件 → 99件（66.7%減）**
- 記録Core CCU：**0.000279739 → 0.000093246（66.7%減）**
- 取得結果・サンプル数：**すべて一致**

各クエリ1回の比較。本処理のみで、探索・検証コストと外部LLM料金は含みません。詳細は[検証記録](tests/acceptance.md)を参照してください。

## 導入

任意の場所にcloneし、使用するエージェントが読むスキルディレクトリへ `skills/newrelic-query-cost` をコピーまたはリンクしてください。シンボリックリンクはcloneを削除・移動すると使えなくなります。

Codexのローカルスキル配置例（既存の同名フォルダがあれば上書きせず確認）：

```sh
git clone https://github.com/newrelickk/newrelic-mcp-skills.git
mkdir -p ~/.codex/skills
ln -s "$(pwd)/newrelic-mcp-skills/skills/newrelic-query-cost" ~/.codex/skills/newrelic-query-cost
```

新しいセッションで、次のように依頼できます。

```text
$newrelic-query-cost このNRQLのコスト効率をレビューして。実行は不要です。
FROM Log SELECT * SINCE 7 days ago LIMIT MAX
目的はcheckoutの直近30分のエラーログ確認です。
```

```text
$newrelic-query-cost 対象アカウントのcheckoutサービスについて、直近1時間の
エラー増加をNew Relic MCPで調査して。実行前にクエリ計画の効率も判断して。
```

レビューだけならMCP接続は不要です。実行にはNew Relic MCPの接続と対象アカウントへの権限が必要です。特定のMCPツール名には依存せず、利用環境のツール仕様を確認します。請求の確定や監視設定の自動変更は行いません。

## Claude Code

上記でcloneした `newrelic-mcp-skills` ディレクトリへ移動して実行します。既存の同名スキルがある場合は上書きせず確認してください。

```sh
mkdir -p ~/.claude/skills
ln -s "$(pwd)/skills/newrelic-query-cost" ~/.claude/skills/newrelic-query-cost
```

Claude Codeを起動し、次のコマンドで呼び出します。

```text
/newrelic-query-cost このNRQLのコスト効率をレビューして。実行は不要です。
```

配置と呼び出し方は[Claude Code公式ドキュメント](https://code.claude.com/docs/en/skills)に基づきます。

## GitHub Copilot CLI

cloneした `newrelic-mcp-skills` ディレクトリ内で実行します。

```sh
mkdir -p ~/.copilot/skills
ln -s "$(pwd)/skills/newrelic-query-cost" ~/.copilot/skills/newrelic-query-cost
```

Copilot CLIのセッション内で読み込みを更新し、呼び出します。

```text
/skills reload
/skills list
/newrelic-query-cost このNRQLのコスト効率をレビューして。実行は不要です。
```

配置とコマンドは[GitHub Copilot CLI公式ドキュメント](https://docs.github.com/en/copilot/how-tos/copilot-cli/customize-copilot/add-skills)に基づきます。

## GitHub Copilotのプロジェクト共有

VS Codeやクラウドエージェント等でプロジェクトのスキルとして使う場合は、対象プロジェクトの `.github/skills/` へスキル一式をコピーします。以下は、このスキルリポジトリのディレクトリ内から実行する例です。コピー先を実際のプロジェクトへ変更してください。

```sh
project_dir=/absolute/path/to/your-project
mkdir -p "$project_dir/.github/skills"
cp -R -n skills/newrelic-query-cost "$project_dir/.github/skills/"
```

共有する場合は、対象プロジェクトで追加ファイルを確認してコミットします。

Copilot Chatで「newrelic-query-costスキルを使って、このNRQLのコスト効率を評価して」と依頼します。利用環境のAgent Skills対応が必要です。詳細は[GitHubのAgent Skillsドキュメント](https://docs.github.com/en/copilot/how-tos/copilot-on-github/customize-copilot/customize-cloud-agent/add-skills)を参照してください。

## 検証範囲

構造・参照検証、静的レビューとMCP実利用検証は[検証記録](tests/acceptance.md)を参照してください。効果は検証条件によって異なります。
