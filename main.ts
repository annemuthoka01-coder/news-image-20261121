/**
 * main.ts
 * Copies entry.png to process.env.MAKEFUN_OUTPUT_DIR or /output.
 * Usage:
 *   MAKEFUN_OUTPUT_DIR=out node main.ts
 */

import * as fs from 'fs';
import * as path from 'path';

function main() {
  const src = path.join(__dirname, 'entry.png');
  const outDir = process.env.MAKEFUN_OUTPUT_DIR || '/output';

  if (!fs.existsSync(src)) {
    console.error(`Error: Source file ${src} does not exist.`);
    process.exit(1);
  }

  const dest = path.join(outDir, 'entry.png');

  // Resolve realpaths if they exist to check if src and dest are the same file
  try {
    const srcReal = fs.realpathSync(src);
    let destReal = '';
    try {
      destReal = fs.realpathSync(dest);
    } catch {}
    if (srcReal === destReal) {
      console.error(`Error: Source and destination are the same file (${src}).`);
      process.exit(1);
    }
  } catch (e) {
    // If realpath fails (e.g. dest doesn't exist yet), that's fine.
  }

  if (!fs.existsSync(outDir)) {
    fs.mkdirSync(outDir, { recursive: true });
  }

  fs.copyFileSync(src, dest);

  const srcStat = fs.statSync(src);
  const destStat = fs.statSync(dest);

  if (srcStat.size !== destStat.size) {
    console.error(`Error: Copied size mismatch (${destStat.size} vs expected ${srcStat.size}).`);
    process.exit(1);
  }

  console.log(`Successfully copied entry.png to ${dest} (${srcStat.size} bytes).`);
}

main();
