from django.contrib import admin
from .models import Question,DTSF01,DTSF02,DTSF03,DTSF04
# from .models import Question
# Register your models here.

admin.site.register(Question)
admin.site.register(DTSF01)
admin.site.register(DTSF02)
admin.site.register(DTSF03)
admin.site.register(DTSF04)