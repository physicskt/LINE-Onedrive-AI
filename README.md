# LINE BOT × OneDrive AI業務支援システム

AI拡張機能付きLINE BOT × OneDrive連携による業務自動化・請求管理システム

## 概要

このシステムは、LINE BOTとOneDriveを連携させ、AI技術を活用した業務自動化と請求管理を実現するシステムです。写真やファイルのアップロード、自動整理、売上管理、請求書作成まで一貫してサポートします。

## 主要機能

### 基本機能

1. **ファイル管理機能**
   - LINE BOTから写真やファイルをアップロード
   - 命名ルールに基づく自動ファイルリネーム
   - OneDrive API（Microsoft Graph）による自動フォルダ振り分け保存

2. **通知・エラー管理**
   - エラー検知・エラーメッセージ自動通知
   - リマインド通知機能（未アップロード自動再通知など）
   - 全エラーログにスタックトレース付与

3. **管理画面（LIFF）**
   - LIFFアプリによるスタッフ用／管理者用画面
   - 命名ルールの管理者編集機能
   - 履歴管理、CSVダウンロード機能

### AI拡張機能

1. **売上管理・計算**
   - 業務委託者ごとの歩合割合設定（例：売上の30%）
   - 売上レシート画像の一括アップロード
   - AI自動読取・売上集計

2. **請求書自動化**
   - ChatGPT API（GPT-4o等）を利用した売上計算・請求書作成補助
   - OneDrive上への請求書自動生成・保存
   - LINE BOT＋Eメール送信による自動配布

3. **AI学習機能（将来拡張）**
   - AI学習による分類・命名ルールの自動補完

## 技術スタック

### コア技術
- **LINE連携**: LINE Messaging API / LIFF
- **クラウドストレージ**: OneDrive API（Microsoft Graph）
- **AI・機械学習**: OpenAI API（GPT-4 Turbo / GPT-4o）
- **プログラミング言語**: Python / Node.js / TypeScript
- **フロントエンド**: Vue.js / React
- **自動化ツール**: Power Automate / Zapier / Make

### データベース（選択肢）
- Firebase
- MySQL
- Google スプレッドシート

### 開発環境
- Git版本管理
- 環境変数管理（.env）
- ログ管理システム
- エラートラッキング

## プロジェクト構造

```
LINE-Onedrive-AI/
├── main.py                 # メインアプリケーション
├── config.py              # 設定ファイル
├── .env                   # 環境変数（.gitignoreに含める）
├── .env.example           # 環境変数テンプレート
├── requirements.txt       # Python依存関係
├── modules/               # アプリケーションモジュール
│   ├── __init__.py
│   ├── line_bot/         # LINE BOT関連
│   ├── onedrive/         # OneDrive API関連
│   ├── ai/               # AI機能関連
│   ├── database/         # データベース関連
│   ├── utils/            # ユーティリティ
│   └── liff/             # LIFF アプリ関連
├── logs/                 # ログファイル
├── tests/                # テストファイル
└── docs/                 # ドキュメント
```

## セットアップ

### 前提条件
- Python 3.8以上
- LINE Developer Account
- Microsoft Azure Account（OneDrive API用）
- OpenAI API Key

### インストール

1. リポジトリをクローン
```bash
git clone https://github.com/physicskt/LINE-Onedrive-AI.git
cd LINE-Onedrive-AI
```

2. 仮想環境を作成・有効化
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

3. 依存関係をインストール
```bash
pip install -r requirements.txt
```

4. 環境変数を設定
```bash
cp .env.example .env
# .envファイルを編集して必要な API キーなどを設定
```

5. アプリケーションを起動
```bash
python main.py
```

## 環境変数設定

`.env`ファイルに以下の変数を設定してください：

```env
# LINE Bot Configuration
LINE_CHANNEL_ACCESS_TOKEN=your_line_channel_access_token
LINE_CHANNEL_SECRET=your_line_channel_secret

# Microsoft Graph API (OneDrive)
MICROSOFT_CLIENT_ID=your_microsoft_client_id
MICROSOFT_CLIENT_SECRET=your_microsoft_client_secret
MICROSOFT_TENANT_ID=your_microsoft_tenant_id

# OpenAI API
OPENAI_API_KEY=your_openai_api_key

# Database Configuration
DATABASE_URL=your_database_url

# Application Settings
DEBUG=False
LOG_LEVEL=INFO
```

## 開発スケジュール

### フェーズ1: 基本機能開発（3-4週間）
- [ ] LINE BOT基本機能
- [ ] OneDrive連携
- [ ] ファイル管理システム
- [ ] LIFF基本画面

### フェーズ2: AI機能拡張（2-3週間）
- [ ] 画像認識・OCR機能
- [ ] ChatGPT連携
- [ ] 自動請求書生成
- [ ] 売上計算システム

### フェーズ3: 高度な機能（継続開発）
- [ ] AI学習機能
- [ ] 高度な自動化
- [ ] パフォーマンス最適化
- [ ] セキュリティ強化

## API仕様

### LINE Webhook
```
POST /webhook
Content-Type: application/json
```

### OneDrive ファイルアップロード
```
POST /api/upload
Content-Type: multipart/form-data
```

### AI 売上計算
```
POST /api/ai/calculate-sales
Content-Type: application/json
```

## テスト

```bash
# 全テスト実行
python -m pytest

# 特定のテスト実行
python -m pytest tests/test_line_bot.py

# カバレッジ付きテスト
python -m pytest --cov=modules
```

## 貢献

1. Forkしてブランチを作成
2. 機能を実装・テストを追加
3. Pull Requestを作成

## ライセンス

このプロジェクトは MIT License の下で公開されています。

## サポート

質問や問題がある場合は、Issueを作成してください。

---

**注意**: このシステムは業務用途のため、本番運用前には十分なセキュリティ検証とテストを実施してください。