from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone

User = get_user_model()


class PostQuerySet(models.QuerySet):
    def get_published_posts(self):
        return self.select_related(
            'location', 'author', 'category'
        ).filter(
            pub_date__range=(
                self.aggregate(
                    first_date=models.Min('pub_date'))['first_date'],
                timezone.now()
            ),
            is_published=True,
            category__is_published=True
        )


class PostManager(models.Manager):
    def get_queryset(self):
        return PostQuerySet(self.model)

    def get_published(self):
        return self.get_queryset().get_published_posts()


class PublicationModel(models.Model):
    is_published = models.BooleanField(
        verbose_name='Опубликовано',
        default=True,
        help_text='Снимите галочку, чтобы скрыть публикацию.'
    )
    created_at = models.DateTimeField(verbose_name='Добавлено',
                                      auto_now_add=True)

    class Meta:
        abstract = True


class Category(PublicationModel):
    title = models.CharField(verbose_name='Заголовок', max_length=256)
    description = models.TextField(verbose_name='Описание')
    slug = models.SlugField(
        verbose_name='Идентификатор',
        help_text=('Идентификатор страницы для URL; разрешены символы '
                   'латиницы, цифры, дефис и подчёркивание.'),
        unique=True
    )

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return (f'|Пост: {self.title[:20]}... \n'
                f'|Описание: {self.description[:40]}...')


class Location(PublicationModel):
    name = models.CharField(verbose_name='Название места', max_length=256)

    class Meta:
        verbose_name = 'местоположение'
        verbose_name_plural = 'Местоположения'

    def __str__(self):
        return f'{self.name[:20]}...'


class PostForeiginKey(models.ForeignKey):
    def __init__(self, to=None, on_delete=models.CASCADE,
                 related_name='posts', **kwargs):
        super().__init__(to, on_delete, related_name, **kwargs)


class Post(PublicationModel):
    title = models.CharField(verbose_name='Заголовок', max_length=256)
    text = models.TextField(verbose_name='Текст')
    pub_date = models.DateTimeField(
        verbose_name='Дата и время публикации',
        help_text=('Если установить дату и время в будущем — можно делать '
                   'отложенные публикации.'),
    )
    author = PostForeiginKey(
        User,
        verbose_name='Автор публикации',
    )
    location = PostForeiginKey(
        Location,
        verbose_name='Местоположение',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    category = PostForeiginKey(
        Category,
        verbose_name='Категория',
        on_delete=models.SET_NULL,
        null=True,
    )
    objects = PostManager()

    class Meta:
        verbose_name = 'публикация'
        verbose_name_plural = 'Публикации'
        ordering = ('-pub_date', 'title')

    def __str__(self):
        return f'|Пост: {self.title[:20]}...\n|Текст: {self.text[:40]}...'
