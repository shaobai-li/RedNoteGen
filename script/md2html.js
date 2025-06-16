import { readFileSync, writeFileSync } from 'fs';
import { marked } from 'marked';
import puppeteer from 'puppeteer';

// Get markdown file path from command line arguments
const mdFile = process.argv[2];
const cssFile = process.argv[3];
if (!mdFile) {
    console.error('Please provide a markdown file path as argument');
    process.exit(1);
}
const pngFile = mdFile.replace(/\.md$/, '.png');

const md = readFileSync(mdFile, 'utf-8');
const html = marked.parse(md);
const css = readFileSync(cssFile, 'utf-8');
const fullHtml = `<!DOCTYPE html><html><head><style>${css}</style></head><body>${html}</body></html>`;

puppeteer.launch().then(async (browser) => {
    const page = await browser.newPage();
    await page.setViewport({ width: 1000, height: 1333 });
    await page.setContent(fullHtml);
    await page.screenshot({ path: pngFile });
    await browser.close();
    console.log(`done: ${pngFile}`);
}).catch(err => {
    console.error('❌ Failed to render PNG:', err);
    process.exit(1);
});