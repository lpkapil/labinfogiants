from django.db import models
from django.contrib.auth.models import User

class PluginVersion(models.Model):
    plugin = models.ForeignKey('Plugin', on_delete=models.CASCADE, related_name="versions")  # No need to change this unless you want a custom related_name
    version = models.CharField(max_length=100)  # For example, "v1.0.0"
    file_data = models.BinaryField()  # Path to the zip file for the version form git using private access
    
    class Meta:
        unique_together = ('plugin', 'version')  # Prevent duplication of version for the same plugin

    def __str__(self):
        return f"{self.version}"

class PluginCategory(models.Model):
    # Name of the category (e.g., "SEO", "Security", "Performance", etc.)
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Plugin Categories"
        ordering = ['name']  # Order by the 'name' field in ascending order


class Plugin(models.Model):
    # Title of the Plugin
    title = models.CharField(max_length=255)

    # GitHub Repository URL
    github_repo_url = models.CharField(max_length=255, unique=True)

    # Category of the plugin (related to PluginCategory model)
    category = models.ForeignKey(PluginCategory, on_delete=models.CASCADE, related_name="plugins")

    # Field to store the selected version as a ForeignKey to PluginVersion
    active_version = models.ForeignKey(PluginVersion, null=True, blank=True, on_delete=models.SET_NULL, related_name="active_for_plugins")  # Changed related_name

    def __str__(self):
        return self.title


class License(models.Model):
    plugin = models.ForeignKey(Plugin, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    license_key = models.CharField(max_length=255, unique=True)
    valid_till = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"License for {self.plugin.title} by {self.user.username}"