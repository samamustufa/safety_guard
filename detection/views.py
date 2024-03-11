# views.py

from django.shortcuts import render
from django.http import HttpResponseRedirect
import os
from .services import process_video
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required



def upload_video(request):
    if request.method == 'POST' and request.FILES.get('video'):
        print("Inside The IFFFFF")

        video_file = request.FILES['video']
        
        # Define the destination folder where you want to save the uploaded video
        destination_folder = r'D:\Users\mustufa\Desktop\django_a_file\version_1_ori\final_safetyweb\static\video'

        if not os.path.exists(destination_folder):
            os.makedirs(destination_folder)

        destination_file_path = os.path.join(destination_folder, video_file.name)

        with open(destination_file_path, 'wb') as destination_file:
            for chunk in video_file.chunks():
                destination_file.write(chunk)

        model_paths = [r'D:\Users\mustufa\Desktop\django_a_file\version_1_ori\final_safetyweb\best4.pt', r'D:\Users\mustufa\Desktop\django_a_file\version_1_ori\final_safetyweb\yolov8m_custom_train31.pt']
        
        success_flags, output_filenames, counts = process_video(destination_file_path, destination_folder, model_paths)

        if all([success_flags]):
            total_count = counts.get('HELMET') + counts.get('NOHELMET') + counts.get('VEST') + counts.get('NOVEST')
            safety_percent = int((counts.get('HELMET') + counts.get('VEST')) /total_count * 100)
            unsafety_percent = 100 - safety_percent
            print(f'total={total_count} ,safe={safety_percent} ,unsafe={unsafety_percent}' )
            safety_data = {
                'video_path': output_filenames[0],
                'safety_percent' : safety_percent,
                'unsafety_percent' : unsafety_percent,
                'total' : total_count
            }
            return redirect('/testvideo/?video_path={}&safety_percent={}&unsafety_percent={}&total={}'.format(output_filenames[0], safety_percent, unsafety_percent, total_count))

    return render(request, 'detection.html')

def test(request):
    video_path = request.GET.get('video_path')
    safety_percent = request.GET.get('safety_percent')
    unsafety_percent = request.GET.get('unsafety_percent')
    total = request.GET.get('total')

    print(safety_percent, unsafety_percent, total)

    context = {
    "safety_data": {
        "video_path": video_path,
        "safety_percent": safety_percent,
        "unsafety_percent": unsafety_percent,
        "total": total
                }
                }

    # safety_data = {
    #     'video_path': video_path,
    #     'safety_percent': safety_percent,
    #     'unsafety_percent': unsafety_percent,
    #     'total': total
    # }
    return render(request, 'dtect_out.html', context['safety_data'])
