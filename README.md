# Screen Commentator

Screen Commentator is a Python application that captures your screen content, extracts text using OCR, and generates concise summaries using the Ollama AI model. The summaries are displayed on a local web interface, which updates every 10 seconds.

## Features

- Automated screen capture and text extraction
- AI-powered summarization using Ollama
- Web interface for displaying summaries
- Copy-to-clipboard functionality
- Preserves text formatting in summaries

## Prerequisites

Before you begin, ensure you have met the following requirements:

- Python 3.7 or higher
- Tesseract OCR installed on your system
- Ollama installed and running on your machine

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/your-username/screen-commentator.git
   cd screen-commentator
   ```

2. Install the required Python packages:
   ```
   pip install -r requirements.txt
   ```

3. Ensure Tesseract OCR is installed on your system. Installation instructions can be found [here](https://github.com/tesseract-ocr/tesseract).

4. Install and set up Ollama on your machine. Follow the instructions [here](https://github.com/jmorganca/ollama).

## Usage

1. Run the application:
   ```
   python screen_commentator.py
   ```

2. Open a web browser and navigate to `http://localhost:5000`.

3. The web interface will display summaries of your screen content, updating every 30 seconds.

4. Use the "Copy to Clipboard" button to easily copy the generated summaries.

## Configuration

- To change the update interval, modify the `time.sleep(30)` line in the `capture_and_comment()` function.
- To use a different Ollama model, change the `model="llama3.2:latest"` parameter in the `generate_comment()` function.

## Contributing

Contributions to the Screen Commentator project are welcome. Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgements

- [Tesseract OCR](https://github.com/tesseract-ocr/tesseract)
- [Ollama](https://github.com/jmorganca/ollama)
- [Flask](https://flask.palletsprojects.com/)
- [Pillow](https://python-pillow.org/)

## Contact

If you have any questions or feedback, please open an issue on the GitHub repository.
