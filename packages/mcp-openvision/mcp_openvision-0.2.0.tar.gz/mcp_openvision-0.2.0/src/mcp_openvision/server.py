"""
OpenVision MCP Server

A simple MCP server that provides image analysis capabilities using OpenRouter.
"""

import base64
import json
import sys
import asyncio
import os
from pathlib import Path
import re
from typing import Dict, List, Optional, Any, Union
from urllib.parse import urlparse

import requests
from mcp.server.fastmcp import FastMCP
from mcp import types

from .config import VisionModel, get_api_key, get_default_model
from .exceptions import OpenRouterError, ConfigurationError

# Initialize FastMCP with dependencies
mcp = FastMCP(
    "OpenVision",
    description="Vision analysis tool for images using OpenRouter",
)


def encode_image_to_base64(image_data: bytes) -> str:
    """Encode image data to base64."""
    return base64.b64encode(image_data).decode("utf-8")


def is_url(string: str) -> bool:
    """
    Check if the provided string is a URL.

    Args:
        string: The string to check

    Returns:
        True if the string is a URL, False otherwise
    """
    try:
        result = urlparse(string)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False


def is_base64(string: str) -> bool:
    """
    Check if the provided string is base64-encoded.

    Args:
        string: The string to check

    Returns:
        True if the string appears to be base64-encoded, False otherwise
    """
    # Remove base64 URL prefix if present
    if string.startswith("data:image"):
        # Extract the actual base64 content
        pattern = r"base64,(.*)"
        match = re.search(pattern, string)
        if match:
            string = match.group(1)

    # Check if string is base64
    try:
        # Check if the string matches base64 pattern
        if not isinstance(string, str):
            return False

        # Check if the string follows base64 format (may have padding)
        # This regex allows for the standard base64 character set and optional padding
        if not re.match(r"^[A-Za-z0-9+/]*={0,2}$", string):
            return False

        # If it's too short, it's probably not base64
        if len(string) < 4:  # Minimum meaningful base64 is 4 chars
            return False

        # Try decoding - this will raise an exception if not valid base64
        decoded = base64.b64decode(string)
        # If we can decode it, it's likely base64
        return True
    except Exception:
        # If any exception occurs during decoding, it's not valid base64
        return False


def load_image_from_url(url: str) -> str:
    """
    Download an image from a URL and convert it to base64.

    Args:
        url: The URL of the image

    Returns:
        The image data as a base64-encoded string

    Raises:
        Exception: If the image cannot be downloaded
    """
    response = requests.get(url, stream=True)
    if response.status_code != 200:
        raise Exception(
            f"Failed to download image from URL: {url}, status code: {response.status_code}"
        )

    return encode_image_to_base64(response.content)


def load_image_from_path(path: str) -> str:
    """
    Load an image from a local file path and convert it to base64.

    Args:
        path: The path to the image file

    Returns:
        The image data as a base64-encoded string

    Raises:
        FileNotFoundError: If the image file does not exist
    """
    file_path = Path(path)
    if not file_path.exists():
        raise FileNotFoundError(f"Image file not found: {path}")

    with open(file_path, "rb") as f:
        return encode_image_to_base64(f.read())


def process_image_input(image: str) -> str:
    """
    Process the image input, which can be a URL, file path, or base64-encoded data.

    Args:
        image: The image input as a URL, file path, or base64-encoded data

    Returns:
        The image data as a base64-encoded string

    Raises:
        ValueError: If the image cannot be processed
    """
    # Check if the image is already base64-encoded
    if is_base64(image):
        return image

    # Check if the image is a URL
    if is_url(image):
        return load_image_from_url(image)

    # Check if the image is a file path
    try:
        return load_image_from_path(image)
    except FileNotFoundError:
        raise ValueError(
            f"Invalid image input: {image}. "
            f"Image must be a base64-encoded string, a URL, or a valid file path."
        )


@mcp.tool()
async def image_analysis(
    image: str,
    prompt: Optional[str] = None,
    messages: Optional[List[Dict[str, Any]]] = None,
    model: Optional[str] = None,
    max_tokens: int = 4000,
    temperature: float = 0.7,
    top_p: Optional[float] = None,
    presence_penalty: Optional[float] = None,
    frequency_penalty: Optional[float] = None,
) -> str:
    """
    Analyze an image using OpenRouter's vision capabilities.

    This tool allows you to send an image to OpenRouter's vision models for analysis.
    You can either provide a simple prompt or customize the full messages array for
    more control over the interaction.

    Args:
        image: The image as a base64-encoded string, URL, or local file path
        prompt: A simple text prompt for the analysis (ignored if messages is provided)
        messages: Optional custom messages array for the OpenRouter chat completions API
        model: The vision model to use (defaults to the value set by OPENROUTER_DEFAULT_MODEL)
        max_tokens: Maximum number of tokens in the response (100-4000)
        temperature: Temperature parameter for generation (0.0-1.0)
        top_p: Optional nucleus sampling parameter (0.0-1.0)
        presence_penalty: Optional penalty for new tokens based on presence in text so far (0.0-2.0)
        frequency_penalty: Optional penalty for new tokens based on frequency in text so far (0.0-2.0)

    Returns:
        The analysis result as text

    Examples:
        Basic usage with just a prompt and file path:
            image_analysis(image="path/to/image.jpg", prompt="Describe this image in detail")

        Basic usage with an image URL:
            image_analysis(image="https://example.com/image.jpg", prompt="Describe this image in detail")

        Advanced usage with custom messages:
            image_analysis(
                image="path/to/image.jpg",
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": "What objects can you see in this image?"},
                            {"type": "image_url", "image_url": {"url": "WILL_BE_REPLACED_WITH_IMAGE"}}
                        ]
                    }
                ]
            )
    """
    # Validate parameter constraints
    if max_tokens < 100 or max_tokens > 4000:
        raise ValueError("max_tokens must be between 100 and 4000")

    if temperature < 0.0 or temperature > 1.0:
        raise ValueError("temperature must be between 0.0 and 1.0")

    if top_p is not None and (top_p < 0.0 or top_p > 1.0):
        raise ValueError("top_p must be between 0.0 and 1.0")

    if presence_penalty is not None and (
        presence_penalty < 0.0 or presence_penalty > 2.0
    ):
        raise ValueError("presence_penalty must be between 0.0 and 2.0")

    if frequency_penalty is not None and (
        frequency_penalty < 0.0 or frequency_penalty > 2.0
    ):
        raise ValueError("frequency_penalty must be between 0.0 and 2.0")

    # Process the image input (URL, file path, or base64)
    try:
        base64_image = process_image_input(image)
    except Exception as e:
        raise ValueError(f"Failed to process image: {str(e)}")

    # If no model specified, use the default model from environment or fallback
    if model is None:
        selected_model = get_default_model()
        model_value = selected_model.value
    else:
        model_value = model

    # Get API key
    try:
        api_key = get_api_key()
    except ConfigurationError as e:
        raise

    print(f"Processing image with model: {model_value}")

    # Prepare messages for the OpenRouter request
    if messages is None:
        # Create default messages from prompt
        default_prompt = prompt or "Analyze this image in detail"
        messages = [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": default_prompt},
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"},
                    },
                ],
            }
        ]
    else:
        # Messages were provided - ensure the image is included
        image_added = False

        # Process each message
        for message in messages:
            if message.get("role") == "user":
                # Check if this message already has image content
                has_image = False
                if "content" in message and isinstance(message["content"], list):
                    for content_item in message["content"]:
                        if content_item.get("type") == "image_url":
                            # Replace any placeholder URLs with the actual image
                            if (
                                content_item.get("image_url", {}).get("url")
                                == "WILL_BE_REPLACED_WITH_IMAGE"
                            ):
                                content_item["image_url"][
                                    "url"
                                ] = f"data:image/jpeg;base64,{base64_image}"
                            has_image = True
                            image_added = True

                # If no image found, add it to the first user message
                if (
                    not has_image
                    and "content" in message
                    and isinstance(message["content"], list)
                ):
                    message["content"].append(
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}"
                            },
                        }
                    )
                    image_added = True
                    break

        # If no user message with content list was found, add a new one with the image
        if not image_added:
            # Use the prompt if provided, or a default
            text_content = prompt or "Analyze this image"
            messages.append(
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": text_content},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}"
                            },
                        },
                    ],
                }
            )

    # Prepare OpenRouter request
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://github.com/modelcontextprotocol/mcp-openvision",
        "X-Title": "MCP OpenVision",
    }

    # Start with required parameters
    payload = {
        "model": model_value,
        "messages": messages,
        "max_tokens": max_tokens,
        "temperature": temperature,
    }

    # Add optional parameters if provided
    if top_p is not None:
        payload["top_p"] = top_p

    if presence_penalty is not None:
        payload["presence_penalty"] = presence_penalty

    if frequency_penalty is not None:
        payload["frequency_penalty"] = frequency_penalty

    print("Sending request to OpenRouter...")

    try:
        # Make the API call
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            json=payload,
        )

        # Check for errors
        if response.status_code != 200:
            error_msg = (
                f"Error from OpenRouter: {response.status_code} - {response.text}"
            )
            print(error_msg)
            raise OpenRouterError(response.status_code, response.text)

        # Parse the response
        result = response.json()
        analysis = result["choices"][0]["message"]["content"]

        print("Analysis completed successfully")

        return analysis

    except requests.RequestException as e:
        error_msg = f"Network error when connecting to OpenRouter: {str(e)}"
        print(error_msg)
        raise OpenRouterError(0, error_msg)
    except json.JSONDecodeError as e:
        error_msg = f"Error parsing OpenRouter response: {str(e)}"
        print(error_msg)
        raise OpenRouterError(0, error_msg)


def main():
    """Run the MCP server."""
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    mcp.run()
