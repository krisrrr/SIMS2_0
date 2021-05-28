from django.shortcuts import redirect


def index_too(request):
    return redirect('activity/')
