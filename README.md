# New Relic MCP Skills

New Relic MCPでの調査に使うAgent Skillsです。

## newrelic-query-cost

[スキル本体](skills/newrelic-query-cost/SKILL.md)は、NRQL・NerdGraphのクエリや実行計画をコスト効率の観点で評価し、意味を保った改善案を返します。

- 対象範囲、時間範囲、反復回数、FACET・時系列の粒度、応答量を評価
- 静的評価と実測を区別し、未確認のCCU・料金・削減率を作らない
- MCPでの実行も依頼された場合は、必要な読み取りだけで検証
- [New Relic公式ドキュメント](skills/newrelic-query-cost/references/official-docs.md)に基づく判断基準を使用

参照元はNew Relicの公開公式ドキュメントです。クエリの範囲・反復・返却量を減らすノウハウと、効果を正しく検証する手順をまとめています。

## 目的を保った改善と実測効果

このスキルは、元の調査目的に必要な対象・期間・母集団・集計定義・属性を保てるか確認してから代替クエリを提案します。期間の短縮や上位N件への置換で必要な情報が欠ける案は、同等な改善として扱いません。用途を限定する案は、その条件を明記します。

動画再生イベントを対象にNew Relic MCPで検証しました。比較対象は同じサービス・環境・固定期間とし、結果の同等性を確認しました。以下は検証環境を特定する情報と生の計測値を除いた集計結果です。

| 本来の目的 | 改善前 → 改善後 | 目的を保てた根拠 | 観測した効果 |
|---|---|---|---|
| 同じ対象・期間の再生試行数と開始数を知る | それぞれを別の2クエリで集計 → `filter(uniqueCount(viewId), WHERE ...)`で1クエリに統合 | 試行数・開始数がそれぞれ一致。対象・期間・各集計の条件と定義を維持 | 本処理の実行数2→1。合計検査イベント数・合計記録Core CCUはいずれも50%減 |
| 全イベントの時刻・イベント名・再生ID・累積再生時間の4属性を確認する | `SELECT *` → `timestamp, actionName, viewId, totalPlaytime`のみ取得 | 両方とも対象期間の全行を取得。必要4属性は重複行の個数も含めて一致。総件数とLIMITを照合して取得漏れがないことも確認 | 結果JSONは93.76%減。検査イベント数・記録Core CCUは変化なし |

属性を絞る案が同等なのは、必要な情報がその4属性で足りる場合です。全属性の保管や未知の属性の探索が目的なら、`SELECT *`の同等な代替にはなりません。集計統合も、FACETの選出対象や比率の分母などが変わる場合は同等性を別途確認します。

性能は`NrdbQuery`、利用量は`NrComputeUsage`で対象クエリ文字列を照合し、比較対象ごとに成功1実行・利用量1記録を確認しました。JSONサイズは結果行をUTF-8のコンパクトJSONにした値で、MCP応答全体や圧縮後の通信量ではありません。

各クエリ1回・少量データでの観測です。表の削減率はこの比較に限り、一般的な削減率や請求額を保証しません。スキーマ確認・効果測定を含む検証全体では11本を実行しており、表の2→1は比較する本処理の実行数です。実効開始・終了時刻はMCP応答に含まれず、応答からの照合はできていません。生テレメトリ・認証情報は掲載していません。

計測値の意味は[公式データ辞書](https://docs.newrelic.com/attribute-dictionary/)と[公式の利用量クエリ](https://docs.newrelic.com/docs/accounts/accounts-billing/new-relic-one-pricing-billing/usage-queries-alerts/)に照らして区別しています。検証内容は[検証記録](tests/acceptance.md)、比較方法は[実測手順](skills/newrelic-query-cost/references/measurement.md)を参照してください。

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

構造・参照検証、静的レビューとMCP実利用検証は[検証記録](tests/acceptance.md)を参照してください。固定期間の実データで集計統合と属性投影の結果同等性、NrdbQueryとNrComputeUsageによる計測を確認しました。各1回の小規模な観測であり、一般的な削減率や請求額を保証するものではありません。
