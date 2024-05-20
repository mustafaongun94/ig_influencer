from .models import Influencer, Post, Story
from django.contrib import admin
from .models import Influencer

class InfluencerAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        if not change and Influencer.objects.count() >= 20:
            self.message_user(request, "You can only have up to 20 influencers.", level='error')
        else:
            super().save_model(request, obj, form, change)


admin.site.register(Influencer, InfluencerAdmin)
admin.site.register(Post)
admin.site.register(Story)
