import express from 'express';
import mongoose from 'mongoose';
import dotenv from 'dotenv-defaults';  // 加載 .env 和 .env.default
import http from 'http';
import WebSocket, { WebSocketServer } from 'ws';
import wsConnect from './wsConnect.js';  // WebSocket 連線邏輯
import mongo from './mongo.js';  // 你的 MongoDB 連線邏輯

// 加載 .env 和 .env.default 配置
dotenv.config();

// 設定 Express
const app = express();
const PORT = process.env.PORT || 5000;  // 設定端口，預設 5000
const MONGO_URL = process.env.MONGO_URL;  // 從環境變數中讀取 MongoDB 連線字串

// MongoDB 連接
mongoose.connect(MONGO_URL, { useNewUrlParser: true, useUnifiedTopology: true })
  .then(() => console.log('🚀 MongoDB 連接成功！'))
  .catch(err => console.error('❌ MongoDB 連接失敗:', err));

// 設定基本的路由
app.get('/', (req, res) => {
  res.send('MongoDB 已連接！');
});

// WebSocket 伺服器設定
const server = http.createServer(app);
const wss = new WebSocketServer({ server });

wss.on('connection', wsConnect);  // 你的 WebSocket 連線處理邏輯

// 啟動伺服器
server.listen(PORT, () => {
  console.log(`🌍 伺服器運行在 http://localhost:${PORT}`);
});
