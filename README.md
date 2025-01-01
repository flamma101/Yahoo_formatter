# README.md

# Yahoo Formatter App

This project is a GUI application for formatting Yahoo credentials using proxies. It allows users to input credentials, apply transformations, and manage proxy settings through a user-friendly interface built with Tkinter.

## Files in the Project

- `src/yahoo_formater_UI.py`: Contains the main application code.
- `requirements.txt`: Lists the dependencies required for the project.
- `setup.py`: The setup script for packaging the application.
- `README.md`: Documentation for the project.

## Installation

To install the necessary dependencies, run:

```
pip install -r requirements.txt
```

## Running the Application

To run the application, execute the following command:

```
python src/yahoo_formater_UI.py
```

## Creating an Executable

To create an executable application from the Python script, you can use PyInstaller. First, ensure you have PyInstaller installed:

```
pip install pyinstaller
```

Then, run the following command in the terminal:

```
pyinstaller --onefile src/yahoo_formater_UI.py
```

This will generate a standalone executable in the `dist` directory.

## Usage

1. Select a proxy file containing your proxies.
2. Input your Yahoo credentials in the provided text area.
3. Click "Run" to process the credentials.
4. The output will be displayed in the output text area.

## License

This project is licensed under the MIT License.