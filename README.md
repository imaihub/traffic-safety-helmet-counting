# Bike helmets deliverable documentation

Welcome to the repository containing code to count bikehelmets and cyclists in videos This guide is designed to help you navigate and utilize these demos.

## Setting Up Your Environment

Before diving into the demos, you'll need to set up your environment. We recommend using Conda, a popular package and environment management system. 
If you don't have Conda installed, you can download it from the Miniconda website (a minimal installer for Conda).

## Creating a Conda Environment

Once Conda  is installed, you can create a new environment specifically for running these demos. We'll use Python 3.11 for this environment.
Open your terminal (Command Prompt on Windows, Terminal on Linux), and run the following command:

``conda create -n bikehelmets python=3.12``

## Activating the Environment

Activate the newly created environment using the command:

``conda activate bikehelmets``

## Installing Required Packages

With the environment activated, you'll need to install the necessary Python packages. These are listed in a requirements.txt file provided in the repository. 
Ensure you're in the repository's root directory in your terminal, then run:

``pip install -r requirements.txt``

# Demos Overview

## Gradio Demo

Gradio allows you to interact with the machine learning model through a web interface. It's user-friendly and does not require coding knowledge.
Running the Gradio Demo

Navigate to the Gradio directory in your terminal, and run the demo script:

``python gradio_server/server.py``

This command starts a local web server. You'll see a URL in the terminal output, which you can open in your web browser to interact with the demo. This mode allows you to use a webcam or camera for real-time analysis.

## CLI Application

This code also supports analyses through a CLI script. 

Run the CLI script with 

``python gradio_server/server.py``

If you want a local camera feed, add the argument --camera-mode like:

``python gradio_server/server.py --camera-mode``

If you want an analysis of a video file, add an --input argument pointing to the video file like:

``python gradio_server/server.py --input /path/to/video.mp4``
