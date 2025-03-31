## MCP Server for DanchoiCloud

[![Release](https://github.com/hoangndst/mcp-server-danchoicloud/actions/workflows/release.yaml/badge.svg)](https://github.com/hoangndst/mcp-server-danchoicloud/actions/workflows/release.yaml)
[![GitHub release](https://img.shields.io/github/release/hoangndst/mcp-server-danchoicloud.svg)](https://github.com/hoangndst/mcp-server-danchoicloud/releases)
![PyPI - Version](https://img.shields.io/pypi/v/mcp-server-danchoicloud)
![Docker Image Version](https://img.shields.io/docker/v/hoangndst/mcp-server-danchoicloud)

### Description

MCP Server Danchoicloud: Check out my blog at [@hoangndst](https://hoangndst.com/blog/model-context-protocol).
### Configuration

#### 1. With Continue:

- Linux: `/home/$USER/.continue/config.yaml`
  ```yaml
  mcpServers:
    - name: danchoicloud
      command: /usr/bin/docker
      args:
        - run
        - -i
        - --rm
        - hoangndst/mcp-server-danchoicloud:${VERSION}
  ```

#### 2. With Cursor:

- Linux: `/home/$USER/.cursor/mcp.json`
  ```json
  {
    "mcpServers": {
      "danchoicloud": {
        "command": "docker",
        "args": ["run", "-i", "--rm", "hoangndst/mcp-server-danchoicloud:${VERSION}"]
      }
    }
  }
  ```

#### 3. With Claude for Desktop:

- macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
- Windows: `%APPDATA%\Claude\claude_desktop_config.json`
- Linux: `/home/$USER/.config/Claude/claude_desktop_config.json` (try to
  install [Claude Desktop for Linux](https://github.com/aaddrick/claude-desktop-debian))
  ```json
  {
    "mcpServers": {
      "danchoicloud": {
        "command": "docker",
        "args": ["run", "-i", "--rm", "hoangndst/mcp-server-danchoicloud:${VERSION}"]
      }
    }
  }
  ```

### Usage

<div align="center">
    <img
        id="figure-1"
        src="./assets/1.png"
        alt="Result from get_sieu_nhan from danchoicloud local server"
        style="width: 80%; max-width: 600px; height: auto; border-radius: 8px;"
    />
    <p>Figure 1: Result from <code>get_sieu_nhan</code> from <code>danchoicloud</code> local server</p>
</div>

### License

This MCP server is licensed under the MIT License. This means you are free to use, modify, and distribute the software,
subject to the terms and conditions of the MIT License. For more details, please see the LICENSE file in the project
repository.