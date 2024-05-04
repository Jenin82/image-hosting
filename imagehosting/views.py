from django.shortcuts import render

from rest_framework.decorators import api_view
from rest_framework.response import Response
# import fitz  
import base64
import requests
from django.core.files.base import ContentFile
# Create your views here.
API_KEY = '6d207e02198a847aa98d0a2a901485a5'
UPLOAD_URL = 'https://freeimage.host/api/1/upload'

@api_view(['POST'])
def image_to_url(request):
    if 'image_file' not in request.FILES:
        return Response({'error': 'Image file not found in request'}, status=400)
    
    try:
        image_file = request.FILES['image_file']
        image_data = image_file.read()

        hosted_url = upload_image(image_data)
        
        return Response({'hosted_url': hosted_url})
    
    except Exception as e:
        return Response({'error': str(e)}, status=500)

def upload_image(image_data):
    headers = {
        'Authorization': f'Bearer {API_KEY}'
    }
    
    base64_image = base64.b64encode(image_data).decode('utf-8')

    data = {
        'key': API_KEY,
        'source': base64_image,
        'format': 'json'
    }

    response = requests.post(UPLOAD_URL, headers=headers, data=data)
    
    if response.status_code == 200:
        return response.json().get('image', {}).get('url')
    else:
        raise Exception(f"Failed to upload image: {response.text}")