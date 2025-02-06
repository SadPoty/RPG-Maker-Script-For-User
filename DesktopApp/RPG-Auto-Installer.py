from customtkinter import *
from CTkMessagebox import CTkMessagebox

import os
import requests
import urllib.request
import json

class InstallerApp(CTk):
    def __init__(self):
        super().__init__()
        self.geometry("500x500")
        set_appearance_mode("system")
        set_default_color_theme("dark-blue")
        self.title("RPG Auto Installer")

        self.game_path = ""
        self.js_folder = ""
        self.plugins_js = ""

        self.left_menu = CTkFrame(self)
        self.left_menu.grid(row=0, column=0, sticky="news")
        self.contents = CTkFrame(self)
        self.contents.grid(row=0, column=1, sticky="news")

        self.create_left_menu()
        self.create_widgets()

    def getGitHubContents(self, path):
        """
        Retrieves the contents of specified directories from a GitHub repository.
        path should be Enhance/ or Cheat/
        """
        owner = "SadPoty"
        repo = "RPG-Maker-Script-For-User"

        url = f"https://api.github.com/repos/{owner}/{repo}/contents/{path}"
        response = requests.get(url)
        return response.json()
    
    def delete_contents_child(self):
        for widget in self.contents.winfo_children():
            widget.destroy()
        self.contents.rowconfigure(0, weight=0)
        self.contents.columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=0)

    def create_left_menu(self):
        """
        Creates the left menu for the GUI.
        """

        btn_menu = CTkButton(self.left_menu, text="Menu", command=self.create_widgets)
        btn_menu.grid(row=0, column=0, padx=10, pady=10)

        btn_cheat = CTkButton(self.left_menu, text="Cheat", command=self.create_cheat_widgets)
        btn_cheat.grid(row=1, column=0, padx=10, pady=10)

        btn_Enhance = CTkButton(self.left_menu, text="Enhance", command=self.create_Enhance_widgets)
        btn_Enhance.grid(row=2, column=0, padx=10, pady=10)

        btn_settings = CTkButton(self.left_menu, text="Settings", command=self.create_settings_widgets)
        btn_settings.grid(row=3, column=0, padx=10, pady=10)

        self.grid_rowconfigure(0, weight=1)
        self.left_menu.rowconfigure(4, weight=1)

        btn_about = CTkButton(self.left_menu, text="About", command=self.create_about_widgets)
        btn_about.grid(row=4, column=0, padx=10, pady=10, sticky="s")

        btn_install = CTkButton(self.left_menu, text="Install", command=lambda:print("Install !"))
        btn_install.grid(row=5, column=0, padx=10, pady=10, sticky="s")

    def create_Enhance_widgets(self):
        """
        Creates the widgets for the GUI.
        """
        self.delete_contents_child()

        list_buttons = []
        i = 0

        script = self.getGitHubContents("Enhance/")
        for script in script:
            btn = CTkButton(self.contents, text=script["name"], command=lambda s=script:print(f"Install {s['name']}"))
            btn.grid(row=i, column=0, padx=10, pady=3, sticky="ew")
            list_buttons.append(btn)
            i += 1

    def create_cheat_widgets(self):
        """
        Creates the widgets for the GUI.
        """
        self.delete_contents_child()

        list_buttons = []
        i = 0

        script = self.getGitHubContents("Cheat/")
        for script in script:
            btn = CTkButton(self.contents, text=script["name"], command=lambda event=script:self.install_script(event))
            btn.grid(row=i, column=0, padx=10, pady=3, sticky="ew")
            list_buttons.append(btn)
            i += 1

    def create_settings_widgets(self):
        """
        Creates the widgets for the GUI.
        """
        self.delete_contents_child()

        label = CTkLabel(self.contents, text="Settings")
        label.grid(row=0, column=0, padx=10, pady=10)

    def create_about_widgets(self):
        """
        Creates the widgets for the GUI.
        """
        self.delete_contents_child()

        label = CTkLabel(self.contents, text="About")
        label.grid(row=0, column=0, padx=10, pady=10)

    def find_dir(self):
        self.game_path = filedialog.askdirectory()
        if self.game_path and any(file.endswith('.exe') for file in os.listdir(self.game_path)):
            if os.path.exists(os.path.join(self.game_path, "www")):
                self.js_folder = os.path.join(self.game_path, "www\\js")
                self.plugins_js = os.path.join(self.js_folder, "plugins.js")
            elif os.path.exists(os.path.join(self.game_path, "js")):
                self.js_folder = os.path.join(self.game_path, "js")
                self.plugins_js = os.path.join(self.js_folder, "plugins.js")
            else:
                CTkMessagebox(title="Error", message="No js or www folder found in the selected directory.")
        else:
            CTkMessagebox(title="Error", message="No game found in the selected directory.")

    def create_widgets(self):
        """
        Creates the widgets for the GUI.
        """
        print(self.game_path)
        self.contents.rowconfigure(0, weight=1)
        self.contents.columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        btn = CTkButton(self.contents, text="Choose game.exe directory", command=self.find_dir, height=50)
        btn.grid(row=0, column=0, padx=10, sticky="ew")

    def install_script(self, script):
        dl_link = script['download_url']
        urllib.request.urlretrieve(dl_link, self.js_folder+"\\plugins"+"\\"+script['name']) # download file to the js folder

        # add the script to the plugins.js
        new_plugin = {
            "name": script['name'],
            "status": True,
            "description": "Idk how I could retrive the description for now",
            "parameters": {}
        }

        with open(self.plugins_js, 'r') as file:
            content = file.read()

        start = content.index('[')
        end = content.rindex(']') + 1
        plugins_list = json.loads(content[start:end])

        plugins_list.append(new_plugin)

        new_plugins_json = json.dumps(plugins_list, indent=4)
        new_content = content[:start] + new_plugins_json + content[end:]

        with open(self.plugins_js, 'w') as file:
            file.write(new_content)

if __name__ == "__main__":
    app = InstallerApp()
    app.mainloop()