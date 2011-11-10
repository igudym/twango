"""
Defines the user-stored defaults for the new twango app.
"""
from django.db import models


class Template(models.Model):
	"""
	
	"""
	
	title = models.CharField(max_length=80)
	def __unicode__(self):
		return self.title

class Section(models.Model):
	"""
	
	"""
	
	title = models.CharField(max_length=80, blank=True)
	template = models.ForeignKey(Template)
	
	@property 
	def blocks(self):
		return Block.objects.filter(section=self)
		
	def __unicode__(self):
		return "Section "+str(self.id)+" "+self.title

class Block(models.Model):
	"""

	"""

	title = models.CharField(max_length=80)
	width = models.IntegerField()
	style = models.TextField(null=True,blank=True)
	section = models.ForeignKey(Section)
	order = models.IntegerField( null=True, blank=True )
	
	class Meta:
		ordering = ('order',)
		
	def __unicode__(self):
		return self.title

