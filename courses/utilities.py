from django.utils.text import slugify


def course_slug(model_instance, title, slug):
    slug = slugify(title)
    model = model_instance.__class__

    while model._default_manager.filter(slug=slug).exists():
        course_pk = model._default_manager.latest('pk')
        new_course_pk = course_pk.pk + 1
        slug = '{}-{}'.format(slug, new_course_pk)
    return slug
