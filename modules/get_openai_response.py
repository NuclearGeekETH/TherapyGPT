import openai
import os
import json
from datetime import date, datetime
from collections import defaultdict
from .memories_utility import load_memory, save_memory

openai.api_key = os.getenv("OPENAI_API_KEY")

# == Core memory save function ==
def add_memory(summary, time_of_event, therapy_notes):
    data = load_memory()
    memory_entry = {
        "timestamp": datetime.now().isoformat(timespec="seconds"),
        "summary": summary,
        "time_of_event": time_of_event,
        "therapy_notes": therapy_notes
    }
    data.setdefault("memory", []).append(memory_entry)
    return save_memory(data)

# == Define tools schema for OpenAI API ==
tools = [
    {
        "type": "function",
        "function": {
            "name": "add_memory",
            "description": "Add a new memory entry with the current timestamp.",
            "parameters": {
                "type": "object",
                "properties": {
                    "summary": {"type": "string", "description": "Summary of the event"},
                    "time_of_event": {"type": "string", "description": "When the event was, or None if unknown."},
                    "therapy_notes": {"type": "string", "description": "Notes about the memory/event."}
                },
                "required": ["summary", "time_of_event", "therapy_notes"]
            },
        }
    }
]

# == Function to execute API-dispatched function call ==
def execute_function_call(tool_call):
    function_name = tool_call.function.name
    arguments = tool_call.function.arguments
    try:
        arguments_contents = json.loads(arguments)
    except Exception as e:
        return f"Error parsing arguments: {arguments!r}\n\n{e}"
    if function_name == "add_memory":
        summary = arguments_contents.get("summary")
        time_of_event = arguments_contents.get("time_of_event")
        therapy_notes = arguments_contents.get("therapy_notes")
        results = add_memory(summary, time_of_event, therapy_notes)
        return results
    return f"Error: function {function_name} does not exist"

# == Main Gradio/OpenAI streaming generator handler with second API call ==
def chat_response(message, history, model, system):
    history.insert(0, {"role": "system", "content": f"{system} You have a function to save a memory you want to remember. The function is called 'add_memory'. Tell the user when you added a memory. Current Date: {date.today()}"})
    history.append({"role": "user", "content": message})

    try:
        completion = openai.chat.completions.create(
            model=model,
            messages=history,
            tools=tools,
            tool_choice="auto",
            stream=True
        )

        partial_message = ""
        tool_call_buffers = defaultdict(lambda: {"name": None, "arguments": "", "tool_call_obj": None})
        executed = False

        # --- STREAM AND BUFFER CHUNKS ---
        for chunk in completion:
            delta = chunk.choices[0].delta
            if delta and getattr(delta, "content", None):
                partial_message += delta.content
                yield partial_message
            if delta and getattr(delta, "tool_calls", None):
                for tc in delta.tool_calls:
                    key = tc.id if tc.id is not None else tc.index
                    if tc.function.name is not None:
                        tool_call_buffers[key]["name"] = tc.function.name
                        tool_call_buffers[key]["tool_call_obj"] = tc
                    if tc.function.arguments:
                        tool_call_buffers[key]["arguments"] += tc.function.arguments

        buffers = list(tool_call_buffers.items())
        # --- MATCH AND RUN TOOL CALLS ---
        for i, (k1, b1) in enumerate(buffers):
            # Arguments (no name)?
            if b1["arguments"] and not b1["name"]:
                for k2, b2 in buffers:
                    if k1 == k2:
                        continue
                    if b2["name"] and not b2["arguments"]:
                        # Merge: use b2's name, b1's arguments
                        name, args, obj = b2["name"], b1["arguments"], b2["tool_call_obj"] or b1["tool_call_obj"]
                        if name and args and args.startswith("{") and args.endswith("}"):
                            obj.function.name = name
                            obj.function.arguments = args
                            response = execute_function_call(obj)
                            yield f"\n\n**Memory Saved:** {response}"
                            executed = True
                            history.append({
                                "tool_call_id": k2,
                                "role": "system",
                                "content": response
                            })

                            # == SECOND API CALL (stream reply after function exec) ==
                            second_completion = openai.chat.completions.create(
                                model=model,
                                messages=history,
                                stream=True
                            )
                            second_partial = ""
                            for chunk in second_completion:
                                d = chunk.choices[0].delta
                                if d and getattr(d, "content", None):
                                    second_partial += d.content
                                    yield second_partial
                            return

        # --- Handle normal (well-formed, both present) case ---
        for call_id, data in tool_call_buffers.items():
            name = data["name"]
            args = data["arguments"].strip()
            obj = data["tool_call_obj"]
            if name and args and args.startswith("{") and args.endswith("}"):
                obj.function.name = name
                obj.function.arguments = args
                response = execute_function_call(obj)
                yield f"\n\n**Memory Saved:** {response}"
                executed = True
                history.append({
                    "tool_call_id": call_id,
                    "role": "system",
                    "content": response
                })
                # == SECOND API CALL (stream reply after function exec) ==
                second_completion = openai.chat.completions.create(
                    model=model,
                    messages=history,
                    stream=True
                )
                second_partial = ""
                for chunk in second_completion:
                    d = chunk.choices[0].delta
                    if d and getattr(d, "content", None):
                        second_partial += d.content
                        yield second_partial
                return

        if not partial_message and not executed:
            yield "No chat message or function call output was produced."

    except Exception as e:
        yield f"OpenAI API returned an API Error: {e}"