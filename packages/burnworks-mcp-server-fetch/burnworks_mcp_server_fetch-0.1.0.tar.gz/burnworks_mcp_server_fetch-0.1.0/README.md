# Fetch MCP Server with CSS selectors function

A Model Context Protocol server that provides web content fetching capabilities. This server enables LLMs to retrieve and process content from web pages, converting HTML to markdown for easier consumption.

The fetch tool will truncate the response, but by using the `start_index` argument, you can specify where to start the content extraction. This lets models read a webpage in chunks, until they find the information they need.

### Available Tools

- `custom-fetch` - Fetches a URL from the internet and extracts its contents as markdown.
    - `url` (string, required): URL to fetch
    - `max_length` (integer, optional): Maximum number of characters to return (default: 5000)
    - `start_index` (integer, optional): Start content from this character index (default: 0)
    - `raw` (boolean, optional): Get raw content without markdown conversion (default: false)
    - `selector` (string, optional): CSS selector, ID, or element name to extract specific content
    - `selector_type` (string, optional): Type of selector: 'css', 'id', or 'element'

### Prompts

- **custom-fetch**
  - Fetch a URL and extract its contents as markdown
  - Arguments:
    - `url` (string, required): URL to fetch
    - `selector` (string, optional): CSS selector, ID, or element name to extract specific content
    - `selector_type` (string, optional): Type of selector: 'css', 'id', or 'element'

## Selector Feature

This enhanced version includes a powerful selector feature that allows you to extract specific content from web pages:

### Types of Selectors

- **ID Selector**: Extract a specific element by its ID attribute
  ```json
  {
    "url": "https://example.com",
    "selector": "main-content",
    "selector_type": "id"
  }
  ```

- **Element Selector**: Extract the first element of a specific type
  ```json
  {
    "url": "https://example.com",
    "selector": "main",
    "selector_type": "element"
  }
  ```

- **CSS Selector**: Extract content using CSS selector syntax
  ```json
  {
    "url": "https://example.com",
    "selector": ".article-content > p",
    "selector_type": "css"
  }
  ```

### Use Cases

- Extract just the main article content from news sites
- Focus on specific sections of documentation pages
- Target precisely the content you need from large web pages

## Installation

Optionally: Install node.js, this will cause the fetch server to use a different HTML simplifier that is more robust.

### Using uv (recommended)

When using [`uv`](https://docs.astral.sh/uv/) no specific installation is needed. We will
use [`uvx`](https://docs.astral.sh/uv/guides/tools/) to directly run *burnworks-mcp-server-fetch*.

### Using PIP

Alternatively you can install `burnworks-mcp-server-fetch` via pip:

```
pip install burnworks-mcp-server-fetch
```

After installation, you can run it as a script using:

```
python -m burnworks_mcp_server_fetch
```

## Configuration

### Configure for Claude.app

Add to your Claude settings:

<details>
<summary>Using uvx</summary>

```json
"mcpServers": {
  "custom-fetch": {
    "command": "uvx",
    "args": ["burnworks-mcp-server-fetch"]
  }
}
```
</details>

<details>
<summary>Using pip installation</summary>

```json
"mcpServers": {
  "custom-fetch": {
    "command": "python",
    "args": ["-m", "burnworks_mcp_server_fetch"]
  }
}
```
</details>

### Customization - robots.txt

By default, the server will obey a websites robots.txt file if the request came from the model (via a tool), but not if
the request was user initiated (via a prompt). This can be disabled by adding the argument `--ignore-robots-txt` to the
`args` list in the configuration.

### Customization - User-agent

By default, depending on if the request came from the model (via a tool), or was user initiated (via a prompt), the
server will use either the user-agent
```
ModelContextProtocol/1.0 (Autonomous; +https://github.com/modelcontextprotocol/servers)
```
or
```
ModelContextProtocol/1.0 (User-Specified; +https://github.com/modelcontextprotocol/servers)
```

This can be customized by adding the argument `--user-agent=YourUserAgent` to the `args` list in the configuration.

### Customization - Proxy

The server can be configured to use a proxy by using the `--proxy-url` argument.

## Debugging

You can use the MCP inspector to debug the server. For uvx installations:

```
npx @modelcontextprotocol/inspector uvx burnworks-mcp-server-fetch
```

Or if you've installed the package in a specific directory or are developing on it:

```
cd path/to/servers/src/fetch
npx @modelcontextprotocol/inspector uv run burnworks-mcp-server-fetch
```

## Example Selector Usage

### Extract Just the Main Content Area

```
custom-fetch
  url: https://example.com/article
  selector: main
  selector_type: element
```

### Extract Content by ID

```
custom-fetch
  url: https://example.com/blog
  selector: article-body
  selector_type: id
```

### Extract with Complex CSS Selector

```
custom-fetch
  url: https://example.com/documentation
  selector: .content-wrapper article > section:first-child
  selector_type: css
```

## Contributing

This project, `burnworks_mcp_server_fetch,` was developed as a fork of the original mcp-server-fetch with added CSS selector functionality. The original project can be found at:

https://github.com/modelcontextprotocol/servers

If you'd like to contribute to this enhanced version, feel free to submit issues or pull requests to our repository. For information about the base MCP servers architecture and implementation patterns, please refer to the original project link above.

## License

This project is licensed under the MIT License. This means you are free to use, modify, and distribute the software, subject to the terms and conditions of the MIT License. For more details, please see the LICENSE file in the project repository.