"""Streamlit UI for device control"""

import asyncio
import base64
from io import BytesIO
from typing import Optional

import streamlit as st
from PIL import Image

from ..api import AnthropicClient
from ..tools import ToolCollection, ToolResult

# Page config
st.set_page_config(
    page_title="Mac & iOS Control",
    page_icon="🤖",
    layout="wide",
)

# Session state
if "client" not in st.session_state:
    tools = ToolCollection()
    st.session_state.client = AnthropicClient(
        tools=tools,
        on_content=lambda text: st.session_state.current_response.markdown(text),
        on_tool_result=lambda result: display_tool_result(result),
    )

def display_tool_result(result: ToolResult):
    """Display tool execution result"""
    container = st.session_state.current_response
    
    if result.error:
        container.error(result.error)
    
    if result.output:
        container.code(result.output)
        
    if result.base64_image:
        image = Image.open(BytesIO(base64.b64decode(result.base64_image)))
        container.image(image, use_column_width=True)

def main():
    st.title("Mac & iOS Control")
    
    # Chat interface
    chat_container = st.container()
    
    # Display message history
    for msg in st.session_state.client.messages:
        role = msg["role"]
        with chat_container.chat_message(role):
            if isinstance(msg["content"], str):
                st.markdown(msg["content"])
            elif isinstance(msg["content"], dict):
                if msg["content"].get("error"):
                    st.error(msg["content"]["error"])
                if msg["content"].get("output"):
                    st.code(msg["content"]["output"])
                if msg["content"].get("image"):
                    image = Image.open(BytesIO(base64.b64decode(msg["content"]["image"])))
                    st.image(image)

    # Input for new message
    if prompt := st.chat_input("Type your instructions..."):
        with chat_container.chat_message("user"):
            st.markdown(prompt)
            
        with chat_container.chat_message("assistant"):
            st.session_state.current_response = st
            asyncio.run(st.session_state.client.send_message(prompt))

if __name__ == "__main__":
    main() 