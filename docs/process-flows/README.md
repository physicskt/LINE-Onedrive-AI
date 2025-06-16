# 処理フロー図 / Process Flow Diagrams 📊

このドキュメントでは、LINE × OneDrive AI業務支援システムの主要な処理フローを図解で説明します。

This document explains the main process flows of the LINE × OneDrive AI Business Support System with diagrams.

## 🗂️ フロー図一覧 / Flow Diagram List

1. [全体システムフロー / Overall System Flow](#overall-system-flow)
2. [ファイルアップロードフロー / File Upload Flow](#file-upload-flow)
3. [レシート処理フロー / Receipt Processing Flow](#receipt-processing-flow)
4. [請求書作成フロー / Invoice Creation Flow](#invoice-creation-flow)
5. [エラーハンドリングフロー / Error Handling Flow](#error-handling-flow)

---

## Overall System Flow

```mermaid
graph TD
    A[📱 ユーザー<br/>User] --> B[LINE BOT]
    
    B --> C{メッセージタイプ<br/>Message Type}
    
    C -->|📸 画像<br/>Image| D[画像処理<br/>Image Processing]
    C -->|📄 ファイル<br/>File| E[ファイル処理<br/>File Processing]
    C -->|💬 テキスト<br/>Text| F[コマンド処理<br/>Command Processing]
    
    D --> G[OneDrive 保存<br/>OneDrive Save]
    E --> G
    
    D --> H[AI 分析<br/>AI Analysis]
    H --> I[売上データ登録<br/>Sales Data Registration]
    
    F --> J{コマンド種別<br/>Command Type}
    J -->|請求書作成<br/>Create Invoice| K[請求書生成<br/>Invoice Generation]
    J -->|売上確認<br/>Check Sales| L[売上表示<br/>Sales Display]
    J -->|設定<br/>Settings| M[LIFF 画面<br/>LIFF Screen]
    
    G --> N[✅ 完了通知<br/>Completion Notice]
    I --> N
    K --> N
    L --> N
    M --> N
    
    N --> A
    
    style A fill:#e1f5fe
    style B fill:#f3e5f5
    style G fill:#e8f5e8
    style H fill:#fff3e0
    style N fill:#e8f5e8
```

---

## File Upload Flow

```mermaid
graph TD
    A[📱 ユーザーがファイル送信<br/>User Sends File] --> B[LINE BOT 受信<br/>LINE BOT Receives]
    
    B --> C[ファイル情報取得<br/>Get File Info]
    C --> D[ファイルダウンロード<br/>Download File]
    
    D --> E{ファイルタイプ判定<br/>File Type Check}
    
    E -->|画像<br/>Image| F[画像解析準備<br/>Prepare Image Analysis]
    E -->|PDF/Document<br/>PDF/Document| G[文書処理準備<br/>Prepare Document Processing]
    E -->|その他<br/>Other| H[汎用ファイル処理<br/>Generic File Processing]
    
    F --> I[OneDrive アップロード<br/>OneDrive Upload]
    G --> I
    H --> I
    
    I --> J[フォルダ振り分け<br/>Folder Classification]
    J --> K[ファイル名自動生成<br/>Auto Generate Filename]
    
    K --> L{アップロード成功？<br/>Upload Success?}
    
    L -->|成功<br/>Success| M[✅ 成功通知<br/>Success Notification]
    L -->|失敗<br/>Failed| N[❌ エラー通知<br/>Error Notification]
    
    M --> O[📊 ログ記録<br/>Log Recording]
    N --> P[🔄 リトライ処理<br/>Retry Processing]
    
    O --> Q[処理完了<br/>Process Complete]
    P --> Q
    
    style A fill:#e1f5fe
    style M fill:#e8f5e8
    style N fill:#ffebee
    style Q fill:#f3e5f5
```

---

## Receipt Processing Flow

```mermaid
graph TD
    A[📸 レシート画像送信<br/>Receipt Image Sent] --> B[画像受信・保存<br/>Image Received & Saved]
    
    B --> C[OneDrive アップロード<br/>OneDrive Upload]
    C --> D[🤖 AI 画像解析開始<br/>AI Image Analysis Start]
    
    D --> E[OpenAI Vision API<br/>OpenAI Vision API]
    E --> F[テキスト抽出<br/>Text Extraction]
    
    F --> G{解析結果確認<br/>Analysis Result Check}
    
    G -->|成功<br/>Success| H[データ構造化<br/>Data Structuring]
    G -->|失敗<br/>Failed| I[❌ 解析エラー<br/>Analysis Error]
    
    H --> J[金額・店舗名抽出<br/>Extract Amount & Store]
    J --> K[売上データベース登録<br/>Register to Sales DB]
    
    K --> L[歩合計算<br/>Commission Calculation]
    L --> M[結果フォーマット<br/>Format Results]
    
    M --> N[✅ 処理結果通知<br/>Processing Result Notice]
    
    I --> O[手動入力案内<br/>Manual Input Guide]
    O --> P[ユーザー修正待ち<br/>Wait for User Correction]
    
    N --> Q[📊 月次集計更新<br/>Update Monthly Summary]
    P --> Q
    Q --> R[処理完了<br/>Process Complete]
    
    style A fill:#e1f5fe
    style E fill:#fff3e0
    style N fill:#e8f5e8
    style I fill:#ffebee
    style R fill:#f3e5f5
```

---

## Invoice Creation Flow

```mermaid
graph TD
    A[💬 請求書作成要求<br/>Invoice Creation Request] --> B[期間指定確認<br/>Period Specification Check]
    
    B --> C[売上データ取得<br/>Get Sales Data]
    C --> D[データ集計<br/>Data Aggregation]
    
    D --> E[歩合計算実行<br/>Execute Commission Calculation]
    E --> F[請求書テンプレート取得<br/>Get Invoice Template]
    
    F --> G[🤖 ChatGPT API 呼び出し<br/>ChatGPT API Call]
    G --> H[請求書コンテンツ生成<br/>Generate Invoice Content]
    
    H --> I[PDF 生成<br/>PDF Generation]
    I --> J[OneDrive 保存<br/>OneDrive Save]
    
    J --> K{保存成功？<br/>Save Success?}
    
    K -->|成功<br/>Success| L[📧 メール送信<br/>Email Send]
    K -->|失敗<br/>Failed| M[❌ 保存エラー<br/>Save Error]
    
    L --> N{メール送信成功？<br/>Email Success?}
    
    N -->|成功<br/>Success| O[✅ 完了通知<br/>Completion Notice]
    N -->|失敗<br/>Failed| P[LINE 通知のみ<br/>LINE Notice Only]
    
    M --> Q[エラー詳細通知<br/>Error Detail Notice]
    
    O --> R[📊 送信履歴記録<br/>Record Send History]
    P --> R
    Q --> R
    R --> S[処理完了<br/>Process Complete]
    
    style A fill:#e1f5fe
    style G fill:#fff3e0
    style O fill:#e8f5e8
    style M fill:#ffebee
    style S fill:#f3e5f5
```

---

## Error Handling Flow

```mermaid
graph TD
    A[⚠️ エラー発生<br/>Error Occurred] --> B[エラー種別判定<br/>Error Type Detection]
    
    B --> C{エラータイプ<br/>Error Type}
    
    C -->|API エラー<br/>API Error| D[API 接続確認<br/>API Connection Check]
    C -->|ファイル処理エラー<br/>File Processing Error| E[ファイル再確認<br/>File Recheck]
    C -->|認証エラー<br/>Authentication Error| F[認証情報確認<br/>Auth Info Check]
    C -->|システムエラー<br/>System Error| G[システム状態確認<br/>System Status Check]
    
    D --> H[🔄 リトライ処理<br/>Retry Processing]
    E --> H
    F --> I[認証更新<br/>Auth Refresh]
    G --> J[緊急通知<br/>Emergency Notice]
    
    H --> K{リトライ成功？<br/>Retry Success?}
    I --> K
    
    K -->|成功<br/>Success| L[✅ 復旧通知<br/>Recovery Notice]
    K -->|失敗<br/>Failed| M[❌ エラー通知<br/>Error Notice]
    
    J --> N[管理者緊急連絡<br/>Admin Emergency Contact]
    
    L --> O[📊 ログ記録<br/>Log Recording]
    M --> P[詳細エラーログ<br/>Detailed Error Log]
    N --> P
    
    P --> Q[ユーザーサポート案内<br/>User Support Guide]
    Q --> R[処理終了<br/>Process End]
    
    style A fill:#ffebee
    style L fill:#e8f5e8
    style M fill:#ffebee
    style N fill:#ff5722,color:#fff
    style R fill:#f3e5f5
```

---

## 🔍 フロー図の見方 / How to Read Flow Diagrams

### 記号の意味 / Symbol Meanings

- 🟦 **四角形 / Rectangle**: 処理ステップ / Processing Step
- 🔷 **ひし形 / Diamond**: 判定・分岐 / Decision/Branch
- 🟢 **緑色 / Green**: 成功・完了 / Success/Complete
- 🔴 **赤色 / Red**: エラー・失敗 / Error/Failed  
- 🟡 **黄色 / Yellow**: AI・外部API / AI/External API
- 🔵 **青色 / Blue**: ユーザー操作 / User Action

### 処理の流れ / Process Flow

1. **開始点** から **終了点** まで矢印に従って進みます
2. **判定ポイント** では条件に応じて分岐します
3. **エラー処理** は赤色の経路で示されます
4. **成功処理** は緑色の経路で示されます

Follow the arrows from **start** to **end** points, with **decision points** branching based on conditions, **error handling** shown in red paths, and **successful processing** shown in green paths.