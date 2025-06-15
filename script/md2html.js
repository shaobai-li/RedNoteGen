import { readFileSync, writeFileSync } from 'fs';
import { marked } from 'marked';

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

const md = readFileSync(mdFile, 'utf-8');
const html = marked.parse(md);

const fullHtml = `<!DOCTYPE html><html><body>${html}</body></html>`;

// console.log(html);


writeFileSync(htmlFile, fullHtml);
console.log(`done: ${htmlFile}`);