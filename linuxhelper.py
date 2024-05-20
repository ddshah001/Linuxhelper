from openai import OpenAI
import os
import configparser

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
            "role": "user",
            "content": "Create a Linux shell script to " + user_input + ". Just return shell script with out explanations",
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

def main():
    user_input = get_user_input()
    script_content = get_chatgpt_response(user_input)
    #create_shell_script(script_content)
    print(f"Generated script:\n{script_content}")
    #run_shell_script()

if __name__ == "__main__":
    main()