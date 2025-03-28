import os
import requests
import json
from typing import Optional, Dict, Any
from mcp.server.fastmcp import FastMCP
from dotenv import load_dotenv

load_dotenv()


SERP_API_KEY = os.getenv("SERP_API_KEY")
if not SERP_API_KEY:
    raise ValueError("SERP_API_KEY environment variable is required")


mcp = FastMCP("serp-geo-mcp")


BASE_URL = "https://serpapi.com/search.json"

def search_geo(params: Dict[str, Any], user_location: Optional[Dict[str, float]] = None) -> Dict[str, Any]:
    """Perform a geo-location based search using SerpApi."""
    try:
        search_params = {
            "api_key": SERP_API_KEY,
            "engine": "google_maps",  
            "q": params.get("q"),
            "hl": params.get("hl", "en"),
            "gl": params.get("gl", "us"),
            "google_domain": params.get("google_domain", "google.com"),
        }

     
        if user_location and "lat" in user_location and "lng" in user_location:
            search_params["lat"] = user_location["lat"]
            search_params["lng"] = user_location["lng"]
      
        elif params.get("location"):
            search_params["q"] = f"{params.get('q')} {params.get('location')}"
          
            if "location" in search_params:
                del search_params["location"]


        print(f"Sending request to: {BASE_URL} with params: {search_params}")
        
        response = requests.get(BASE_URL, params=search_params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        error_message = e.response.text if hasattr(e, 'response') and e.response else str(e)
        raise Exception(f"Serp API error: {error_message}")
    except Exception as e:
        raise Exception(f"Geo search error: {str(e)}")

def format_results(response: Dict[str, Any], query: str) -> str:
    """Format Serp API response into human-readable text."""
    output = []

    if "error" in response:
        return f"Error from SERP API: {response['error']}"

    output.append("Detailed Results: geo locations")
    output.append(f"title: {query}")
    if "local_results" in response:
        output.append(f"\nLocal Places:")
        for result in response["local_results"]:
            output.append(f"\nName: {result.get('title', 'No title')}")
            output.append(f"Address: {result.get('address', 'No address')}")
            if "rating" in result:
                output.append(f"Rating: {result['rating']}/5 ({result.get('reviews', 'No')} reviews)")
            if "hours" in result:
                output.append(f"Hours: {result['hours']}")
            if "phone" in result:
                output.append(f"Phone: {result['phone']}")
            if "website" in result:
                output.append(f"Website: {result['website']}")
            if "description" in result:
                output.append(f"Description: {result['description']}")
    
    elif "local_results" in response and isinstance(response["local_results"], dict):
        if "places" in response["local_results"]:
            output.append("\nLocal Places:")
            for place in response["local_results"]["places"]:
                output.append(f"\nName: {place.get('name', 'No name')}")
                output.append(f"Address: {place.get('address', 'No address')}")
                if "rating" in place:
                    output.append(f"Rating: {place['rating']}")
                if "reviews" in place:
                    output.append(f"Reviews: {place['reviews']}")
                if "type" in place:
                    output.append(f"Type: {place['type']}")
    
    elif "place_results" in response:
        result = response["place_results"]
        output.append(f"\nPlace Details:")
        output.append(f"Name: {result.get('title', 'No title')}")
        output.append(f"Address: {result.get('address', 'No address')}")
        if "rating" in result:
            output.append(f"Rating: {result['rating']}/5 ({result.get('reviews', 'No')} reviews)")
        if "phone" in result:
            output.append(f"Phone: {result['phone']}")
        if "website" in result:
            output.append(f"Website: {result['website']}")
        if "description" in result:
            output.append(f"Description: {result['description']}")
    
    elif "organic_results" in response:
        output.append("\nWeb Results:")
        for result in response["organic_results"]:
            output.append(f"\nTitle: {result.get('title', 'No title')}")
            output.append(f"URL: {result.get('link', 'No URL')}")
            if "snippet" in result:
                output.append(f"Snippet: {result['snippet']}")
    
    if "search_metadata" in response:
        if "status" in response["search_metadata"]:
            output.append(f"\nSearch Status: {response['search_metadata']['status']}")
        if "id" in response["search_metadata"]:
            output.append(f"Search ID: {response['search_metadata']['id']}")
    
    if len(output) <= 2: 
        output.append("\nNo results found. Try refining your search terms.")

    return "\n".join(output)

@mcp.tool(description="A geo-location based search tool using SerpApi for Google Maps.")
async def serp_geo_search(
    q: str,
    location: Optional[str] = None,
    hl: Optional[str] = "en",
    gl: Optional[str] = "us",
    google_domain: Optional[str] = "google.com",
    user_lat: Optional[float] = None,
    user_lng: Optional[float] = None
) -> Dict[str, Any]:
    """Search geo-locations using SerpApi's Google Maps engine."""
    params = {
        "q": q,
        "location": location,
        "hl": hl,
        "gl": gl,
        "google_domain": google_domain
    }

    user_location = None
    if user_lat is not None and user_lng is not None:
        user_location = {"lat": user_lat, "lng": user_lng}
    elif "near me" in q.lower() and (user_lat is None or user_lng is None):
        return {
            "content": [{"type": "text", "text": "Please turn on your location or provide coordinates to find results near you."}],
            "isError": True
        }

    try:
        response = search_geo(params, user_location)
        formatted_results = format_results(response, q)
        return {"content": [{"type": "text", "text": formatted_results}]}
    except Exception as e:
        return {"content": [{"type": "text", "text": str(e)}], "isError": True}

if __name__ == "__main__":
    print("Serp Geo MCP server running on stdio...")
    mcp.run()