from django.shortcuts import render_to_response, render
from models import *


def template(request,template_id=1):
	"""
	you will have to replace "index.html"
	with (yourappname)/index.html
	and createa folder named (yourappname) in the templates directory.
	"""	   
	
	#required functions:
	#Add Row
	#Remove Row
	#Add cell
	#remove cell

	#for now - we just	
	sections = Section.objects.filter(template=template_id) 
	
	if request.method == 'POST':
		
		# possible actions from here:
		# Add a new block to a section
		# remove a block from a section
		if 'section' in request.POST.keys():
			# We are now either adding a block, removing a block, or gettin a section
			if 'add_block' in request.POST.keys():
				section = Section.objects.get(id=request.POST['section'])
				block = Block()
				block.section=section
				block.width=request.POST['add_block']
				block.title="-untitled-"
				block.save()
				
		
		else:
			section = Section()
			section.template_id=template_id
			section.save()
		

	return render(request,'grid_designer/index.html',{'sections':sections})

