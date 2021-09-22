from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from django.utils.text import slugify
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils.translation import ugettext_lazy as _


class Menu(models.Model):
    title = models.CharField(_('title'), max_length=128)
    slug = models.CharField(max_length=64, default='', blank=True, unique=True)
    footer = models.BooleanField(default=True, verbose_name='footerga qoyish')
    header = models.BooleanField(default=True, verbose_name='headerda qoyish')

    def __str__(self):
        return f'{self.title}'


class Footer(models.Model):
    phone = models.CharField(_('phone'), max_length=18)
    mail = models.EmailField(max_length=32)
    full_address = models.CharField(_('full_address'), max_length=255)
    copyright = models.CharField(_('copyright'), max_length=256)
    address_link = models.URLField(null=True, blank=True)

    youtube = models.URLField(max_length=64, null=True, blank=True)
    facebook = models.URLField(max_length=64, null=True, blank=True)
    telegram = models.URLField(max_length=64, null=True, blank=True)
    instagram = models.URLField(max_length=64, null=True, blank=True)


class Region(models.Model):
    title = models.CharField(max_length=50)

    def __str__(self):
        return self.title


class District(models.Model):
    title = models.CharField(_('title'), max_length=50)
    region = models.ForeignKey(Region,
                               verbose_name=_('region'), on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Mahalla(models.Model):
    title = models.CharField(_('title'), max_length=50)
    district = models.ForeignKey(District, verbose_name=_('district'), on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.title


class TreeType(models.Model):
    title = models.CharField(_('title'), max_length=50)

    def __str__(self):
        return self.title


class Tree(models.Model):
    title = models.CharField(_('title'), max_length=100)
    type = models.ForeignKey(TreeType, verbose_name=_('tree-type'), on_delete=models.CASCADE)
    price = models.PositiveIntegerField(validators=[MinValueValidator(0)])

    def __str__(self):
        return f'{self.title}-{self.type}'


class Blank(models.Model):
    choices = [
        (1, 'Click'),
        (2, 'Payme'),
        (3, 'Apelsin'),
    ]
    region = models.ForeignKey(Region, verbose_name=_('region'), on_delete=models.CASCADE)
    district = models.ForeignKey(District, verbose_name=_('district'), on_delete=models.CASCADE)
    mahalla = models.ForeignKey(Mahalla, verbose_name=_('mahalla'), on_delete=models.CASCADE, null=True, blank=True)
    social_media_url = models.URLField()
    payment_type = models.IntegerField(choices=choices, null=True)

    def __str__(self):
        return f'{self.region} blank'


class TreeBlank(models.Model):
    blank = models.ForeignKey(Blank, verbose_name=_('blank'), on_delete=models.CASCADE, related_name='trees')
    tree = models.ForeignKey(Tree, verbose_name=_('tree'), on_delete=models.CASCADE)
    amount = models.PositiveIntegerField(validators=[MinValueValidator(1)])

    # price = models.IntegerField(default)
    def __str__(self):
        return f'{self.blank}-{self.tree}'


class LeganEntity(models.Model):
    name = models.CharField(_('name'), max_length=100)
    image = models.ImageField(upload_to='legal')
    hover_image = models.ImageField(upload_to='hover-legal')

    def __str__(self):
        return f'{self.name}'


class MostPlanted(models.Model):
    choices = [
        (1, 'Instagram'),
        (2, 'Facebook'),
        (3, 'Twitter'),
        (4, 'Telegram'),
    ]

    type = models.IntegerField(choices=choices, default=1)
    account_link = models.URLField()
    name = models.CharField(_('name'), max_length=100, default='insta_name')
    image = models.ImageField(upload_to='most_planted')
    # image_url = models.URLField(null=True,blank=True,max_length=400)
    username = models.CharField(_('username'), max_length=50)
    tree_amount = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f'{self.name} - {self.tree_amount}'


class Index(models.Model):
    s1_title = models.CharField(_('s1_title'), max_length=200, null=True, blank=True)
    s1_description = models.CharField(_('s1_description'), max_length=200, null=True, blank=True)
    s1_btn_text = models.CharField(_('s1_btn_text'), max_length=16, null=True, blank=True)
    s1_image = models.ImageField(upload_to='index', null=True, blank=True)
    s1_slug = models.SlugField(max_length=250, null=True, unique=True, blank=True)

    s2_title = models.CharField(_('s2_title'), max_length=200, null=True, blank=True)
    s2_description = models.CharField(_('s2_description'), max_length=200, null=True, blank=True)
    s2_btn_text = models.CharField(_('s2_btn_text'), max_length=16, null=True, blank=True)
    s2_image = models.ImageField(upload_to='index', null=True, blank=True)
    s2_slug = models.SlugField(max_length=250, null=True, unique=True, blank=True)

    s3_title = models.CharField(_('s3_title'), max_length=200, null=True, blank=True)
    s3_description = models.CharField(_('s3_description'), max_length=200, null=True, blank=True)
    s3_btn_text = models.CharField(_('s3_btn_text'), max_length=16, null=True, blank=True)
    s3_image = models.ImageField(upload_to='index', null=True, blank=True)
    s3_slug = models.SlugField(max_length=250, null=True, unique=True, blank=True)


class RegionStatistics(models.Model):
    region = models.ForeignKey(Region, verbose_name=_('region'), on_delete=models.CASCADE)
    image = models.ImageField(upload_to='region', blank=True, null=True)
    donated_trees = models.PositiveIntegerField(default=0, validators=[MinValueValidator(0)])
    donated_people = models.PositiveIntegerField(default=0, validators=[MinValueValidator(0)])
    planted_trees = models.PositiveIntegerField(default=0, validators=[MinValueValidator(0)])
    on_plan_planting = models.PositiveIntegerField(default=0, validators=[MinValueValidator(0)])

    def __str__(self):
        return f'{self.region} statistic'


class StaticPage(models.Model):
    title = models.CharField(_('Title'), max_length=255)
    content = RichTextUploadingField(_('Kontent'))
    slug = models.SlugField(max_length=255, verbose_name='slug')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('Static page')
        verbose_name_plural = _('Static pages')

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if hasattr(self, 'slug') and hasattr(self, 'title'):  # edit
            if self.slug:
                pass
            else:
                self.slug = generate_unique_slug(self.__class__, self.title)
        super(StaticPage, self).save(*args, **kwargs)


def generate_unique_slug(klass, field):
    """
    return unique slug if origin slug is exist.
    eg: foo-bar => foo-bar-1

    :param klass is Class model.
    :param field is specific field for title.
    """
    origin_slug = slugify(field)
    unique_slug = origin_slug
    numb = 1
    while klass.objects.filter(slug=unique_slug).exists():
        unique_slug = '%s-%d' % (origin_slug, numb)
        numb += 1
    return unique_slug


# class BaseModel(models.Model):
#     created_at = models.DateTimeField(auto_now=True,null=True)

class ContactForm(models.Model):
    name = models.CharField(max_length=255, default="")
    phone = models.CharField(max_length=30, default="")
    email = models.EmailField(default="")
    text = models.TextField(max_length=1000, default="")
    created_at = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Feedback')
        verbose_name_plural = _('Feedbacks')
