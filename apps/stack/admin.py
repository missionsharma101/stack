from django.contrib import admin

from apps.stack.models import *

admin.site.register(User)
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(Reply)



