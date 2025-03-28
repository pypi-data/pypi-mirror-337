import os
from typing import Any
import aiohttp
from mcp.server.fastmcp import FastMCP

# Initialize FastMCP server with dependencies
dep = ["aiohttp"]
mcp = FastMCP("wiz", dependencies=dep)

# Environment variables
USER = os.environ.get('KS_USER', 'admin')
BASE_URL = os.environ.get('KS_APISERVER_ENDPOINT', 'http://172.31.17.47:30881')
TOKEN = os.environ.get('KS_TOKEN', 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJodHRwOi8va3MtY29uc29sZS5rdWJlc3BoZXJlLXN5c3RlbS5zdmM6MzA4ODAiLCJzdWIiOiJhZG1pbiIsImV4cCI6MTc0MzE0NzkzNiwiaWF0IjoxNzQzMTQwNzM2LCJ0b2tlbl90eXBlIjoiYWNjZXNzX3Rva2VuIiwidXNlcm5hbWUiOiJhZG1pbiJ9.iW2_HWBcDVn7NNE_J1iyOpsG2T4cJZi3At80Rl9WtSw')

HEADERS = {
    "Accept": "application/json",
    "X-Remote-User": USER,
    "Authorization": f"Bearer {TOKEN}"
}

async def fetch_json(session: aiohttp.ClientSession, url: str) -> Any:
    async with session.get(url, headers=HEADERS) as response:
        return await response.json()

@mcp.tool()
async def get_logging(cluster: str, pod: str) -> Any:
    """Get logs and events
    Args:
        cluster: Cluster name
        pod: Pod name
    """
    url = f"{BASE_URL}/kapis/logging.kubesphere.io/v1alpha2/logs?cluster={cluster}&pods={pod}&size=30"
    async with aiohttp.ClientSession() as session:
        return await fetch_json(session, url)

@mcp.tool()
async def get_event(cluster: str, pod: str) -> Any:
    """Get logs and events
    Args:
        cluster: Cluster name
        pod: Pod name
    """
    url = f"{BASE_URL}/kapis/logging.kubesphere.io/v1alpha2/events?cluster={cluster}&involved_object_name_filter={pod}&size=30"
    async with aiohttp.ClientSession() as session:
        return await fetch_json(session, url)

@mcp.tool()
async def get_all_clusters() -> Any:
    """Get all clusters"""
    url = f"{BASE_URL}/kapis/tenant.kubesphere.io/v1beta1/clusters"
    async with aiohttp.ClientSession() as session:
        resp = await fetch_json(session, url)
        return [cluster['metadata']['name'] for cluster in resp['items']]

@mcp.tool()
async def get_all_pods(cluster: str) -> Any:
    """Get all pods in a cluster
    Args:
        cluster: Cluster name
    """
    url = f"{BASE_URL}/clusters/{cluster}/kapis/resources.kubesphere.io/v1alpha3/pods"
    async with aiohttp.ClientSession() as session:
        resp = await fetch_json(session, url)
        return [
            {
                "name": item['metadata']['name'],
                "status": item['status']['phase'],
                "namespace": item['metadata']['namespace']
            }
            for item in resp['items']
        ]

@mcp.tool()
async def get_all_namespaces(cluster: str) -> Any:
    """Get all namespaces in a cluster
    Args:
        cluster: Cluster name
    """
    url = f"{BASE_URL}/clusters/{cluster}/kapis/resources.kubesphere.io/v1alpha3/namespaces"
    async with aiohttp.ClientSession() as session:
        resp = await fetch_json(session, url)
        return [{"name": item['metadata']['name']} for item in resp['items']]


@mcp.prompt()
def analyse_special_cluster(cluster: str) -> str:
    """Analyse all clusters and provide report
    Args:
        cluster: Cluster name
    """
    return f"Please analyse the cluster {cluster} status and give me a report."

@mcp.prompt()
def analyse_all_cluster() -> Any:
    """Analyze all clusters and provide a summary report
    """
    return "Please analyse all cluster status and give me a report"

if __name__ == "__main__":
    # Initialize and run the server
    mcp.run(transport="stdio")