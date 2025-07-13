# Virtual Room Decorator SDXL

A Django web application that generates beautiful room designs using AI. Users can input text prompts describing their dream room, and the application will generate realistic room images using the SDXL-Lightning model via Hugging Face's inference API.

## Features

- 🎨 **AI-Powered Room Generation**: Uses SDXL-Lightning model for high-quality room designs
- 💡 **Example Prompts**: Click-to-use example prompts for inspiration
- ⚡ **Real-time Generation**: Fast image generation with loading animations
- 📱 **Responsive Design**: Beautiful, modern UI that works on all devices
- 🚀 **Deployable**: Ready for deployment on Render or other platforms
- 🔑 **API Token Required**: Uses Hugging Face inference API (token needed)
- 📥 **Download Images**: Download generated images as JPEG files
- 📚 **Recent Images**: History of up to 5 recent images with delete functionality

## Example Prompts

- "luxury bedroom with plants and natural light"
- "modern minimalist living room with neutral colors"
- "cozy cottage kitchen with warm lighting"
- "industrial loft with exposed brick and modern furniture"
- "scandinavian dining room with wooden table and plants"
- "boho bedroom with colorful textiles and macrame"
- "art deco living room with gold accents and velvet furniture"
- "zen meditation room with bamboo and natural elements"

## Local Development

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- Hugging Face API token (free from https://huggingface.co/settings/tokens)

### Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd virtual_room_decorator_sdxl
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up API token**
   ```bash
   # Add your Hugging Face token to environment variables
   export HF_API_TOKEN="your_token_here"
   ```

5. **Run migrations**
   ```bash
   python manage.py migrate
   ```

6. **Start the development server**
   ```bash
   python manage.py runserver
   ```

7. **Open your browser**
   Navigate to `http://127.0.0.1:8000/`

## Deployment on Render

### Option 1: Using render.yaml (Recommended)

1. Push your code to a Git repository (GitHub, GitLab, etc.)
2. Connect your repository to Render
3. Render will automatically detect the `render.yaml` file and deploy your application

### Option 2: Manual Setup

1. Create a new Web Service on Render
2. Connect your Git repository
3. Use these settings:
   - **Build Command**: `./build.sh`
   - **Start Command**: `gunicorn virtual_room_decorator_sdxl.wsgi:application`
   - **Environment**: Python 3.9

## Project Structure

```
virtual_room_decorator_sdxl/
├── manage.py                          # Django management script
├── requirements.txt                   # Python dependencies
├── build.sh                          # Build script for deployment
├── render.yaml                       # Render deployment configuration
├── .env                              # Environment variables (API token)
├── virtual_room_decorator_sdxl/      # Main Django project
│   ├── __init__.py
│   ├── settings.py                   # Django settings
│   ├── urls.py                       # Main URL configuration
│   └── wsgi.py                       # WSGI application
└── room_decorator/                   # Main application
    ├── __init__.py
    ├── apps.py                       # App configuration
    ├── urls.py                       # App URL patterns
    ├── views.py                      # View functions
    └── templates/                    # HTML templates
        └── room_decorator/
            └── home.html             # Main page template
```

## API Endpoints

- `GET /` - Home page with the room generation form
- `POST /generate/` - Generate room image from text prompt

### Generate Image API

**Endpoint**: `POST /generate/`

**Request Body**:
```json
{
    "prompt": "luxury bedroom with plants"
}
```

**Response**:
```json
{
    "success": true,
    "image": "base64_encoded_image_data",
    "prompt": "luxury bedroom with plants"
}
```

**Error Response**:
```json
{
    "success": false,
    "error": "Error message"
}
```

## Technologies Used

- **Backend**: Django 5.2.4
- **Frontend**: HTML5, CSS3, JavaScript (Vanilla)
- **AI Model**: SDXL via Hugging Face Inference API
- **Deployment**: Render (with Gunicorn)
- **Styling**: Bootstrap 5.3.0 with custom CSS

## Features Implemented

- ✅ **3-Column Layout**: Sample prompts, form, and results side-by-side
- ✅ **Bootstrap Design**: Modern, responsive UI
- ✅ **8 Sample Prompts**: Clickable examples
- ✅ **Loading Animation**: Bootstrap spinner during generation
- ✅ **Download Button**: Save images as JPEG files
- ✅ **Recent Images**: History with delete functionality
- ✅ **Error Handling**: Comprehensive error messages
- ✅ **Auto-scroll**: Smooth scrolling to results
- ✅ **Mobile Responsive**: Works on all devices

## Error Handling

The application includes comprehensive error handling for:
- Network connectivity issues
- API timeouts
- Invalid JSON data
- Missing prompts
- Authentication errors
- Server errors

## Performance Considerations

- Uses lightweight dependencies to stay under Render's 4GB limit
- Implements proper timeout handling for API calls
- Optimized image delivery using base64 encoding
- Responsive design for all device sizes

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is open source and available under the MIT License.

## Support

If you encounter any issues:
1. Check the browser console for JavaScript errors
2. Verify your internet connection
3. Try refreshing the page
4. Check if the Hugging Face API is accessible

---

**Note**: This application uses the Hugging Face inference API with the SDXL model. The API token is configured in the `.env` file. For production use, consider using a paid API service or hosting your own model.
