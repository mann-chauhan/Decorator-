import base64
import json
import os
import requests
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from dotenv import load_dotenv
from PIL import Image, ImageDraw, ImageFont
import io

# Load environment variables from .env file
load_dotenv()

HUGGINGFACE_API_TOKEN = os.getenv("HUGGINGFACE_API_TOKEN") or os.getenv("HF_API_TOKEN")

# --- Use SDXL Lightning Free API ---
def generate_image_api(prompt):
    API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0"
    
    # Check if API token is available
    if not HUGGINGFACE_API_TOKEN or HUGGINGFACE_API_TOKEN == "your_huggingface_token_here":
        print("WARNING: Hugging Face API token not found, using demo mode")
        return generate_demo_image(prompt)
    
    headers = {
        "Authorization": f"Bearer {HUGGINGFACE_API_TOKEN}"
    }
    payload = {
        "inputs": prompt,
    }
    
    try:
        print(f"Making API request to {API_URL} with prompt: {prompt[:50]}...")
        response = requests.post(API_URL, headers=headers, json=payload, timeout=30)
        print(f"API Response Status: {response.status_code}")
        
        if response.status_code == 200:
            print("API call successful, returning image data")
            return response.content
        else:
            print(f"API call failed with status {response.status_code}: {response.text}")
            print("Falling back to demo mode")
            return generate_demo_image(prompt)
    except requests.exceptions.RequestException as e:
        print(f"Request exception: {str(e)}")
        print("Falling back to demo mode")
        return generate_demo_image(prompt)
    except Exception as e:
        print(f"Unexpected error in generate_image_api: {str(e)}")
        return generate_demo_image(prompt)

def generate_demo_image(prompt):
    """Generate a demo image when API is not available"""
    print(f"Generating demo image for prompt: {prompt}")
    
    # Create a visible demo image (512x512 pixels)
    width, height = 512, 512
    
    # Create a gradient background
    image = Image.new('RGB', (width, height), color='#f0f0f0')
    draw = ImageDraw.Draw(image)
    
    # Draw a gradient background
    for y in range(height):
        r = int(200 + (y / height) * 55)
        g = int(220 + (y / height) * 35)
        b = int(240 + (y / height) * 15)
        draw.line([(0, y), (width, y)], fill=(r, g, b))
    
    # Draw a decorative border
    draw.rectangle([10, 10, width-10, height-10], outline='#667eea', width=3)
    
    # Add text
    try:
        # Try to use a default font
        font = ImageFont.load_default()
    except:
        # Fallback to default size
        font = ImageFont.load_default()
    
    # Add title
    title = "Demo Room Design"
    title_bbox = draw.textbbox((0, 0), title, font=font)
    title_width = title_bbox[2] - title_bbox[0]
    title_x = (width - title_width) // 2
    draw.text((title_x, 50), title, fill='#333333', font=font)
    
    # Add prompt text (wrapped)
    words = prompt.split()
    lines = []
    current_line = ""
    for word in words:
        test_line = current_line + " " + word if current_line else word
        bbox = draw.textbbox((0, 0), test_line, font=font)
        if bbox[2] - bbox[0] < width - 100:  # Leave margin
            current_line = test_line
        else:
            if current_line:
                lines.append(current_line)
            current_line = word
    if current_line:
        lines.append(current_line)
    
    # Draw wrapped text
    y_position = 150
    for line in lines[:6]:  # Limit to 6 lines
        bbox = draw.textbbox((0, 0), line, font=font)
        line_width = bbox[2] - bbox[0]
        x = (width - line_width) // 2
        draw.text((x, y_position), line, fill='#666666', font=font)
        y_position += 30
    
    # Add a decorative element
    draw.ellipse([width//2-50, height-150, width//2+50, height-50], fill='#667eea', outline='#4a5fd1', width=2)
    
    # Convert to bytes
    img_byte_arr = io.BytesIO()
    image.save(img_byte_arr, format='PNG')
    img_byte_arr = img_byte_arr.getvalue()
    
    return img_byte_arr


def home(request):
    if request.method == "GET" and request.GET.get("prompt"):
        prompt = request.GET.get("prompt", "A modern minimal living room with wood floor")
        image_bytes = generate_image_api(prompt)
        if image_bytes:
            return HttpResponse(image_bytes, content_type="image/png")
        else:
            return HttpResponse("Error generating image", status=500)
    return render(request, 'room_decorator/home.html')


@csrf_exempt
@require_http_methods(["POST"])
def generate_image(request):
    try:
        data = json.loads(request.body)
        prompt = data.get('prompt', '').strip()
        if not prompt:
            return JsonResponse({
                'success': False,
                'error': 'Prompt is required'
            }, status=400)
        
        print(f"Received generate request with prompt: {prompt}")
        image_bytes = generate_image_api(prompt)
        
        if image_bytes:
            base64_image = base64.b64encode(image_bytes).decode('utf-8')
            print("Image generated successfully, returning base64 data")
            return JsonResponse({
                'success': True,
                'image': base64_image,
                'prompt': prompt
            })
        else:
            error_msg = "Error generating image from Hugging Face SDXL Turbo API."
            if not HUGGINGFACE_API_TOKEN or HUGGINGFACE_API_TOKEN == "your_huggingface_token_here":
                error_msg = "Hugging Face API token not configured. Please add your token to the .env file."
            
            print(f"Image generation failed: {error_msg}")
            return JsonResponse({
                'success': False,
                'error': error_msg
            }, status=500)
    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'error': 'Invalid JSON data'
        }, status=400)
    except Exception as e:
        print(f"Unexpected error in generate_image: {str(e)}")
        return JsonResponse({
            'success': False,
            'error': f'Unexpected error: {str(e)}'
        }, status=500) 