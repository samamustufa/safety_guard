from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.conf import settings
from .services import store_uploaded_video, count_persons_entered_restricted_area, store_restricted_area_data, get_first_frame
from django.shortcuts import get_object_or_404
from .models import RestrictedAreaData
from login.models import Login
import os
import json
import traceback
from django.urls import reverse

person_count = 0
output_filename=""
def restrictArea(request):
    try:
        return render(request,'restricted_page.html' )
    except Exception as e:
        pass


UPLOAD_FOLDER = r"D:\Users\mustufa\Desktop\django_a_file\version_1_ori\final_safetyweb\static\upload_folder"

def restricted_area_detection(request):
    if request.method == "POST":
        video = request.FILES.get('video')

        if video:
            # Store the uploaded video and get the video path
            video_path = store_uploaded_video(video)
            # Get the first frame image path
            first_frame_path = get_first_frame(video_path)

            # Redirect to the 'define_area' route with the video_path
            return redirect('define_area', video_path=video_path, first_frame_path=first_frame_path)

    return render(request, 'restricted_page.html')

def define_area(request, video_path, first_frame_path):
    video_path = request.GET.get('video_path', None)
    first_frame_path = request.GET.get('first_frame_path', None)
    print("VID", video_path)

    if request.method == 'POST':
        video = request.FILES.get('video')
        video_path = store_uploaded_video(video)
        first_frame_path = get_first_frame(video_path)
        print("First Frame Path:", first_frame_path)

    return render(request, 'define_area.html', {'video_path': video_path, 'first_frame_path': first_frame_path})

def process_restricted_area(request):
    global person_count,output_filename
    try:
        # Get the JSON data from the request body
        data = request.body.decode('utf-8')
        
        # Check if data is None or empty
        if not data:
            raise ValueError("JSON data is missing or empty in the request body")

        # Parse JSON data
        coordinates = json.loads(data)['coordinates']

        # Fetch the single user instance
        user = get_object_or_404(Login, id=1)

        # Convert coordinates to the desired format [(x1, y1), (x2, y2), ...]
        converted_coordinates = [(round(coord['x']), round(coord['y'])) for coord in coordinates if 'x' in coord and 'y' in coord]

        # Automatically detect the video path from the uploaded files in the UPLOAD_FOLDER
        uploaded_files = os.listdir(UPLOAD_FOLDER)
        if uploaded_files:
            latest_uploaded_file = max(uploaded_files, key=lambda f: os.path.getctime(os.path.join(UPLOAD_FOLDER, f)))
            video_path = os.path.join(UPLOAD_FOLDER, latest_uploaded_file)
        else:
            raise ValueError("No video file uploaded")

        # Implement your AI code for person counting using the coordinates
        person_count, output_filename = count_persons_entered_restricted_area(video_path, converted_coordinates, user.id)  # Pass user.id instead of user

        # Store restricted area data associated with the single user
        # store_restricted_area_data(video_path, person_count, user.id)  # Pass user.id instead of user

        # Return person_count in the JSON response
        return JsonResponse({'success': True, 'person_count': person_count, 'output_filename': output_filename})
            
    except Exception as e:
        # Log the exception traceback for debugging purposes
        traceback.print_exc()

        # Return an error response
        return JsonResponse({'success': False, 'error': str(e)}, status=500)



def restricted_area_result(request):
    global person_count, output_filename

    try:
        return render(request, 'restricted_output.html', {'person_count': person_count, 'output_filename': output_filename})
    except Exception as e:
        # Log the exception for debugging purposes
        print(f"Error in restricted_area_result: {str(e)}")

        # Return an error response
        return JsonResponse({'error': 'Internal Server Error'}, status=500)

