# %%
import os
import PIL.Image
from google import genai

# %%
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
sysprompt = """
              This is a digital image of an old mathematical statistics textbook. Extract the text from the image and return it in valid LaTeX format. Do not include any latex class or package declarations; I will add them later (amsart/amsmath/amssymb etc). Think carefully about the formatting of the equations and the text, ignore equation and section numbers, newlines, and spacing. Return the raw LaTeX code.
              """.replace("\n", " ").strip()
# %%


def convert_page(
    pgno,
    sysprompt=sysprompt,
    mod="gemini-2.0-flash-lite",
):
    """
    Convert a page of the PDF to an image and extract text using Gemini.
    """
    # Load the image
    image_path = f"pdf_images/Pfanzagl_1982_page_{pgno}.png"
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Image {image_path} not found.")
    # Open the image
    image = PIL.Image.open(f"pdf_images/Pfanzagl_1982_page_{pgno}.png")
    # send the image to the model
    try:
        response = client.models.generate_content(
            model=mod, contents=[sysprompt, image]
        )
    except genai.errors.APIError as e:
        print(f"Error in Gemini response: {e.message}")
        return None
    if response.text is not None:
        # Extract the text
        outstring = (
            response.text.replace("\n", " ")
            .replace(r"\\", r"\\")
            .replace("```", "")
            .replace("latex", "")
        )
        # write the output to a file
        with open(f"raw_tex/Pfanzagl_1982_page_{pgno}.tex", "w") as f:
            f.write(outstring)


# %%
for i in range(100, 105):
    convert_page(i)
    os.sleep(1)

# %%
