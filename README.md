# PKMConverter
各PKMサービスのデータを相互に移行するためのスクリプト(Python)
- Google Keep
- Scrapbox
- Obsidian, NoteDiscovery

# 説明 (ver0.0.1)
## 使用方法
1. [Google Keep のデータをエクスポート](https://support.google.com/keep/answer/10017039?hl=ja)し、zip形式でダウンロードする。  
2. zipを解凍し、Keepディレクトリ内のjsonファイルをdata_keepディレクトリに置く。
3. スクリプトを実行する。
    ```bash
    python main.py
    ```
4. data_scrapboxディレクトリにscrapbox.jsonが生成されるので、それを[Scrapboxにインポート](https://scrapbox.io/help-jp/Import_Pages_%2F_Export_Pages)する。

なお、現状(ver0.0.1)ではtextContent(通常のメモ)にしか対応しておらず、チェックリストなどの形式には非対応(スキップされる)。また、画像なども全て無視される。