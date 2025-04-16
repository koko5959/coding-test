# 設計メモ
## モデル
フローチャート(ナイーブ、自然言語的)

```mermaid
flowchart TD
    Start@{ shape: circle }
    Process_1@{ shape: rect, label: "初期化" }
    Output_Base@{ shape: lean-r, label: "途中単語とカウンタを出力" }
    Input_1@{ shape: lean-l, label: "入力" }
    Condition_1@{shape: diamond, label: "入力が半角英字かつ1文字 かつ まだ入力されていない?"}
    Output_ReInput@{shape: lean-r, label: "半角英字での入力を促す"}
    Condition_2@{shape: diamond, label: "入力が正解?"}
    Process_2@{ shape: rect, label: "カウンタ-1" }
    Process_3@{ shape: rect, label: "途中単語の更新" }
    Condition_3@{shape: diamond, label: "カウンタが0?"}
    Condition_4@{shape: diamond, label: "途中単語にアンダーバーがない?"}
    Output_Success@{shape: lean-r, label: "成功を出力"}
    Output_Fail@{shape: lean-r, label: "失敗を出力"}
    Input_ToEnd@{shape: lean-l, label: "何かしらの文字を入力"}
    End@{shape: circle}
    Start --> Process_1
    Process_1 --> Output_Base
    Output_Base --> Input_1
    Input_1 --> Condition_1
    Condition_1 -->|No| Output_ReInput
    Output_ReInput --> Output_Base
    Condition_1 -->|Yes| Condition_2
    Condition_2 -->|No| Process_2
    Condition_2 -->|Yes| Process_3
    Process_2 --> Condition_3
    Condition_3 -->|Yes| Output_Fail
    Condition_3 -->|No| Output_Base
    Process_3 --> Condition_4
    Condition_4 -->|Yes| Output_Success
    Condition_4 -->|No| Output_Base
    Output_Success & Output_Fail --> Input_ToEnd
    Input_ToEnd --> End
```


## 設計の方針
 - 変数や処理はクラスにまとめる
 - クラスに状態を持たせる
    - Playing: 継続
    - Won: 勝利
    - Lost: 敗北
 - 入出力の受け取りと条件分岐はmain関数にまとめる

## 必要なクラス変数
 - counter
    - Integer
    - 残試行回数
 - word
    - String
    - 正解の単語
    - 途中単語は都度作成することにする
 - state
    - String
    - 状態
 - guessed_letters
    - Set
    - ユーザーの入力

## 必要な関数
 - get_display_word(self): string
    - 表示用単語を返す
 - process_guess(self, guess): string or None
    - ユーザーの入力を受取り、状態を更新する
    - 入力バリデーションでエラーの場合、stringを返す
    - その他の場合、エラーを返す
 - get_status(self): string or None
    - stateがWon or Lostなら、現在のゲームの状態に応じたメッセージを返す
    - stateがPlaying なら、Noneを返す

## メモ
- 英語1文字の判定(str.isalpha vs str.encode('utf-8').isalpha())
    - str.isalpha()は、strが複数バイト文字の時、Trueを返す可能性がある
        - 実際の動作で試したが、どういう条件でそうなるのか不明。複数バイト文字を勝手にエンコードして分割し、それがたまたまアルファベットとして判定されるとTrueになるのかな？仕組みがよくわからない
        - https://docs.python.org/ja/3.13/library/stdtypes.html#str.isalpha
    - strをutf-8でエンコードして、bytes.isalpha()でASCII文字判定した方がよい
        - https://docs.python.org/ja/3.13/library/stdtypes.html#str.isalpha

## Todo: スクリプトを前提にフローチャートを書き直す