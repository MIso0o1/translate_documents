# Document Translation API

## Overview

This project provides a **FastAPI-based API** for translating various document formats, including Word documents, Excel spreadsheets, and PowerPoint presentations. It leverages external translation services to process the content **asynchronously**, significantly speeding up the translation of paragraphs and other text elements. The API is designed to be secure with API key authentication.

## Features

*   **Document Translation:** Supports translation of `.docx`, `.xlsx`, and `.pptx` files.
*   **Asynchronous Processing:** Utilizes `asyncio` and `httpx` for concurrent translation requests, leading to faster processing times.
*   **API Key Authentication:** Ensures secure access to the translation service.
*   **Scalable:** Designed for efficient deployment and handling of concurrent requests.
*   **Error Handling:** Robust error handling for file not found, missing API keys, and other issues.

## Technologies Used

*   **Backend Framework:** FastAPI, Uvicorn
*   **Asynchronous HTTP Client:** httpx
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

    If deploying to a cloud platform, ensure this environment variable is configured there.

5.  **Run the application:**

    The application now uses `uvicorn`.

    ```bash
    uvicorn __main__:app --host 0.0.0.0 --port 5000 --reload
    ```

    The API will run on `http://0.0.0.0:5000` by default. You can access the interactive API documentation (Swagger UI) at `http://0.0.0.0:5000/docs`.

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
    *   `500 Internal Server Error`: For other server-side errors.

## Project Structure

```
document-translation-api/
├── Procfile                    # Heroku Procfile for deployment (updated for Uvicorn)
├── requirements.txt            # Python dependencies (updated for FastAPI/Uvicorn)
├── __init__.py                 # Package initialization
├── __main__.py                 # Main API entry point (FastAPI application)
├── document_processor.py       # Core logic for document type detection and dispatching (async-enabled)
├── excel_translate.py          # Handles Excel (.xlsx) document translation (async-enabled)
├── hyperlinks.py               # Utility for handling hyperlinks in documents (async-enabled)
├── powerpoint_translate.py     # Handles PowerPoint (.pptx) presentation translation (async-enabled)
├── translate_text.py           # Core text translation utility (async-enabled)
└── translate_word.py           # Handles Word (.docx) document translation (async-enabled)
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request or open an issue for any bugs or feature requests.

## License

This project is open-source and available under the MIT License.
