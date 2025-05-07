from django.conf import settings
from django.shortcuts import get_object_or_404,  render
from django.views.generic import ListView

from .models import Post


class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = settings.PAGE_SIZE
    template_name = 'blog/post/list.html'


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
