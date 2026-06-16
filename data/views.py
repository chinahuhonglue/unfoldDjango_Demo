from pathlib import Path

from django.conf import settings
from django.http import FileResponse, Http404
from django.shortcuts import render

MEMORIAL_PHOTO_FILENAME = "沱龙峡留念.png"


def _memorial_photo_path() -> Path:
    return Path(settings.BASE_DIR) / MEMORIAL_PHOTO_FILENAME


def memorial_photo_page(request):
    photo_path = _memorial_photo_path()
    if not photo_path.is_file():
        raise Http404("纪念照文件不存在")

    context = {
        "photo_filename": MEMORIAL_PHOTO_FILENAME,
        "photo_caption": "二零二五年七月，王雲（左一）胡鴻略（右一）同志于沱龍峡留念。",
    }
    return render(request, "memorial/photo.html", context)


def download_memorial_photo(request):
    photo_path = _memorial_photo_path()
    if not photo_path.is_file():
        raise Http404("纪念照文件不存在")

    inline = request.GET.get("inline") == "1"
    return FileResponse(
        photo_path.open("rb"),
        as_attachment=not inline,
        filename=MEMORIAL_PHOTO_FILENAME,
        content_type="image/png",
    )
