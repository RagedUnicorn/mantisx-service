# mantisx-service

![](docs/mantisx-service.png)

A Python service for retrieving and processing MantisX training session data.

## Features

- Retrieve shooting session data from MantisX API
- Filter sessions by drill type (e.g., Holster Draw Analysis)
- Save session data to JSON files
- Flexible date range and time-based filtering
- Configurable logging levels
- Comprehensive test suite

## Installation

1. Clone the repository
2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   venv\Scripts\activate  # On Windows
   # or
   source venv/bin/activate  # On Linux/Mac
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Basic Usage

```bash
python main.py --days-back 7 --output-dir sessions
```

### Date Range Filtering

```bash
python main.py --start-date 25/06/2025 --end-date 28/06/2025
```

### Arguments

- `--days-back` - Number of days to look back for sessions (default: 1)
- `--start-date` - Start date (format: DD/MM/YYYY)
- `--end-date` - End date (format: DD/MM/YYYY)
- `--output-dir` - Output directory for session files (default: output_data)

## Testing

The project includes a comprehensive test suite using pytest. See [tests/README.md](tests/README.md) for detailed testing documentation.

### Quick Test Commands
```bash
# Run all tests
python3 -m pytest tests/ -v

# Run with coverage
python3 -m pytest tests/ --cov=. --cov-report=term-missing -v

# Run specific test file
python3 -m pytest tests/test_main.py -v
```

### VS Code Integration

The project includes VS Code configurations for debugging tests:

1. Open VS Code
2. Go to Run and Debug (Ctrl+Shift+D)
3. Select one of the test configurations:
   - "Debug Tests" - Run all tests with debugger
   - "Debug Current Test File" - Debug the currently open test file
   - "Debug Tests with Coverage" - Run all tests with coverage report

You can also run tests from the Testing sidebar in VS Code.

## Development

### Project Structure

```
├── main.py              # Main application entry point
├── models/              # Data models
├── network/             # Network utilities and API calls
├── utils/               # Utility functions
├── tests/               # Test suite
├── output_data/         # Default output directory
└── .vscode/             # VS Code configuration
```

### Environment Variables

- `MANTISX_SERVICE_LOG_LEVEL` - Set logging level (10=DEBUG, 20=INFO, 30=WARNING, 40=ERROR)

## License

MIT License

Copyright (c) 2025 Michael Wiesendanger

Permission is hereby granted, free of charge, to any person obtaining
a copy of this software and associated documentation files (the
"Software"), to deal in the Software without restriction, including
without limitation the rights to use, copy, modify, merge, publish,
distribute, sublicense, and/or sell copies of the Software, and to
permit persons to whom the Software is furnished to do so, subject to
the following conditions:

The above copyright notice and this permission notice shall be
included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
