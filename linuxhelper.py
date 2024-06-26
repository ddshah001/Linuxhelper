from openai import OpenAI
import os
import configparser
import re
import argparse
import platform

parser = argparse.ArgumentParser(description='A Linux shell script helper tool.')
parser.add_argument('-v', '--verbose', action='store_true', help='Show AI generated output and exported version of script', default=False)
parser.add_argument('-r', '--run', action='store_true', help='Run shell script but use this option with caution', default=False)

def getarg():
    args = parser.parse_args()
    return args

def getOSdetails():
    os_name = platform.system()
    os_release = platform.release()
    os_version = platform.version()
    distro_name = "Unknown"
    if os.path.exists("/etc/os-release"):
        with open("/etc/os-release") as f:
            for line in f:
                if line.startswith("NAME="):
                    distro_name = line.split("=")[1].strip().strip('"')
                    break

    return os_name, os_release, os_version, distro_name

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
    #Get operating system information
    os_name, os_release, os_version, distro_name = getOSdetails()

    # System Message
    system_message = f"""
    You are a shell script writer, only provide shell script without explanations

    Consider below operating system details while writing shell script:
    os_name: {os_name}
    os_release: {os_release}
    os_version: {os_version}
    distro_name: {distro_name}
    """
    #print(system_message)
    response = client.chat.completions.create(
        messages=[
        {
            "role": "system",
            "content": system_message

        },
        {
            "role": "user",
            "content": "Create a Linux shell script to " + user_input + ".",
        }
    ],
    model="gpt-3.5-turbo",
    )

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
    script_content = extract_code(response)
    if(getarg().verbose == True):
        print("AI's Generated Response")
        print(response)
        print(f"Generated script:\n{script_content}")
    create_shell_script(script_content)
    if(getarg().run == True):
        print(f"Generated script:\n{script_content}")
        print("-------------------------------------------------------------------")
        accept = input("Please validate above scipt, enter yes to confirm and run: ")
        if(accept == "yes"):
            run_shell_script()

if __name__ == "__main__":
    main()
