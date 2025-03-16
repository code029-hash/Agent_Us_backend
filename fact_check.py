import aiohttp
import asyncio
import json
from extract_claim import extract_main_claim

# Google Fact Check API Key (Make sure it's correct)
FACT_CHECK_API_KEY = "your_api_key_here"

async def check_google_fact_check(claim):
    """Check the claim using Google Fact Check API."""
    google_url = f"https://factchecktools.googleapis.com/v1alpha1/claims/search?query={claim}&key={FACT_CHECK_API_KEY}"

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(google_url) as response:
                status_code = response.status
                data = await response.json()

                print(f"\n📢 API Response Status: {status_code}")
                print(f"📢 API Response Data: {json.dumps(data, indent=2)}\n")

                if status_code != 200:
                    return "Error"

                if "claims" in data and len(data["claims"]) > 0:
                    for claim in data["claims"]:
                        if claim.get("claimReview"):
                            for review in claim["claimReview"]:
                                rating = review.get("textualRating", "").lower()
                                if "true" in rating or "verified" in rating:
                                    return "Verified"
                                elif "false" in rating or "misleading" in rating:
                                    return "Unverified"

                return "Disputed"
    except Exception as e:
        print(f"⚠️ Exception: {str(e)}")
        return "Error"

async def fact_check(news_summary):
    """Extracts claim and checks it using Google Fact Check API."""
    claim = extract_main_claim(news_summary)
    print(f"\n🔍 Extracted Claim: {claim}\n")
    return await check_google_fact_check(claim)

# Example usage
async def main():
    summary = "NASA confirms signs of alien life on Mars."
    result = await fact_check(summary)
    print(f"\n✅ Fact Check Result: {result}\n")
