import { createRequire } from "node:module";
import { dirname, resolve } from "node:path";
import { fileURLToPath } from "node:url";

export const root = resolve(dirname(fileURLToPath(import.meta.url)), "..");
export const toolRoot = process.env.VIDEO_TOOLS ? resolve(process.env.VIDEO_TOOLS) : root;
export const requireTool = createRequire(resolve(toolRoot, "package.json"));
