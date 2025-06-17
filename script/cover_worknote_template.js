import fs from 'fs';
import { Resvg } from '@resvg/resvg-js';

// 动态变量
const noteTitle = '#用到了AI的工作笔记#';
const number = 'NOTE: No. 1';
const title1 = '用AI从SOP一步步';
const title2 = '生成流程图';
const subtitle1 = '- 提示词要求提取节点';
const subtitle2 = '- AI生成Mermaid，再变流程图';
const date = 'DATE: 2025-06-13';

// const bgColor = '#fef9f6';DATE
const bgColor = '#ffffff';
const textColor = '#333';
const accentColor = '#6b7280';
const collectionsImagePath = './collections/mebrand_20250613_nobg.png';

const a = 50

const svg = `
<svg width="1000" height="1333" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <style>
    @font-face {
      font-family: 'SmileySans', sans-serif;
      src: url('SmileySans-Oblique.ttf') format('truetype');
    }

    text {
      font-family: 'SmileySans', sans-serif;
    }
  </style>

  <!-- 背景 -->
  <rect width="100%" height="100%" fill="${bgColor}" />
  
  <!-- 主标题 -->
  
  <text x="900" y="1120" font-size="56" fill="${textColor}" font-weight="500" text-anchor="end">${subtitle1}</text>
  <text x="900" y="1200" font-size="56" fill="${textColor}" font-weight="500" text-anchor="end">${subtitle2}</text>

  <defs>
    <filter id="shadow" x="-20%" y="-20%" width="140%" height="140%">
      <feDropShadow dx="10" dy="10" stdDeviation="10" flood-opacity="0.3"/>
    </filter>
  </defs>

  <!-- 圆角矩形背景 -->
  <rect x="50" y="${50 + a}" width="900" height="820" 
    rx="60" ry="60" 
    fill="white" 
    stroke="black" 
    stroke-width="1"
    filter="url(#shadow)"/>
  
  <!-- 图片元素 -->
  <image x="670" y="${90 + a}" width="250" height="250" xlink:href="${collectionsImagePath}" />
  <line x1="70" y1="${350 + a}" x2="930" y2="${350 + a}" stroke="black" stroke-width="3"/>
  <text x="80" y="${390 + a}" font-size="28" fill="${textColor}" font-weight="500">${noteTitle}</text>
  <text x="580" y="${390 + a}" font-size="28" fill="black">${number}</text>
  <text x="750" y="${390 + a}" font-size="28" fill="black">${date}</text>
  
  <text x="110" y="${630 + a}" font-size="115" fill="${textColor}" font-weight="500">${title1}</text>
  <text x="110" y="${780 + a}" font-size="115" fill="${textColor}" font-weight="500">${title2}</text>
</svg>`;


// 保存 SVG
fs.writeFileSync('page_cover1.svg', svg, 'utf-8');
console.log('✅ 已生成 page_cover1.svg');

const resvg = new Resvg(svg, {
  font: {
    loadSystemFonts: false, // 不加载系统字体
    fontFiles: ['./SmileySans-Oblique.ttf'], // 指定字体文件路径
  }
});
const pngBuffer = resvg.render().asPng();
fs.writeFileSync('page_cover1.png', pngBuffer);
console.log('✅ 已生成 page_cover1.png');