from django.db import models


class Person(models.Model):
    name       = models.CharField(verbose_name='姓名', max_length=32, unique=True, default='')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '人物'
        verbose_name_plural = verbose_name


class Book(models.Model):
    name       = models.CharField(verbose_name='书名', max_length=32, unique=True, default='')
    abstract   = models.TextField(verbose_name='摘要', blank=True, default='')
    author     = models.ForeignKey(Person, on_delete=models.PROTECT, verbose_name='作者', related_name='book_set', null=True, blank=True)
    reader_set = models.ManyToManyField(to=Person, verbose_name='读者', related_name='read_book_set', blank=True)
    datetime   = models.DateTimeField(verbose_name='修改日期', auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '书籍'
        verbose_name_plural = verbose_name
        ordering = ["-datetime"]

