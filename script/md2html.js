import { readFileSync, writeFileSync } from 'fs';
import { marked } from 'marked';
import puppeteer from 'puppeteer';

// Get markdown file path from command line arguments
const mdFile = process.argv[2];
const htmlFile = process.argv[3];
if (!mdFile) {
    console.error('Please provide a markdown file path as argument');
    process.exit(1);
}
if (!htmlFile) {
    htmlFile = mdFile.replace(/\.md$/, '.html');
}
const pngFile = htmlFile.replace(/\.html$/, '.png');

const md = readFileSync(mdFile, 'utf-8');
const html = marked.parse(md);
const fullHtml = `<!DOCTYPE html><html><body>${html}</body></html>`;

puppeteer.launch().then(async (browser) => {
    const page = await browser.newPage();
    await page.setContent(fullHtml);
    await page.screenshot({ path: pngFile });
    await browser.close();
    console.log(`done: ${pngFile}`);
}).catch(err => {
    console.error('❌ Failed to render PNG:', err);
    process.exit(1);
});