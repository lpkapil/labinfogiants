import requests
from django.db import IntegrityError
from app_wp_plugin_server.models import PluginVersion, Plugin  # Import the models

class GitRepoTagsFetcher:
    def __init__(self, plugin_id, auth_token=None):
        """
        Initializes the GitRepoTagsFetcher.
        
        :param plugin_id: The ID of the Plugin instance to associate with the version.
        :param auth_token: Personal Access Token for Git authentication (if using private repositories).
        """
        self.plugin_id = plugin_id  # Plugin ID to associate with the version
        self.auth_token = auth_token

        # Fetch the plugin instance to get the repository URL
        self.plugin = Plugin.objects.get(id=self.plugin_id)
        self.repo_url = self.plugin.github_repo_url  # Get the GitHub repo URL from the plugin

        # Strip the '.git' part from the URL to get the repository name
        self.repo_api_url = f"https://api.github.com/repos/{self._get_repo_name()}/tags"
        
        # Print out the URL for debugging purposes
        print(f"API URL: {self.repo_api_url}")

    def _get_repo_name(self):
        """
        Extracts the repository name from the GitHub URL, removing the '.git' suffix if present.
        """
        # Remove '.git' from the end of the URL if it exists
        repo_name = self.repo_url.strip('.git').split("https://github.com/")[-1]
        return repo_name

    def fetch_tags_with_download_urls(self):
        """
        Fetches all tags and their corresponding download zip URLs from the repository using the GitHub API.
        
        :return: List of PluginVersion objects that have been created or updated.
        """
        headers = {
            'Authorization': f'Bearer {self.auth_token}',  # Authentication header using Bearer token
            'Accept': 'application/vnd.github+json',  # Accept header for GitHub API response
            'X-GitHub-Api-Version': '2022-11-28',  # GitHub API version header
            'User-Agent': 'python'  # User-Agent header to avoid GitHub blocking the request
        }

        # Make a GET request to GitHub API to get the tags
        response = requests.get(self.repo_api_url, headers=headers)

        # Check if the response is successful
        if response.status_code != 200:
            raise Exception(f"Error fetching tags: {response.status_code}, {response.text}")
        
        # Parse the response to get tags
        tags_data = response.json()

        plugin_version_instances = []
        
        # Download the zip file for each tag and store it in the database as binary data
        for tag in tags_data:
            tag_name = tag['name']
            repo_name = self._get_repo_name()  # Get the repository name for the zip file
            download_url = f"https://github.com/{repo_name}/archive/refs/tags/{tag_name}.zip"

            # Check if the version already exists for the plugin
            if PluginVersion.objects.filter(plugin_id=self.plugin_id, version=tag_name).exists():
                print(f"Version {tag_name} already exists for plugin {self.plugin_id}. Skipping.")
                continue  # Skip to the next tag if the version already exists

            # Debugging: Print the download URL and status
            print(f"Attempting to download {tag_name} from {download_url}")

            response = requests.get(download_url, headers=headers)
            if response.status_code == 200:
                # Create a new PluginVersion instance
                try:
                    # Create and save the new PluginVersion instance
                    plugin_version = PluginVersion.objects.create(
                        plugin=self.plugin,
                        version=tag_name,
                        file_data=response.content  # Store the zip file content (binary data)
                    )
                    plugin_version_instances.append(plugin_version)
                    print(f"Version {tag_name} successfully downloaded and stored in the database.")
                except IntegrityError:
                    # Handle the case where a duplicate version might still be inserted due to race conditions
                    print(f"Duplicate entry found for version {tag_name} in the database.")
            else:
                # Log the error if download fails
                print(f"Failed to download {tag_name}. Status code: {response.status_code}. Response: {response.text}")

        return plugin_version_instances
