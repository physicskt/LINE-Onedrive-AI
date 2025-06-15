# デプロイメントガイド

## 前提条件

- Python 3.8以上
- LINE Developer Account
- Microsoft Azure Account
- OpenAI API Key

## セットアップ手順

### 1. リポジトリのクローン

```bash
git clone https://github.com/physicskt/LINE-Onedrive-AI.git
cd LINE-Onedrive-AI
```

### 2. 自動セットアップ

```bash
./setup.sh
```

### 3. 環境変数の設定

`.env`ファイルを編集して、必要なAPI キーとトークンを設定してください：

```env
# LINE Bot設定
LINE_CHANNEL_ACCESS_TOKEN=your_line_channel_access_token
LINE_CHANNEL_SECRET=your_line_channel_secret

# Microsoft Graph API設定
MICROSOFT_CLIENT_ID=your_microsoft_client_id
MICROSOFT_CLIENT_SECRET=your_microsoft_client_secret
MICROSOFT_TENANT_ID=your_microsoft_tenant_id

# OpenAI API設定
OPENAI_API_KEY=your_openai_api_key

# その他設定
SECRET_KEY=your_secret_key_here
```

### 4. アプリケーションの起動

```bash
python3 main.py
```

## API設定手順

### LINE Bot設定

1. [LINE Developers Console](https://developers.line.biz/)にアクセス
2. 新しいChannel（Messaging API）を作成
3. Channel Access TokenとChannel Secretを取得
4. Webhook URLを設定: `https://your-domain.com/webhook`

### Microsoft Graph API設定

1. [Azure Portal](https://portal.azure.com/)にアクセス
2. App registrationを作成
3. 必要な権限を設定:
   - `Files.ReadWrite`
   - `Sites.ReadWrite.All`
4. Client IDとClient Secretを取得

### OpenAI API設定

1. [OpenAI Platform](https://platform.openai.com/)にアクセス
2. API Keyを生成
3. 使用制限と請求設定を確認

## 本番環境デプロイ

### Heroku

```bash
# Herokuアプリを作成
heroku create your-app-name

# 環境変数を設定
heroku config:set LINE_CHANNEL_ACCESS_TOKEN=your_token
heroku config:set LINE_CHANNEL_SECRET=your_secret
# ... その他の環境変数

# デプロイ
git push heroku main
```

### AWS EC2

```bash
# EC2インスタンスに接続
ssh -i your-key.pem ubuntu@your-ec2-instance

# プロジェクトをクローン
git clone https://github.com/physicskt/LINE-Onedrive-AI.git
cd LINE-Onedrive-AI

# セットアップ実行
./setup.sh

# Gunicornで起動
gunicorn --bind 0.0.0.0:8000 main:app
```

### Docker

```bash
# Dockerイメージをビルド
docker build -t line-onedrive-ai .

# コンテナを起動
docker run -p 8000:8000 --env-file .env line-onedrive-ai
```

## 監視とメンテナンス

### ログの確認

```bash
# アプリケーションログ
tail -f logs/app.log

# エラーログ
tail -f logs/error.log
```

### ヘルスチェック

```bash
curl http://localhost:8000/health
```

### バックアップ

- 定期的にデータベースのバックアップを取得
- 設定ファイルのバックアップを保持
- OneDriveのデータも定期的に確認

## トラブルシューティング

### よくある問題

1. **LINE Webhookエラー**
   - SSL証明書が有効か確認
   - Webhook URLが正しく設定されているか確認

2. **OneDrive接続エラー**
   - Microsoft Graph APIの権限を確認
   - Client IDとSecretが正しいか確認

3. **AI機能エラー**
   - OpenAI APIキーが有効か確認
   - API使用制限に達していないか確認

### ログレベルの変更

開発中は`.env`ファイルで：

```env
DEBUG=True
LOG_LEVEL=DEBUG
```

本番環境では：

```env
DEBUG=False
LOG_LEVEL=INFO
```