from django.shortcuts import render_to_response, redirect
from django.template import Template, RequestContext
import urls
import time

def index(request):
	from urls import urlpatterns
	from conf.g_added_apps import *
	
	installed_apps = INSTALLED_APPS
	iap = ()
	
	#List the set of installed apps
	for installed_app in installed_apps:
		 iap += (installed_app.split('.')[-1],) #remove the app package info
	
	#Handle Base Actions
	if request.method == 'POST':
		"""
		We got a post request, now lets start creating our new app
		the system should log the event, since its a cli operation.
		"""
		app_name = request.POST['appname']
		from django.core.management import call_command
		call_command('initapp',app_name)
		time.sleep(1.0)
		return redirect("/"+app_name.replace(".","/")+"/")
	
	return render_to_response('twango/index.html',{'installed_apps':iap},context_instance=RequestContext(request))

#for now we don't need csrf
from django.contrib.csrf.middleware import csrf_exempt
index = csrf_exempt(index)