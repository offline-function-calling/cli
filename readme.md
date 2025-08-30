# Offline Function Calling Agent

This CLI helps you interact with a function calling enabled offline LLM using Ollama. It uses the [`@offline-function-calling/sdk`](https://github.com/offline-function-calling/sdk) library.

## Installation

The CLI is still under active development. During this phase, installation has to be done manually by cloning the git repository, installing the dependencies, and running the `main.py` script. Before running the below commands, please follow the instructions [here](./tools.md#python) to install `python` and `uv`.

```bash
git clone https://github.com/offline-function-calling/cli ; cd cli
uv run main.py --model gemma3:27b-fc --tools ./tools
```

The `gemma3:*-fc` models must be created using the Modelfiles in the `models/` directory of this repository:

```bash
ollama create gemma3:27b-fc --file models/gemma3-27b-fc.modelfile
ollama create gemma3:12b-fc --file models/gemma3-12b-fc.modelfile
```

or, you could pull and use the [`gamemaker1/gemma3:12b-fc`](https://ollama.com/gamemaker1/gemma3:12b-fc) and [`gamemaker1/gemma3:27b-fc`](https://ollama.com/gamemaker1/gemma3:27b-fc) models instead. Note that it is recommended to use the 27b parameter model only if you have 20-24 GB of RAM or more.

## Usage

To run the CLI, just `cd` into the directory where it was installed and run the following:

```bash
uv run main.py \
  --model gemma3:27b-fc \               # the model to use, must support tool calls using ollama
  --tools ./tools \                     # the path to the directory containing .py files with tool code
  --ollama http://localhost:11434       # the url at which the ollama server is running
```

You type multiline messages to send to the model, and submit it by pressing <kbd>Enter</kbd> and then <kbd>Ctrl</kbd>+<kbd>D</kbd>. Typing `/exit` or pressing <kbd>Ctrl</kbd>+<kbd>C</kbd> twice exits the chat, and typing `/help` prints a small message on how to use the CLI.

You can add more tools by just creating files in the custom tools directory that you mention. Each file must have one or more Python functions with docstrings that contain a description of what the tool does, as well as what the parameters are. The CLI comes with some builtin tools, which can be listed using the `/tools` command. If you add/remove tools mid-conversation, you can run the `/tools reload` command to update the list of available tools.

You can attach files from your computer by specifying the relative/absolute path to the files, or by specifying a `file://` URI. If it is a image/audio file, the CLI will pass it on to the model. If it is a document, the CLI will extract the text contents and append them to the end of the your message.
