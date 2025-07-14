#!/usr/bin/env python
import os
import dotenv
import logging
import json
import time
from typing import Any, Dict, List, Optional, Union
from datetime import datetime, timedelta
from mcp.server.fastmcp import FastMCP
from sterling_b2b import SterlingB2B

# Configure logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("sterling_b2b_mcp_server")


def get_sb2b_client() -> SterlingB2B:
    """Get Sterling B2B client."""
    if dotenv.load_dotenv():
        logger.info("Environment configuration loaded: .env file")
    else:
        logger.info("Environment configuration loaded: No .env file found")

    host = os.getenv("B2BI_RESTAPI_URL", "")
    user = os.getenv("B2BI_USERNAME", "")
    pwd = os.getenv("B2BI_PASSWORD", "")

    if not host:
        logger.error("Missing required configuration: B2BI_RESTAPI_URL environment variable is not set.")
        raise ValueError("Missing required configuration: B2BI_RESTAPI_URL environment variable is not set.")

    if not user or not pwd:
        logger.error("Missing required configuration: B2BI_USERNAME or B2BI_PASSWORD environment variable is not set.")
        raise ValueError("Missing required configuration: B2BI_USERNAME or B2BI_PASSWORD environment variable is not set.")

    logger.info(f"Sterling B2Bi configuration validated host={host}, username={user}, password='XXXXXXX'")

    return SterlingB2B(host=host, username=user, password=pwd, verify_ssl=False)


# Initialize Sterling B2Bi client
sb2b = get_sb2b_client()

mcp = FastMCP("Sterling B2Bi MCP", port=8000, host="0.0.0.0")


@mcp.tool(description="List of all Trading Partners in Sterling B2Bi/Filegateway")
async def get_trading_partners() -> List[str]:
    """List of all Sterling B2Bi/Filegateway Trading Partners.

    Returns:
        List of trading partner IDs
    """
    logger.info("List Trading Partners")
    try:
        trading_partners = []
        items = sb2b.get_trading_partners()
        for item in items:
            trading_partners.append(item.get('_id'))
        return trading_partners
    except Error as e:
        logger.error(f"Failed to list trading partners: {str(e)}")
        return []


@mcp.tool(description="List of all Trading Partners with details in Sterling B2Bi/Filegateway")
async def get_trading_partners_with_details() -> List[Dict[str,Any]]:
    """List of all Sterling B2Bi/Filegateway Trading Partners and some details.

    Returns:
        List of trading partner IDs
    """
    logger.info("List Trading Partners")
    try:
        # trading_partners = []
        params = {
            '_range': '0-100',
            'searchFor': '',
            '_include': 'community,emailAddress,username,phone'  # Include additional fields as needed
        }
        # items = sb2b.get_trading_partners(params=params)
        # for item in items:
        #     trading_partners.append({
        #         'id': item.get('_id'), 
        #         'community': item.get('community'), 
        #         'emailAddress': item.get('emailAddress'),
        #         'username': item.get('username'),
        #         'phone': item.get('phone'),
        #         })
        return sb2b.get_trading_partners(params=params)
    except Error as e:
        logger.error(f"Failed to list trading partners: {str(e)}")
        return []

@mcp.tool(description="Get Trading Partners by ID")
async def get_trading_partner_by_id(trading_partner_id: str) -> Optional[Dict[str, Any]]:
    """Get a Trading Partner by ID.

    Args:
        trading_partner_id (str): The ID of the trading partner.

    Returns:
        Dict with trading partner details or None if not found.
    """
    logger.info(f"Get Trading Partner by ID: {trading_partner_id}")
    try:
        item = sb2b.get_trading_partner_by_id(trading_partner_id)
        if item:
            return item
        else:
            logger.warning(f"Trading Partner with ID {trading_partner_id} not found.")
            return None
    except Error as e:
        logger.error(f"Failed to get trading partner by ID: {str(e)}")
        return None

@mcp.tool(description="Get Communities in Sterling B2Bi/Filegateway")
async def get_communities() -> List[str]:
    """Get a list of all Communities in Sterling B2Bi/Filegateway.

    Returns:
        List of community IDs
    """
    logger.info("Get Communities")
    try:
        communities = []
        items = sb2b.get_communities()
        for item in items:
            communities.append(item.get('_id'))
        return communities
    except Error as e:
        logger.error(f"Failed to get communities: {str(e)}")
        return []

if __name__ == "__main__":
    logger.info("Starting Sterling B2Bi MCP Server")
    mcp.run(transport="sse")
    # Run the server with the stdio transport
    # mcp.run(transport="stdio")
