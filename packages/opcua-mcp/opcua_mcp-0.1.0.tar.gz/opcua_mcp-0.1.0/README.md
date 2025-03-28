# OPC UA MCP Server

An MCP server that connects to OPC UA-enabled industrial systems, allowing AI agents to monitor, analyze, and control operational data in real time.

This project is ideal for developers and engineers looking to bridge AI-driven workflows with industrial automation systems.

![GitHub License](https://img.shields.io/github/license/kukapay/opcua-mcp)
![Python Version](https://img.shields.io/badge/python-3.10+-blue)
![Status](https://img.shields.io/badge/status-active-brightgreen.svg)

## Features

- **Read OPC UA Nodes**: Retrieve real-time values from industrial devices.
- **Write to OPC UA Nodes**: Control devices by writing values to specified nodes.
- **Seamless Integration**: Works with MCP clients like Claude Desktop for natural language interaction.


### Tools
The server exposes two tools:
- **`read_opcua_node`**:
  - **Description**: Read the value of a specific OPC UA node.
  - **Parameters**:
    - `node_id` (str): OPC UA node ID (e.g., `ns=2;i=2`).
  - **Returns**: A string with the node ID and its value (e.g., "Node ns=2;i=2 value: 42").

- **`write_opcua_node`**:
  - **Description**: Write a value to a specific OPC UA node.
  - **Parameters**:
    - `node_id` (str): OPC UA node ID (e.g., `ns=2;i=3`).
    - `value` (str): Value to write (converted based on node type).
  - **Returns**: A success or error message (e.g., "Successfully wrote 100 to node ns=2;i=3").

### Example Prompts

- "What’s the value of node ns=2;i=2?" → Returns the current value.
- "Set node ns=2;i=3 to 100." → Writes 100 to the node.

## Installation

### Prerequisites
- Python 3.10 or higher
- An OPC UA server (e.g., a simulator or real industrial device)

### Install Dependencies
Clone the repository and install the required Python packages:

```bash
git clone https://github.com/kukapay/opcua-mcp.git
cd opcua-mcp
pip install asyncua mcp[cli]
```

### MCP Client Configuration

```json
{
 "mcpServers": {
   "opcua-mcp": {
     "command": "python",
     "args": ["path/to/opcua_mcp/main.py"],
     "env": {
        "OPCUA_SERVER_URL": "your-opc-ua-server-url"
     }
   }
 }
}
```


## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
