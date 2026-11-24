// News image entry for 23 November 2026, Node 22, standard library only.
//
// The picture lives in entry.png next to this file. Before anything is
// shipped, this program checks the file really is a PNG by reading its
// eight-byte magic signature; a file that fails that check stops the run
// with an error instead of sending bad bytes to the judge. A file that
// passes is copied byte for byte to /output/entry.png.
//
// To try the copy outside the grader, point MAKEFUN_OUTPUT_DIR at a folder
// of your own, for example:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { readFileSync, writeFileSync } from 'node:fs';
import { join } from 'node:path';

// The PNG magic: the eight bytes every PNG file starts with.
const PNG_MAGIC = Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]);

const picture = readFileSync(new URL('./entry.png', import.meta.url));
if (!picture.subarray(0, PNG_MAGIC.length).equals(PNG_MAGIC)) {
  throw new Error('entry.png is not a PNG: its first eight bytes are not the PNG signature');
}
writeFileSync(join(process.env.MAKEFUN_OUTPUT_DIR ?? '/output', 'entry.png'), picture);
