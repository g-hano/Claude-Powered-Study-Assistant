class Tool:
    def __init__(self, tool_name: str, tool_description: str, tool_parameters: list):
        self.name = tool_name
        self.description = tool_description
        self.parameters = tool_parameters
        
    def info(self):
        print(f"""\n
        Tool Name: {self.tool_name}\n
        Tool Description: {self.description}\n
        Tool Parameters: {self.parameters}
        """)