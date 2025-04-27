# React Project Generator

This project uses Agno and Mem0 to generate React projects based on image input. It uses Groq's Llama 3.3 70B model for text extraction and code generation.

## Features

- Image upload and processing
- Text extraction from images using LLM
- React project structure generation
- Component and page generation
- Web-based interface for project management

## Prerequisites

- Python 3.8+
- Groq API key
- Node.js and npm (for running generated React projects)

## Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd react-project-generator
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file in the root directory with your Groq API key:
```
GROQ_API_KEY=your_api_key_here
```

4. Create necessary directories:
```bash
mkdir uploads
mkdir generated_projects
mkdir templates
```

## Usage

1. Start the FastAPI server:
```bash
python main.py
```

2. Open your browser and navigate to `http://localhost:8000`

3. Upload an image containing your React project requirements

4. The system will:
   - Extract text from the image
   - Generate a React project structure
   - Create necessary components and pages
   - Provide a downloadable project structure

## Project Structure

```
.
├── main.py              # FastAPI application
├── react_generator.py   # React project generation logic
├── requirements.txt     # Python dependencies
├── uploads/            # Temporary storage for uploaded images
├── generated_projects/ # Generated React projects
└── templates/          # HTML templates
```

## Generated React Project Structure

The generated React projects follow a standard structure:

```
project_name/
├── src/
│   ├── components/     # Reusable React components
│   ├── pages/         # Page components
│   ├── styles/        # CSS and styling files
│   ├── utils/         # Utility functions
│   └── assets/        # Static assets
├── public/            # Public files
└── package.json       # Project dependencies
```

## API Endpoints

- `POST /upload-image/`: Upload an image for processing
- `GET /project/{project_name}`: Get project structure details

## Contributing

Feel free to submit issues and enhancement requests.

## License

This project is licensed under the MIT License. 