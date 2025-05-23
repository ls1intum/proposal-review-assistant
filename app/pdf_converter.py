import re
import pymupdf4llm
from langfuse.callback import CallbackHandler

from app.settings import settings
from app.models import get_model


callbacks = []
if settings.langfuse_enabled:
    langfuse_handler = CallbackHandler()
    langfuse_handler.auth_check()
    callbacks.append(langfuse_handler)


ImageModel = get_model(settings.IMAGE_MODEL_NAME)
image_model = ImageModel().with_config(callbacks=callbacks)

FormatModel = get_model(settings.FORMAT_MODEL_NAME)
format_model = FormatModel().with_config(callbacks=callbacks)


def convert_pdf_to_clean_markdown(path: str):
  md_text = pymupdf4llm.to_markdown(path, embed_images=True)
  
  # Replace first four lines
  md_text = re.sub(r'^(.*?\n){4}', '', md_text)

  # Replace page numbers
  md_text = re.sub(r'\n\d+\n', '\n', md_text)

  # Remove image links with OCR descriptions
  while "![]" in md_text:
      data = re.search(r'!\[\]\((.*?)\n\)', md_text)
      message = {
          "role": "user",
          "content": [
              {
                  "type": "text",
                  "text": "Accurately describe the image in detail so a blind person can understand it perfectly:",
              },
              {
                  "type": "image_url",
                  "image_url": { "url": data.group(1) },
              },
          ],
      }
      response = image_model.invoke([message])
      description = "<<< OCR IMAGE DESCRIPTION START >>>\n" + response.content + "\n<<< OCR IMAGE DESCRIPTION END >>>\n"
      md_text = md_text.replace(data.group(0), description)

  # Fix formatting
  result = format_model.invoke(
      [
          { "role": "system", "content": "Fix the line breaks and formatting in the following markdown text. Keep the OCR IMAGE DESCRIPTION intact." },
          { "role": "user", "content": md_text }
      ],
      prediction={"type": "content", "content": md_text },
  )
  return result.content