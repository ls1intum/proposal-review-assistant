from langfuse import Langfuse
from langchain_core.prompts import PromptTemplate


def get_prompt(key, fallback):
  langfuse = Langfuse()

  try:
    langfuse.get_prompt(key)
  except:
    langfuse.create_prompt(
      name=key,
      prompt=fallback,
      labels=["production"],
    )

  def get_fresh_prompt():
    langfuse_prompt = langfuse.get_prompt(
      key,
      fallback=fallback,
      cache_ttl_seconds=30
    )

    return PromptTemplate.from_template(
      langfuse_prompt.get_langchain_prompt(),
      metadata={"langfuse_prompt": langfuse_prompt},
    )
  
  return get_fresh_prompt