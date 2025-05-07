from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic.detail import DetailView

# Create your views here.

def PostList(request):
    return HttpResponse('Welcome to-postlist-')

#PostDetail
def PostDetail(request,idea = None):

    main_idea = idea
    if not idea % 2 == 0:
        idea += 1
        return  HttpResponse(
            f"your idea after changng gets:{idea}"
        )
    return HttpResponse(
        f"your idea doesn't need to change///{main_idea}"
    )
# --- Class Base View for PostDetail --- #
class PostDetail(DetailView):
model = Blog


###
def PostListByYear(request,year):
    return HttpResponse(f"year is : {year}")

### regex in url ###
def ArchiveByYear(request,year = None):
    return HttpResponse(f"You chose year :{year}")

