from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required

from .models import Media


@login_required
def media_video_api(request, media_id):

    media = get_object_or_404(Media, id=media_id)

    if not media.content:
        return JsonResponse(
            {
                "success": False,
                "message": "فایل فیلم وجود ندارد."
            },
            status=404
        )

    return JsonResponse({
        "success": True,
        "data": {
            "id": media.id,
            "title": media.title,
            "description": media.description,
            "video": media.content.url,
        }
    })