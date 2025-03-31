from openai import OpenAI

def classify(name,
             input_text=None, 
             api_key=None, 
             baseprompt=None,
             model='gpt-4-0125-preview', 
             temperature=0,
             top_p = 0,
             logprobs=None,
             max_length=250000,
             base_url=None):
    
    if base_url is not None:
        client = OpenAI(
                        api_key=api_key,
                        base_url=base_url
                        )

    else:
        client = OpenAI(
                        api_key=api_key
                        )

    # split_base = baseprompt.split("COMPOUND_NAME")
    user_prompt = str(name) + "\n" + str(input_text)
    user_prompt = user_prompt[:max_length]

    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "system", "content": baseprompt}, {"role": "user", "content": user_prompt}],
        temperature=temperature,
        top_p=top_p,
        logprobs=logprobs,
        stream=False
        )
    
    if logprobs:
        return response.choices[0].message.content, response.choices[0].logprobs
    else:
        return response.choices[0].message.content