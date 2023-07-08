import sys
import math
import subprocess
import requests
from bs4 import BeautifulSoup

PREFERRED_STREAMS = ["Vidoza", "Streamtape", "VOE"]

def get_links(url: str):
    all_links = []
    response = requests.get(url)
    assert response.status_code == 200
    parsed = BeautifulSoup(response.content, "html.parser")
    episodes = parsed.find("table", class_="episodes")
    for i, episode in enumerate(episodes.find_all("tr"), start=1):
        links = episode.find_all("td")[-1]
        sorted_links = []
        for link in links.find_all("a"):
            url = link["href"]
            if url.startswith("serie"):
                url = "https://bs.to/" + url
            elif url.startswith("/serie"):
                url = "https://bs.to" + url
            title = link["title"]
            try:
                sorted_links.append((url, PREFERRED_STREAMS.index(title)))
            except ValueError:
                sorted_links.append((url, math.inf))
        if sorted_links:
            min_by_index = min(sorted_links, key=lambda x: x[1])[0]
            all_links.append(min_by_index)
        else:
            print(f"No url found for episode {i}", file=sys.stderr)
    return all_links

if __name__ == "__main__":
    url = sys.argv[1]
    links = get_links(url)
    for link in links:
        print(link)
    try:
        add_links = subprocess.Popen(["JDownloader", "-add-links", *links],  stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        add_links.communicate()
    except Exception:
        print("\nFailed to add links to JDownloader 2")
