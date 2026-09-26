import os
from dotenv import load_dotenv
from openai import OpenAI
import argparse
from prompts import system_prompt
from call_function import available_functions
from call_function import call_function
import json

load_dotenv()
api_key = os.environ.get("OPENROUTER_API_KEY")

if not api_key:
    raise RuntimeError("Could not load Openrouter API Key. Make sure it is set in .env")

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key,
)

parser = argparse.ArgumentParser(description="Chatbot")
parser.add_argument("user_prompt", type=str, help="User prompt")
parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
args = parser.parse_args()
# Now we can access `args.user_prompt`

messages = [
    {"role": "system", "content": system_prompt},
    {"role": "user", "content": args.user_prompt},
]

for _ in range(20):

    response = client.chat.completions.create(
        model="openrouter/free",
        messages= messages,
        tools=available_functions,
        temperature=0,
    )

    if not response.usage.prompt_tokens:
        raise RuntimeError("Request failed, please repeat.")

    if args.verbose:
        print(f"User prompt: {args.user_prompt}")
        print(f"Prompt tokens: {response.usage.prompt_tokens}")
        print(f"Response tokens: {response.usage.completion_tokens}")

    message = response.choices[0].message
    messages.append(message)
    if message.tool_calls:
        for tool_call in message.tool_calls:
            function_args = json.loads(tool_call.function.arguments or "{}")
            #print(f"Calling function: {tool_call.function.name}({function_args})")
            result_message = call_function(tool_call, args.verbose)
            if not result_message["content"]:
                raise Exception("Tool call did not return any result.")
            if args.verbose:
                print(f"-> {result_message['content']}")
            messages.append(result_message)
    else:
        print(message.content)
        break
    if _ == 19:
        exit(1)
