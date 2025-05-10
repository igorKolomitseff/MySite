import markdown
from django import template
from django.db.models import Count
from django.utils.safestring import mark_safe

from blog.models import Post

register = template.Library()


LATEST_POSTS_COUNT = 5
MOST_COMMENTED_POSTS_COUNT = 5


@register.simple_tag
def total_posts():
    return Post.published.count()


@register.simple_tag
def get_most_commented_posts(count=MOST_COMMENTED_POSTS_COUNT):
    return Post.published.annotate(
        total_comments=Count('comments')
    ).order_by(
        '-total_comments'
    )[:count]


@register.inclusion_tag('blog/post/latest_posts.html')
def show_latest_posts(count=LATEST_POSTS_COUNT):
    return {
        'latest_posts': Post.published.order_by('-publish')[:count]
    }


@register.filter(name='markdown')
def markdown_format(text):
    return mark_safe(markdown.markdown(text))