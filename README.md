# Azure Wiki Search Server
This mcp server implements the MCP specification to allow AI agents to search on Azure wiki.

## Tools
* __search_wiki__

    Search Edge Wiki to find related material for {query}.
* __get_wiki_by_path__

    Get wiki content by provided path.

## Prerequest 
1. Install the [latest VS code](https://code.visualstudio.com/download).
2. Install the [GitHub Copilot](https://marketplace.visualstudio.com/items?itemName=GitHub.copilot) and [GitHub Copilot Chat](https://marketplace.visualstudio.com/items?itemName=GitHub.copilot-chat) extensions
3. Install Python 3.10 or higher.
4. Install uv.
    On Windows
    ```
    powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
    ```

    On Mac|Linux
    ```
    curl -LsSf https://astral.sh/uv/install.sh | sh
    ```
5. Prepare a Personal Access Token and make sure it's have permission to read wiki.

## Local Setup
1. Clone this repo.
    ```
    git clone https://github.com/coder-linping/azure-wiki-search-server.git 
    cd azure-wiki-search-server
    ```
2. Setup env.
    On Windows
    ```
    uv venv
    .venv/Scripts/activate
    ```

    On Mac | Linux
    ```
    uv venv
    source .venv/bin/activate
    ```
3. Configuration for VS Code

    For manual installation, add the following JSON block to your User Settings (JSON) file in VS Code. You can do this by pressing Ctrl + Shift + P and typing Preferences: Open User Settings (JSON).

    Optionally, you can add it to a file called .vscode/mcp.json in your workspace. This will allow you to share the configuration with others.

    ```
      "mcp": {
        "servers": {
          "edge_wiki": {
            "command": "uv",
            "args": [
                "--directory",
                "<absolute path to your cloned folder>",
                "run",
                "src/edge_wiki.py"
            ],
            "env": {
                "PAT": "Your personal access token",
                "ORG": "Your organization，default is microsoft",
                "PROJECT": "Your project, default is Edge"
            },
          }
        }
      }
    ```
