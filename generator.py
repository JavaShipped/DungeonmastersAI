import tkinter as tk
from tkinter import filedialog, messagebox
import openai
import random
import threading

# The content of your generate_text function
def generate_text(pre_prompt, prompt, format_choice):
    full_prompt = f"{pre_prompt}\n{prompt}"
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=full_prompt,
        max_tokens=2000,
        n=1,
        stop=None,
        temperature=0.8,
        top_p=1,
        frequency_penalty=0.3,
        presence_penalty=0.45,
    )
    
    generated_text = response.choices[0].text.strip()

    if format_choice == "Markdown Formatting":
        # Convert generated_text to Markdown
        pass
    elif format_choice == "Use BBcode Formatting":
        # Convert generated_text to BBcode
        pass

    return generated_text

def save_to_file(filename, generated_text):
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(generated_text)
    # The content of your save_to_file function

# Predefined pre_prompts

# The content of your tavern_pre_prompt function
def tavern_pre_prompt():
    races = ["Human", "Elf", "Dwarf", "Halfling", "Gnome", "Half-Elf", "Half-Orc", "Tiefling"]
    genders = ["male", "female", "non-binary"]
    race = random.choice(races)
    gender = random.choice(genders)
    pre_prompt = f"""
    - Tavern Name.
    - Innkeeper (use all races in DnD and weight random genders 1:1:1 male, female, non-binary): {race} {gender}
    - Number of Rooms.
    - List 6 Drinks and cost.
    - List 5 Meals and cost.
    - What does the tavern look like.
    - 3 Named, notable patrons with a story hook and a secret.
    - A quest board with 3 quests on it appropriate for the size.
    """
    return pre_prompt


# The content of your random_npc_pre_prompt function
def random_npc_pre_prompt():
    races = ["Human", "Elf", "Dwarf", "Halfling", "Gnome", "Half-Elf", "Half-Orc", "Tiefling"]
    genders = ["male", "female", "non-binary"]
    race = random.choice(races)
    gender = random.choice(genders)
    pre_prompt = f"""
        Write an NPC stat block for dungeons and dragons 5e 
        - Name
        - Race: {race}
        - Gender: {gender}
        - Class
        - Profession if applicable
        - Alignment
        - Adult narrative backstory Backstory.
        - Short physical description
        - 3 Secrets
        - A story hook
        - A unique Personality Trait.
        - Ability Scores, weapons, features and spells.
        - An inventory
        - Money
    """
    return pre_prompt

# The content of your town_generator_pre_prompt function
def town_generator_pre_prompt():
    pre_prompt = """
    This is for a dungeons and dragons 5e game:
    Use the template:
    - Town Name
    - Population
    - Size
    - Notable Landmarks
    - Type of Government
    - Town History
    - Economy and Trade
    - Points of Interest
    """
    return pre_prompt

    # The content of your quest_generator_pre_prompt function
def quest_generator_pre_prompt():
    quest_type = ["Fetch", "Kill", "Escort", "delivery", "Push the button", "Mystery", "Lore/world building"]
    quest = random.choice(quest_type)
    races = ["Human", "Elf", "Dwarf", "Halfling", "Gnome", "Half-Elf", "Half-Orc", "Tiefling"]
    genders = ["male", "female", "non-binary"]

    npc_descriptions = []
    for _ in range(3):
        race = random.choice(races)
        gender = random.choice(genders)
        npc_descriptions.append(f"{race} {gender}")

    npc_descriptions_str = ", ".join(npc_descriptions)

    pre_prompt = f"""
        Adventure guide Template:
        - Quest title.
        - What is the story hook?
        - What type of quest is it? (Fetch, Kill, Escort, Delivery, Push the Button, Mystery or Lore Quests): {quest}
        - What is the reward?
        - 3 possible hooks for the adventure.
        - Who are the important NPC's. Describe their appearance, motivations and relevant details like class and profession. Use: {npc_descriptions_str}.
        - Outline and list the adventure steps. 
        - Summarise least 3 combat and/or social encounters. 
        - Include a text or riddle based puzzle and its solution.
            """
    return pre_prompt


presets = [
    {"name": "Tavern", "pre_prompt": tavern_pre_prompt, "prompt": "Build a tavern", "format": "BBcode"},
    {"name": "Random NPC", "pre_prompt": random_npc_pre_prompt, "prompt": "Create a random NPC", "format": "Markdown"},
    {"name": "Town", "pre_prompt": town_generator_pre_prompt, "prompt": "Generate a town", "format": "Markdown"},
    {"name": "Quest", "pre_prompt": quest_generator_pre_prompt, "prompt": "Create a quest", "format": "Markdown"},
]

class TextGeneratorApp:
    def generate_thread(self):
        try:
            self.generate_button.config(state=tk.DISABLED, text="Waiting for API...")
            self.generate()
        finally:
            self.generate_button.config(state=tk.NORMAL, text="Generate")

    def __init__(self, root):
        self.root = root
        self.root.title("Bunions & Flagons cool little AI generator")

        self.api_key_label = tk.Label(root, text="Enter your API key:")
        self.api_key_label.grid(row=0, column=0, sticky=tk.W)
        self.api_key_entry = tk.Entry(root)
        self.api_key_entry.grid(row=0, column=1, sticky=tk.W+tk.E)

        self.api_key_entry = tk.Entry(root, show="*")  # Mask the API key with asterisks
        self.api_key_entry.grid(row=0, column=1, sticky=tk.W+tk.E)

        self.show_api_key = tk.BooleanVar()
        self.show_api_key.set(False)
        self.show_api_key_button = tk.Button(
            root,
            text="Show",
            command=self.toggle_api_key_visibility,

        )
        self.show_api_key_button.grid(row=0, column=2, sticky=tk.W)

        self.preset_label = tk.Label(root, text="Select a preset:")
        self.preset_label.grid(row=1, column=0, sticky=tk.W)

        self.preset_var = tk.StringVar(root)
        self.preset_var.set("Custom")
        self.preset_options = ["Custom"] + [preset["name"] for preset in presets]
        self.preset_menu = tk.OptionMenu(root, self.preset_var, *self.preset_options)
        self.preset_menu.grid(row=1, column=1, sticky=tk.W)

        self.prompt_label = tk.Label(root, text="Enter the prompt:")
        self.prompt_label.grid(row=2, column=0, sticky=tk.W)
        self.prompt_entry = tk.Entry(root)
        self.prompt_entry.grid(row=2, column=1, sticky=tk.W+tk.E)

        self.format_label = tk.Label(root, text="Select output format:")
        self.format_label.grid(row=3, column=0, sticky=tk.W)
        self.format_var = tk.StringVar(root)
        self.format_var.set("Markdown")
        self.format_options = ["Markdown", "BBcode"]
        self.format_menu = tk.OptionMenu(root, self.format_var, *self.format_options)
        self.format_menu.grid(row=3, column=1, sticky=tk.W)

        self.generate_button = tk.Button(root, text="Generate", command=self.start_generate_thread)
        self.generate_button.grid(row=4, column=0, columnspan=2, sticky=tk.W+tk.E)

        self.output_text = tk.Text(root, wrap=tk.WORD)
        self.output_text.grid(row=5, column=0, columnspan=2, sticky=tk.N+tk.S+tk.W+tk.E)

        self.save_button = tk.Button(root, text="Save to file", command=self.save_to_file)
        self.save_button.grid(row=6, column=0, columnspan=2, sticky=tk.W+tk.E)

        # Configure the grid to be responsive
        for i in range(2):
            root.columnconfigure(i, weight=1)
        for i in range(7):
            root.rowconfigure(i, weight=1)
        # Set the weight of row 5 (output_text) to a higher value to allocate more space to it
        root.rowconfigure(5, weight=4)

    def start_generate_thread(self):
        generate_thread = threading.Thread(target=self.generate_thread)
        generate_thread.start()

    def toggle_api_key_visibility(self):
        self.show_api_key = not self.show_api_key
        if self.show_api_key:
            self.api_key_entry.configure(show="")
            self.show_api_key_button.configure(text="Hide")
        else:
            self.api_key_entry.configure(show="*")
            self.show_api_key_button.configure(text="Show")

    def save_to_file(self):
        file_name = filedialog.asksaveasfilename(defaultextension=".txt")
        if not file_name:
            return

        generated_text = self.output_text.get(1.0, tk.END)

        with open(file_name, "w", encoding="utf-8") as file:
            file.write(generated_text)

        messagebox.showinfo("File Saved", f"Text saved to {file_name}")


    def generate(self):
        api_key = self.api_key_entry.get()
        openai.api_key = api_key
        if not api_key:
            messagebox.showerror("API Key Required", "Please enter your API key.")
            return

        preset_name = self.preset_var.get()
        custom_prompt = self.prompt_entry.get()
        if preset_name == "Custom":
            pre_prompt = ""
            prompt = custom_prompt
        else:
            selected_preset = next(preset for preset in presets if preset["name"] == preset_name)
            pre_prompt = selected_preset["pre_prompt"]()
            prompt = f"{custom_prompt}\n{selected_preset['prompt']}"


        format_choice = self.format_var.get()
        prompt = f"{format_choice}\n{self.prompt_entry.get()}"

        generated_text = generate_text(pre_prompt, prompt, format_choice)

        self.output_text.delete(1.0, tk.END)
        self.output_text.insert(tk.END, generated_text)
        
    def save_to_file(self):
        file_name = filedialog.asksaveasfilename(defaultextension=".txt")
        if not file_name:
            return

        generated_text = self.output_text.get(1.0, tk.END)

        with open(file_name, "w", encoding="utf-8") as file:
            file.write(generated_text)

        messagebox.showinfo("File Saved", f"Text saved to {file_name}")

if __name__ == "__main__":
    root = tk.Tk()
    app = TextGeneratorApp(root)
    root.mainloop()
