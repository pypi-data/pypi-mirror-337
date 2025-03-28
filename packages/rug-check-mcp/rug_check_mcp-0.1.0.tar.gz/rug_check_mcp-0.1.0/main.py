import os
import json
import requests
from typing import Dict, Any
from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP

# Load environment variables from .env file
load_dotenv()

# Retrieve Solsniffer API key from environment variables
API_KEY = os.getenv("SOLSNIFFER_API_KEY")
if not API_KEY:
    raise ValueError("SOLSNIFFER_API_KEY not found in environment variables")

# Solsniffer API configuration
BASE_URL = "https://solsniffer.com/api/v2/token"

# Create an MCP server instance
mcp = FastMCP("Rug Check MCP")

def fetch_token_data(token_address: str) -> Dict:
    """Fetch token data from Solsniffer API."""
    headers = {"X-API-KEY": API_KEY, "accept": "application/json"}
    response = requests.get(f"{BASE_URL}/{token_address}", headers=headers)
    if response.status_code == 200:
        return response.json()
    raise Exception(f"API request failed: {response.status_code} - {response.text}")

@mcp.tool()
def analysis_token(token_address: str) -> Dict[str, Any]:
    """
    Analyze Solana token data using the Solsniffer API and return structured results.

    Args:
        token_address (str): The Solana token contract address to analyze (e.g., "9VxExA1iRPbuLLdSJ2rB3nyBxsyLReT4aqzZBMaBaY1p").
            Must be a valid Solana public key or token address.

    Returns:
        Dict[str, Any]: A dictionary containing the token analysis with the following structure:
            - token_address (str): The analyzed token's contract address.
            - token_name (str): The name of the token (e.g., "REVSHARE").
            - token_symbol (str): The token's symbol (e.g., "REVS").
            - snif_score (int): Solsniffer risk score (0-100, higher indicates lower risk).
            - market_cap (float): Market capitalization in USD.
            - price (float): Current price per token in USD.
            - supply_amount (float): Total supply of the token in circulation.
            - risks (dict): Risk assessment categorized by severity:
                - high (dict): High-risk indicators.
                    - count (int): Number of high-risk issues detected.
                    - details (dict): Dictionary of high-risk factors with boolean values (e.g., {"Mintable risks found": True}).
                - moderate (dict): Moderate-risk indicators.
                    - count (int): Number of moderate-risk issues detected.
                    - details (dict): Dictionary of moderate-risk factors with boolean values.
                - low (dict): Low-risk indicators.
                    - count (int): Number of low-risk issues detected.
                    - details (dict): Dictionary of low-risk factors with boolean values.
            - audit_risk (dict): Audit-related risk factors:
                - mint_disabled (bool): True if minting authority is disabled.
                - freeze_disabled (bool): True if freeze authority is disabled.
                - lp_burned (bool): True if liquidity pool tokens are burned.
                - top_10_holders_significant (bool): True if the top 10 holders control a significant share.

    Raises:
        Exception: If the Solsniffer API request fails (e.g., due to an invalid token address, network issues, or API key errors).
    """
    # Fetch raw data from Solsniffer API
    data = fetch_token_data(token_address)
    token_data = data["tokenData"]
    token_info = data["tokenInfo"]

    # Parse risk details from JSON strings
    high_risks = json.loads(token_data["indicatorData"]["high"]["details"])
    moderate_risks = json.loads(token_data["indicatorData"]["moderate"]["details"])
    low_risks = json.loads(token_data["indicatorData"]["low"]["details"])

    # Structure the analysis result
    result = {
        "token_address": token_data["tokenOverview"]["address"],
        "token_name": token_data["tokenName"],
        "token_symbol": token_data["tokenSymbol"],
        "snif_score": token_data["score"],
        "market_cap": token_info["mktCap"],
        "price": float(token_info["price"]),
        "supply_amount": token_info["supplyAmount"],
        "risks": {
            "high": {
                "count": token_data["indicatorData"]["high"]["count"],
                "details": high_risks
            },
            "moderate": {
                "count": token_data["indicatorData"]["moderate"]["count"],
                "details": moderate_risks
            },
            "low": {
                "count": token_data["indicatorData"]["low"]["count"],
                "details": low_risks
            }
        },
        "audit_risk": {
            "mint_disabled": token_data["auditRisk"]["mintDisabled"],
            "freeze_disabled": token_data["auditRisk"]["freezeDisabled"],
            "lp_burned": token_data["auditRisk"]["lpBurned"],
            "top_10_holders_significant": token_data["auditRisk"]["top10Holders"]
        }
    }
    return result

# Run the server if this file is executed directly
if __name__ == "__main__":
    mcp.run()
