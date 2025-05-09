from django.conf import settings
from django.core.mail import send_mail
from django.core.paginator import Paginator
from django.db.models import Count
from django.shortcuts import get_object_or_404,  render
from django.views.decorators.http import require_POST
# from django.views.generic import ListView
from taggit.models import Tag

from .forms import CommentForm, EmailPostForm
from .models import Post


SIMILAR_POSTS_COUNT = 4


@require_POST
def post_comment(request, post_id):
    post = get_object_or_404(
        Post,
        id=post_id,
        status=Post.Status.PUBLISHED
    )
    comment = None
    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.save()
    return render(
        request,
        'blog/post/comment.html',
        {
            'post': post,
            'form': form,
            'comment': comment
        },
    )


def post_list(request, tag_slug=None):
    posts = Post.published.all()
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        posts = posts.filter(tags__in=[tag])
    paginator = Paginator(posts, settings.PAGE_SIZE)
    page_number = request.GET.get('page')
    page_object = paginator.get_page(page_number)
    return render(
        request,
        'blog/post/list.html',
        {
            'page_obj': page_object,
            'tag': tag,
        }
    )


# class PostListView(ListView):
#     queryset = Post.published.all()
#     context_object_name = 'posts'
#     paginate_by = settings.PAGE_SIZE
#     template_name = 'blog/post/list.html'


def post_detail(request, year, month, day, post_slug):
    post = get_object_or_404(
        Post,
        status=Post.Status.PUBLISHED,
        slug=post_slug,
        publish__year=year,
        publish__month=month,
        publish__day=day
    )
    post_tags_ids = post.tags.values_list('id', flat=True)
    similar_posts = Post.published.filter(
        tags__in=post_tags_ids
    ).exclude(
        id=post.id
    )
    similar_posts = similar_posts.annotate(
        same_tags=Count('tags')
    ).order_by(
        '-same_tags', '-publish'
    )[:SIMILAR_POSTS_COUNT]
    return render(
        request,
        'blog/post/detail.html',
        {
            'post': post,
            'comments': post.comments.filter(active=True),
            'form': CommentForm(),
            'similar_posts': similar_posts
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



