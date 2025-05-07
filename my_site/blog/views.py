from django.shortcuts import get_object_or_404,  render

from .models import Post


def post_list(request):
    return render(
        request,
        'blog/post/list.html',
        {
            'posts': Post.published.all(),
        }
    )


def post_detail(request, post_id):
    return render(
        request,
        'blog/post/detail.html',
        {
            'post': get_object_or_404(
                Post,
                id=post_id,
                status=Post.Status.PUBLISHED
            ),
        }
    )
