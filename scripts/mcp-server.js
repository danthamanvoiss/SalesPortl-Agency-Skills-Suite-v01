/**
 * MCP Server for SalesPortl Agency Skills Suite
 * Handles stdio transport for MCP protocol
 */

import fs from "fs";
import path from "path";
import readline from "readline";
import { fileURLToPath } from "url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const registryPath = path.join(__dirname, "../registry.json");

const registry = JSON.parse(fs.readFileSync(registryPath, "utf-8"));

const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout,
});

// MCP Server Protocol Handler
function handleRequest(request) {
  if (request.method === "resources/list") {
    return {
      resources: registry.domains.map((d) => ({
        uri: `salesportl://skill/${d.id}`,
        name: d.name,
        description: d.description,
        mimeType: "application/json",
      })),
    };
  }

  if (request.method === "tools/list") {
    const tools = [];
    registry.domains.forEach((domain) => {
      for (let i = 0; i < domain.skills_count; i++) {
        tools.push({
          name: `${domain.id}-skill-${i + 1}`,
          description: `${domain.name} - Skill ${i + 1}`,
          inputSchema: {
            type: "object",
            properties: {
              input: { type: "string" },
            },
          },
        });
      }
    });
    return { tools };
  }

  if (request.method === "tools/call") {
    return {
      content: [
        {
          type: "text",
          text: `Executed: ${request.params.name}`,
        },
      ],
    };
  }

  return { error: "Unknown method", method: request.method };
}

// Read requests from stdin
rl.on("line", (line) => {
  try {
    const request = JSON.parse(line);
    const response = handleRequest(request);
    console.log(JSON.stringify(response));
  } catch (err) {
    console.error(JSON.stringify({ error: err.message }));
  }
});

console.error(`[SalesPortl MCP Server] Ready - ${registry.metadata.total_skills} skills available`);
