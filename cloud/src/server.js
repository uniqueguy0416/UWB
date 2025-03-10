import express from 'express';
import mongoose from 'mongoose';
import dotenv from 'dotenv-defaults';
import PalletModel from './models/pallet.js';


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

app.post('/addPallet', async (req, res) => {
  const palletData = new PalletModel({
    type: '田字型',
    content: '貨物A',
    status: 'static',
    position: [1, 2],
    final_user: 'User1',
  });

  try {
    const result = await palletData.save();  // 儲存資料
    res.json(result);  // 回傳儲存的資料
  } catch (err) {
    res.status(500).json({ message: err.message });
  }
});
