import os
import re
import xml.etree.ElementTree as ET

from anthropic import Anthropic

from personal_assistant_utils import *
from personal_assistant_tools import TOOLS

client = Anthropic(
    api_key=os.environ.get("ANTHROPIC"),
)
MODEL_NAME = "claude-3-opus-20240229"
memory = []
while True:
    question = input("Ask Claude: ")
    if question.lower() == "q":
        break
    add_to_memory("user", question, memory)
    message = {
        "role": "user", 
        "content": question
    }

    names = [tool.name for tool in TOOLS]
    descriptions = [tool.description for tool in TOOLS]
    parameters = [tool.parameters for tool in TOOLS]
    all_tools = construct_format_tool_for_claude_prompt(names, descriptions, parameters)
    system_prompt = construct_tool_use_system_prompt([all_tools])

    function_calling_message = client.messages.create(
        model=MODEL_NAME,
        max_tokens=1024,
        messages=[message],
        system=system_prompt,
        stop_sequences=["\nHuman:", "\nAssistant", "</function_calls>"]
    ).content[0].text + '</function_calls>'

    xml_pattern = r'<function_calls>.*?</function_calls>'
    xml_parts = re.findall(xml_pattern, function_calling_message, re.DOTALL)  # handle thought texts
        
    has_that_tool = False
    for xml_part in xml_parts:
        root = ET.fromstring(xml_part)
        tool_name = root.find('.//tool_name').text

        # Call functions
        tool_functions = {
            "wikipedia_search": wikipedia_search,
            "duckduckgo_search": duckduckgo_search,
            "save_note": save_note,
            "code_executer": code_executer,
            "calculator": do_pairwise_arithmetic,
            "search_youtube": search_youtube,
            "extract_text_from_file": extract_text_from_file
        }
    
        for key, func in tool_functions.items():
            if tool_name == key:
                has_that_tool = True
                #print("-"*12)
                #print(xml_parts)
                #print("-"*12)
                inp = root.find('.//user_input').text
                result = func(inp)   
                formatted_results = [{
                'tool_name': tool_name,
                'tool_result': result
                }]
                function_results = construct_successful_function_run_injection_prompt(formatted_results)
                partial_assistant_message = function_calling_message + "</function_calls>" + function_results # concatinate full answer
                add_to_memory("assistant", result, memory)
            
    if not has_that_tool:
        final_message = client.messages.create(
            model=MODEL_NAME,
            max_tokens=1024,
            messages=[
                message,
                {
                    "role":"assistant",
                    "content":function_calling_message
                }
            ],
            system=system_prompt
        ).content[0].text
   
    final_message = client.messages.create(
        model=MODEL_NAME,
        max_tokens=1024,
        messages=[
            message,
            {
                "role":"assistant",
                "content":partial_assistant_message
            }
        ],
        system=system_prompt
    ).content[0].text
    print(partial_assistant_message+final_message)
