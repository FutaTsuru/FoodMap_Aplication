# システム概要
aws_experimentはawsを用いた、大学周辺の飲食店マップアプリを構築した。
サイドバーには飲食店のジャンルごとにラジオボタンがあり、指定したジャンルのお店のマーカーを出現させることが出来る。
加えて現在地から近い飲食店や、行動履歴からいつも通る道沿いのお店のマーカーを出現させることが出来るラジオボタンもある。マーカーを押すとその店の詳細情報がポップアップする。
S3に今回対象としたお店の情報（店名, ジャンル, 店の写真, 緯度経度など）を格納。lambdaで現在地取得や飲食店との距離計算, Javascript,htmlを用いたマーカー処理を行っている。

![Image](https://github.com/user-attachments/assets/8c8f9c04-76ea-400c-a658-8ae10a4fb087)
