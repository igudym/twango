from django.db import models


class Section(models.Model):
	"""
	
	"""
	
	title = models.CharField(max_length=80)
	def __unicode__(self):
		return self.title