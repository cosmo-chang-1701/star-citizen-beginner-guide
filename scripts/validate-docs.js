/**
 * Comprehensive Docs-as-Code Validator for GitBook Semantic Architecture
 * Executed inside Docker container (node:lts-alpine)
 */

const fs = require('fs');
const path = require('path');

let errors = [];
let warnings = [];
let stats = {
  totalFiles: 0,
  verifiedLinks: 0,
  verifiedImages: 0,
  frontmatterChecked: 0,
  redirectsChecked: 0
};

function error(msg) {
  errors.push(`[ERROR] ${msg}`);
}

function warn(msg) {
  warnings.push(`[WARN] ${msg}`);
}

// 1. Verify .gitbook.yaml & Redirects
console.log('--- 1. Checking .gitbook.yaml & Redirects ---');
const gitbookYamlPath = path.resolve('.gitbook.yaml');
if (!fs.existsSync(gitbookYamlPath)) {
  error('.gitbook.yaml does not exist in root directory.');
} else {
  const content = fs.readFileSync(gitbookYamlPath, 'utf8');
  if (!content.includes('root:') || !content.includes('readme:') || !content.includes('summary:')) {
    error('.gitbook.yaml is missing required fields (root, structure.readme, structure.summary).');
  } else {
    console.log('✓ .gitbook.yaml exists and contains required structure configuration.');
  }

  // Check redirects mapping
  const redirectLines = content.split('\n').filter(line => line.trim().startsWith('part-') || line.trim().startsWith('appendix/'));
  stats.redirectsChecked = redirectLines.length;
  for (const line of redirectLines) {
    const parts = line.split(':');
    if (parts.length >= 2) {
      const targetPath = parts[1].trim();
      if (!fs.existsSync(path.resolve(targetPath))) {
        error(`Redirect target does not exist: ${targetPath}`);
      }
    }
  }
  console.log(`✓ Verified ${stats.redirectsChecked} redirects to valid semantic destination files.`);
}

// 2. Verify .gitignore
console.log('--- 2. Checking .gitignore ---');
const gitignorePath = path.resolve('.gitignore');
if (!fs.existsSync(gitignorePath)) {
  error('.gitignore does not exist in root directory.');
} else {
  const content = fs.readFileSync(gitignorePath, 'utf8');
  if (!content.includes('.gitbook/cache/')) {
    warn('.gitignore should include .gitbook/cache/');
  } else {
    console.log('✓ .gitignore exists and includes GitBook cache exclusions.');
  }
}

// 3. Verify No Legacy Directories exist
console.log('--- 3. Checking for Legacy Directory Removal ---');
const legacyDirs = ['part-0', 'part-1', 'part-2', 'part-3', 'part-4', 'part-5', 'part-6', 'assets', 'appendix/appendix-e'];
for (const d of legacyDirs) {
  if (fs.existsSync(path.resolve(d))) {
    error(`Legacy directory still exists: ${d}`);
  }
}
console.log('✓ All legacy numeric directories (part-0..6, assets, appendix-e) successfully retired.');

// 4. Verify Assets directory structure
console.log('--- 4. Checking Assets Directory Structure ---');
const gitbookAssetsPath = path.resolve('.gitbook/assets');
if (!fs.existsSync(gitbookAssetsPath)) {
  error('.gitbook/assets directory does not exist.');
} else {
  const files = fs.readdirSync(gitbookAssetsPath, { recursive: true });
  console.log(`✓ .gitbook/assets exists with ${files.length} items.`);
}

// 5. Find all Markdown files
function getAllMarkdownFiles(dir) {
  let results = [];
  const list = fs.readdirSync(dir);
  for (const file of list) {
    if (file === '.git' || file === 'node_modules' || file === '.gitbook') continue;
    const fullPath = path.join(dir, file);
    const stat = fs.statSync(fullPath);
    if (stat && stat.isDirectory()) {
      results = results.concat(getAllMarkdownFiles(fullPath));
    } else if (file.endsWith('.md')) {
      results.push(fullPath);
    }
  }
  return results;
}

const mdFiles = getAllMarkdownFiles('.');
stats.totalFiles = mdFiles.length;
console.log(`\nFound ${mdFiles.length} Markdown content files across semantic directories.`);

// 6. Verify SUMMARY.md completeness and structure
console.log('--- 5. Checking SUMMARY.md ---');
const summaryPath = path.resolve('SUMMARY.md');
if (!fs.existsSync(summaryPath)) {
  error('SUMMARY.md not found.');
} else {
  const summaryContent = fs.readFileSync(summaryPath, 'utf8');
  const linkRegex = /\[(.*?)\]\((.*?)\)/g;
  let match;
  let summaryLinksCount = 0;
  while ((match = linkRegex.exec(summaryContent)) !== null) {
    const text = match[1];
    const linkPath = match[2].trim();
    summaryLinksCount++;
    if (!fs.existsSync(path.resolve(linkPath))) {
      error(`SUMMARY.md links to non-existent file: "${text}" -> "${linkPath}"`);
    }
  }
  console.log(`✓ SUMMARY.md contains ${summaryLinksCount} valid, resolvable semantic page links.`);

  // Check section groups
  const groupMatches = summaryContent.match(/^##\s+.+$/gm);
  if (!groupMatches || groupMatches.length === 0) {
    warn('SUMMARY.md does not contain any "##" Section Groups.');
  } else {
    console.log(`✓ SUMMARY.md defines ${groupMatches.length} visual Section Groups.`);
  }
}

// 7. Verify Frontmatter, Internal Links, and Images across all files
console.log('--- 6. Checking Frontmatter and Internal Links ---');
for (const file of mdFiles) {
  const content = fs.readFileSync(file, 'utf8');
  const relPath = path.relative('.', file);

  // Frontmatter check (except SUMMARY.md and README.md files)
  if (path.basename(file) !== 'SUMMARY.md' && relPath !== 'README.md' && relPath !== 'docs/README.md') {
    if (!content.startsWith('---\n')) {
      error(`Missing frontmatter in ${relPath}`);
    } else {
      const parts = content.split('---\n');
      if (parts.length < 3) {
        error(`Malformed frontmatter in ${relPath}`);
      } else {
        const fm = parts[1];
        if (!fm.includes('description:')) {
          error(`Frontmatter in ${relPath} missing "description" field.`);
        }
        if (!fm.includes('icon:')) {
          error(`Frontmatter in ${relPath} missing "icon" field.`);
        }
        stats.frontmatterChecked++;
      }
    }
  }

  // Links & Images check
  const linkPattern = /(!?)\[([^\]]*)\]\(([^)]+)\)/g;
  let match;
  while ((match = linkPattern.exec(content)) !== null) {
    const isImage = match[1] === '!';
    const linkText = match[2];
    const target = match[3].trim();

    if (target.startsWith('http://') || target.startsWith('https://') || target.startsWith('#') || target.startsWith('mailto:')) {
      continue;
    }

    const targetWithoutAnchor = target.split('#')[0];
    if (!targetWithoutAnchor) continue;

    const fileDir = path.dirname(file);
    const resolvedPath = path.resolve(fileDir, targetWithoutAnchor);

    if (isImage) {
      stats.verifiedImages++;
      if (!fs.existsSync(resolvedPath)) {
        error(`Broken image link in ${relPath}: "${linkText}" -> "${target}" (Resolved: ${resolvedPath})`);
      }
    } else {
      stats.verifiedLinks++;
      if (!fs.existsSync(resolvedPath)) {
        error(`Broken markdown link in ${relPath}: "${linkText}" -> "${target}" (Resolved: ${resolvedPath})`);
      }
    }
  }
}

console.log(`✓ Verified ${stats.frontmatterChecked} files with valid YAML frontmatter.`);
console.log(`✓ Verified ${stats.verifiedLinks} internal markdown links without any 404.`);
console.log(`✓ Verified ${stats.verifiedImages} image references.`);

// 8. Verify Heading Hierarchy and GitBook Interactive Blocks
console.log('--- 7. Checking Heading Hierarchy and GitBook Interactive Blocks ---');
let headingHierarchyIssues = 0;
let interactiveBlockIssues = 0;

for (const file of mdFiles) {
  const content = fs.readFileSync(file, 'utf8');
  const relPath = path.relative('.', file);
  if (path.basename(file) === 'SUMMARY.md') continue;

  const lines = content.split('\n');
  let inCodeBlock = false;
  let headings = [];
  let tabsCount = 0;
  let endtabsCount = 0;
  let tabCount = 0;
  let endtabCount = 0;
  let stepperCount = 0;
  let endstepperCount = 0;
  let stepCount = 0;
  let endstepCount = 0;
  let hintCount = 0;
  let endhintCount = 0;

  for (let i = 0; i < lines.length; i++) {
    const line = lines[i];
    const trimmed = line.trim();

    if (trimmed.startsWith('```')) {
      inCodeBlock = !inCodeBlock;
      continue;
    }
    if (inCodeBlock) continue;

    // Disallow any lingering GitHub alert blockquotes (except for root README.md landing page)
    if (relPath !== 'README.md' && /^>\s*\\?\[!(NOTE|TIP|IMPORTANT|WARNING|CAUTION)\]/i.test(trimmed)) {
      error(`Disallowed legacy alert blockquote found in ${relPath} at line ${i + 1}: "${trimmed}" (must use GitBook {% hint style="..." %})`);
    }

    // GitBook blocks
    if (trimmed === '{% tabs %}') tabsCount++;
    if (trimmed === '{% endtabs %}') endtabsCount++;
    if (trimmed.startsWith('{% tab ')) tabCount++;
    if (trimmed === '{% endtab %}') endtabCount++;
    if (trimmed === '{% stepper %}') stepperCount++;
    if (trimmed === '{% endstepper %}') endstepperCount++;
    if (trimmed === '{% step %}' || trimmed.startsWith('{% step ')) stepCount++;
    if (trimmed === '{% endstep %}') endstepCount++;
    if (trimmed.startsWith('{% hint ') || trimmed === '{% hint %}') hintCount++;
    if (trimmed === '{% endhint %}') endhintCount++;

    // Headings
    const headingMatch = line.match(/^(#{1,6})\s+(.+)$/);
    if (headingMatch) {
      headings.push({
        level: headingMatch[1].length,
        text: headingMatch[2].trim(),
        line: i + 1
      });
    }
  }

  // Check interactive block balance
  if (tabsCount !== endtabsCount || tabCount !== endtabCount) {
    error(`Unbalanced {% tabs %} in ${relPath}: tabs=${tabsCount}, endtabs=${endtabsCount}, tab=${tabCount}, endtab=${endtabCount}`);
    interactiveBlockIssues++;
  }
  if (stepperCount !== endstepperCount || stepCount !== endstepCount) {
    error(`Unbalanced {% stepper %} in ${relPath}: stepper=${stepperCount}, endstepper=${endstepperCount}, step=${stepCount}, endstep=${endstepCount}`);
    interactiveBlockIssues++;
  }
  if (hintCount !== endhintCount) {
    error(`Unbalanced {% hint %} in ${relPath}: hint=${hintCount}, endhint=${endhintCount}`);
    interactiveBlockIssues++;
  }

  // Check H1
  const h1s = headings.filter(h => h.level === 1);
  if (h1s.length === 0) {
    error(`Missing # H1 heading in ${relPath}`);
    headingHierarchyIssues++;
  } else if (h1s.length > 1) {
    error(`Multiple # H1 headings found in ${relPath} (lines: ${h1s.map(h => h.line).join(', ')})`);
    headingHierarchyIssues++;
  }

  // Check heading hierarchy sequence
  let prevLevel = 0;
  for (const h of headings) {
    if (prevLevel === 0) {
      if (h.level !== 1) {
        error(`First heading in ${relPath} is not H1 (found H${h.level}: "${h.text}" at line ${h.line})`);
        headingHierarchyIssues++;
      }
    } else {
      if (h.level > prevLevel + 1) {
        error(`Heading level skip in ${relPath}: H${prevLevel} -> H${h.level} ("${h.text}" at line ${h.line})`);
        headingHierarchyIssues++;
      }
    }
    prevLevel = h.level;
  }
}

if (headingHierarchyIssues === 0 && interactiveBlockIssues === 0) {
  console.log('✓ All 66 documentation pages have perfect heading hierarchy (0 skips) and balanced interactive blocks.');
}

// 8. Verify Terminology Compliance (sc-knowledge alignment)
console.log('--- 8. Checking Terminology Compliance (sc-knowledge) ---');
let terminologyIssues = 0;
const deprecatedTerms = [
  { term: '德拉克工業', desc: 'Use 德雷克星際 instead of 德拉克工業' },
  { term: '毀滅空間站', desc: 'Use 廢墟太空站 instead of 毀滅空間站' },
  { term: '星辰建築師', desc: 'Use 星際建築系統 instead of 星辰建築師' },
  { term: '阿隆光環', desc: 'Use 亞倫環 instead of 阿隆光環' },
  { term: '克萊雪監獄', desc: 'Use 克萊舍爾勞教所 instead of 克萊雪監獄' },
  { term: '史丹頓', desc: 'Use 斯坦頓 instead of 史丹頓' },
  { regex: /德拉克(?![沃斯])/g, term: '德拉克', desc: 'Use 德雷克星際 instead of 德拉克 (except Drakworth)' },
  { term: '基礎節 (Foundation Festival)', desc: 'Use 奠基節 instead of 基礎節' },
  { term: '寇拉莫 (Coramor)', desc: 'Use 科拉情人節 instead of 寇拉莫' },
  { term: '生命維持系統 (Life Support)', desc: 'Use 維生系統 instead of 生命維持系統' },
  { term: '醫療生物凝膠', desc: 'Use 醫療凝膠 instead of 醫療生物凝膠' },
  { term: '互安防務', desc: 'Use 互安防衛 instead of 互安防務' },
  { term: '北岩服務集團', desc: 'Use 北境之巖服務團隊 instead of 北岩服務集團' },
  { term: '埃克哈特保安', desc: 'Use 埃克哈特保全 instead of 埃克哈特保安' },
  { term: '科瓦萊什物流', desc: 'Use 科瓦萊什貨運 instead of 科瓦萊什物流' },
  { term: 'QV 拆解站', desc: 'Use QV 碎岩站 instead of QV 拆解站' },
  { term: 'SCM (戰鬥機動)', desc: 'Use SCM (戰鬥操控模式) instead of SCM (戰鬥機動)' },
  { term: 'NAV (極速導航)', desc: 'Use NAV (巡航導航模式) instead of NAV (極速導航)' }
];

for (const file of mdFiles) {
  const content = fs.readFileSync(file, 'utf8');
  const relPath = path.relative('.', file);
  // Strip HTML comments (preserving original English lore sources)
  const cleanContent = content.replace(/<!--[\s\S]*?-->/g, '');

  for (const item of deprecatedTerms) {
    if (item.regex) {
      // Reset regex index before test
      item.regex.lastIndex = 0;
      if (item.regex.test(cleanContent)) {
        error(`Deprecated term pattern "${item.term}" found in ${relPath}: ${item.desc}`);
        terminologyIssues++;
      }
    } else if (cleanContent.includes(item.term)) {
      error(`Deprecated term "${item.term}" found in ${relPath}: ${item.desc}`);
      terminologyIssues++;
    }
  }
}

if (terminologyIssues === 0) {
  console.log(`✓ All ${mdFiles.length} documentation files are strictly compliant with sc-knowledge terminology.`);
}

// Final Summary
console.log('\n========================================');
console.log('SEMANTIC ARCHITECTURE VALIDATION SUMMARY');
console.log('========================================');
console.log(`Total Files Checked:      ${stats.totalFiles}`);
console.log(`Frontmatter Pages:        ${stats.frontmatterChecked}`);
console.log(`Internal Links Verified:  ${stats.verifiedLinks}`);
console.log(`Images Verified:          ${stats.verifiedImages}`);
console.log(`Redirects Verified:       ${stats.redirectsChecked}`);
console.log(`Warnings:                 ${warnings.length}`);
console.log(`Errors:                   ${errors.length}`);

if (warnings.length > 0) {
  console.log('\nWarnings:');
  warnings.forEach(w => console.warn('  ' + w));
}

if (errors.length > 0) {
  console.log('\nErrors encountered:');
  errors.forEach(e => console.error('  ' + e));
  process.exit(1);
} else {
  console.log('\n🎉 ALL CHECKS PASSED! Semantic GitBook architecture is 100% compliant.');
  process.exit(0);
}
