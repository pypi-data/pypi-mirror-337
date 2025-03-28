from enum import StrEnum
from typing import Literal

import mcp.server.stdio
from mcp.server import NotificationOptions, Server
from mcp.server.models import InitializationOptions
from mcp.types import TextContent, Tool
from pydantic import BaseModel, Field

from .load import load_hch_service_general_info, load_hch_service_price_info

RES_SERVICE_OPTS = Literal[
    "Detail Cleaning",
    "Move In Cleaning",
    "Move Out Cleaning",
    "Post-Renovation Cleaning",
    "Spring Cleaning (Occupied Unit)",
    "Floor Cleaning or Floor Care",
    "Formaldehyde (VOC)",
    "Disinfecting",
    "Household Accessory Cleaning (e.g. Sofa, Mattress, Carpet, Curtains)",
    "Customised or Combination Cleaning",
]


COM_SERVICE_OPTS = Literal["Commercial Cleaning", "Placeholder Option"]


class HchTools(StrEnum):
    RES_SERVICE_GENERAL_INFO = "get_residential_service_general_info"
    RES_SERVICE_PRICE_INFO = "get_residential_service_price_info"
    RES_SERVICE_BOOKING_REQS = "get_residential_service_booking_requirements"
    COM_SERVICE_GENERAL_INFO = "get_commercial_service_general_info"
    COM_SERVICE_PRICE_INFO = "get_commercial_service_price_info"
    COM_SERVICE_BOOKING_REQS = "get_commercial_service_booking_requirements"


class HchGetResidentialServiceGeneralInfo(BaseModel):
    service: RES_SERVICE_OPTS = Field(
        description="Select a residential service option to obtain its general information."
    )


class HchGetResidentialServicePriceInfo(BaseModel):
    service: RES_SERVICE_OPTS = Field(
        description="Select a residential service option to obtain its price information.",
    )


class HchGetResidentialServiceBookingRequirements(BaseModel):
    service: RES_SERVICE_OPTS = Field(
        description="Select a residential service option to obtain its booking requirements.",
    )


class HchGetCommercialServiceGeneralInfo(BaseModel):
    service: COM_SERVICE_OPTS = Field(
        description="Select a commercial service option to obtain its general information.",
    )


class HchGetCommercialServicePriceInfo(BaseModel):
    service: COM_SERVICE_OPTS = Field(
        description="Select a commercial service option to obtain its price information.",
    )


class HchGetCommercialServiceBookingRequirements(BaseModel):
    service: COM_SERVICE_OPTS = Field(
        description="Select a commercial service option to obtain its booking requirements.",
    )


server = Server("home-clean-home")
service2general_info, service2booking_reqs = load_hch_service_general_info()
service2price_info = load_hch_service_price_info()


def get_residential_service_general_info(service: RES_SERVICE_OPTS) -> str:
    """Get service general information with respect to the user selected residential service.

    Args:
        service (RES_SERVICE_OPTS): Select a residential service option to obtain its general information.

    Returns:
        str: Service general information.
    """
    general_info = service2general_info.get(service, None)
    if not general_info:
        return f"No general information found for {service=}."

    return f"{'=' * 50}\n".join(general_info)


def get_residential_service_price_info(service: RES_SERVICE_OPTS) -> str:
    """Get service price information with respect to the user selected residential service.

    Args:
        service (RES_SERVICE_OPTS): Select a residential service option to obtain its price information.

    Returns:
        str: Service price information.
    """
    price_info = service2price_info.get(service, None)
    if not price_info:
        return f"No price information found for {service=}."

    return f"{'=' * 50}\n".join(price_info)


def get_residential_service_booking_requirements(service: RES_SERVICE_OPTS) -> str:
    """Get service booking requirements with respect to the user selected residential service.

    Args:
        service (RES_SERVICE_OPTS): Select a residential service option to obtain its booking requirements.

    Returns:
        str: Service booking requirements.
    """
    booking_reqs = service2booking_reqs.get(service, None)
    if not booking_reqs:
        return f"No booking requirements found for {service=}."

    return booking_reqs


def get_commercial_service_general_info(service: COM_SERVICE_OPTS) -> str:
    """Get service general information with respect to the user selected commercial service.

    Args:
        service (COM_SERVICE_OPTS): Select a commercial service option to obtain its general information.

    Returns:
        str: Service general information.
    """
    general_info = service2general_info.get(service, None)
    if not general_info:
        return f"No general information found for {service=}."

    return f"{'=' * 50}\n".join(general_info)


def get_commercial_service_price_info(service: COM_SERVICE_OPTS) -> str:
    """Get service price information with respect to the user selected commercial service.

    Args:
        service (COM_SERVICE_OPTS): Select a commerical service option to obtain its price information.

    Returns:
        str: Service price information.
    """
    price_info = service2price_info.get(service, None)
    if not price_info:
        return f"No price information found for {service=}."

    return f"{'=' * 50}\n".join(price_info)


def get_commercial_service_booking_requirements(service: COM_SERVICE_OPTS) -> str:
    """Get service booking requirements with respect to the user selected commercial service.

    Args:
        service (COM_SERVICE_OPTS): Select a commercial service option to obtain its booking requirements.

    Returns:
        str: Service booking requirements.
    """
    booking_reqs = service2booking_reqs.get(service, None)
    if not booking_reqs:
        return f"No booking requirements found for {service=}."

    return booking_reqs


@server.list_tools()
async def handle_list_tools() -> list[Tool]:
    """List available tools. Each tool specifies its arguments using JSON Schema validation.

    Returns:
        list[Tool]: A list of tools available for the server.
    """
    return [
        Tool(
            name=HchTools.RES_SERVICE_GENERAL_INFO,
            description="Get service general information with respect to the user selected residential service.",
            inputSchema=HchGetResidentialServiceGeneralInfo.model_json_schema(),
        ),
        Tool(
            name=HchTools.RES_SERVICE_PRICE_INFO,
            description="Get service price information with respect to the user selected residential service.",
            inputSchema=HchGetResidentialServicePriceInfo.model_json_schema(),
        ),
        Tool(
            name=HchTools.RES_SERVICE_BOOKING_REQS,
            description="Get service booking requirements with respect to the user selected residential service.",
            inputSchema=HchGetResidentialServiceBookingRequirements.model_json_schema(),
        ),
        Tool(
            name=HchTools.COM_SERVICE_GENERAL_INFO,
            description="Get service general information with respect to the user selected commercial service.",
            inputSchema=HchGetCommercialServiceGeneralInfo.model_json_schema(),
        ),
        Tool(
            name=HchTools.COM_SERVICE_PRICE_INFO,
            description="Get service price information with respect to the user selected commercial service.",
            inputSchema=HchGetCommercialServicePriceInfo.model_json_schema(),
        ),
        Tool(
            name=HchTools.COM_SERVICE_BOOKING_REQS,
            description="Get service booking requirements with respect to the user selected commercial service.",
            inputSchema=HchGetCommercialServiceBookingRequirements.model_json_schema(),
        ),
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    """Handle tool execution requests. Tools can modify server state and notify clients of changes.

    Args:
        name (str): Tool name.
        arguments (dict): Tool arguments.

    Returns:
        list[TextContent]: A list of text content to be sent to the client.
    """
    match name:
        case HchTools.RES_SERVICE_GENERAL_INFO:
            service = arguments["service"]
            service_details_info = get_residential_service_general_info(service)
            return [
                TextContent(
                    type="text",
                    text=f"{service_details_info}",
                )
            ]

        case HchTools.RES_SERVICE_PRICE_INFO:
            service = arguments["service"]
            price_info = get_residential_service_price_info(service)
            return [
                TextContent(
                    type="text",
                    text=f"{price_info}",
                )
            ]

        case HchTools.RES_SERVICE_BOOKING_REQS:
            service = arguments["service"]
            booking_reqs = get_residential_service_booking_requirements(service)
            return [
                TextContent(
                    type="text",
                    text=f"{booking_reqs}",
                )
            ]

        case HchTools.COM_SERVICE_GENERAL_INFO:
            service = arguments["service"]
            service_details_info = get_commercial_service_general_info(service)
            return [
                TextContent(
                    type="text",
                    text=f"{service_details_info}",
                )
            ]

        case HchTools.COM_SERVICE_PRICE_INFO:
            service = arguments["service"]
            price_info = get_commercial_service_price_info(service)
            return [
                TextContent(
                    type="text",
                    text=f"{price_info}",
                )
            ]

        case HchTools.COM_SERVICE_BOOKING_REQS:
            service = arguments["service"]
            booking_reqs = get_commercial_service_booking_requirements(service)
            return [
                TextContent(
                    type="text",
                    text=f"{booking_reqs}",
                )
            ]

        case _:
            raise ValueError(f"Unknown tool: {name}")


async def main():
    # Run the server using stdin/stdout streams
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="home-clean-home",
                server_version="0.1.0",
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                ),
            ),
        )
