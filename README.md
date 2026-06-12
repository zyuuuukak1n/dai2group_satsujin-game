# 🔪 連続殺人ゲーム 考察＆ガチ投票サイト

だいにぐるーぷによる大人気企画『殺人ゲーム』の非公式ファンサイト・考察データベースです。
参加者のアリバイ情報や伏線を整理し、リアルタイムで「誰が殺人鬼か」を予想・投票できる機能を備えています！

## ✨ 特徴 (Features)

- **🕵️‍♂️ 情報整理＆考察:** 各キャラクターの能力、アリバイ状況、未回収の伏線を一覧化
- **📊 リアルタイムガチ投票:** ユーザー全員の投票結果をリアルタイムで集計・表示
- **🛡️ セキュアなアーキテクチャ:** Node.js (Express) バックエンドによる厳格なバリデーションとレートリミットを実装。FirebaseのAPIキーなどを隠蔽した堅牢なシステム設計

---

## 🛠️ 技術スタック (Tech Stack)

**フロントエンド**
- HTML / Vanilla JavaScript
- Tailwind CSS (スタイリング)
- FontAwesome (アイコン)

**バックエンド**
- Node.js / Express
- Zod (入力値バリデーション)
- Express Rate Limit (DDoS・過剰アクセス対策)
- Firebase Admin SDK (Firestore トランザクション処理)
- Jest / Supertest (テスト)

---

## 🚀 ローカル環境での動かし方 (Getting Started)

Firebaseの設定なしでも、すぐに動かして試せる「モックDBモード」を搭載しています！

### 1. リポジトリのクローン
\`\`\`bash
git clone https://github.com/your-username/satsujin-game-vote.git
cd satsujin-game-vote
\`\`\`

### 2. 依存関係のインストール
\`\`\`bash
npm install
\`\`\`

### 3. 環境変数の設定
ルートディレクトリに \`.env\` ファイルを作成し、以下の内容をコピーしてください。

\`\`\`env
PORT=3000
NODE_ENV=development
# MOCK_DBをtrueにするとFirebaseなしで動作します！
MOCK_DB=true
CORS_ORIGIN="*"
RATE_LIMIT_WINDOW_MS=900000
RATE_LIMIT_MAX_REQUESTS=100
\`\`\`

### 4. サーバーの起動
\`\`\`bash
npm start
\`\`\`
ブラウザで \`http://localhost:3000\` にアクセスするとサイトが表示されます。

---

## 🔥 Firebase連携（本番運用）

実際にFirestoreと連携させて本番運用を行う場合は、以下の手順を実施してください。

1. Firebaseコンソールから「プロジェクトの設定」＞「サービスアカウント」を開く
2. 「新しい秘密鍵の生成」からJSONファイルをダウンロード
3. \`.env\` ファイルを以下のように設定（\`MOCK_DB\` は削除または \`false\` にします）

\`\`\`env
FIREBASE_PROJECT_ID="your_project_id"
FIREBASE_CLIENT_EMAIL="firebase-adminsdk-xxx@your-project-id.iam.gserviceaccount.com"
FIREBASE_PRIVATE_KEY="-----BEGIN PRIVATE KEY-----\nあなたのプライベートキー\n-----END PRIVATE KEY-----\n"
\`\`\`
※ \`FIREBASE_PRIVATE_KEY\` の改行は \`\n\` にエスケープした状態で1行にして記載してください。

---

## 🧪 テストの実行

Jest と Supertest を使用したテストコードを同梱しています。バリデーションやセキュリティ周りの挙動を確認できます。

\`\`\`bash
npm test
\`\`\`

---

## 📄 ライセンス (License)

本プロジェクトは [MIT License](LICENSE) の下で公開されています。自由にご利用・改変いただけます。

※ 当サイトはファンメイドの非公式プロジェクトであり、「だいにぐるーぷ」様および関係各所とは一切関係ありません。
