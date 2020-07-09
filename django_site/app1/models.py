from django.db import models


class Product(models.Model):
    name = models.CharField(verbose_name='产品', max_length=32, unique=True, default='')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "产品"
        verbose_name_plural = "产品"
        # ordering = ["-datetime"]

class Project(models.Model):
    name = models.CharField(verbose_name='项目', max_length=32, unique=True, default='')
    product = models.ForeignKey(verbose_name='所属产品', to=Product, on_delete=models.PROTECT, default=1, parent_link=True)
    configs = models.TextField(verbose_name='配置', blank=True, default='')
    datetime = models.DateTimeField(verbose_name='修改日期', auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "项目"
        verbose_name_plural = "项目"
