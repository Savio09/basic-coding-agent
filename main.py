import sys

from call_function import available_functions, call_function
from prompts import system_prompt

MAX_ITERATIONS = 20


def main():
    import os
    from dotenv import load_dotenv
    from openai import OpenAI
    import argparse

    load_dotenv()
    api_key = os.environ.get("OPENROUTER_API_KEY")

    if api_key == None:
        raise RuntimeError("Ensure you add your own api key")

    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key
    )

    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": args.user_prompt},
    ]

    if args.verbose:
        print(f"User prompt: {args.user_prompt}")

    for _ in range(MAX_ITERATIONS):
        response = client.chat.completions.create(
            model="nvidia/nemotron-3-ultra-550b-a55b:free",
            messages=messages,
            tools=available_functions,
            temperature=0,
        )

        usable = response.usage
        if not usable:
            raise RuntimeError("There was an error with this request")

        if args.verbose:
            print(f"Prompt tokens: {usable.prompt_tokens}")
            print(f"Response tokens: {usable.completion_tokens}")

        message = response.choices[0].message
        messages.append(message)

        if not message.tool_calls:
            print("Final response:")
            print(message.content)
            return message.content

        for tool_call in message.tool_calls:
            result_message = call_function(tool_call, verbose=args.verbose)
            if not result_message.get("content"):
                raise RuntimeError(
                    f"Function {tool_call.function.name} returned no content"
                )
            if args.verbose:
                print(f"-> {result_message['content']}")
            messages.append(result_message)

    print(f"Error: no final response after {MAX_ITERATIONS} iterations")
    sys.exit(1)


if __name__ == "__main__":
    main()
