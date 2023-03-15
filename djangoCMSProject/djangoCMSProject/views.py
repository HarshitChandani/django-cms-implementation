from django.shortcuts import render, HttpResponse, redirect
from django.template.defaultfilters import slugify
from django.contrib.auth.decorators import login_required

from cms.utils import get_current_site
from cms.models.pagemodel import TreeNode
# from cms.utils.conf import get_cms_setting
from cms.utils.page_permissions import user_can_change_page

from djangoCMSProject.utils.index import getPageTemplate, get_page_from_request, duplicate_slug_check


def viewPage(request, slug):
    site = get_current_site()  # Return current site in form of domain.
    page = get_page_from_request(request, use_path=slug)  # Return Page
    # # Check If nodes are available in site.
    treeNodes = TreeNode.objects.get_for_site(site)

    if not page and not slug and not treeNodes.exists():
        # No page|Slug|No Node is available then render welcome page
        # welcome.html is not available yet.
        return render(request, template_name="page/welcome.html")

    if not page:
        # no_page.html is not available yet.
        return render(request, template_name="page/no_page.html")
    if page.login_required and not request.user.is_authenticated():
        return redirect("authentication:login")
    template = getPageTemplate(manual_template=None, page_id=page.id)
    return render(request, template)


def AddPageForm(request):
    return render(request, "page/add.html")


def handleAddPageRequest(request):
    from cms.api import create_page, add_plugin
    from cms import constants

    if (request.method == "POST"):
        title, menu_title, isPagePublished, page_content = request.POST["title"], request.POST[
            "menu-title"], request.POST.getlist("isPagePublished"), request.POST["page-content"]

        slug = slugify(title)
        if not slug:
            return HttpResponse("Slug will not empty")

        if not duplicate_slug_check(slug):
            return HttpResponse("Invalid Slug.")

        menu_title = menu_title.lower()
        template = getPageTemplate()
        published = True if isPagePublished[0] == 'true' else False
        site = get_current_site()
        language = 'en'
        pluginType = 'TextPlugin'
        newPage = create_page(title=title, template=template, language=language, menu_title=menu_title,
                              slug=slug, apphook=None, apphook_namespace=None, redirect=None, meta_description=None, created_by='python-api', site=site, published=published, login_required=False,
                              limit_visibility_in_menu=constants.VISIBILITY_ALL,
                              position='first-child')

        # No need to add IF condition as we are not including log-in functionality

        # if request.user.is_authenticated and newPage.placeholders.has_add_plugin_permission(User):

        placeholders = newPage.placeholders.get(slot='content')

        # if newPage.placeholders.has_add_plugin_permission(User):
        add_plugin(placeholders, pluginType, language, body=page_content)
        return redirect("/")


@login_required
def editPageContent(request, slug):
    # In Web content editing mode.
    if request.user.is_authenticated():
        page = get_page_from_request(request, use_path=slug)
        if user_can_change_page(request.user, page):
            # User can edit this page.
            pass

        else:
            print("User didn't has permissions to edit the page content.")
            return HttpResponse("User didn't has permissions to edit the page content.")
