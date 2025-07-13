import base64
import json
import os
import requests
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


def home(request):
    """Home page with the form for room decoration prompts."""
    return render(request, 'room_decorator/home.html')


@csrf_exempt
@require_http_methods(["POST"])
def generate_image(request):
    """Generate image using the Hugging Face API."""
    try:
        # Parse the JSON data from the request
        data = json.loads(request.body)
        prompt = data.get('prompt', '').strip()
        
        if not prompt:
            return JsonResponse({
                'success': False,
                'error': 'Prompt is required'
            }, status=400)
        
        # API endpoint for SDXL model (requires Hugging Face token)
        api_url = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0"
        
        # Prepare the payload
        payload = {"inputs": prompt}
        
        # Prepare headers with API token if available
        headers = {}
        api_token = os.getenv('HF_API_TOKEN')
        if api_token:
            headers['Authorization'] = f'Bearer {api_token}'
        
        # Make the API request
        response = requests.post(api_url, json=payload, headers=headers, timeout=60)
        
        if response.status_code == 200:
            # Convert the image to base64
            image_data = response.content
            base64_image = base64.b64encode(image_data).decode('utf-8')
            
            return JsonResponse({
                'success': True,
                'image': base64_image,
                'prompt': prompt
            })
        elif response.status_code == 401:
            return JsonResponse({
                'success': False,
                'error': 'API authentication required. This model requires a Hugging Face API token. Please add your token to use this feature.'
            }, status=401)
        else:
            return JsonResponse({
                'success': False,
                'error': f'API request failed with status {response.status_code}'
            }, status=500)
            
    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'error': 'Invalid JSON data'
        }, status=400)
    except requests.exceptions.Timeout:
        return JsonResponse({
            'success': False,
            'error': 'Request timed out. Please try again.'
        }, status=408)
    except requests.exceptions.RequestException as e:
        return JsonResponse({
            'success': False,
            'error': f'Network error: {str(e)}'
        }, status=500)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': f'Unexpected error: {str(e)}'
        }, status=500) 