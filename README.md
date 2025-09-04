# Document Translation API

## Overview

This project provides a Flask-based API for translating various document formats, including Word documents, Excel spreadsheets, and PowerPoint presentations. It leverages external translation services to process the content and returns the translated documents. The API is designed to be secure with API key authentication.

## Features

*   **Document Translation:** Supports translation of `.docx`, `.xlsx`, and `.pptx` files.
*   **API Key Authentication:** Ensures secure access to the translation service.
*   **Scalable:** Designed to be deployed on platforms like Heroku.
*   **Error Handling:** Robust error handling for file not found, missing API keys, and other issues.

## Technologies Used

*   **Backend Framework:** Flask, Flask-RESTful
*   **Document Processing:** `python-docx`, `openpyxl`, `python-pptx`
*   **Translation:** External translation service (implementation details are abstracted by `document_processor.py`)

## Setup and Installation

To set up and run the project locally, follow these steps:

1.  **Clone the repository:**

    ```bash
    git clone <repository_url>
    cd document-translation-api
    ```

2.  **Create a virtual environment and activate it:**

    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4.  **Set up environment variables:**

    You need to set an `API_KEY` environment variable for authentication. For example:

    ```bash
    export API_KEY="your_secret_api_key"
    ```

    If deploying to Heroku, ensure this environment variable is configured there.

5.  **Run the application:**

    ```bash
    python __main__.py
    ```

    The API will run on `http://0.0.0.0:5000` by default.

## API Endpoints

### `POST /translate`

Translates an uploaded document.

*   **Method:** `POST`
*   **Headers:**
    *   `X-API-Key`: Your API key for authentication.
*   **Form Data:**
    *   `file`: The document file to be translated (`.docx`, `.xlsx`, or `.pptx`).
    *   `language`: The target language for translation (e.g., `es` for Spanish, `fr` for French).

*   **Response:**
    *   `200 OK`: Returns a JSON object with the base64-encoded translated content.
        ```json
        {
            "translated_content": "base64_encoded_translated_file"
        }
        ```
    *   `400 Bad Request`: If no file or target language is provided.
    *   `401 Unauthorized`: If the API key is missing or invalid.
    *   `404 Not Found`: If the file is not found.
    *   `500 Internal Server Error`: For other server-side errors.

## Project Structure

```
document-translation-api/
├── Procfile                    # Heroku Procfile for deployment
├── requirements.txt            # Python dependencies
├── __init__.py                 # Package initialization
├── __main__.py                 # Main API entry point
├── document_processor.py       # Core logic for document type detection and dispatching
├── excel_translate.py          # Handles Excel (.xlsx) document translation
├── hyperlinks.py               # Utility for handling hyperlinks in documents
├── powerpoint_translate.py     # Handles PowerPoint (.pptx) presentation translation
├── translate_text.py           # Core text translation utility
└── translate_word.py           # Handles Word (.docx) document translation
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request or open an issue for any bugs or feature requests.

## License

This project is open-source and available under the MIT License.

