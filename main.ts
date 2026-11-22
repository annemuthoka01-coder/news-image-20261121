import * as fs from 'fs';
import * as path from 'path';
import { fileURLToPath } from 'url';

const here = path.dirname(fileURLToPath(import.meta.url));

function main() {
  const src = path.join(here, 'entry.png');
  const outDir = process.env.MAKEFUN_OUTPUT_DIR || '/output';
  if (!fs.existsSync(src)) {
    console.error('Error: entry.png not found next to main.ts');
    process.exit(1);
  }
  fs.mkdirSync(outDir, { recursive: true });
  const dest = path.join(outDir, 'entry.png');
  if (path.resolve(src) !== path.resolve(dest)) {
    fs.copyFileSync(src, dest);
  }
  const a = fs.statSync(src).size;
  const b = fs.statSync(dest).size;
  if (a !== b) {
    console.error('Error: copied size mismatch');
    process.exit(1);
  }
  console.log('Copied entry.png to ' + dest + ' (' + a + ' bytes)');
}

main();
