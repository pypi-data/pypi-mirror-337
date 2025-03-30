def generate_text(prompt: str, model="default"):
    """
    Generates text from a given prompt using a specified LLM.

    Args:
        prompt: The text prompt to feed to the LLM.
        model:  The identifier of the LLM to use (default: "default").

    Returns:
        The generated text response.
    """
    
    if model == "default":
        return f"Generated text for prompt: {prompt} (using default model)"
    else:
        return f"Generated text for prompt: {prompt} (using model: {model})"