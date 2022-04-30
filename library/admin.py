
from django.contrib import admin

from .models import Account,Book,Borrow,BorrowRules,BookInstance,BookReview

# Register your models here.
class BookInstanceInline(admin.TabularInline):
    model = BookInstance

class BookAdmin(admin.ModelAdmin):
    list_display = ('isbn','title','author','publisher','storage',)
    inlines = [BookInstanceInline]
    list_filter = ['author','publisher']
    search_fields = ['isbn','title','author','publisher']

class AccountInline(admin.TabularInline):
    model = Account

class BorrowRulesAdmin(admin.ModelAdmin):
    list_display = ('id','bor_period','day_fine','quota')
    inlines = [AccountInline]

class BorrowAdmin(admin.ModelAdmin):
    model = Borrow
    list_display = ('id','account','bookins','bor_time','bor_status','return_date','is_expired','f','fine')
    list_filter = ['bor_status','account']
    list_editable = ('bor_status','f')
    search_fields = ['id']

class BorrowInline(admin.TabularInline):
    model = Borrow
    list_display=('bookins','bor_time','bor_status','return_date')

class AccountAdmin(admin.ModelAdmin):
    list_display = ('id','accoount_name','account_pwd','register_time','account_satus','keeping_num','current_fine','fine_filt')
    list_editable = ('account_satus',)
    list_filter = ['account_satus','register_time']
    search_fields = ['accoount_name']
    inlines = [BorrowInline]
    def check_success(self, request, queryset):
        queryset.update(account_satus='N')
    check_success.short_description = "use permission"

    def freeze_account(self, request, queryset):
        queryset.update(account_satus='F')
    freeze_account.short_description = 'freeze account'
    actions = ['check_success','freeze_account']


admin.site.register(Book, BookAdmin)
admin.site.register(BorrowRules, BorrowRulesAdmin)
admin.site.register(Account,AccountAdmin)
admin.site.register(Borrow,BorrowAdmin)
admin.site.register(BookReview)
