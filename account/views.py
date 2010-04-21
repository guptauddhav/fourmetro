# Create your views here.
from django import http
from django.template.loader import render_to_string

from util.view_utils import fm_render
from account.forms import SignUpForm
from account import utils

####################################
# UTILITIES USED BY MULTIPLE VIEWS #
####################################

# These utilities encapsulate some logic used by both the registration
# workflow and the "I forgot my password" workflow.
class BadHash(Exception):
    def __init__(self, response):
        self.response = response

def confirm_request_hash(request, task):
    if request.method == 'GET':
        d = request.GET
    elif request.method == 'POST':
        d = request.POST
    else:
        raise http.Http404('Invalid method')
    
    # Verify the hash.
    try:
        email, email_hash = d['e'], d['h']
        if email_hash != utils.make_email_hash(email, task):
            raise KeyError
    except KeyError:
        form_link = {utils.CREATE_TASK: '/accounts/register/', 
                     utils.RESET_TASK: '/accounts/password-change/'}[task]
        response = http.HttpResponseNotFound(
                            render_to_string('accounts/hash_error.html', 
                                             {'form_link': form_link}))
    
def send_confirmation_and_redirect(request, email, task):
    email_activation_key = utils.make_email_hash(email, task)
    phone_activation_code = utils.make_verify_phone_code()
    u = utils.create_user(
                    name=request.POST.get('name'), 
                    password=request.POST.get('password'), 
                    email=request.POST.get('email'), 
                    phone_number=request.POST.get('phone_number'), 
                    phone_activation_code=phone_activation_code, 
                    email_activation_key=email_activation_key)
    u.save()
    utils.send_verification_email(email, task)
    return http.HttpResponseRedirect('/account/email-sent/')

########################
# REGISTRATION PROCESS #
########################

def register(request):
    # If the user is already logged in, redirect to the dashboard.
    # TODO: add user object to request.
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            return send_confirmation_and_redirect(request, 
                                                  form.cleaned_data['email'], 
                                                  utils.CREATE_TASK)
    else:
        form = SignUpForm()
    return fm_render(request, 'account/register_form.html', {'form': form})

def confirm_email(request):
    try:
        email, email_hash = confirm_request_hash(request, utils.CREATE_TASK)
    except BadHash, e:
        return e.response