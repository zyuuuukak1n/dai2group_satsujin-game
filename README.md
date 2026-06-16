# 🔪 連続殺人ゲーム 考察＆ガチ投票サイト

[![OGP Image](https://zyuuuukak1n.dev/dai2group/satsujin-game/img_ogp.png)](https://zyuuuukak1n.dev/dai2group/satsujin-game/)

**▶ [公開済みのWebページはこちらからご覧いただけます！](https://zyuuuukak1n.dev/dai2group/satsujin-game/)**

だいにぐるーぷによる大人気企画『殺人ゲーム』の非公式ファンサイト・考察データベースです。
参加者のアリバイ情報や伏線を整理し、リアルタイムで「誰が殺人鬼か」を予想・投票できる機能を備えています！

---

## ✨ 特徴 (Features)

- **🕵️‍♂️ 情報整理＆考察:** 各キャラクターの能力、アリバイ状況、未回収の伏線を一覧化。
- **📊 リアルタイムガチ投票:** ユーザー全員の投票結果をリアルタイムで集計・表示します。
- **⚡ 超軽量な静的構成:** サーバーサイドを持たない、完全なフロントエンド完結型のシンプルな構成です。

---

## 🛠️ 技術スタック (Tech Stack)

当サイトは、ファイル数を最小限に抑えた非常にシンプルな静的ファイル構成（HTML, CSS, Vanilla JavaScript）で構築されています。

- **HTML / Vanilla JavaScript**: フレームワークに依存しない軽量で高速な構成。
- **Tailwind CSS (CDN)**: スタイリングの効率化とカスタマイズ性を両立。
- **Firebase Firestore**: バックエンドサーバーを構築することなく、ブラウザから直接SDKを利用してリアルタイムな投票集計を実現。
- **セキュアな設定管理**: FirebaseのAPIキーなどのシークレット情報を外部の `config.js` に切り出し、Git管理から除外することで安全性を確保しています。

---

## 🚀 ローカル環境での動かし方 (Getting Started)

当プロジェクトは静的ファイルのみで構成されているため、ビルドやサーバー構築は不要です。

### 1. リポジトリのクローン
```bash
git clone <your-repository-url>
cd dai2group_satsujin-game
```

### 2. 環境設定ファイルの作成
ルートディレクトリにある `config.example.js` をコピーして `config.js` を作成し、ご自身のFirebaseプロジェクトの設定値を入力してください。

```bash
cp config.example.js config.js
```

### 3. ブラウザで開く
`index.html` をお好みのブラウザで直接開くか、VSCode等の拡張機能「Live Server」を利用して表示してください。
これだけで完全に動作します！

---

## 📄 ライセンス (License)

本プロジェクトは [MIT License](LICENSE) の下で公開されています。自由にご利用・改変いただけます。

※ 当サイトはファンメイドの非公式プロジェクトであり、「だいにぐるーぷ」様および関係各所とは一切関係ありません。
