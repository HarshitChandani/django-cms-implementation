from django.conf import settings
from django.shortcuts import get_object_or_404, HttpResponse

from cms.utils import get_current_site
from cms.models.pagemodel import Page
from cms.models.titlemodels import Title


def getPageTemplate(manual_template=None, page_id=None):

    cms_templates = "CMS_TEMPLATES"
    templates = getattr(settings, cms_templates)

    if len(templates) == 1:
        return templates[0][0]

    if manual_template and manual_template in [pair[0] for pair in templates]:
        return manual_template

    if page_id is not None:
        pageQuery = get_object_or_404(Page, pk=page_id)
        return pageQuery.template

    return templates[0][0]


def get_page_from_path(site, path):
    from cms.models.titlemodels import Title

    titles = Title.objects.select_related('page__node')
    titles = titles.filter(published=True)
    titles = titles.filter(path=(path or ''))
    for title in titles.iterator():

        # If use is authenticated then the use can view also non-published pages
        return title.page
    return


def get_page_from_request(request, use_path=None, clean_path=None):

    path = request.path_info if use_path is None else use_path
    site = get_current_site()
    page = get_page_from_path(site, path)
    return page


def duplicate_slug_check(slug=None):
    if slug is None:
        return False
    titles = Title.objects.filter(slug=slug).exists()
    if titles:
        return False
    else:
        return True
