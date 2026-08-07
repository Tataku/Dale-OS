import { execFile } from "node:child_process";
import { existsSync } from "node:fs";
import path from "node:path";
import { promisify } from "node:util";
const execFileAsync = promisify(execFile);
function resolveRoot(): string {
  if (process.env.DALE_OS_ROOT) return path.resolve(process.env.DALE_OS_ROOT);
  if (existsSync(path.resolve(process.cwd(), "tools"))) return process.cwd();
  return path.resolve(process.cwd(), "../..");
}
export async function runDaleTool(script: string, payload: unknown) {
  const root = resolveRoot(); const target = path.join(root, "tools", script);
  if (!existsSync(target)) throw new Error(`Dale OS tool not found: ${target}. Set DALE_OS_ROOT to the repository root.`);
  const python = process.env.DALE_OS_PYTHON ?? "python3";
  const { stdout } = await execFileAsync(python, [target], { input: JSON.stringify(payload), timeout: 15_000, maxBuffer: 2 * 1024 * 1024 });
  return JSON.parse(stdout);
}
