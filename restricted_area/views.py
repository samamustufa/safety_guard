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
        person_count = count_persons_entered_restricted_area(video_path, converted_coordinates, user.id)  # Pass user.id instead of user

        # Store restricted area data associated with the single user
        # store_restricted_area_data(video_path, person_count, user.id)  # Pass user.id instead of user

        # Return person_count in the JSON response
        return JsonResponse({'success': True, 'person_count': person_count})
            
    except Exception as e:
        # Log the exception traceback for debugging purposes
        traceback.print_exc()

        # Return an error response
        return JsonResponse({'success': False, 'error': str(e)}, status=500)


def restricted_area_result(request):
    # try:
    # data_0 = request.body.decode('utf-8')
    # print('data0:', data_0)
    # Check if request body contains valid JSON data
    # print(request.body)
    if True:
        print('inside body reqqqaqqqq')
        # data = json.loads(data_0)
        data = {}
        person_count = data.get('person_count', 0)

        uploaded_files = os.listdir(UPLOAD_FOLDER)
        
        if uploaded_files:
            latest_uploaded_file = max(uploaded_files, key=lambda f: os.path.getctime(os.path.join(UPLOAD_FOLDER, f)))
            os.remove(os.path.join(UPLOAD_FOLDER, latest_uploaded_file))
        
        return render(request, 'restricted_area_result.html', {'person_count': person_count, 'video_name': latest_uploaded_file})

    else:
        # Return an error response if request body is empty or malformed
        return JsonResponse({'success': False, 'error': 'Invalid request body'}, status=400)

    # except Exception as e:
    #     # Log the exception for debugging purposes
    #     print(f"Error in restricted_area_result: {str(e)}")

    #     # Return an error response
    #     return JsonResponse({'success': False, 'error': 'Internal Server Error'}, status=500)



def view_restricted_area_video(request):
    video_directory = os.path.join(settings.MEDIA_ROOT, 'output')
    video_filename = 'output_video.mp4'
    video_path = os.path.join(video_directory, video_filename)

    # Set response headers
    headers = {
        'Content-Type': 'video/mp4',
        'Accept-Ranges': 'bytes',
    }

    return HttpResponse(open(video_path, 'rb'), content_type='video/mp4')

