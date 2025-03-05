# Bike Helmet Detection and Cyclist Counting System

Welcome to the repository containing code to count bikehelmets and cyclists in videos This guide is designed to help you navigate and utilize these demos.

# Table of Contents
1. [Introduction](#introduction)
2. [Setting Up Your Environment](#setting-up-your-environment)
3. [Creating a Conda Environment](#creating-a-conda-environment)
4. [Activating the Environment](#activating-the-environment)
5. [Installing Required Packages](#installing-required-packages)
6. [Demos Overview](#demos-overview)
   - [Gradio Demo](#gradio-demo)
   - [CLI Application](#cli-application)
7. [Deployment](#deployment)
   - [Ubuntu](#ubuntu)
   - [Windows](#windows)

## Introduction

This repository contains code to detect and count bike helmets and cyclists from video streams using a machine learning model. The system can be run either in real-time via a webcam or on pre-recorded video footage. Additionally, it provides two methods of interaction: a user-friendly web interface built with Gradio and a command-line interface (CLI).

## Setting Up Your Environment

Before diving into the demos, you'll need to set up your environment. We recommend using Conda, a popular package and environment management system. 
If you don't have Conda installed, you can download it from the Miniconda website (a minimal installer for Conda).

## Cloning the Repository

First, clone the repository to your local machine using the following command (This assumes you have Git installed from https://git-scm.com/downloads):

```bash
git clone https://github.com/imaihub/traffic-safety-helmet-counting.git
cd your-repository
```

## Creating a Conda Environment

Once Conda  is installed (from https://www.anaconda.com/download), you can create a new environment specifically for running these demos. We'll use Python 3.12 for this environment.
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

```markdown
## Running the Gradio Demo
After running `python gradio_server/server.py`, you should see output similar to the following in your terminal:

```bash
Running on local URL: http://127.0.0.1:7860
Press CTRL+C to quit
```

Then, open the URL http://127.0.0.1:7860 in your browser to access the Gradio web interface.

![assets/GUI.png](assets/GUI.png)

## CLI Application

This code also supports analyses through a CLI script. 

Run the CLI script with 

``python scripts/cli.py``

If you want a local camera feed, add the argument --camera-mode like:

``python scripts/cli.py --camera-mode``

If you want an analysis of a video file, add an --input argument pointing to the video file like:

``python scripts/cli.py --input /path/to/video.mp4``

Here is an example of what you will see:

![assets/UI.png](assets/UI.png)

## Deployment

It is also possible to deploy the Gradio webserver as a Docker container. Depending on the Operating System, there are different instructions for installing docker.

### Ubuntu

First install docker using: 

```bash
sudo apt install docker.io
sudo apt install docker-compose

# Add Docker's official GPG key:
sudo apt-get update
sudo apt-get install ca-certificates curl
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc

# Add the repository to Apt sources:
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "${UBUNTU_CODENAME:-$VERSION_CODENAME}") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt-get update

sudo apt-get install -y docker-compose-plugin
```

If you wish to run the models on the GPU, install nvidia-container-toolkit following the instructions from (https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/install-guide.html) or execute

```bash
curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey | sudo gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg \
  && curl -s -L https://nvidia.github.io/libnvidia-container/stable/deb/nvidia-container-toolkit.list | \
    sed 's#deb https://#deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg] https://#g' | \
    sudo tee /etc/apt/sources.list.d/nvidia-container-toolkit.list

sudo apt-get update
sudo apt-get install -y nvidia-container-toolkit
sudo apt-get install -y nvidia-docker2

sudo systemctl restart docker
```

To run this server locally in a Docker container, run

```bash
sudo docker compose up
```

## Windows

To install Docker for Windows, follow the guide in https://docs.docker.com/desktop/setup/install/windows-install/

In case of wanting to use a NVIDIA GPU, you will also need to install CUDA on WSL (follow https://developer.nvidia.com/cuda/wsl)