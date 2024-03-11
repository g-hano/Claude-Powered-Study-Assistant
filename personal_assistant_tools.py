from Tool import Tool

# TODO Wikipedia Search --------------------------------------------------------------------------------

tool1_name = "wikipedia_search"
tool1_description = """Searches Wikipedia based on user input. It is useful when user asks something more scientific or specific"""
tool1_parameters = [
    {
        "name": "user_input",
        "type": "str",
        "description": "The user input that the user wants to search Wikipedia for."
    }
]

# TODO DuckDuckGo Search --------------------------------------------------------------------------------
tool2_name = "duckduckgo_search"
tool2_description = """Utilizes DuckDuckGo's Search API to find information on the internet. This tool is handy for general inquiries or topics that may not be as extensively covered on Wikipedia."""
tool2_parameters = [
    {   
        "name": "user_input",
        "type": "str",
        "description": "The query string for the search. Use this parameter to input the topic or question you'd like to search the internet for."
    }
]

# TODO Note Saving --------------------------------------------------------------------------------
tool3_name = "save_note"
tool3_description = """Saves notes to 'notes.txt' for further user access."""
tool3_parameters = [
    {   
        "name": "user_input",
        "type": "str",
        "description": "The note string that we are saving."
    }
]

# TODO Code Executer --------------------------------------------------------------------------------
tool4_name = "code_executer"
tool4_description = """Executes the provided code string and compares the result to the expected output. 
The function returns True if the result matches the expected output, otherwise returns False. 
Any exceptions that occur during code execution are caught and printed as an error message."""
tool4_parameters = [
    {   
        "name": "user_input",
        "type": "str",
        "description": "The code string to be executed."
    },
    {
        "name": "expected_output",
        "type": "Any",
        "description": "The expected output value to compare against the result of executing the code string."   
    }
]

# TODO Calculator --------------------------------------------------------------------------------
tool5_name = "calculator"
tool5_description = """Calculator function for doing basic arithmetic. 
Supports addition, subtraction, multiplication"""    
tool5_parameters = [
    {
        "name": "first_operand",
        "type": "int",
        "description": "First operand (before the operator)"
    },
    {
        "name": "second_operand",
        "type": "int",
        "description": "Second operand (after the operator)"
    },
    {
        "name": "operator",
        "type": "str",
        "description": "The operation to perform. Must be either +, -, *, or /"
    }
]

# TODO YouTube Search --------------------------------------------------------------------------------
tool6_name = "search_youtube"
tool6_description = """Searches YouTube based on the given user_input. Returns most related 5 videos."""    
tool6_parameters = [
    {
        "name": "user_input",
        "type": "str",
        "description": "The input that the user wants to search YouTube for."
    }
]

# TODO File Reading --------------------------------------------------------------------------------
tool7_name = "extract_text_from_file"
tool7_description = """Extracts text from various file formats (PDF, TXT, DOCX) using PyPDF2 and python-docx libraries."""    
tool7_parameters = [
    {
        "name": "user_input",
        "type": "str",
        "description": "The file path for the PDF, TXT, or DOCX file from which text needs to be extracted."
    }
]

               
wiki = Tool(tool1_name, tool1_description, tool1_parameters)
search = Tool(tool2_name, tool2_description, tool2_parameters)        
save = Tool(tool3_name, tool3_description, tool3_parameters)        
execute = Tool(tool4_name, tool4_description, tool4_parameters)        
calculator = Tool(tool5_name, tool5_description, tool5_parameters)        
youtube = Tool(tool6_name, tool6_description, tool6_parameters)        
read = Tool(tool7_name, tool7_description, tool7_parameters)

TOOLS = [wiki, search, save, execute, calculator, youtube, read]