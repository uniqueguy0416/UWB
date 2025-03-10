import express from 'express';
import mongoose from 'mongoose';
import dotenv from 'dotenv-defaults';

dotenv.config();

const app = express();
const PORT = process.env.PORT || 5000;
const MONGO_URL = process.env.MONGO_URL;

mongoose.connect(MONGO_URL)
  .then(() => console.log('🚀 MongoDB 連接成功！'))
  .catch(err => console.error('❌ MongoDB 連接失敗:', err));

app.listen(PORT, () => {
  console.log(`🌍 伺服器運行在 http://localhost:${PORT}`);
});
