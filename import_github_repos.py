from git.repo import Repo  # You may need to install the GitPython library: pip install GitPython
import requests
from requests.auth import HTTPBasicAuth
import os
import time
import logging

# GitHub credentials
username = "PUT_YOUR_GITHUB_USERNAME_HERE"
token = "PASTE_YOUR_GENERATED_TOKEN_HERE" 

# GitHub API endpoint
api_endpoint = "https://api.github.com/users/PUT_YOUR_GITHUB_USERNAME_HERE/repos" 

base_path = "PASTE_PATH_OF_LOCAL_FOLDER_WHERE_YOU_WANT_TO_IMPORT_YOUR_REPOS" 

#######################################################################################
#NOTE: **Do not** modify the code below unless you know what changes you want to make: 
#######################################################################################

# Set up logging
# This file saves a txt file, github_clone_repos.txt, on local repos folder recording whether the repo was succesfully cloned/pulled 
log_file_path = os.path.join(base_path, "github_clone_repos.log")
logging.basicConfig(filename=log_file_path, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


# Make a request to get the list of repositories
response = requests.get(api_endpoint, auth=HTTPBasicAuth(username, token))

# Check if the request was successful
if response.status_code == 200:
    repos = response.json()

    # Clone each repository
    for repo in repos:
        repo_name = repo['name']
        repo_url = repo['clone_url']
        repo_path = os.path.join(base_path, repo_name)

        # If the repository doesn't exist locally, clone it
        if not os.path.exists(repo_path):
            try:
                Repo.clone_from(repo_url, repo_path)
                logging.info(f"Repository '{repo_name}' cloned.")
            except Exception as e:
                logging.error(f"Error cloning repository '{repo_name}': {e}")
        else:
            # If the repository exists locally, pull the latest changes
            try:
                local_repo = Repo(repo_path)
                local_repo.remotes.origin.pull()
                logging.info(f"Repository '{repo_name}' updated.")
            except Exception as e:
                logging.error(f"Error updating repository '{repo_name}': {e}")
else:
    logging.error(f"Failed to fetch repositories. Status code: {response.status_code}")


logging.info("All repositories cloned.")
