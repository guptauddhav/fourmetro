from django import forms
from account.models import User

INVALID_LOGIN_MSG = "The phone number and/or password you entered is invalid."
EMAIL_EXISTS = "This email address is already registered."
USERNAME_EXISTS = "The username already exists."
NO_COOKIES = "Your Web browser doesn't appear to have cookies enabled. " \
             "Enable cookies, then try again."
PHONE_EXISTS = "This phone number is already registered."

class SignUpForm(forms.Form):
    # Registration form.
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    password = forms.CharField(max_length=30, widget=forms.PasswordInput)
    phone_number = forms.IntegerField()
    updates = forms.BooleanField()
    
    def clean_email(self):
        value = self.cleaned_data['email'].lower()
        if User.objects.filter(
                            email=value
                        ).count():
            raise forms.ValidationError(EMAIL_EXISTS)
        return value
    
    def clean_phone_number(self):
        value = self.cleaned_data['phone_number']
        if User.objects.filter(
                            phone_number=value
                        ).filter(
                            is_verified_phone=True     
                        ).count():
            raise forms.ValidationError(PHONE_EXISTS)
        return value
            
        
class LoginForm(forms.Form):
    # Form used for signing in.
    phone_number = forms.IntegerField()
    password = forms.CharField(max_length=30, widget=forms.PasswordInput)
    
    def clean(self):
        """
        Checks if the username and password are valid.
        """
        phone_number = self.cleaned_data.get('phone_number')
        password = self.cleaned_data.get('password')
        
        if phone_number and password:
            self.user = User.objects.user_by_password(phone_number, password)
            if self.user is None:
                raise forms.ValidationError(INVALID_LOGIN_MSG)
            elif not self.user.is_active:
                raise forms.ValidationError(INVALID_LOGIN_MSG)
        
        # Checks if the test cookie during login worked or not.
        if not self.request.session.test_cookie_worked():
            raise forms.ValidationError(NO_COOKIES)
        
        return self.cleaned_data