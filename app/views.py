import cv2
from cvzone.HandTrackingModule import HandDetector
from django.core.files.storage import default_storage
from django.http import StreamingHttpResponse, HttpResponseServerError
from django.shortcuts import render
from django.views.decorators import gzip

from . import ml_model
from .forms import UploadFileForm
from django.views.decorators.csrf import ensure_csrf_cookie

from .ml_model import classify


@ensure_csrf_cookie
def upload_display_video(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['file']
            file_path = handle_uploaded_file(file)
            ml_result = ml_model.run_ml(file_path)
            return render(request, "upload-display-video.html", {'filename': file_path,
                                                                 'ml_result': ml_result})
    else:
        form = UploadFileForm()
    return render(request, 'upload-display-video.html', {'form': form})


def handle_uploaded_file(f):
    file_name = default_storage.save(f.name, f)
    return file_name


def main(request):
    return render(request, 'index.html')


class VideoCamera(object):
    def __init__(self):
        self.video = cv2.VideoCapture(0)

    def __del__(self):
        self.video.release()

    def get_frame(self):
        ret, img = self.video.read()
        detector = HandDetector(maxHands=1)
        offset = 20
        hands = detector.findHands(img, draw=False)
        if hands:
            hand = hands[0]
            x, y, w, h = hand['bbox']
            roi = img[y: y + 225 + offset, x - offset: x + 290 + offset]
            if len(roi) > 1 and roi[1].size != 0:
                gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
                gray = cv2.GaussianBlur(gray, (7, 7), 0)
                alpha = classify(gray)
                cv2.rectangle(img, (x - offset, y - offset), (x + w + offset, y + h + offset), (0, 255, 0), 2)
                font = cv2.FONT_HERSHEY_SIMPLEX
                cv2.putText(img, alpha, (0, 130), font, 5, (0, 0, 255), 2)
        ret, jpeg = cv2.imencode('.jpg', img)
        return jpeg.tobytes()


def gen(camera):
    while True:
        img = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + img + b'\r\n\r\n')


@gzip.gzip_page
def live(request):
    try:
        return StreamingHttpResponse(gen(VideoCamera()), content_type="multipart/x-mixed-replace;boundary=frame")
    except HttpResponseServerError as e:
        print("Streaming stopped")
