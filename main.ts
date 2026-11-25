// THE WORLD — Wednesday 25 November 2026 (news-image-20261125 entry).
//
// A newspaper front page summing up the world's news of 25 November 2026
// in one 1024x1024 image. The front page was pre-rendered by render.py
// (Pillow, flat vector illustration + real text, deterministic) and is held
// in this repository as entry.png. This program copies it to the output
// directory, verifying the PNG signature, the 1024x1024 dimensions and the
// 1 MiB size gate first.
//
// Run outside the grader's container with:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { mkdirSync, readFileSync, writeFileSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const SIG = Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]);

const here = dirname(fileURLToPath(import.meta.url));
const bytes = readFileSync(join(here, 'entry.png'));

if (!bytes.subarray(0, 8).equals(SIG)) throw new Error('not a PNG');
// IHDR width/height are big-endian uint32 at offsets 16 and 20.
const width = bytes.readUInt32BE(16);
const height = bytes.readUInt32BE(20);
if (width > 1024 || height > 1024) {
  throw new Error(`image too large: ${width}x${height}`);
}
if (bytes.length > 1024 * 1024) {
  throw new Error(`image over 1 MiB: ${bytes.length} bytes`);
}

const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
mkdirSync(outDir, { recursive: true });
writeFileSync(join(outDir, 'entry.png'), bytes);
console.log(`wrote entry.png (${width}x${height}, ${bytes.length} bytes)`);
