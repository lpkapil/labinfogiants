from django import forms
from django.contrib import admin
from app_wp_plugin_server.models import Plugin, PluginCategory, PluginVersion, License

# Register your models here.

# Register the PluginCategory model
class PluginCategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)  # Display the category name in the list
    search_fields = ('name',)  # Allow searching by category name

    class Meta:
        verbose_name = "Plugin Category"  # Singular name
        verbose_name_plural = "Plugin categories"  # Plural name
        ordering = ['name']  # Order categories alphabetically

# Custom form for the Plugin model to display active_version as a select
class PluginAdminForm(forms.ModelForm):
    class Meta:
        model = Plugin
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # If the instance is not being created (i.e., it's being edited), display the active_version field
        if not self.instance.pk:  # Instance is being created (Add Plugin view)
            self.fields['active_version'].widget = forms.HiddenInput()  # Hide active_version in Add view
            self.fields['active_version'].widget.attrs['style'] = 'display: none;'
        else:
            # When editing, filter PluginVersion based on the current Plugin instance
            active_version = forms.ModelChoiceField(
                queryset=PluginVersion.objects.filter(plugin=self.instance),  # Filter by current plugin instance
                required=False,
                empty_label="Select a version",  # Optional: label for "no version selected"
                widget=forms.Select(attrs={'class': 'vTextField'})
            )
            self.fields['active_version'] = active_version  # Add the active_version field to the form


# Register the Plugin model with the custom form
class PluginAdmin(admin.ModelAdmin):
    list_display = ('title', 'github_repo_url', 'category', 'active_version')  # Display the title, URL, and category
    search_fields = ('title', 'github_repo_url', 'category__name')  # Search by title, URL, or category name
    list_filter = ('category',)  # Allow filtering by category
    form = PluginAdminForm  # Use the custom form for the Plugin model

class LicenseAdmin(admin.ModelAdmin):
    list_display = ('plugin', 'user', 'license_key', 'valid_till', 'created_at')
    list_filter = ('user', 'plugin')  # Add filters by user and plugin  
    # readonly_fields = ('license_key',)  # Make license_key read-only in the admin

# Register both models with the admin site
admin.site.register(PluginCategory, PluginCategoryAdmin)
admin.site.register(Plugin, PluginAdmin)
admin.site.register(License, LicenseAdmin)
