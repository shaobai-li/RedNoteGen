const fs = require('fs');
const marked = require('marked');

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

const md = fs.readFileSync(mdFile, 'utf-8');
const html = marked.parse(md);

console.log(html);

// fs.writeFileSync(htmlFile, html);
// console.log(`done: ${htmlFile}`);