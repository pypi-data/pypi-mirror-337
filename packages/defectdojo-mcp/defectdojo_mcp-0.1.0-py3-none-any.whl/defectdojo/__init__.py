from typing import Any, Dict, List, Optional, Union
import httpx
import os
from mcp.server.fastmcp import FastMCP

# Initialize FastMCP server
mcp = FastMCP("defectdojo")

# Get configuration from environment variables
DD_API_BASE = os.environ.get("DEFECTDOJO_API_BASE", "")
DD_API_TOKEN = os.environ.get("DEFECTDOJO_API_TOKEN", "")

# Validation will be performed when client is actually used, not at import time
def validate_api_token(token):
    """Validate that an API token is provided."""
    if not token:
        raise ValueError("DEFECTDOJO_API_TOKEN environment variable must be set")
    return token


class DefectDojoClient:
    """Client for interacting with the DefectDojo API."""
    
    def __init__(self, base_url: str, api_token: str):
        """Initialize the DefectDojo API client.
        
        Args:
            base_url: Base URL for the DefectDojo API
            api_token: API token for authentication
        """
        self.base_url = base_url
        self.headers = {
            "Authorization": f"Token {api_token}",
            "Content-Type": "application/json"
        }
        self.client = httpx.AsyncClient(headers=self.headers)
    
    async def get_findings(self, filters: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Get findings with optional filters.
        
        Args:
            filters: Optional dictionary of filter parameters
            
        Returns:
            API response as a dictionary with pagination metadata
        """
        url = f"{self.base_url}/api/v2/findings/"
        params = filters or {}
        
        try:
            response = await self.client.get(url, params=params)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            return {"error": f"HTTP error: {e.response.status_code}", "details": e.response.text}
        except Exception as e:
            return {"error": f"Error fetching findings: {str(e)}"}
    
    async def search_findings(self, query: str, filters: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Search for findings using a text query.
        
        Args:
            query: Text to search for in findings
            filters: Optional additional filter parameters
            
        Returns:
            API response as a dictionary
        """
        url = f"{self.base_url}/api/v2/findings/"
        params = filters or {}
        params["search"] = query
        
        try:
            response = await self.client.get(url, params=params)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            return {"error": f"HTTP error: {e.response.status_code}", "details": e.response.text}
        except Exception as e:
            return {"error": f"Error searching findings: {str(e)}"}
    
    async def update_finding(self, finding_id: int, data: Dict[str, Any]) -> Dict[str, Any]:
        """Update a finding by ID.
        
        Args:
            finding_id: ID of the finding to update
            data: Dictionary of fields to update
            
        Returns:
            API response as a dictionary
        """
        url = f"{self.base_url}/api/v2/findings/{finding_id}/"
        
        try:
            response = await self.client.patch(url, json=data)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            return {"error": f"HTTP error: {e.response.status_code}", "details": e.response.text}
        except Exception as e:
            return {"error": f"Error updating finding: {str(e)}"}
    
    async def add_note_to_finding(self, finding_id: int, note: str) -> Dict[str, Any]:
        """Add a note to a finding.
        
        Args:
            finding_id: ID of the finding to add a note to
            note: Text content of the note
            
        Returns:
            API response as a dictionary
        """
        url = f"{self.base_url}/api/v2/notes/"
        data = {
            "entry": note,
            "finding": finding_id
        }
        
        try:
            response = await self.client.post(url, json=data)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            return {"error": f"HTTP error: {e.response.status_code}", "details": e.response.text}
        except Exception as e:
            return {"error": f"Error adding note: {str(e)}"}
    
    async def create_finding(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new finding.
        
        Args:
            data: Dictionary containing finding details
            
        Returns:
            API response as a dictionary
        """
        url = f"{self.base_url}/api/v2/findings/"
        
        try:
            response = await self.client.post(url, json=data)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            return {"error": f"HTTP error: {e.response.status_code}", "details": e.response.text}
        except Exception as e:
            return {"error": f"Error creating finding: {str(e)}"}
    
    async def get_products(self, filters: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Get products with optional filters.
        
        Args:
            filters: Optional dictionary of filter parameters
            
        Returns:
            API response as a dictionary with pagination metadata
        """
        url = f"{self.base_url}/api/v2/products/"
        params = filters or {}
        
        try:
            response = await self.client.get(url, params=params)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            return {"error": f"HTTP error: {e.response.status_code}", "details": e.response.text}
        except Exception as e:
            return {"error": f"Error fetching products: {str(e)}"}
            
    async def get_engagements(self, filters: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Get engagements with optional filters.
        
        Args:
            filters: Optional dictionary of filter parameters
            
        Returns:
            API response as a dictionary with pagination metadata
        """
        url = f"{self.base_url}/api/v2/engagements/"
        params = filters or {}
        
        try:
            response = await self.client.get(url, params=params)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            return {"error": f"HTTP error: {e.response.status_code}", "details": e.response.text}
        except Exception as e:
            return {"error": f"Error fetching engagements: {str(e)}"}
    
    async def get_engagement(self, engagement_id: int) -> Dict[str, Any]:
        """Get a specific engagement by ID.
        
        Args:
            engagement_id: ID of the engagement to retrieve
            
        Returns:
            API response as a dictionary
        """
        url = f"{self.base_url}/api/v2/engagements/{engagement_id}/"
        
        try:
            response = await self.client.get(url)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            return {"error": f"HTTP error: {e.response.status_code}", "details": e.response.text}
        except Exception as e:
            return {"error": f"Error fetching engagement: {str(e)}"}
    
    async def create_engagement(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new engagement.
        
        Args:
            data: Dictionary containing engagement details
            
        Returns:
            API response as a dictionary
        """
        url = f"{self.base_url}/api/v2/engagements/"
        
        try:
            response = await self.client.post(url, json=data)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            return {"error": f"HTTP error: {e.response.status_code}", "details": e.response.text}
        except Exception as e:
            return {"error": f"Error creating engagement: {str(e)}"}
    
    async def update_engagement(self, engagement_id: int, data: Dict[str, Any]) -> Dict[str, Any]:
        """Update an existing engagement.
        
        Args:
            engagement_id: ID of the engagement to update
            data: Dictionary containing fields to update
            
        Returns:
            API response as a dictionary
        """
        url = f"{self.base_url}/api/v2/engagements/{engagement_id}/"
        
        try:
            response = await self.client.patch(url, json=data)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            return {"error": f"HTTP error: {e.response.status_code}", "details": e.response.text}
        except Exception as e:
            return {"error": f"Error updating engagement: {str(e)}"}


# Create a function to get the client when needed
def get_client(validate_token=True, base_url=None, token=None):
    """Get a configured DefectDojo client.
    
    Args:
        validate_token: Whether to validate that the token is set (default: True)
        base_url: Optional base URL override for testing
        token: Optional token override for testing
        
    Returns:
        A configured DefectDojoClient instance
        
    Raises:
        ValueError: If DEFECTDOJO_API_TOKEN environment variable is not set and validate_token is True
    """
    # Use provided values or get from environment
    actual_token = token if token is not None else os.environ.get("DEFECTDOJO_API_TOKEN", "")
    actual_base_url = base_url if base_url is not None else os.environ.get(
        "DEFECTDOJO_API_BASE", 
        "https://defectdojo.shared.linearft.tools"
    )
    
    # Only validate if requested (skipped for tests)
    if validate_token and not actual_token:
        raise ValueError("DEFECTDOJO_API_TOKEN environment variable must be set")
    
    return DefectDojoClient(actual_base_url, actual_token)


@mcp.tool(
    name="get_findings",
    description="Get findings with filtering options and pagination support"
)
async def get_findings(product_name: Optional[str] = None, status: Optional[str] = None, 
                       severity: Optional[str] = None, limit: int = 20, 
                       offset: int = 0) -> Dict[str, Any]:
    """Get findings with optional filters and pagination.
    
    Args:
        product_name: Optional product name filter
        status: Optional status filter
        severity: Optional severity filter
        limit: Maximum number of findings to return per page (default: 20)
        offset: Number of records to skip (default: 0)
        
    Returns:
        Dictionary with status, data/error, and pagination metadata
    """
    filters = {}
    if product_name:
        filters["product_name"] = product_name
    if status:
        filters["status"] = status
    if severity:
        filters["severity"] = severity
    if limit:
        filters["limit"] = limit
    if offset:
        filters["offset"] = offset
    
    client = get_client()
    result = await client.get_findings(filters)
    
    if "error" in result:
        return {"status": "error", "error": result["error"], "details": result.get("details", "")}
    
    return {"status": "success", "data": result}


@mcp.tool(
    name="search_findings",
    description="Search for findings using a text query with pagination support"
)
async def search_findings(query: str, product_name: Optional[str] = None, 
                         status: Optional[str] = None, severity: Optional[str] = None, 
                         limit: int = 20, offset: int = 0) -> Dict[str, Any]:
    """Search for findings using a text query with pagination.
    
    Args:
        query: Text to search for in findings
        product_name: Optional product name filter
        status: Optional status filter
        severity: Optional severity filter
        limit: Maximum number of findings to return per page (default: 20)
        offset: Number of records to skip (default: 0)
        
    Returns:
        Dictionary with status, data/error, and pagination metadata
    """
    filters = {}
    if product_name:
        filters["product_name"] = product_name
    if status:
        filters["status"] = status
    if severity:
        filters["severity"] = severity
    if limit:
        filters["limit"] = limit
    if offset:
        filters["offset"] = offset
    
    client = get_client()
    result = await client.search_findings(query, filters)
    
    if "error" in result:
        return {"status": "error", "error": result["error"], "details": result.get("details", "")}
    
    return {"status": "success", "data": result}


@mcp.tool(
    name="update_finding_status",
    description="Update the status of a finding (Active, Verified, False Positive, Mitigated, Inactive)"
)
async def update_finding_status(finding_id: int, status: str) -> Dict[str, Any]:
    """Update the status of a finding.
    
    Args:
        finding_id: ID of the finding to update
        status: New status for the finding
        
    Returns:
        Dictionary with status and data/error
    """
    data = {"active": True}  # Default to active
    
    # Map common status values to API fields
    status_lower = status.lower()
    if status_lower == "false positive":
        data["false_p"] = True
    elif status_lower == "verified":
        data["verified"] = True
    elif status_lower == "mitigated":
        data["active"] = False
        data["mitigated"] = True
    elif status_lower == "inactive":
        data["active"] = False
    elif status_lower != "active":
        return {"status": "error", "error": f"Unsupported status: {status}"}
    
    client = get_client()
    result = await client.update_finding(finding_id, data)
    
    if "error" in result:
        return {"status": "error", "error": result["error"], "details": result.get("details", "")}
    
    return {"status": "success", "data": result}


@mcp.tool(
    name="add_finding_note",
    description="Add a note to a finding"
)
async def add_finding_note(finding_id: int, note: str) -> Dict[str, Any]:
    """Add a note to a finding.
    
    Args:
        finding_id: ID of the finding to add a note to
        note: Text content of the note
        
    Returns:
        Dictionary with status and data/error
    """
    if not note.strip():
        return {"status": "error", "error": "Note content cannot be empty"}
    
    client = get_client()
    result = await client.add_note_to_finding(finding_id, note)
    
    if "error" in result:
        return {"status": "error", "error": result["error"], "details": result.get("details", "")}
    
    return {"status": "success", "data": result}


@mcp.tool(
    name="create_finding",
    description="Create a new finding"
)
async def create_finding(title: str, test_id: int, severity: str, description: str, 
                        cwe: Optional[int] = None, cvssv3: Optional[str] = None,
                        mitigation: Optional[str] = None, impact: Optional[str] = None,
                        steps_to_reproduce: Optional[str] = None) -> Dict[str, Any]:
    """Create a new finding.
    
    Args:
        title: Title of the finding
        test_id: ID of the test to associate the finding with
        severity: Severity level (Critical, High, Medium, Low, Informational)
        description: Description of the finding
        cwe: Optional CWE identifier
        cvssv3: Optional CVSS v3 score
        mitigation: Optional mitigation steps
        impact: Optional impact description
        steps_to_reproduce: Optional steps to reproduce
        
    Returns:
        Dictionary with status and data/error
    """
    # Validate severity
    valid_severities = ["critical", "high", "medium", "low", "informational"]
    if severity.lower() not in valid_severities:
        return {"status": "error", "error": f"Invalid severity. Must be one of: {', '.join(valid_severities)}"}
    
    data = {
        "title": title,
        "test": test_id,
        "severity": severity.capitalize(),
        "description": description,
    }
    
    # Add optional fields if provided
    if cwe is not None:
        data["cwe"] = cwe
    if cvssv3:
        data["cvssv3"] = cvssv3
    if mitigation:
        data["mitigation"] = mitigation
    if impact:
        data["impact"] = impact
    if steps_to_reproduce:
        data["steps_to_reproduce"] = steps_to_reproduce
    
    client = get_client()
    result = await client.create_finding(data)
    
    if "error" in result:
        return {"status": "error", "error": result["error"], "details": result.get("details", "")}
    
    return {"status": "success", "data": result}


@mcp.tool(
    name="list_products",
    description="List all products with optional filtering and pagination support"
)
async def list_products(name: Optional[str] = None, prod_type: Optional[int] = None, 
                       limit: int = 50, offset: int = 0) -> Dict[str, Any]:
    """List all products with optional filtering and pagination.
    
    Args:
        name: Optional name filter (partial match)
        prod_type: Optional product type ID filter
        limit: Maximum number of products to return per page (default: 50)
        offset: Number of records to skip (default: 0)
        
    Returns:
        Dictionary with status, data/error, and pagination metadata
    """
    filters = {"limit": limit}
    if name:
        filters["name__icontains"] = name
    if prod_type:
        filters["prod_type"] = prod_type
    if offset:
        filters["offset"] = offset
    
    client = get_client()
    result = await client.get_products(filters)
    
    if "error" in result:
        return {"status": "error", "error": result["error"], "details": result.get("details", "")}
    
    return {"status": "success", "data": result}


@mcp.tool(
    name="list_engagements",
    description="List engagements with optional filtering and pagination support"
)
async def list_engagements(product_id: Optional[int] = None, 
                          status: Optional[str] = None, 
                          name: Optional[str] = None,
                          limit: int = 20, offset: int = 0) -> Dict[str, Any]:
    """List engagements with optional filtering and pagination.
    
    Args:
        product_id: Optional product ID filter
        status: Optional status filter (Active, Completed)
        name: Optional name filter (partial match)
        limit: Maximum number of engagements to return per page (default: 20)
        offset: Number of records to skip (default: 0)
        
    Returns:
        Dictionary with status, data/error, and pagination metadata
    """
    filters = {"limit": limit}
    if product_id:
        filters["product"] = product_id
    if status:
        filters["status"] = status
    if name:
        filters["name__icontains"] = name
    if offset:
        filters["offset"] = offset
    
    client = get_client()
    result = await client.get_engagements(filters)
    
    if "error" in result:
        return {"status": "error", "error": result["error"], "details": result.get("details", "")}
    
    return {"status": "success", "data": result}


@mcp.tool(
    name="get_engagement",
    description="Get a specific engagement by ID"
)
async def get_engagement(engagement_id: int) -> Dict[str, Any]:
    """Get a specific engagement by ID.
    
    Args:
        engagement_id: ID of the engagement to retrieve
        
    Returns:
        Dictionary with status and data/error
    """
    client = get_client()
    result = await client.get_engagement(engagement_id)
    
    if "error" in result:
        return {"status": "error", "error": result["error"], "details": result.get("details", "")}
    
    return {"status": "success", "data": result}


@mcp.tool(
    name="create_engagement",
    description="Create a new engagement"
)
async def create_engagement(product_id: int, name: str, 
                           start_date: str, end_date: Optional[str] = None,
                           status: str = "Active", 
                           description: Optional[str] = None) -> Dict[str, Any]:
    """Create a new engagement.
    
    Args:
        product_id: ID of the product to associate the engagement with
        name: Name of the engagement
        start_date: Start date in YYYY-MM-DD format
        end_date: Optional end date in YYYY-MM-DD format
        status: Status of the engagement (default: Active)
        description: Optional description
        
    Returns:
        Dictionary with status and data/error
    """
    # Validate status
    valid_statuses = ["active", "completed"]
    if status.lower() not in valid_statuses:
        return {"status": "error", "error": f"Invalid status. Must be one of: {', '.join(valid_statuses)}"}
    
    # Prepare data payload
    data = {
        "product": product_id,
        "name": name,
        "target_start": start_date,
        "status": status.capitalize()
    }
    
    # Add optional fields
    if end_date:
        data["target_end"] = end_date
    if description:
        data["description"] = description
    
    client = get_client()
    result = await client.create_engagement(data)
    
    if "error" in result:
        return {"status": "error", "error": result["error"], "details": result.get("details", "")}
    
    return {"status": "success", "data": result}


@mcp.tool(
    name="update_engagement",
    description="Update an existing engagement"
)
async def update_engagement(engagement_id: int, name: Optional[str] = None,
                           start_date: Optional[str] = None, 
                           end_date: Optional[str] = None,
                           status: Optional[str] = None, 
                           description: Optional[str] = None) -> Dict[str, Any]:
    """Update an existing engagement.
    
    Args:
        engagement_id: ID of the engagement to update
        name: Optional new name
        start_date: Optional new start date in YYYY-MM-DD format
        end_date: Optional new end date in YYYY-MM-DD format
        status: Optional new status (Active, Completed)
        description: Optional new description
        
    Returns:
        Dictionary with status and data/error
    """
    # Validate status if provided
    if status:
        valid_statuses = ["active", "completed"]
        if status.lower() not in valid_statuses:
            return {"status": "error", "error": f"Invalid status. Must be one of: {', '.join(valid_statuses)}"}
    
    # Prepare data payload with only provided fields
    data = {}
    if name:
        data["name"] = name
    if start_date:
        data["target_start"] = start_date
    if end_date:
        data["target_end"] = end_date
    if status:
        data["status"] = status.capitalize()
    if description:
        data["description"] = description
    
    # If no fields were provided, return an error
    if not data:
        return {"status": "error", "error": "At least one field must be provided for update"}
    
    client = get_client()
    result = await client.update_engagement(engagement_id, data)
    
    if "error" in result:
        return {"status": "error", "error": result["error"], "details": result.get("details", "")}
    
    return {"status": "success", "data": result}


@mcp.tool(
    name="close_engagement",
    description="Close an engagement"
)
async def close_engagement(engagement_id: int) -> Dict[str, Any]:
    """Close an engagement by setting its status to completed.
    
    Args:
        engagement_id: ID of the engagement to close
        
    Returns:
        Dictionary with status and data/error
    """
    data = {
        "status": "Completed"
    }
    
    client = get_client()
    result = await client.update_engagement(engagement_id, data)
    
    if "error" in result:
        return {"status": "error", "error": result["error"], "details": result.get("details", "")}
    
    return {"status": "success", "data": result}


def main():
    """Initialize and run the MCP server."""
    print("Starting DefectDojo MCP server...")
    mcp.run(transport='stdio')

if __name__ == "__main__":
    # Initialize and run the server
    main()
