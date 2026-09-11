# SALESPORTL MCP INTEGRATION GUIDE

## Quick Connect

Follow these steps to register SalesPortl-Agency-Skills-Suite-v01 with your SalesPortl instance:

---

## 1. Prerequisites

- SalesPortl instance running (accessible at your configured URL)
- Node.js 18+ installed
- This repository cloned locally

```bash
git clone https://github.com/danthamanvoiss/SalesPortl-Agency-Skills-Suite-v01.git
cd SalesPortl-Agency-Skills-Suite-v01
npm install
```

---

## 2. Create config.json

```bash
cp config.example.json config.json
```

Edit `config.json` with your SalesPortl details:

```json
{
  "salesportl": {
    "mcp_server": "https://your-salesportl-instance.com",
    "api_key": "YOUR_SALESPORTL_API_KEY",
    "workspace": "your-workspace-name"
  },
  "domains": {
    "sales": { "enabled": true },
    "marketing": { "enabled": true },
    "marketing-seo": { "enabled": true },
    "legal": { "enabled": true },
    "ads": { "enabled": true },
    "proposals": { "enabled": true },
    "reputation": { "enabled": true },
    "recruiting": { "enabled": true }
  }
}
```

---

## 3. SalesPortl MCP Connection Details

Add this to your **SalesPortl settings** → **Integrations** → **Add MCP Server**:

```json
{
  "name": "SalesPortl Agency Skills Suite",
  "type": "mcp",
  "protocol": "stdio",
  "command": "node",
  "args": [
    "scripts/mcp-server.js"
  ],
  "cwd": "/path/to/SalesPortl-Agency-Skills-Suite-v01",
  "env": {
    "SALESPORTL_API_KEY": "YOUR_API_KEY",
    "SALESPORTL_ENDPOINT": "https://your-salesportl-instance.com"
  }
}
```

---

## 4. Register Skills with SalesPortl

```bash
npm run register:salesportl
```

This will:
- ✅ Connect to your SalesPortl instance
- ✅ Read all domains from registry.json
- ✅ Generate .mcp.json tool definitions
- ✅ Register 280+ skills as callable MCP tools
- ✅ Return status report

**Output example:**
```
✅ Registering 280 skills across 14 domains...
  ✓ Sales (14 skills registered)
  ✓ Marketing (15 skills registered)
  ✓ Marketing-SEO (236 skills registered)
  ✓ Legal (14 skills registered)
  [... more domains ...]
✅ All skills registered successfully!
```

---

## 5. Verify Connection

```bash
node scripts/test-salesportl-connection.js
```

Expected output:
```
✅ Connected to SalesPortl
✅ 14 domains loaded
✅ 280 skills ready
✅ MCP server running on stdio
```

---

## 6. Start Using Skills in SalesPortl

Now all 280+ skills are available in your SalesPortl agent. Example usage in SalesPortl:

```
/sales prospect https://example.com
/marketing audit website
/legal review contract
/ads create campaign
```

---

## Environment Variables

You can also configure via environment variables instead of config.json:

```bash
export SALESPORTL_ENDPOINT="https://your-salesportl-instance.com"
export SALESPORTL_API_KEY="your-api-key"
export SALESPORTL_WORKSPACE="your-workspace"

npm run register:salesportl
```

---

## Troubleshooting

### Connection Failed

```bash
node scripts/test-salesportl-connection.js --verbose
```

Check:
- ✓ SalesPortl endpoint URL is correct
- ✓ API key is valid
- ✓ SalesPortl instance is running
- ✓ Firewall allows connection

### Skills Not Appearing

```bash
node scripts/list-skills.js
```

Re-register:
```bash
npm run register:salesportl -- --force
```

### Check Logs

```bash
node scripts/mcp-server.js --verbose
```

---

## Adding New Domains

See [ADDING-MODULES.md](../ADDING-MODULES.md) for step-by-step instructions.

After adding a new domain:
```bash
npm run register:salesportl
```

---

## API Reference

### Register Skills
```bash
POST /mcp/register
Body: { domains: ["sales", "marketing", ...] }
```

### Get Skill Status
```bash
GET /mcp/skills?domain=sales
```

### Execute Skill
```bash
POST /mcp/execute
Body: { skill: "skill-name", inputs: {...} }
```

---

## Support

- Issues: https://github.com/danthamanvoiss/SalesPortl-Agency-Skills-Suite-v01/issues
- Discussions: https://github.com/danthamanvoiss/SalesPortl-Agency-Skills-Suite-v01/discussions
