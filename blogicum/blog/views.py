from django.shortcuts import get_object_or_404, render

from blog.models import Category, Post


def index(request):
    post_list = Post.objects.get_published_posts()[:5]
    return render(request, 'blog/index.html', {'post_list': post_list})


def category_posts(request, category_slug):
    category = get_object_or_404(Category.objects.filter(slug=category_slug),
                                 is_published=True)
    return render(request, 'blog/category.html', {
        'category': category,
        'post_list': category.posts.get_published_posts(),
    })


def post_detail(request, post_id):
    post = get_object_or_404(Post.objects.get_published_posts(), pk=post_id)
    return render(request, 'blog/detail.html', {'post': post})
