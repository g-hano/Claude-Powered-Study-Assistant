# Function to add a message to memory
def add_to_memory(role, content, memory):
    memory.append({"role": role, "content": content})

# Function to retrieve the latest message from memory
def get_latest_message(role, memory):
    for message in reversed(memory):
        if message["role"] == role:
            return message["content"]
    return None

# Claude accepts in this special format    
def construct_format_tool_for_claude_prompt(names, descriptions, parameter_lists):
    num_tools = len(names)
    constructed_prompts = ""
    for i in range(num_tools):
        name = names[i]
        description = descriptions[i]
        parameters = parameter_lists[i]
        constructed_prompt = (
            "<tool_description>\n"
                "<tool_name>"
                    f"{name}\n"
                "</tool_name>\n"
                
                "<description>\n"
                    f"{description}\n"
                "</description>\n"
                
                "<parameters>\n"
                    f"{construct_format_parameters_prompt(parameters)}\n"
                "</parameters>\n"
            "</tool_description>"
        )
        constructed_prompts += constructed_prompt + "\n"
    return constructed_prompts

# Claude accepts in this special format    
def construct_format_parameters_prompt(parameters):
    constructed_prompt = "\n".join(f"<parameter>\n<name>{parameter['name']}</name>\n<type>{parameter['type']}</type>\n<description>{parameter['description']}</description>\n</parameter>" for parameter in parameters)

    return constructed_prompt

# Claude accepts in this special format    
def construct_tool_use_system_prompt(tools):
    tool_use_system_prompt = (
        "In this environment you have access to a set of tools you can use to answer the user's question.\n"
        "\n"
        "You may call them like this:\n"
        "<function_calls>\n"
        "<invoke>\n"
        "<tool_name>$TOOL_NAME</tool_name>\n"
        "<parameters>\n"
        "<$PARAMETER_NAME>$PARAMETER_VALUE</$PARAMETER_NAME>\n"
        "...\n"
        "</parameters>\n"
        "</invoke>\n"
        "</function_calls>\n"
        "\n"
        "Here are the tools available:\n"
        "<tools>\n"
        + '\n'.join([tool for tool in tools]) +
        "\n</tools>"
    )
    return tool_use_system_prompt


def construct_successful_function_run_injection_prompt(invoke_results):
    constructed_prompt = (
        "<function_results>\n"
        + '\n'.join(
            f"<result>\n<tool_name>{res['tool_name']}</tool_name>\n<stdout>\n{res['tool_result']}\n</stdout>\n</result>" 
            for res in invoke_results
        ) + "\n</function_results>"
    )
    
    return constructed_prompt

import wikipedia
def wikipedia_search(user_input: str):
    """The user input that the user wants to search Wikipedia for."""
    return wikipedia.search(user_input)

from langchain_community.tools import DuckDuckGoSearchRun
def duckduckgo_search(user_input: str):
    search = DuckDuckGoSearchRun()
    return search.run(user_input)

import os
def save_note(user_input: str):
    file_path = "notes.txt"
           
    with open(file_path, "a") as f:
        f.write(user_input+"\n")

from typing import Any    
def code_executer(user_input: str, expected_output: Any) -> bool:
    try:
        exec_result = exec(user_input)
        if exec_result == expected_output:
            return True
        else:
            print("Expected output:", expected_output)
            print("Actual output:", exec_result)
            return False
    except Exception as e:
        print("Error executing code: ", e)
        return False
    
def do_pairwise_arithmetic(num1, num2, operation):
    if operation == '+':
        return num1 + num2
    elif operation == "-":
        return num1 - num2
    elif operation == "*":
        return num1 * num2
    elif operation == "/":
        return num1 / num2
    else:
        return "Error: Operation not supported."

from youtubesearchpython import VideosSearch    
def search_youtube(user_input: str):
    videos_search = VideosSearch(user_input, limit=5)
    results = videos_search.result()
    return results['result']

import PyPDF2
import docx
def extract_text_from_pdf(file_path):
    with open(file_path, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
    return text
def extract_text_from_docx(file_path):
    doc = docx.Document(file_path)
    text = ""
    for paragraph in doc.paragraphs:
        text += paragraph.text + '\n'
    return text
def extract_text_from_txt(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        text = file.read()
    return text
def extract_text_from_file(user_input):
    text = ""
    try:
        if user_input.endswith('.pdf'):
            text = extract_text_from_pdf(user_input)
        elif user_input.endswith('.docx'):
            text = extract_text_from_docx(user_input)
        elif user_input.endswith('.txt'):
            text = extract_text_from_txt(user_input)
        else:
            raise ValueError("Unsupported file format")
        return text
    except Exception as e:
        print("Error reading file: ", e)