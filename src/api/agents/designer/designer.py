import prompty
import prompty.azure
import json
from pathlib import Path
from openai import AzureOpenAI
from azure.identity import DefaultAzureCredential, get_bearer_token_provider

def image_gen(image_prompt):
    import os
    import requests

    token_provider = get_bearer_token_provider(
        DefaultAzureCredential(), "https://cognitiveservices.azure.com/.default"
    )

    client = AzureOpenAI(
        azure_endpoint = f"https://mmhan-m2xchnk3-australiaeast.openai.azure.com/openai/deployments/dall-e-3/images/generations?api-version=2024-02-01", 
        api_version="2024-02-01",
        azure_ad_token_provider=token_provider
    )


    result = client.images.generate(
        model="dall-e-3", # the name of your DALL-E 3 deployment
        prompt=image_prompt,
        n=1
    )

    json_response = json.loads(result.model_dump_json())

    # Set the directory for the stored image
    image_dir = os.path.join(os.curdir, 'images')

    # If the directory doesn't exist, create it
    if not os.path.isdir(image_dir):
        os.mkdir(image_dir)

    # Initialize the image path (note the filetype should be png)
    image_path = os.path.join(image_dir, 'generated_image.png')

    # Retrieve the generated image
    image_url = json_response["data"][0]["url"]  # extract image URL from response
    generated_image = requests.get(image_url).content  # download the image
    with open(image_path, "wb") as image_file:
        image_file.write(generated_image)

    return image_path


def design(article, instructions="Generate a detailed prompt that helps a writer create a unique image for their story."):
    result = prompty.execute(
        "designer.prompty",
        inputs={"article": article, "instructions": instructions}
    )

    image_location = image_gen(result)

    return image_location


if __name__ == "__main__":
    from dotenv import load_dotenv

    load_dotenv()

    # base = Path(__file__).parent

    # products=json.loads(Path(base / "products.json").read_text())
    article= """
    Winter Camping: Embracing the Chill with Cool Trends and Cozier Gear
    Winter camping? That's right! As we bundle up and marvel at snow-laden landscapes, more and more outdoor enthusiasts are heading into the frosty wilderness for a different kind of adventure. With the latest trends and gear making it not just bearable but delightful, let's dive into what's hot (or should we say warm?) in the realm of cold-weather camping.
    Tranquility by the Water
    Imagine waking up to a frosty morning with a serene lake or a flowing river right at your doorstep. That's the trend catching on fast among winter campers—seeking tranquility by the water. Sites near lakes, rivers, or coastal areas are gaining popularity not just for their breathtaking winter beauty but also for activities like icy kayaking or simply meditating by the shore. (MSN).
    Warm and Waterproof Gear
    Now, for those braving the chill, staying warm is non-negotiable. The essentials? A warm sleeping quarter and waterproof camping gear. The right gear makes the experience from a frosty challenge to a cozy, snow-laden retreat. (MSN)
    Tents that Turn the Cold Away
    Choosing the right tent is critical for any winter camping trip. Take for instance the Alpine Explorer Tent. This tent is a fortress against the cold with its waterproof build and adjustable vents that keep out the frost while maintaining airflow to stave off condensation. Interested in star-gazing or catching the silhouette of snowflakes against the night sky? The SkyView 2-Person Tent promises not just a shelter but an immersive outdoor experience with its durable, waterproof materials and mesh panels for stargazing (SkyView 2-Person Tent).
    Sleeping Bags for Dreamy Nights
    Don't just sleep; dream warmly with the right sleeping bag. The CozyNights Sleeping Bag or the MountainDream Sleeping Bag both offer comfort but cater to slightly different needs. While CozyNights ensures comfort in slightly warmer conditions, MountainDream is a winner for the hardcore winter campe. Its synthetic insulation keeps you snug in temperatures as low as 15°F. Its mummy shape is not only a heat retainer but also reduces packing bulk, making it an excellent companion for those snowy reaches (MountainDream Sleeping Bag).
    S'mores and Stories
    No camping trip, winter or not, is complete without the quintessential campfire treat—s'mores! As you curl up in your CozyNights Sleeping Bag, indulge in crafting that perfect s'more. A little heat from the fire, a piece of chocolate, and you're not just surviving the winter; you're thriving in it (NHK World).
    Balancing the Chill with Thrills
    The thrill seekers aren't left out in the cold either. Many winter campers bring along skis or snowshoes, turning their camping site into a base camp for snowy escapades. This blend of high-octane day activities with peaceful, starry nights by the campfire creates a winter camping experience that’s both balanced and exhilarating.
    Conclusion
    So, whether it's the calm by a frozen lakeside or the thrill of icy adventures, winter camping is more than just enduring the cold; it's about embracing and enjoying it. With the right gear like the Alpine Explorer Tent and the MountainDream Sleeping Bag, you're not only geared up for winter but ready to enjoy it to its fullest. This winter, step out, set up camp, bask in the icy air, and yes, enjoy that s'more—you've earned it!
    """

    image_location = design(
        article,
        "Generate a detailed prompt that helps a writer create a unique image for their story.")
    
    print(f"Open image in {image_location}")

