from django.http import Http404
from django.shortcuts import get_object_or_404, render
from django.utils import timezone
from blog.models import Category, Post


CURRENT_DATRTIME = timezone.now()


def index(request):
    post_list = Post.objects.select_related(
        'location', 'author', 'category'
    ).filter(
        pub_date__lt=CURRENT_DATRTIME,
        is_published=True,
        category__is_published=True,
    ).order_by('-pub_date', 'title')[:5]
    return render(request, 'blog/index.html', {'post_list': post_list})


def category_posts(request, category_slug):
    try:
        category = Category.objects.get(
            slug=category_slug, is_published=True)
    except Category.DoesNotExist as exc:
        raise Http404('Этой категории нет в публикации.') from exc

    post_list = Post.objects.select_related(
        'location', 'author', 'category'
    ).filter(
        category__slug=category_slug,
        pub_date__lt=CURRENT_DATRTIME,
        is_published=True,
        category__is_published=True
    ).order_by('-pub_date', 'title')
    return render(request, 'blog/category.html', {
        'post_list': post_list,
        'category': category,
    })


def post_detail(request, post_id):
    post = get_object_or_404(
        Post.objects.select_related(
            'location', 'author', 'category'
        ).filter(
            pub_date__lt=CURRENT_DATRTIME,
            is_published=True,
            category__is_published=True,
        ),
        pk=post_id
    )
    return render(request, 'blog/detail.html', {'post': post})