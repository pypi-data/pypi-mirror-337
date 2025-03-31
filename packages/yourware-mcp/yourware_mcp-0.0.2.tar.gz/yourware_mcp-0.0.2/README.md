For production

```
{
  "mcpServers": {
    "yourware-mcp": {
      "command": "uvx",
      "args": ["yourware-mcp@latest", "stdio"],
      "env": {}
    }
  }
}
```

For staging

```
{
  "mcpServers": {
    "yourware-mcp": {
      "command": "uvx",
      "args": ["yourware-mcp@latest", "stdio"],
      "env": {
        "YOURWARE_ENDPOINT": "https://staging.yourware.so"
      }
    }
  }
}
```
