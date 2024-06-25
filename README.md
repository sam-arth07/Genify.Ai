# Genify.Ai : Application Generator

This Python script allows users to input requirements and generates applications accordingly. It's a versatile tool that can create various types of applications based on user-defined specifications.

## Usage

1. **Run the Script:**
   - Make sure you have Python installed on your system.
   - Set the variable``` GOOGLE_API_KEY ``` to the api key that you have generated from Gemini Ai.
   - Execute the `main.py` script using the following command:
     ```
     python main.py
     ```

2. **User Prompts:**
   - The script will prompt you for specific details about the application you want to generate.
   - Answer the prompts with relevant information.

3. **Generated Application:**
   - Once all prompts are completed, the script will generate the application files.
   - The output will be saved in a folder named after the application type (e.g., `portfolio_site`).

4. **Customization:**
   - You can modify the script to add more application templates or customize existing ones.
   - Feel free to enhance the functionality by extending the codebase.

## Supported Application Types

1. **Portfolio Site:**
   - Generates a basic portfolio website using HTML, CSS, and JavaScript.
   - Includes sections for personal details, projects, skills, and contact information.

2. **Blog App:**
   - Creates a simple blog application with user authentication.
   - Uses a database (e.g., SQLite) to store blog posts and user data.

3. **To-Do List App:**
   - Generates a to-do list application.
   - Allows users to add, edit, and delete tasks.

## Dependencies

- Python 3.x
- Additional dependencies (if required) based on the specific application type.

## Example Usage

1. Run the script:
      ``` python main.py ```
   
2. Answer the prompts:
   - Choose the application type (e.g., "portfolio_site").
   - Provide relevant details (e.g., name, skills, project descriptions).

3. Check the generated files in the output folder.
  
4. Additional the script will automatically zip the generated file structure with the same name and in the same directory.
Feel free to explore and adapt this script to suit your needs! 🚀

