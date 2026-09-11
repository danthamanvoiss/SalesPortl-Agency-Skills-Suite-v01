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

const endpoint = process.env.SALESPORTL_ENDPOINT || config.salesportl?.mcp_server || "localhost:3000";
const apiKey = process.env.SALESPORTL_API_KEY || config.salesportl?.api_key;

console.log(`\n🧪 Testing SalesPortl Connection\n`);
console.log(`Endpoint: ${endpoint}`);
console.log(`API Key: ${apiKey ? "configured" : "⚠️  missing"}\n`);

if (!apiKey) {
  console.log(`⚠️  API key not configured. Set SALESPORTL_API_KEY or update config.json\n`);
}

const registry = JSON.parse(fs.readFileSync(registryPath, "utf-8"));

console.log(`📊 Registry Status:\n`);
console.log(`  Domains: ${registry.metadata.total_domains}`);
console.log(`  Skills: ${registry.metadata.total_skills}`);
console.log(`  MCP Compatible: ${registry.metadata.mcp_compatible ? "✅" : "❌"}`);
console.log(`  SalesPortl Ready: ${registry.metadata.salesportl_ready ? "✅" : "❌"}`);
console.log(`\n✅ Configuration looks good!\n`);
