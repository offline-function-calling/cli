# Offline Function Calling Agent

This CLI helps you interact with a function-calling enabled offline LLM using Ollama. It uses the [`@offline-function-calling/sdk`](https://github.com/offline-function-calling/sdk) library.

## Installation

For now, the installation has to be done by cloning the git repository, installing the dependencies ([`uv`](https://docs.astral.sh/uv/) is recommended), and running the `main.py` script.

```bash
git clone https://github.com/offline-function-calling/cli ; cd cli
uv run main.py --model gemma3:27b-fc --tools ./tools
```

Note that the `gemma3:*-fc` models must be created using the Modelfiles in the `models/` directory of this repository:

```bash
ollama create gemma3:27b-fc --file models/gemma3-27b-fc.modelfile
ollama create gemma3:12b-fc --file models/gemma3-12b-fc.modelfile
```

Note that it is recommended to use the 27b parameter model only if you have 20-24 GB of RAM or more.

## Usage

You can add more tools by just creating files in the custom tools directory that you mention. Each file must have one or more Python functions with docstrings that contain a description of what the tool does, as well as what the parameters are.
