#!/usr/bin/env node

import fs from "fs";
import path from "path";
import { fileURLToPath } from "url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const registryPath = path.join(__dirname, "../registry.json");

const registry = JSON.parse(fs.readFileSync(registryPath, "utf-8"));

console.log(`\n📋 Registered Skills\n`);

registry.domains.forEach((domain) => {
  console.log(`${domain.id.toUpperCase()} (${domain.skills_count} skills)`);
  console.log(`  ${domain.description}\n`);
});

console.log(`Total: ${registry.metadata.total_skills} skills\n`);
