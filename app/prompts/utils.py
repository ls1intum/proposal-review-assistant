from langfuse import Langfuse
from langchain_core.prompts import PromptTemplate
from app.settings import settings
from logging import getLogger

logger = getLogger(__name__)


def get_prompt(key, fallback):
  # Only initialize Langfuse if credentials are properly configured
  if not settings.langfuse_enabled:
    # Return a simple prompt template if Langfuse is not enabled
    def get_fallback_prompt():
      return PromptTemplate.from_template(fallback)
    return get_fallback_prompt

  langfuse = Langfuse()

  try:
    langfuse.get_prompt(key)
  except Exception as e:
    logger.warning(f"Failed to fetch prompt '{key}' from Langfuse: {e}")
    try:
      langfuse.create_prompt(
        name=key,
        prompt=fallback,
        labels=["production"],
      )
    except Exception as create_error:
      logger.warning(f"Failed to create prompt '{key}' in Langfuse: {create_error}")
      # Fall back to local prompt if Langfuse is unavailable
      def get_fallback_prompt():
        return PromptTemplate.from_template(fallback)
      return get_fallback_prompt

  def get_fresh_prompt():
    try:
      langfuse_prompt = langfuse.get_prompt(
        key,
        fallback=fallback,
        cache_ttl_seconds=30
      )

      return PromptTemplate.from_template(
        langfuse_prompt.get_langchain_prompt(),
        metadata={"langfuse_prompt": langfuse_prompt},
      )
    except Exception as e:
      logger.warning(f"Failed to fetch fresh prompt '{key}' from Langfuse: {e}")
      # Fall back to local prompt
      return PromptTemplate.from_template(fallback)
  
  return get_fresh_prompt