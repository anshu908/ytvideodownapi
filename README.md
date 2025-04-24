# Multi Video Downloader API Documentation

## Overview
A unified Flask-based API that supports downloading videos from YouTube, Instagram, TikTok, and Snapchat. It uses cookies only for YouTube to support all available video qualities.

---

## 🚀 Getting Started

### Run the Server:
```bash
python multi_downloader_api.py
```

The API will be available at:
```
http://localhost:8000
```

---

## 📍 API Endpoints

### 1. `/` (Root)
**Method:** GET  
**Description:** Shows welcome message and developer credit.

### 2. `/available`
**Method:** GET  
**Description:** Returns list of supported platforms and developer info.

**Example Response:**
```json
{
  "supported_platforms": [
    {"name": "YouTube", "url_pattern": "youtube.com", "cookies": true},
    {"name": "Instagram", "url_pattern": "instagram.com", "cookies": false},
    {"name": "TikTok", "url_pattern": "tiktok.com", "cookies": false},
    {"name": "Snapchat", "url_pattern": "snapchat.com", "cookies": false}
  ],
  "developer": {
    "name": "Anshu",
    "project": "Multi Video Downloader API",
    "github": "https://github.com/cyber-ansh",
    "telegram": "@cyber_ansh"
  }
}
```

---

### 3. `/info`
**Method:** GET  
**Params:**
- `url` (required) – YouTube video URL

**Description:** Returns metadata and available formats for a YouTube video. Only works for YouTube.

**Example:**
```
GET /info?url=https://www.youtube.com/watch?v=abc123
```

---

### 4. `/download`
**Method:** GET  
**Params:**
- `url` (required) – Video URL (YouTube/Instagram/TikTok/Snapchat)
- `quality` (optional) – Format string or 'best' (default: 'best')
- `audio` (optional) – Set to `true` to download audio only (YouTube only)

**Examples:**
- YouTube: `/download?url=https://www.youtube.com/watch?v=abc123&quality=best`
- Instagram: `/download?url=https://www.instagram.com/reel/xyz`
- TikTok: `/download?url=https://www.tiktok.com/@user/video/xyz`
- Snapchat: `/download?url=https://www.snapchat.com/discover/xyz`
- YouTube Audio Only: `/download?url=https://www.youtube.com/watch?v=abc123&audio=true`

**Note:** YouTube requires a valid `cookies.txt` file in the project directory.

---

## 📁 Tools to Use

- **Browser:** Paste endpoint URL for direct download
- **Postman/Insomnia:** For testing GET requests
- **Frontend (React/Vue):** Use `fetch` or `axios` to trigger download from your app

---

## 👨‍💻 Developer
- **Name:** Anshu
- **GitHub:** https://github.com/anshu908
- **Telegram:** t.me/cyber_ansh


