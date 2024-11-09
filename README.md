# Mac & iOS Anthropic Control

A tool that allows Claude to control Mac and iOS devices through the Anthropic API.

## Acknowledgments

This project builds upon and was inspired by the excellent [Anthropic Computer Use Demo](https://github.com/anthropics/anthropic-quickstarts/tree/main/computer-use-demo). The original demo provides a robust foundation for computer control through Claude, and we've extended it to support native macOS and iOS automation.

We highly recommend checking out the original demo to understand the core concepts and implementation patterns.

## Features

- Control Mac OS through native commands and GUI automation
- Control iOS devices through Appium/XCUITest
- Streamlit-based interface for interaction
- Support for multiple LLM providers (Anthropic, Bedrock, Vertex)
- Automatic screen resolution scaling
- File system interaction capabilities

## Prerequisites

- macOS Sonoma 15.7 or later
- Python 3.12+
- Homebrew
- Xcode and iOS Simulator/Device
- Node.js and npm (for Appium)

## Installation

1. Install system dependencies:

```bash
# Install Homebrew if not installed
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install required packages
brew install python@3.12 cliclick node

# Install Appium and dependencies
npm install -g appium
npm install -g appium-xcuitest-driver
```

2. Install Python dependencies:

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

3. Configure environment:

```bash
cp .env.example .env
# Edit .env with your settings
```

## Usage

1. Start the Streamlit interface:

```bash
streamlit run src/ui/streamlit_app.py
```

2. Access the interface at http://localhost:8501

## Environment Variables

- `ANTHROPIC_API_KEY`: Your Anthropic API key
- `API_PROVIDER`: anthropic/bedrock/vertex
- `SCREEN_WIDTH`: Display width (default: 1280)
- `SCREEN_HEIGHT`: Display height (default: 800)
- `IOS_DEVICE_ID`: iOS device UDID (optional)

## Security Notice

⚠️ This tool grants Claude control over your devices. Use with caution and never provide access to sensitive information or accounts. 