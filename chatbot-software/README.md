# Simple Command Line Chatbot

A simple Python chatbot that can be compiled into an executable file.

## Running the Chatbot

```bash
python chatbot.py
```

## Compiling to EXE

To compile this chatbot into an executable file, you'll need PyInstaller:

1. Install PyInstaller:
```bash
pip install -r requirements.txt
```

2. Compile to EXE:
```bash
pyinstaller --onefile --console chatbot.py
```

This will create an executable in the `dist/` folder.

### PyInstaller Options:
- `--onefile`: Creates a single executable file
- `--console`: Keeps the console window (for command line apps)
- `--name`: Specify a custom name for the executable (optional)

Example with custom name:
```bash
pyinstaller --onefile --console --name MyChatbot chatbot.py
```

## Features

- Simple keyword-based responses
- Handles common greetings and farewells
- Easy to extend with more sophisticated logic

