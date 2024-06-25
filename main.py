from pydoc import replace
from matplotlib.artist import get
import os
import zipfile
import google.generativeai as genai
import textwrap
import google.generativeai as genai
import re
from IPython.display import display
from IPython.display import Markdown

# Initialize Gemini API (replace 'your-api-key' with an actual API key)
GOOGLE_API_KEY = 'AIzaSyCCFVSBduDGNH23PLGgwHdl2Gk8bYXg_aw'

def to_markdown(text):
    text= text.replace('•', '  *')
    return Markdown(textwrap.indent(text, '> ',predicate=lambda _:True))

safety_settings = [
    {
        "category": "HARM_CATEGORY_DANGEROUS",
        "threshold": "BLOCK_NONE",
    },
    {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_NONE",
    },
    {
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "BLOCK_NONE",
    },
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_NONE",
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_NONE",
    },
]

genai.configure(api_key = GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash', safety_settings=safety_settings)
chat = model.start_chat(history=[])
# Function to get user input
def get_user_input():
    user_input = input("What application do you want to build/generate? ")
    return user_input
# Function to call Gemini AI and get the file structure
# def get_file_structure(prompt):
#     # response = requests.post(GEMINI_API_URL, headers=headers, json=data)
#     response = generate_content(prompt=prompt)
#     response_json = response.json()
#     file_structure = response_json['content']
#     return json.loads(file_structure)  # Assuming the response is JSON formatted
# # Function to generate files based on the file structure
# def generate_files(file_structure, prompt):
#     for file_path, file_content_prompt in file_structure.items():
#         response = generate_content(prompt)
#         response_json = response.json()
#         file_content = response_json['content']
#         os.makedirs(os.path.dirname(file_path), exist_ok=True)
#         with open(file_path, 'w') as f:
#             f.write(file_content)

# Function to zip the generated files
def zip_files(output_filename='generated_application.zip', folder='.'):
    with zipfile.ZipFile(output_filename, 'w') as zipf:
        for root, dirs, files in os.walk('.'):
            for file in files:
                if file != output_filename:  # Avoid zipping the zip file itself
                    zipf.write(os.path.join(root, file))

def generate_content(prompt,stream=True):
    file_format = """
    You will output the content of each file necessary to achieve the goal, including ALL code.
    Represent files like so:

    FILENAME : path
    CODE

    The following tokens must be replaced like so:
    FILENAME is the lowercase combined relative path and file name including the file extension.
    CODE is the code in the file.

    Example representation of a file:

    FILENAME : src/hello_world.py
    print("Hello World")
    
    Do not comment on what every file does. Please note that the code should be fully functional. No placeholders.
    """ 
    entrypoint = f"""
    The user will ask you to write a script that runs the code in a specific way. Here is the user prompt = {prompt}.
    You will answer with code blocks that include all the necessary terminal commands.
    Do not install globally. Do not use sudo.
    Do not explain the code, just give the commands.
    Do not use placeholders, use example values (like . for a folder argument) if necessary.
    """

    generate = f"""
    Think step by step and reason yourself to the correct decisions to make sure we get it right.
    First lay out the names of the core classes, functions, methods that will be necessary, As well as a quick comment on their purpose.

    adhere to the file format.
    FILE_FORMAT = {file_format}

    You will start with the "entrypoint" prompt here : {entrypoint}, and then go to the ones that are imported by that prompt, and so on.
    Please note that the code should be fully functional. No placeholders.

    Follow a language and framework appropriate best practice file naming convention.
    Make sure that files contain all imports, types etc. The code should be fully functional. Make sure that code in different files are compatible with each other.
    Ensure to implement all code, if you are unsure, write a plausible implementation.
    Include module dependency or package manager dependency definition file.
    Before you finish, double check that all parts of the architecture is present in the files.

    When you are done, write finish with "this concludes a fully working implementation."
    """
    main_prompt = f"""You are an expert at generating code and programming. You will perform the tasks provided to you to the best of your knowledge.
    Think step by step and reason yourself to the correct decisions to make sure we get it right.
    Follow a language and framework appropriate best practice file naming convention.
    Make sure that files contain all imports, types etc. The code should be fully functional. Make sure that code in different files are compatible with each other.
    Ensure to implement all code, if you are unsure, write a plausible implementation.
    Include module dependency or package manager dependency definition file.
    Before you finish, double check that all parts of the architecture is present in the files.
    First lay out the names of the core classes, functions, methods that will be necessary, As well as a quick comment on their purpose. Strictly adhere to these next few lines and generate code that follow these instructions: 
     
    1) note: you can name the root directory as the thing user ask you to create. For eg if user asks you to create a portfolio site then you can name the root directory as portfolio_site.
    2) Make sure to specify the file name before starting to generate code for a particular file. For eg if you are asked to make portfolio website then before starting to code the html,css and js for it, Write 'File : index.html' and then write html code below it, likewise Mention 'File : styles.css' and 'File : index.js' before writing respective codes. Here is an example representation of a file: {file_format}
    3)Generate python code to create the file structure using file handling in python and append the generated code to the respective files mentioned in step 2. It is absolutely mandatory to generate shell.py code.The shell.py code must include the code for a specific file as well as the code for generating the file structure.

    if you are asked to generate a portfolio site using html,css and js then only write code for the main.py and it should look like this:
    import os
    os.makedirs('portfolio_site',exist_ok=True)
    with open('portfolio_site/index.html','w') as f:
        f.write("<!DOCTYPE html> 
        <html lang="en">
        <head>
            <meta charset="UTF-8">

    <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Portfolio - Web Developer</title>
        <link rel="stylesheet" href="styles.css">

    </head>
    <body>
        <header>
            <h1>My Portfolio</h1>
            <nav>
                <ul>
                    <li><a href="#about">About</a></li>
                    <
    li><a href="#projects">Projects</a></li>
                    <li><a href="#skills">Skills</a></li>
                    <li><a href="#contact">Contact</a></li>
                </ul>
            </nav>
        </header>

        <section
    id="about">
            <h2>About Me</h2>
            <p>I'm a passionate web developer with a strong foundation in HTML, CSS, JavaScript, and other relevant technologies. I'm always eager to learn new things and I'm excited about the potential of the web.</p>
        </
    section>

        <section id="projects">
            <h2>Projects</h2>
            <div class="projects-container">
                <!-- Add project divs here -->
            </div>
        </section>

        <section id="skills">
            <h2>Skills</h2>
            <ul class="skills
    -list">
                <li>HTML</li>
                <li>CSS</li>
                <li>JavaScript</li>
                <li>Python</li>
                <!-- Add more skills here -->
            </ul>
        </section>

        <footer id="contact
    ">
            <h2>Contact</h2>
            <p>Email: your_email@example.com</p>
            <p>Phone: +1 (123) 456-7890</p>
            <p>LinkedIn: your_linkedin_profile</p>

        </footer>

        <script src="index.js"></script>
    </body>
    </html>")
    Similarly for other files.
    Please note that the code should be fully functional. No placeholders.
    Now the user will provide you with the actual prompt and make sure to adhere to the instructions mentioned above.
    Here is the prompt = {prompt}."""

    response = chat.send_message(main_prompt,stream=stream,safety_settings=safety_settings)
    return response
def print_content(res):
    for chunk in res:
        if(chunk):
            print(chunk.text,end='')
def return_content(res):
    chunks = []
    for c in res:
        chunks.append(c.text)
    return chunks



def get_shell_code(res):
    
    chunks = return_content(res)
    chunks = ''.join(chunks)
    shell_code = re.findall(r'```(python)(.*?)```', chunks, re.DOTALL)
    shell_code = [code.strip() for _, code in shell_code]
    try:
        with open('shell.py', 'w') as f:
            f.write(shell_code[0])
    except Exception as e:
        print(e)
    exec(shell_code[0])

zip_prompt = """One more thing to note is that you need to generate code to zip the particular file structure generated before.
    For example if the user asks you to generate a portfolio site using html,css and js then you need to generate code to zip the portfolio_site folder which will include all the necessary files:
        with zipfile.ZipFile(output_filename, 'w') as zipf:
        for root, dirs, files in os.walk('portfolio_site'):
            for file in files:
                if file != output_filename:  # Avoid zipping the zip file itself
                    zipf.write(os.path.join(root, file))"""



if __name__ == "__main__":
    user_prompt = get_user_input()
    response = generate_content(prompt=user_prompt,stream=True)
    print_content(response)
    get_shell_code(response)
    print("Application generated successfully.")
    # response2 = chat.send_message(zip_prompt,stream=False,safety_settings=safety_settings)
    # print("Generating zip file...")
    # print_content(response2)
    # get_shell_code(response2)
    # print("Application generated and zipped successfully.")

