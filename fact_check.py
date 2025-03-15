import requests

def fact_check(query):
    """Fetch fact-check information for a given query using Google Fact Check API."""
    API_KEY = "YOUR_API_KEY"  # Replace with your actual API key
    url = f"https://factchecktools.googleapis.com/v1alpha1/claims:search?query={query}&key={API_KEY}"

    try:
        response = requests.get(url)
        data = response.json()

        if "claims" not in data:
            return "No fact-checking results found."

        results = []
        for claim in data["claims"]:
            text = claim["text"]
            rating = claim["claimReview"][0]["textualRating"] if "claimReview" in claim and claim["claimReview"] else "Not Rated"
            publisher = claim["claimReview"][0]["publisher"]["name"] if "claimReview" in claim and claim["claimReview"] else "Unknown Publisher"
            results.append(f"Claim: {text}\nRating: {rating}\nPublisher: {publisher}\n")

        return "\n".join(results)

    except Exception as e:
        return f"Error fetching fact check: {str(e)}"

# Example usage
query = "Donald Trump election fraud"
print(fact_check(query))
