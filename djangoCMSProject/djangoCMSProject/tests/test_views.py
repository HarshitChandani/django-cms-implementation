from django.test import Client, RequestFactory
from django.urls import reverse
from django.contrib.auth.models import User, AnonymousUser
from django.contrib.sessions.middleware import SessionMiddleware


from cms.test_utils.testcases import CMSTestCase
from cms.api import create_page
from cms.models.pagemodel import Page

from djangoCMSProject.views import handleAddPageRequest
from djangoCMSProject.utils.index import get_page_from_request, get_page_from_path, getPageTemplate
from authentication.views import handle_login, handle_signup, handle_logout


class ViewTestCase(CMSTestCase):

    def setUp(self):
        self.client = Client()

    def test_render_add_page_form_template(self):
        # Test the rendering of correct and proper template.

        url = reverse('add-page-form')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'page/add.html')

    def test_correct_slug_ednpoint_redirect(self):
        # To test whether the page is being redirected properly according to the slug.

        create_page("celebaltech", "playground.html",
                    'en', published=True)

        response = self.client.get("/celebaltech")
        self.assertEqual(response.status_code, 200)

    def test_get_page_from_path(self):

        # Test the get_page_from_path function in utils file.

        create_page("one", "playground.html",
                    'en', published=True)
        create_page("two", "playground.html", 'en', published=True)
        page_1 = get_page_from_path(None, "one")
        page_2 = get_page_from_path(None, "two")
        self.assertIsInstance(page_1, Page)
        self.assertIsInstance(page_2, Page)

    def test_get_page(self):
        # Test the return type of get_path_from_request funtion

        request = {
            'path_info': '/'
        }
        create_page("microsoft", "playground.html",
                    'en', published=True)
        slug1 = "microsoft"
        page = get_page_from_request(request, use_path=slug1)
        self.assertIsInstance(page, Page)
        self.assertEqual(page.login_required, False)
        self.assertEqual(page.is_home, False)

    def test_get_page_template(self):

        # Test the get_page_template function of utils file

        page_1 = create_page("page_1", "fullwidth.html", 'en', published=True)
        page_2 = create_page("page_2", "playground.html", 'en', published=True)

        pageTemplate_1 = getPageTemplate(
            manual_template=None, page_id=page_1.id)
        page_template_2 = getPageTemplate(
            manual_template="playground.html", page_id=page_2.id)

        self.assertEqual(pageTemplate_1, "fullwidth.html")
        self.assertNotEqual(page_template_2, "fullwidth.html")


class AuthenticationTestCase(CMSTestCase):

    def setUp(self):
        self.credentials = {
            'username': 'admin',
            'password': 'admin',
            'email': 'harshitchandani144@gmail.com'
        }
        # Create a WSGI Factory instance.
        self.factory = RequestFactory()
        self.user = User.objects.create_user(**self.credentials)
        self.user.save()

    def test_auth_default_url_redirect(self):
        response = self.client.get("/auth/")
        self.assertTemplateUsed(response, "login.html")
        self.assertEqual(response.status_code, 200)

    def test_auth_signup_url_redirect(self):
        response = self.client.get("/auth/signup/")
        self.assertTemplateUsed(response, "register.html")
        self.assertEqual(response.status_code, 200)

    def test_auth_login_process(self):
        '''
            Test the handle_login function view
            Summary: handle_login function handles all the login process used for authentication.
        '''
        values = {
            'username': 'admin',
            'password': 'admin'
        }

        # WSGI request instance for the post method.
        # WSGI request would not use an middleware.
        request = self.factory.post('/auth/login/', data=values)

        # type of request.user is the instance of User Model without any values .
        request.user = AnonymousUser()

        # Add session attribute to the request for the creating the session after login.
        middleware = SessionMiddleware(request)
        middleware.process_request(request)
        request.session.save()

        # Disable CSRF checks.
        request._dont_enforce_csrf_checks = True

        response = handle_login(request)
        self.assertEqual(response.status_code, 302)

        # (Optional).If we check redirect then we have to add client attribute in response .
        response.client = Client()
        self.assertRedirects(response, '/')

    def test_auth_signup_process(self):
        '''
            Test the handle_signup function view.
            Summary: handle_signup function handles the signup process used for authentication.
        '''

        new_user_values = {
            'first_name': 'Martin',
            'last_name': 'Garrix',
            'username': 'martin.garrix@celebaltech.com',
            'password': 'martin'
        }
        # WSGI request instance for the post method.
        request = self.factory.post('/auth/register/', data=new_user_values)

        # AnonymousUser
        request.user = AnonymousUser()

        # Disable CSRF checks.
        request._dont_enforce_csrf_checks = True

        response = handle_signup(request)
        self.assertEqual(response.status_code, 302)

        old_user_values = {
            'first_name': 'Martin',
            'last_name': 'Garrix',
            'username': 'admin',
            'password': 'admin'
        }
        request_1 = self.factory.post('/auth/register/', data=old_user_values)

        request_1.user = AnonymousUser()
        request_1._dont_enforce_csrf_checks = True
        response_1 = handle_signup(request_1)
        self.assertEqual(response_1.status_code, 200)

    def test_auth_logout_process(self):
        '''
            Test the handle_logout function view.
            Summary: handle_logout function handles the logout process.
        '''
        request = self.factory.get('/auth/logout')
        request.user = self.user

        # Session Middleware
        middleware = SessionMiddleware(request)
        middleware.process_request(request)
        request.session.save()

        response = handle_logout(request)
        self.assertEqual(response.status_code, 302)

        # (Optional): If we check on redirects
        response.client = Client()
        self.assertRedirects(response, "/")
