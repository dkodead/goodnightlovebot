const { Client, LocalAuth } = require('whatsapp-web.js');
const qrcode = require('qrcode-terminal');
const express = require('express');
const bodyParser = require('body-parser');

const app = express();
const port = 3000;

app.use(bodyParser.json());

const client = new Client({
  authStrategy: new LocalAuth(),
  puppeteer: {
    headless: true,
    args: ['--no-sandbox', '--disable-setuid-sandbox']
  }
});

client.on('qr', (qr) => {
  console.log('[QR] Scan this QR code in WhatsApp:');
  qrcode.generate(qr, { small: true });
});

client.on('ready', () => {
  console.log('[INFO] WhatsApp client is ready.');
});

client.on('auth_failure', msg => {
  console.error('[ERROR] Auth failure:', msg);
});

app.post('/send', async (req, res) => {
  const { to, message } = req.body;
  if (!to || !message) {
    return res.status(400).json({ status: 'error', message: 'Missing \"to\" or \"message\"' });
  }

  try {
    await client.sendMessage(to, message);
    console.log(`[INFO] Sent message to ${to}`);
    res.json({ status: 'success', message: 'Message sent.' });
  } catch (error) {
    console.error('[ERROR] Failed to send:', error);
    res.status(500).json({ status: 'error', message: 'Failed to send message.' });
  }
});

client.initialize();

app.listen(port, () => {
  console.log(`[INFO] WhatsApp sender server running on http://localhost:${port}`);
});
