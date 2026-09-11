import fs from "fs";
import path from "path";
import { fileURLToPath } from "url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const registryPath = path.join(__dirname, "../registry.json");

const registry = JSON.parse(fs.readFileSync(registryPath, "utf-8"));

console.log(`\n🔧 SalesPortl MCP Server - Initial Setup\n`);
console.log(`Total Skills: ${registry.metadata.total_skills}`);
console.log(`Total Domains: ${registry.metadata.total_domains}`);
console.log(`\nRegistered Domains:\n`);

registry.domains.forEach((domain) => {
  console.log(`  ✓ ${domain.id.padEnd(20)} ${domain.name.padEnd(40)} (${domain.skills_count} skills)`);
});

console.log(`\n✅ Ready for SalesPortl MCP integration\n`);
