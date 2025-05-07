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


def post_detail(request, year, month, day, post_slug):
    return render(
        request,
        'blog/post/detail.html',
        {
            'post': get_object_or_404(
                Post,
                status=Post.Status.PUBLISHED,
                slug=post_slug,
                publish__year=year,
                publish__month=month,
                publish__day=day
            ),
        }
    )
