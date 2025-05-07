from django.conf import settings
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404,  render

from .models import Post


def post_list(request):
    posts = Post.published.all()
    paginator = Paginator(posts, settings.PAGE_SIZE)
    page_number = request.GET.get('page')
    page_object = paginator.get_page(page_number)
    return render(
        request,
        'blog/post/list.html',
        {
            'page_object': page_object,
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
