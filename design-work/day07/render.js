const puppeteer = require('puppeteer');
const path = require('path');

(async () => {
  const browser = await puppeteer.launch({ headless: 'new' });
  const page = await browser.newPage();
  await page.setViewport({ width: 1200, height: 1200, deviceScaleFactor: 2 });

  const filePath = 'file://' + path.resolve(__dirname, 'index.html');
  await page.goto(filePath, { waitUntil: 'networkidle0' });
  await page.evaluateHandle('document.fonts.ready');

  await page.evaluate(() => { document.body.style.zoom = '1'; });
  await new Promise(r => setTimeout(r, 300));

  const card = await page.$('.card');
  const out = path.resolve(__dirname, '../../images/day07.png');
  await card.screenshot({ path: out, type: 'png', omitBackground: false });

  await browser.close();
  console.log('Saved:', out);
})();
