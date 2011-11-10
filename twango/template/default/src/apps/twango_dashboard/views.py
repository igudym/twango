from django.shortcuts import render_to_response

def index(request):
    """
    you will have to replace "index.html"
    with (yourappname)/index.html
    and createa folder named (yourappname) in the templates directory.
    """    

    return render_to_response('twango/app_index.html')
