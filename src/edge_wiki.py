import json
import os
from azure.devops.connection import Connection
from azure.devops.v7_0.search.models import WikiSearchRequest
from msrest.authentication import BasicAuthentication
from mcp.server.fastmcp import FastMCP
from urllib.parse import unquote
from azure_token_manager import AzureTokenManager

mcp = FastMCP("edge_wiki")

org = os.getenv('ORG', 'microsoft')
project = os.getenv('PROJECT', 'Edge')

# Initialize the token manager instance
azure_token_manager = AzureTokenManager()

def get_connection() -> Connection:
    personal_access_token = azure_token_manager.get_access_token()
    if not personal_access_token:
        raise ValueError("No valid access token found. Please restart the server.")

    organization_url = f'https://dev.azure.com/{org}'
    credentials = BasicAuthentication('', personal_access_token)
    connection = Connection(base_url=organization_url, creds=credentials)
    return connection

def get_wiki_url(project_id: str, wiki_id: str, path: str) -> str:
    """ Construct the URL for the Edge Wiki page """
    correct_path = path.replace("-", "%20").replace(".md", "")
    return f'https://dev.azure.com/{org}/{project_id}/_wiki/wikis/{wiki_id}/?pagePath={correct_path}'

@mcp.prompt()
def start_edge_wiki_search() -> str:
    """ Prompt user for a search query to find Edge Wiki content"""

    return """
      You're an AI assistant for Microsoft Edge Wiki.

      Your task is to analyze the user's question and extract the relevant keywords to form a query. Ensure that words like "How to," "What is," and similar phrases are removed from the query.
      If the query does not work, please try simpifying the query to include keywords only and try again.

      Use this refined query to search for the relevant wiki entries using `search_wiki`.
      Once you obtain the wiki path from the search results, use it as is to retrieve the full wiki content using search_wiki_by_path. It is important to note that the path should not be decoded when it is URL-encoded.

      Answer the user's question based on the comprehensive information found in the wiki content. Include a reference to your sources by creating a link using the following format:
      "For more details, see [Filename](url)", where url is the 'url' field from the get_wiki_by_path response.
    """

@mcp.tool()
async def search_wiki(query: str) -> str:
    """ Search Edge Wiki to find related material for {query}"""

    try:
        search_client = get_connection().clients.get_search_client()

        search_request = WikiSearchRequest(search_text=query, top=500)
        result = search_client.fetch_wiki_search_results(request = search_request, project=project)

        return json.dumps([{
            'file_name': wiki.file_name,
            'path': wiki.path,
            'wiki_id': wiki.wiki.id,
            'url': get_wiki_url(wiki.project.id, wiki.wiki.id, wiki.path),
        } for wiki in result.results], indent=2)
    except Exception as e:
        return f"Error searching wiki: {str(e)}"

@mcp.tool()
async def get_wiki_by_path(path: str, wiki_id: str) -> str:
    """ Get Edge Wiki content by path returned from search_wiki"""

    wiki_client = get_connection().clients.get_wiki_client()

    # replace - with space and remove .md extension
    correct_path = path.replace("-", " ")
    if correct_path.endswith('.md'):
        correct_path = correct_path[:-3]

    correct_path = unquote(correct_path)
    result = wiki_client.get_page(project, wiki_identifier=wiki_id, path=correct_path, include_content=True)

    return json.dumps({
            'path': result.page.path,
            'content': result.page.content
    }, indent=2)

if __name__ == "__main__":
    # Initialize and run the server
    mcp.run(transport='stdio')

