from django.contrib import admin
from .models import Campaign, Volunteer

@admin.register(Campaign)
class CampaignAdmin(admin.ModelAdmin):
    list_display = ['title', 'goal_amount', 'collected_amount', 'start_date', 'end_date']
    list_filter = ['start_date', 'end_date']
    search_fields = ['title', 'description']
    
    # Calcul automatique du pourcentage
    def progress_percentage(self, obj):
        if obj.goal_amount > 0:
            return f"{(obj.collected_amount / obj.goal_amount * 100):.1f}%"
        return "0%"
    progress_percentage.short_description = "Progression"

@admin.register(Volunteer)
class VolunteerAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'message']
    search_fields = ['name', 'email']
    list_filter = []




#admin admin