# 第2回 解答

## 演習

- 使ったモデル・設定（`result.json` の `config` から）：
    "base_model": "Qwen/Qwen3.5-0.8B",
    "revision": "2fc06364715b967f1860aea9cf38778875588b17",
    "seed": 42,
    "num_train_epochs": 5,
    "warmup_steps": 6,
    "lr": 0.0002,
    "lora_r": 16,
    "lora_alpha": 32,
    "max_seq_len": 512,
    "max_new_tokens": 96,
    "gen": {
      "do_sample": false
- 自分で学習を実行したか（`executed_training_myself`）：はい （実行できた範囲：§7まで）
- 学習前：`format_rate` = 0.09523809523809523　 / `content_rate` = 0.0
- 学習後：`format_rate` = 1.0　 / `content_rate` = 0.9047619047619048
- 退行した質問：なし
- 学習後に残った失敗と、その型（根拠なしの質問に断定した / 根拠ありの質問に確認要求で逃げた / 形式の崩れ）：なし
- 知識を問う質問（セクション 6）の結果（学習前の分類 → 学習後の分類）と気づいたこと：最終課題の締め切りを問う質問に対して知識のない「最終課題」の締め切りを断定的に回答していて、誤りを生む可能性がある
- 学習で変わったこと・変わらなかったこと：学習後でも「期日」に関する質問は締め切りだと断定して回答している感じがあり、「成績はいつ出ますか」という質問にneed_review:falseと誤った回答をしている

## 宿題

- 取り組んだレベル：基礎 
- 変えた設定やデータ："num_train_epochs": 20　→ "num_train_epochs": 5
- 結果（比較表や数字）：
"num_train_epochs": 20 学習後 format_rate` = 1.0　 / `content_rate` = 0.9047619047619048
"num_train_epochs": 5  学習後 format_rate` = 1.0　 / `content_rate` = 0.7142857142857143
- ファインチューニングが向く場面・向かない場面についての考察：formatを合わせるのは少ないエポックでも可能なのに対してcontentはエポック5と20とで差が見られたので、contentを合わせるタスクのほうが向いていないと考えられる。
