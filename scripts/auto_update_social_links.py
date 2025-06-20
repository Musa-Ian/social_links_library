import requests
from bs4 import BeautifulSoup
import re
import json
from datetime import datetime
import os
from github import Github
from dotenv import load_dotenv

SOCIAL_LINKS_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '../data/social_links.json'))

# Load environment variables
load_dotenv()
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
GITHUB_REPO = os.getenv('GITHUB_REPO')  # e.g. 'username/repo'

# --- Pattern Scraping Functions ---
def fetch_instagram_pattern():
    url = "https://help.instagram.com/370452623149242"
    resp = requests.get(url)
    soup = BeautifulSoup(resp.text, "html.parser")
    links = [a['href'] for a in soup.find_all('a', href=True) if "instagram.com" in a['href']]
    for link in links:
        match = re.match(r"https://(www\\.)?instagram\\.com/([A-Za-z0-9_.]+)/?", link)
        if match:
            return "https://instagram.com/{username}"
    return None

def fetch_twitter_pattern():
    # Twitter's help page for usernames
    url = "https://help.twitter.com/en/managing-your-account/how-to-change-your-username"
    resp = requests.get(url)
    soup = BeautifulSoup(resp.text, "html.parser")
    # Look for example links
    links = [a['href'] for a in soup.find_all('a', href=True) if "twitter.com" in a['href']]
    for link in links:
        match = re.match(r"https://(www\\.)?twitter\\.com/([A-Za-z0-9_]+)/?", link)
        if match:
            return "https://twitter.com/{username}"
    return None

def fetch_facebook_pattern():
    # Facebook's help page for profile links
    url = "https://www.facebook.com/help/203305893040179"
    resp = requests.get(url)
    soup = BeautifulSoup(resp.text, "html.parser")
    links = [a['href'] for a in soup.find_all('a', href=True) if "facebook.com" in a['href']]
    for link in links:
        match = re.match(r"https://(www\\.)?facebook\\.com/([A-Za-z0-9.]+)/?", link)
        if match:
            return "https://facebook.com/{username}"
    return None

# --- Community Signal Functions ---
def search_github_issues(platform):
    url = f"https://api.github.com/search/issues?q={platform}+profile+link+changed+in:title,body&sort=updated&order=desc"
    resp = requests.get(url)
    data = resp.json()
    results = []
    for item in data.get("items", []):
        results.append({"title": item['title'], "url": item['html_url']})
    return results

def search_stackoverflow(platform):
    url = f"https://api.stackexchange.com/2.3/search?order=desc&sort=activity&intitle={platform}+profile+link+changed&site=stackoverflow"
    resp = requests.get(url)
    data = resp.json()
    results = []
    for item in data.get("items", []):
        results.append({"title": item['title'], "url": item['link']})
    return results

# --- JSON Update & PR Functions ---
def load_current_patterns():
    with open(SOCIAL_LINKS_PATH, "r") as f:
        return json.load(f)

def save_patterns(patterns):
    with open(SOCIAL_LINKS_PATH, "w") as f:
        json.dump(patterns, f, indent=2)

def update_pattern(platform, new_pattern):
    patterns = load_current_patterns()
    updated = False
    for p in patterns:
        if p["platform"] == platform and p["url_pattern"] != new_pattern:
            print(f"Pattern change detected for {platform}: {p['url_pattern']} -> {new_pattern}")
            p["url_pattern"] = new_pattern
            p["last_verified"] = datetime.now().strftime("%Y-%m-%d")
            updated = True
    if updated:
        save_patterns(patterns)
        print("Patterns updated.")
    return updated

def create_pull_request(branch_name, commit_message, pr_title, pr_body):
    if not GITHUB_TOKEN or not GITHUB_REPO:
        print("GitHub token or repo not set. Skipping PR creation.")
        return
    g = Github(GITHUB_TOKEN)
    repo = g.get_repo(GITHUB_REPO)
    # Get default branch
    default_branch = repo.default_branch
    # Create new branch from default
    sb = repo.get_branch(default_branch)
    repo.create_git_ref(ref=f"refs/heads/{branch_name}", sha=sb.commit.sha)
    # Update file in new branch
    with open(SOCIAL_LINKS_PATH, "r") as f:
        content = f.read()
    element = repo.get_contents("data/social_links.json", ref=branch_name)
    repo.update_file(element.path, commit_message, content, element.sha, branch=branch_name)
    # Create PR
    pr = repo.create_pull(title=pr_title, body=pr_body, head=branch_name, base=default_branch)
    print(f"Pull Request created: {pr.html_url}")

def main():
    changes = []
    # --- Scrape and update patterns ---
    for platform, fetch_func in [
        ("instagram", fetch_instagram_pattern),
        ("twitter", fetch_twitter_pattern),
        ("facebook", fetch_facebook_pattern)
    ]:
        new_pattern = fetch_func()
        if new_pattern:
            updated = update_pattern(platform, new_pattern)
            if updated:
                changes.append(platform)
    # --- Community signals ---
    for platform in ["instagram", "twitter", "facebook"]:
        print(f"\nCommunity signals for {platform}:")
        gh_issues = search_github_issues(platform)
        so_posts = search_stackoverflow(platform)
        for issue in gh_issues[:3]:
            print(f"GitHub: {issue['title']} - {issue['url']}")
        for post in so_posts[:3]:
            print(f"StackOverflow: {post['title']} - {post['url']}")
    # --- PR if changes ---
    if changes:
        branch = f"auto/social-link-update-{datetime.now().strftime('%Y%m%d%H%M%S')}"
        commit_msg = f"Auto-update social link patterns: {', '.join(changes)}"
        pr_title = commit_msg
        pr_body = f"Automated update for: {', '.join(changes)}.\n\nPlease review the changes."
        create_pull_request(branch, commit_msg, pr_title, pr_body)
    else:
        print("No pattern changes detected. No PR created.")

if __name__ == "__main__":
    main()

# TODO: Extend to more platforms and sources (Wikipedia, Reddit, Twitter API, etc.) 