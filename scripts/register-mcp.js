#!/usr/bin/env node

import fs from "fs";
import path from "path";
import { fileURLToPath } from "url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const registryPath = path.join(__dirname, "../registry.json");
const configPath = path.join(__dirname, "../config.json");

let config = {};
if (fs.existsSync(configPath)) {
  config = JSON.parse(fs.readFileSync(configPath, "utf-8"));
}

const registry = JSON.parse(fs.readFileSync(registryPath, "utf-8"));

console.log("\n📊 SalesPortl MCP Registration\n");

const endpoint = process.env.SALESPORTL_ENDPOINT || config.salesportl?.mcp_server || "localhost:3000";
const apiKey = process.env.SALESPORTL_API_KEY || config.salesportl?.api_key || "not-configured";

console.log(`🔗 Endpoint: ${endpoint}`);
console.log(`🔑 API Key: ${apiKey === "not-configured" ? "⚠️  NOT CONFIGURED" : "✅ configured"}\n`);

console.log(`📦 Registering ${registry.metadata.total_skills} skills across ${registry.metadata.total_domains} domains...\n`);

let totalRegistered = 0;

registry.domains.forEach((domain) => {
  const enabled = config.domains?.[domain.id]?.enabled !== false;
  const status = enabled ? "✅" : "⏸️ ";
  console.log(`${status} ${domain.id.padEnd(20)} ${domain.skills_count} skills`);
  if (enabled) totalRegistered += domain.skills_count;
});

console.log(`\n✨ Ready to register ${totalRegistered} skills!\n`);
console.log(`Next steps:\n`);
console.log(`1. Configure config.json with your SalesPortl details`);
console.log(`2. Run: npm run register:salesportl`);
console.log(`3. Verify: node scripts/test-salesportl-connection.js\n`);
