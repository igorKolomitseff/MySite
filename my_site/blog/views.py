from django.conf import settings
from django.core.mail import send_mail
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404,  render
from django.views.generic import ListView

from .forms import EmailPostForm
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


def post_share(request, post_id):
    post = get_object_or_404(
        Post,
        id=post_id,
        status=Post.Status.PUBLISHED
    )

    sent = False

    if request.method == 'POST':
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            post_url = request.build_absolute_uri(
                post.get_absolute_url()
            )
            subject = (
                f'{cleaned_data["name"]} recommends you read {post.title}'
            )
            message = (
                f'Read {post.title} at {post_url}\n\n'
                f'{cleaned_data["name"]}\'s comments: '
                f'{cleaned_data["comments"]}'
            )
            send_mail(
                subject,
                message,
                'igor25011@gmail.com',
                [cleaned_data['to']]
            )
            sent = True
    else:
        form = EmailPostForm()
    return render(
        request,
        'blog/post/share.html',
        {
            'post': post,
            'form': form,
            'sent': sent
        }
    )
