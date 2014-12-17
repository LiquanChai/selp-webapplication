from django.test import TestCase
 
from django.contrib.auth.models import User
from usermgt import forms


class UsermgtTests(TestCase):
    """
    Test the model and manager used in the default backend.
    
    """
    user_info = {'username': 'liquanchai',
                 'password': '1234567890',
                 'email': 'liquanchai@example.com'}
    
    def setUp(self):
    	pass

    def tearDown(self):
    	pass

    def test_registration_form(self):
        """
        Test that ``RegistrationForm`` enforces username constraints
        and matching passwords.
        """
        # Create a user so we can verify that duplicate usernames aren't
        # permitted.
        User.objects.create_user('liquanchai', 'liquanchai@example.com', 'secret')

        invalid_data_dicts = [
            # Non-alphanumeric username.
            {'data': {'username': 'foo/bar',
                      'email': 'foo@haha.com',
                      'password1': 'foo',
                      'password2': 'foo'},
            'error': ('username', [u"This value may contain only letters, numbers and @/./+/-/_ characters."])},
            # Already-existing username.
            {'data': {'username': 'liquanchai',
                      'email': 'liquanchai@haha.com',
                      'password1': 'secret',
                      'password2': 'secret'},
            'error': ('username', [u"A user with that username already exists."])},
            # Mismatched passwords.
            {'data': {'username': 'foo',
                      'email': 'foo@example.com',
                      'password1': 'foo',
                      'password2': 'bar'},
            'error': ('__all__', [u"The two password fields didn't match."])},
            ]

        for invalid_dict in invalid_data_dicts:
            form = forms.RegistrationForm(data=invalid_dict['data'])
            self.failIf(form.is_valid())
            self.assertEqual(form.errors[invalid_dict['error'][0]],
                             invalid_dict['error'][1])

        form = forms.RegistrationForm(data={'username': 'foo',
                                            'email': 'foo@haha.com',
                                            'password1': 'foo',
                                            'password2': 'foo'})
        self.failUnless(form.is_valid())
 
