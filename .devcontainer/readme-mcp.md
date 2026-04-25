在 Codespace 中运行 MCP 服务的说明：

- devcontainer 会在创建后运行 .devcontainer/start-mcp.js，这个脚本会读取 samples/mcp-configs/mcp-config.json 并启动 `context7` 与 `filesystem` 两个服务（使用 npx 调用各自包）。
- 确保仓库的 Codespaces secrets 包含任何需要的环境变量（例如 GITHUB_TOKEN），若需要请在 Codespaces 页面中注入。
- 转发端口：3000 (filesystem), 3001 (context7)。在 Codespaces 的 Ports 选项卡可查看/公开。
