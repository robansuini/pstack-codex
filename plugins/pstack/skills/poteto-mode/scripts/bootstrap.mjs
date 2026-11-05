import { existsSync } from "node:fs";
import { fileURLToPath } from "node:url";
import { spawnSync } from "node:child_process";

const directory = fileURLToPath(new URL(".", import.meta.url));
const [major, minor] = process.versions.node.split(".").map(Number);
if (!((major === 22 && minor >= 18) || (major === 23 && minor >= 6) || major >= 24)) {
  console.error("watch-pr requires Node 22.18+, 23.6+, or a later major version.");
  process.exit(1);
}
if (!existsSync(new URL("node_modules/commander/package.json", import.meta.url))) {
  const result = spawnSync("npm", ["ci", "--omit=dev", "--ignore-scripts", "--no-audit", "--no-fund"], {
    cwd: directory,
    stdio: ["ignore", 2, 2],
  });
  if (result.error) console.error(result.error.message);
  if (result.status !== 0) process.exit(result.status ?? 1);
}
