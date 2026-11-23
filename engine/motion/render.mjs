// usage: node render.mjs jobs.json   (jobs = [{comp, props, len, out}]) – einmal bündeln, alle Clips rendern
import {bundle} from "@remotion/bundler";
import {renderMedia, renderStill, selectComposition} from "@remotion/renderer";
import fs from "fs"; import path from "path"; import {fileURLToPath} from "url";
const here = path.dirname(fileURLToPath(import.meta.url));
const jobs = JSON.parse(fs.readFileSync(process.argv[2], "utf8"));
const chrome = process.env.CHROME || "/usr/bin/google-chrome";
const serveUrl = await bundle({entryPoint: path.join(here, "src/index.ts")});
for (const j of jobs) {
  const inputProps = {comp: j.comp, props: j.props, len: j.len};
  const comp = await selectComposition({serveUrl, id: "Motion", inputProps, browserExecutable: chrome});
  if (j.still !== undefined) {
    await renderStill({serveUrl, composition: comp, inputProps, frame: Math.round(j.still * 30), output: j.out, browserExecutable: chrome, scale: j.scale || 1});
  } else {
    await renderMedia({serveUrl, composition: comp, inputProps, codec: "h264", crf: 16, muted: true, outputLocation: j.out, browserExecutable: chrome, concurrency: 2});
  }
  console.log("ok", j.out);
}
