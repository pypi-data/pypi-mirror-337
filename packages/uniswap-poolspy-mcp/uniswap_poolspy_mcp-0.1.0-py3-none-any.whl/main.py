from mcp.server.fastmcp import FastMCP
import httpx
import json
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Retrieve the API key from environment variables
API_KEY = os.getenv("THEGRAPH_API_KEY")
if not API_KEY:
    raise ValueError("THEGRAPH_API_KEY is not set in the .env file")
    
SUBGRAPH_URLS = {
    "ethereum": f"https://gateway.thegraph.com/api/{API_KEY}/subgraphs/id/5zvR82QoaXYFyDEKLZ9t6v9adgnptxYpKpSbxtgVENFV",
    "base": f"https://gateway.thegraph.com/api/{API_KEY}/subgraphs/id/GqzP4Xaehti8KSfQmv3ZctFSjnSUYZ4En5NRsiTbvZpz",
    "optimism": f"https://gateway.thegraph.com/api/{API_KEY}/subgraphs/id/Cghf4LfVqPiFw6fp6Y5X5Ubc8UpmUhSfJL82zwiBFLaj",
    "arbitrum": f"https://gateway.thegraph.com/api/{API_KEY}/subgraphs/id/FbCGRftH4a3yZugY7TnbYgPJVEv2LvMT6oF1fxPe9aJM",
    "polygon": f"https://gateway.thegraph.com/api/{API_KEY}/subgraphs/id/3hCPRGf4z88VC5rsBKU5AA9FBBq5nF3jbKJG7VZCbhjm",
    "bsc": f"https://gateway.thegraph.com/api/{API_KEY}/subgraphs/id/A1fvJWQLBeUAggX2WQTMm3FKjXTekNXo77ZySun4YN2m",
    "avalanche": f"https://gateway.thegraph.com/api/{API_KEY}/subgraphs/id/GVH9h9KZ9CqheUEL93qMbq7QwgoBu32QXQDPR6bev4Eo",
    "celo": f"https://gateway.thegraph.com/api/{API_KEY}/subgraphs/id/ESdrTJ3twMwWVoQ1hUE2u7PugEHX3QkenudD6aXCkDQ4",
    "blast": f"https://gateway.thegraph.com/api/{API_KEY}/subgraphs/id/2LHovKznvo8YmKC9ZprPjsYAZDCc4K5q4AYz8s3cnQn1",
}

ORDER_BY_OPTIONS = {
  "timestamp": "createdAtTimestamp",
  "txcount": "txCount",
  "volume": "volumeUSD",
  "tvl": "totalValueLockedUSD"
}

# Initialize the MCP server
mcp = FastMCP("Uniswap-PoolSpy")

# Async function to query the subgraph using httpx
async def query_subgraph(chain: str, query: str, variables: dict = None) -> dict:
    async with httpx.AsyncClient(timeout=10.0) as client:
        payload = {"query": query}
        if variables:
            payload["variables"] = variables
        response = await client.post(SUBGRAPH_URLS[chain], json=payload)
        if response.status_code != 200:
            raise Exception(f"Subgraph query failed with status {response.status_code}: {response.text}")
        result = response.json()
        if "errors" in result:
            raise Exception(f"GraphQL errors: {json.dumps(result['errors'], indent=2)}")
        return result

# Fetch recently created pools with a customizable time range and limit
async def fetch_recent_pools(chain: str, order_by:str, time_range_seconds: int, limit: int) -> list[dict]:
    time_ago = int((datetime.utcnow() - timedelta(seconds=time_range_seconds)).timestamp())
    order_by = ORDER_BY_OPTIONS[order_by]
    query = f"""
    query RecentPools($timestamp: BigInt!, $limit: Int!) {{
        pools(
            where: {{ createdAtTimestamp_gt: $timestamp }}
            orderBy: {order_by}
            orderDirection: desc
            first: $limit
        ) {{
            id
            token0 {{ symbol }}
            token1 {{ symbol }}
            createdAtTimestamp
            createdAtBlockNumber
            txCount
            volumeUSD
            totalValueLockedUSD
        }}
    }}
    """
    variables = {"timestamp": str(time_ago), "limit": limit}  # Convert timestamp to string for BigInt
    try:
        result = await query_subgraph(chain, query, variables)
        pools = result.get("data", {}).get("pools", [])
        if not pools:
            print(f"No pools found for timestamp > {time_ago}. Response: {json.dumps(result, indent=2)}")
        return pools
    except Exception as e:
        print(f"Error in fetch_recent_pools: {str(e)}")
        raise

# MCP Tool: List newly created trading pools
@mcp.tool()
async def get_new_pools(chain: str = "ethereum", order_by: str = "timestamp", time_range_seconds: int = 300, limit: int = 100) -> str:
    """
    Returns a list of trading pools created in the specified time range on Uniswap V3.

    Parameters:
        chain (str): The blockchain on which Uniswap is deployed. Default is 'ethereum'. Supported options include: 'ethereum', 'base', 'optimism', 'arbitrum', 'polygon', 'bsc', 'avalanche', 'celo' and 'blast'.
        order_by (str): The field to sort data in descending order before returning to the user. Default is 'timestamp'. Supported options include: 
          - timestamp: Sort by Timestamp
          - txcount: Sort by Transaction Count
          - tvl: Sort by Total Value Locked
          - volume: Sort by Volume 
        time_range_seconds (int): The time range in seconds to look back for new pools.
                                  Default is 300 seconds (5 minutes).
        limit (int): The maximum number of pools to return.
                     Default is 100 pools.
    """        
    try:
        chain = chain.lower()
        if chain not in SUBGRAPH_URLS:
            raise ValueError(f"Chain must be one of {list(SUBGRAPH_URLS.keys())}")
        order_by = order_by.lower()
        if order_by not in ORDER_BY_OPTIONS:
            raise ValueError(f"Order_by must be one of {list(ORDER_BY_OPTIONS.keys())}")
        
        pools = await fetch_recent_pools(chain, order_by, time_range_seconds=time_range_seconds, limit=limit)
        time_range_minutes = time_range_seconds // 60  # Convert to minutes for display
        output = f"Newly Created Trading Pools (Last {time_range_minutes} Minutes, Limit: {limit}):\n"
        for pool in pools:
            timestamp = datetime.fromtimestamp(int(pool["createdAtTimestamp"])).strftime('%Y-%m-%d %H:%M:%S')
            volume_usd = float(pool["volumeUSD"])  # Ensure float for formatting
            tvl_usd = float(pool["totalValueLockedUSD"])  # Ensure float for formatting
            output += (
                f"Pool Address: {pool['id']}\n"
                f"Tokens: {pool['token0']['symbol']}/{pool['token1']['symbol']}\n"
                f"Created At: {timestamp}\n"
                f"Block Number: {pool['createdAtBlockNumber']}\n"
                f"Transaction Count: {pool['txCount']}\n"
                f"Volume (USD): {volume_usd:.2f}\n"
                f"Total Value Locked (USD): {tvl_usd:.2f}\n\n"
            )
        return output if pools else f"No pools created in the last {time_range_minutes} minutes."
    except Exception as e:
        return f"Error fetching new pools: {str(e)}"

# Run the server
if __name__ == "__main__":
    mcp.run()
