from django.contrib import admin
from models import *

class BlockInline(admin.TabularInline):
	model = Block

class SectionAdmin(admin.ModelAdmin):
	inlines = [
		BlockInline
	]
	
admin.site.register(Block)

admin.site.register(Section, SectionAdmin)
admin.site.register(Template)

