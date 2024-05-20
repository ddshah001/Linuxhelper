from openai import OpenAI
import os
import configparser
import re

config = configparser.ConfigParser()
config.read("config.ini")


# Ensure you have set your OpenAI API key
client = OpenAI(
    # This is the default and can be omitted
    api_key=config.get("OpenAI", "key"),
)

def get_user_input():
    return input("Please enter the task you want to automate with a shell script: ")

def get_chatgpt_response(user_input):
    #print("Create a Linux shell script to " + user_input)
    response = client.chat.completions.create(
        messages=[
        {
            "role": "system",
            "content": "You are a shell script writer, only provide shell script with out explanations"

        },
        {
            "role": "user",
            "content": "Create a Linux shell script to " + user_input + ".",
        }
    ],
    model="gpt-3.5-turbo",
    )

    #response = openai.Completion.create(
    #    model="text-davinci-003",
    #    prompt=f"Create a Linux shell script to {user_input}",
    #    max_tokens=200,
    #    temperature=0.5
    #)
    return response.choices[0].message.content

def create_shell_script(content, filename="script.sh"):
    with open(filename, "w") as file:
        file.write(content)
    os.chmod(filename, 0o755)  # Make the file executable

def run_shell_script(filename="script.sh"):
    os.system(f"./{filename}")

def extract_code(api_output):
    # Regular expression pattern to match code blocks enclosed in triple backticks
    pattern = r'```bash(.*?)```'
    
    # Find all code blocks using the pattern
    code_blocks = re.findall(pattern, api_output, re.DOTALL)
    if(len(code_blocks)==0):
        extracted_code = api_output
    else:
        extracted_code = code_blocks[0]
    
    
    return extracted_code

def main():
    user_input = get_user_input()
    response=get_chatgpt_response(user_input)
    print(response)
    script_content = extract_code(response)
    create_shell_script(script_content)
    print(f"Generated script:\n{script_content}")
    run_shell_script()

if __name__ == "__main__":
    main()
