import fs from "fs";
import path from "path";
import { execSync } from "child_process";
import { fileURLToPath } from "url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

async function main() {
  console.log("🚀 Starting TTS generation with Kokoro-Vietnamese (hung_thinh voice)...");
  try {
    execSync("python generate_tts.py", {
      cwd: __dirname,
      encoding: "utf-8",
      stdio: "inherit",
    });
  } catch (error) {
    console.error("❌ Error running Kokoro-Vietnamese TTS generation:", error);
  }
}

main();
