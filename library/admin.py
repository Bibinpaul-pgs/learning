from django.contrib import admin

from library.models import User, Book, IssueBook

# Register your models here.

# admin.site.register(User)
admin.site.register(Book)
admin.site.register(IssueBook)