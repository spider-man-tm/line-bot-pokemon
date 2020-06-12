Name: ポケモンお知らせLINE Bot
====

<br><br>

## 概要
ガラル地方のポケモンの強さやタイプなどを教えてくれるボットです。

<br><br>

## 環境
pipenvを使って以下のPipfileから必要なライブラリをインストール
```
[[source]]
name = "pypi"
url = "https://pypi.org/simple"
verify_ssl = true

[dev-packages]

[packages]
flask = "==1.1.2"
line-bot-sdk = "==1.16.0"
sqlalchemy = "==1.3.17"
pandas = "==1.0.4"
psycopg2-binary = "==2.8.5"

[requires]
python_version = "3.8"
```

<br><br>

## システム構成
![fig1](https://github.com/spider-man-tm/readme_figure/blob/master/line-bot_pokemon/system.png)

<br><br>

## LINEの画面
![fig2](https://github.com/spider-man-tm/readme_figure/blob/master/line-bot_pokemon/line_image.png)