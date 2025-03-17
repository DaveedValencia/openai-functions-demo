from openai import OpenAI
import json
from assistant_tools import beast_mode

api_key = "OPEN-AI-API-KEY"
org = "OPEN-AI-ORG-ID"
assistant_id = "ASSISTANT-ID"

client = OpenAI(api_key=api_key, organization=org)

USER_INPUT = "Why is the moon white? in beast mode"

thread = client.beta.threads.create()

message = client.beta.threads.messages.create(
    thread_id=thread.id,
    role="user",
    content=USER_INPUT
)

run = client.beta.threads.runs.create_and_poll(
    thread_id=thread.id,
    assistant_id=assistant_id
)

if run.status == 'completed':
    messages = client.beta.threads.messages.list(thread_id=thread.id)
    response = json.loads(messages.data[0].content[0].text.value)
    print(response['response'])

elif run.status == 'requires_action':
    tool_outputs = []
    for tool in run.required_action.submit_tool_outputs.tool_calls:
        if tool.function.name == 'beast_mode':
            user_args = json.loads(tool.function.arguments)
            print(user_args['user_input'])

            tool_response = beast_mode(user_args['user_input'])

            tool_outputs.append({
                "tool_call_id": tool.id,
                "output": tool_response
            })

            try:
                run = client.beta.threads.runs.submit_tool_outputs_and_poll(
                    thread_id=thread.id,
                    run_id=run.id,
                    tool_outputs=tool_outputs
                )
            
            except Exception as e:
                print(e)

            if run.status == 'failed':
                print("tool call failed, debug needed.")
            
            elif run.status == 'completed':
                messages = client.beta.threads.messages.list(thread_id=thread.id)
                response = json.loads(messages.data[0].content[0].text.value)
                print(response['response'])
