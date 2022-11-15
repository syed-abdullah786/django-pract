from django.shortcuts import render
from django.http import HttpResponse
from .models import MeetUps
from .forms import UserForm
from django.views import View
from django.contrib.auth import authenticate

# Create your views here.
def login(request):
    return render(request, 'abpractice/login.html')


class FormCheck(View):

    def get(self, request,hell):
        form = UserForm
        meetings = [
            {'title': 'with Qasim', 'location': 'at Gujrat'},
            {'title': 'with Ahsan', 'location': 'at Lahore'}
        ]
        return render(request, 'abpractice/index.html',
                      {'form': form,
                       'meets': meetings,
                       'show_meets': True})

    def post(self, request, hell):
        form = UserForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            form.save()
            return render(request, 'abpractice/detail.html')

#
# def index(request,hell):
#     if request.method == 'POST':
#         form = UserForm(request.POST)
#         if form.is_valid():
#             print(form.cleaned_data)
#             form.save()
#             return render(request, 'abpractice/detail.html')
#     else:
#         form = UserForm
#
#     met = MeetUps.objects.all()
#     meetings = [
#             {'title': 'with Qasim', 'location': 'at Gujrat'},
#             {'title': 'with Ahsan', 'location': 'at Lahore'}
#         ]
#     return render(request, 'abpractice/index.html',
#                  {'form':form,
#                   'meets': meetings,
#                   'show_meets': True})

def details(request):

    user = authenticate(mailing_address='qasim@gmail.com', city='gujrat')
    if user is not None:
        print('yes user')
    else:
        print('no user')
    met = MeetUps.objects.all()
    return render(request, 'abpractice/detail.html',
                  {
                      'meets': met
                  })
