import google.generativeai as genai
import logging

# Set up Gemini API key
GEMINI_API_KEY = "AIzaSyBt1yAxMXHVekKZVl_Png28Wc_KO42jmZc"  # Replace with your actual API key
genai.configure(api_key=GEMINI_API_KEY)

def change_tone(summaries, tone="comedy"):
    """
    Modify the tone of multiple summaries using the Gemini API.

    :param summaries: A list of summaries.
    :param tone: The desired tone ("comedy", "satirical", etc.).
    :return: A list of modified summaries in the specified tone.
    """
    try:
        if not summaries:
            return []

        prompt = f"Rewrite the following news summaries in a {tone} tone while keeping them meaningful and coherent:\n\n"

        for idx, summary in enumerate(summaries):
            prompt += f"{idx + 1}. {summary}\n\n"

        # Sending a single API request
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(prompt)

        if response.text:
            # Splitting response into individual summaries
            modified_summaries = response.text.strip().split("\n\n")

            # Ensure response count matches input count
            if len(modified_summaries) != len(summaries):
                logging.warning("Mismatch in modified summaries count. Returning original summaries.")
                return summaries  # Fallback to original summaries if API response is incomplete

            return modified_summaries

        return summaries  # Return original summaries if API fails

    except Exception as e:
        logging.error(f"Error in change_tone: {str(e)}")
        return summaries  # Return original summaries on failure
