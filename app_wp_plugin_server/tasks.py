from celery import shared_task
from app_wp_plugin_server.models import Plugin
import time
from app_wp_plugin_server.services.git_service import GitRepoTagsFetcher
from app_wp_plugin_server.models import Plugin

# wroker task
@shared_task
def populate_plugin_versions(data):
    """
    Loops through all plugins and fetches the tags from GitHub.
    For each plugin, it calls the GitRepoTagsFetcher to store versions.

    :param auth_token: The personal access token to authenticate the GitHub API calls.
    """
    # Get all plugin objects
    plugins = Plugin.objects.all()

    for plugin in plugins:
        print(f"Processing plugin: {plugin.title} ({plugin.id})")

        # Initialize GitRepoTagsFetcher for each plugin
        fetcher = GitRepoTagsFetcher(plugin_id=plugin.id, auth_token=auth_token)

        # Fetch and store versions for the current plugin
        plugin_versions = fetcher.fetch_tags_with_download_urls()

        if plugin_versions:
            print(f"Successfully stored versions for plugin {plugin.title}")
        else:
            print(f"No new versions found or skipped for plugin {plugin.title}")

# download and save images
# @shared_task
# def download_save_docs(data):
#     from .mywork_images import LoadALCData
#     processor = LoadALCData()
#     returned_result = processor.download_and_save_gia_docs(data)
#     return returned_result


# # every 5 seconds
# @shared_task(bind=True)
# def process_mywork_queue(self):
#     task_name = self.name
#     lock, created = TaskLock.objects.get_or_create(task_name=task_name)
#     if created:
#         from .mywork_images import LoadALCData
#         processor = LoadALCData()
#         returned_result = processor.process_imports_job_webhook()
#         time.sleep(1)
#         lock.delete()
#         return returned_result
#     else:
#         print(f"{task_name} is already running, skipping...")
#         return [f"{task_name} is already running, skipping..."]


# # every 5 minutes
# @shared_task(bind=True)
# def schedule_mywork_jobs_docs_delete(self):
#     task_name = self.name
#     lock, created = TaskLock.objects.get_or_create(task_name=task_name)
#     if created:
#         from .mywork_images import LoadALCData
#         processor = LoadALCData()
#         returned_result = processor.schedule_import_jobs_docs_delete()
#         time.sleep(1)
#         lock.delete()
#         return returned_result
#     else:
#         print(f"{task_name} is already running, skipping...")
#         return [f"{task_name} is already running, skipping..."]