import subprocess

def run_node_script(usernames):
    # Run the Node.js script with the provided usernames
    subprocess.run(['node', 'scraper.js'] + usernames, check=True)

# List of GitHub usernames
usernames = ['aarcee17', 'spurjhattam2207', 'iteles']

# Run the script for the list of usernames
run_node_script(usernames)
