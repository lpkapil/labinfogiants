from django.http import JsonResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from app_wp_plugin_server.models import License, Plugin
from django.utils import timezone
import json

@method_decorator(csrf_exempt, name='dispatch')
class CheckPluginUpdateAPIView(View):
    def post(self, request, *args, **kwargs):
        # Parse JSON data from the request body
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({"status": "error", "message": "Invalid JSON"}, status=400)
        
        # Retrieve license_key and plugin_name from the parsed data
        license_key = data.get('license_key', None)
        plugin_name = data.get('plugin_name', None)
        action = data.get('action', None)
        
        # Check if both arguments are provided
        if not license_key:
            return JsonResponse({"status": "error", "message": "License key is required"}, status=400)
        
        if not plugin_name:
            return JsonResponse({"status": "error", "message": "Plugin name is required"}, status=400)
        
        # Validate the license_key
        try:
            license = License.objects.get(license_key=license_key)
        except License.DoesNotExist:
            return JsonResponse({"status": "error", "message": "Invalid license key"}, status=400)
        
        # Check if the license has expired
        if license.valid_till < timezone.now():
            return JsonResponse({"status": "error", "message": "License has expired"}, status=400)
        
        # Validate if the license is associated with the correct plugin
        try:
            plugin = Plugin.objects.get(title=plugin_name)
        except Plugin.DoesNotExist:
            return JsonResponse({"status": "error", "message": "Invalid plugin name"}, status=400)
        
        # Check if the license is for the provided plugin
        if license.plugin != plugin:
            return JsonResponse({"status": "error", "message": "License key is not valid for the given plugin"}, status=400)
        

        if plugin_name == 'ig-feedback':
            if action == 'info':
                response = {
                    "slug": "ig-feedback",
                    "version": "1.1",
                    "new_version": "1.1",
                    "author": "Kapil Yadav",
                    "name": "IG Feedback",
                    "text_domain": "ig-feedback",
                    "description": "A simple plugin for user feedback collection.",
                    "homepage": "https://example.com/plugin",
                    "plugin_uri": "https://example.com/plugin-uri",
                    "requires": "6.0",
                    "tested": "6.7.1",
                    "requires_php": "7.0",
                    "download_url": "https://example.com/plugin/download.zip",
                    "downloaded": 12540,
                    "last_updated": "2025-01-21",
                    "sections": {
                        "description": "The new version of the IG Feedback plugin",
                        "changelog": "Some new features by Kapil Yadav",
                        "custom": "This is custom section"
                    },
                    "banners": {
                        "low": "http://infogiants.com/plugins/auto-update-plugin/banner-772x250.jpg",
                        "high": "http://infogiants.com/plugins/auto-update-plugin/banner-1544x500.jpg"
                    },
                    "download_link": "https://example.com/plugin/update.zip",
                    "url": "https://example.com/plugin/update.zip",
                    "package": "https://example.com/plugin/update.zip",
                    "requires_php": "7.0",
                    "requires_mysql": "5.6",
                    "license": "GPLv2 or later"
                }
            else:
                response = {
                    "slug": "ig-feedback",
                    "version": "1.1",
                    "new_version": "1.1",
                    "author": "Kapil Yadav",
                    "name": "IG Feedback",
                    "text_domain": "ig-feedback",
                    "description": "A simple plugin for user feedback collection.",
                    "homepage": "https://example.com/plugin",
                    "plugin_uri": "https://example.com/plugin-uri",
                    "requires": "6.0",
                    "tested": "6.7.1",
                    "requires_php": "7.0",
                    "download_url": "https://example.com/plugin/download.zip",
                    "downloaded": 12540,
                    "last_updated": "2025-01-21",
                    "sections": {
                        "description": "The new version of the IG Feedback plugin",
                        "changelog": "Some new features by Kapil Yadav",
                        "custom": "This is custom section"
                    },
                    "banners": {
                        "low": "http://infogiants.com/plugins/auto-update-plugin/banner-772x250.jpg",
                        "high": "http://infogiants.com/plugins/auto-update-plugin/banner-1544x500.jpg"
                    },
                    "download_link": "https://example.com/plugin/update.zip",
                    "url": "https://example.com/plugin/update.zip",
                    "package": "https://example.com/plugin/update.zip",
                    "requires_php": "7.0",
                    "requires_mysql": "5.6",
                    "license": "GPLv2 or later"
                }

        if plugin_name == 'ig-topbar':
            if action == 'info':
                response = {
                    "slug": "ig-topbar",
                    "version": "1.1",
                    "new_version": "1.1",
                    "author": "Kapil Yadav",
                    "name": "IG TopBar",
                    "text_domain": "ig-topbar",
                    "description": "A simple plugin for topbar.",
                    "homepage": "https://example.com/plugin",
                    "plugin_uri": "https://example.com/plugin-uri",
                    "requires": "6.0",
                    "tested": "6.7.1",
                    "requires_php": "7.0",
                    "download_url": "https://example.com/plugin/download.zip",
                    "downloaded": 12540,
                    "last_updated": "2025-01-21",
                    "sections": {
                        "description": "The new version of the IG TopBar plugin",
                        "changelog": "Some new features by Kapil Yadav",
                        "custom": "This is custom section123"
                    },
                    "banners": {
                        "low": "http://infogiants.com/plugins/auto-update-plugin/banner-772x250.jpg",
                        "high": "http://infogiants.com/plugins/auto-update-plugin/banner-1544x500.jpg"
                    },
                    "download_link": "https://example.com/plugin/update.zip",
                    "url": "https://example.com/plugin/update.zip",
                    "package": "https://example.com/plugin/update.zip",
                    "requires_php": "7.0",
                    "requires_mysql": "5.6",
                    "license": "GPLv2 or later"
                }
            else:
                response = {
                    "slug": "ig-topbar",
                    "version": "1.1",
                    "new_version": "1.1",
                    "author": "Kapil Yadav",
                    "name": "IG TopBar",
                    "text_domain": "ig-topbar",
                    "description": "A simple plugin for feedback.",
                    "homepage": "https://example.com/plugin",
                    "plugin_uri": "https://example.com/plugin-uri",
                    "requires": "6.0",
                    "tested": "6.7.1",
                    "requires_php": "7.0",
                    "download_url": "https://example.com/plugin/download.zip",
                    "downloaded": 12540,
                    "last_updated": "2025-01-21",
                    "sections": {
                        "description": "The new version of the IG TopBar plugin",
                        "changelog": "Some new features by Kapil Yadav",
                        "custom": "This is custom section123"
                    },
                    "banners": {
                        "low": "http://infogiants.com/plugins/auto-update-plugin/banner-772x250.jpg",
                        "high": "http://infogiants.com/plugins/auto-update-plugin/banner-1544x500.jpg"
                    },
                    "download_link": "https://example.com/plugin/update.zip",
                    "url": "https://example.com/plugin/update.zip",
                    "package": "https://example.com/plugin/update.zip",
                    "requires_php": "7.0",
                    "requires_mysql": "5.6",
                    "license": "GPLv2 or later"
                }
        
        

        return JsonResponse(response)


        # If all checks pass
        # return JsonResponse({
        #     "status": "success", 
        #     "message": "License key and plugin name are valid", 
        #     "data": {
        #         "license_key": license_key,
        #         "plugin_name": plugin_name
        #     }
        # })
