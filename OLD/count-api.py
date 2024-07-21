import requests

# Set the base URL and endpoint
base_url = "http://c0a21099-ja-0701.a910.tak-cslab.org"
endpoint = "/wp-json/wp-statistics/v2/hit"

# Define the page URIs you want to get view counts for
page_uris = [
    "http://c0a21099-ja-0701.a910.tak-cslab.org/",
    "http://c0a21099-ja-0701.a910.tak-cslab.org/archives/5881",
    # Add more URIs as needed
]

# Function to get view count for a specific page URI
def get_view_count(page_uri):
    url = f"{base_url}{endpoint}"
    params = {"page_uri": page_uri}
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"}
    response = requests.get(url, params=params, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        print(f"API response for {page_uri}: {data}")
        return data.get('count', 0)  # Assuming 'count' holds the view count
    else:
        print(f"Failed to retrieve data: {response.status_code}")
        print(response.json())
        return 0

# Retrieve view counts for all specified URIs
view_counts = {}
for uri in page_uris:
    view_counts[uri] = get_view_count(uri)

# Print the retrieved view counts
for uri, count in view_counts.items():
    print(f"View count for {uri}: {count}")