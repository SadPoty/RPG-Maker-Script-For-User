from customtkinter import *
from CTkMessagebox import CTkMessagebox

import os
import requests
import urllib.request
import json

class InstallerApp(CTk):
    def __init__(self):
        super().__init__()
        self.geometry("600x500")
        set_appearance_mode("system")
        set_default_color_theme("dark-blue")
        self.title("RPG Auto Installer")

        self.GitToken = self.getGitToken()

        self.game_path = ""
        self.js_folder = ""
        self.plugins_js = ""
        self.list_script_btn = []
        self.list_frame = []
        self.list_ToInstall = []

        self.left_menu = CTkFrame(self, border_color="black", border_width=1)
        self.left_menu.grid(row=0, column=0, sticky="ns", rowspan=2)
        self.contents = CTkFrame(self, border_color="black", border_width=1)
        self.contents.grid(row=0, column=1, sticky="news")
        self.InstallBtnFrame = CTkFrame(self, border_color="black", border_width=1)
        self.InstallBtnFrame.grid(row=1, column=1, sticky="news")

        self.create_install_btn()
        self.create_left_menu()
        self.create_widgets()

    def getGitToken(self):
        if os.path.exists("settings.txt"):
            with open("settings.txt", "r") as f:
                for line in f:
                    if line.strip().startswith('Github Token : "'):
                        return line.strip().split('"')[1]
        return ""

    def getGitHubContents(self, path):
        """
        Retrieves the contents of specified directories from a GitHub repository.
        path should be Enhance/ or Cheat/
        """

        owner = "SadPoty"
        repo = "RPG-Maker-Script-For-User"

        url = f"https://api.github.com/repos/{owner}/{repo}/contents/{path}"
        headers = {"Accept": "application/vnd.github.v3.raw"}
        if self.GitToken != "":
            headers["Authorization"] = f"token {self.GitToken}"
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")
            return []
    
    def getScriptData(self, path):
        """
        Retrieves the first line of a specified script.
        path should be Enhance/x.js or Cheat/x.js
        """
        owner = "SadPoty"
        repo = "RPG-Maker-Script-For-User"


        url = f"https://api.github.com/repos/{owner}/{repo}/contents/{path}"
        headers = {"Accept": "application/vnd.github.v3.raw"}
        if self.GitToken != "":
            headers["Authorization"] = f"token {self.GitToken}"

        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            content = response.text.splitlines()

            if content:
                json_data = content[0][3:]
                try:
                    metadata = json.loads(json_data) 
                    return metadata
                except json.JSONDecodeError:
                    CTkMessagebox(title="Error", message="JSON is invalid")
                    return
        CTkMessagebox(title="Error", message=f"Error {response.status_code}: {response.json()}")
        return
    
    def delete_contents_child(self):
        for widget in self.contents.winfo_children():
            widget.destroy()

        self.list_frame = []
        self.list_script_btn = []

        self.contents.rowconfigure(0, weight=0)
        self.contents.columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=0)

    def create_install_btn(self):
        """
        Creates the install button for the GUI.
        """

        btn_install = CTkButton(self.InstallBtnFrame, text="Install", command=self.install_all_script, fg_color="green")
        btn_install.grid(row=0, column=0, padx=10, pady=10, sticky="s")

        self.GameIsSelected = CTkLabel(self.InstallBtnFrame, text="No game has been selected.", text_color="red")
        self.GameIsSelected.grid(row=0, column=1, padx=10, pady=10, sticky="s")

        self.InstallBtnFrame.columnconfigure(0, weight=1)

    def create_left_menu(self):
        """
        Creates the left menu for the GUI.
        """

        btn_menu = CTkButton(self.left_menu, text="Menu", command=self.create_widgets)
        btn_menu.grid(row=0, column=0, padx=10, pady=10)

        btn_cheat = CTkButton(self.left_menu, text="Cheat", command=lambda:self.create_script_widgets("Cheat/"))
        btn_cheat.grid(row=1, column=0, padx=10, pady=10)

        btn_Enhance = CTkButton(self.left_menu, text="Enhance", command=lambda:self.create_script_widgets("Enhance/"))
        btn_Enhance.grid(row=2, column=0, padx=10, pady=10)

        btn_settings = CTkButton(self.left_menu, text="Settings", command=self.create_settings_widgets)
        btn_settings.grid(row=3, column=0, padx=10, pady=10)

        self.grid_rowconfigure(0, weight=1)
        self.left_menu.rowconfigure(4, weight=1)

        btn_about = CTkButton(self.left_menu, text="About", command=self.create_about_widgets)
        btn_about.grid(row=4, column=0, padx=10, pady=10, sticky="s")

        btn_install = CTkButton(self.left_menu, text="Install", command=lambda:print("Install !"))
        btn_install.grid(row=5, column=0, padx=10, pady=10, sticky="s")

    def create_script_widgets(self, path):
        """
        Creates the widgets for the GUI.
        """
        self.delete_contents_child()
        i = 0

        frame = CTkFrame(self.contents)
        frame.grid(row=0, column=0, padx=10, pady=10, sticky="news")
        self.contents.rowconfigure(0, weight=1)
        self.contents.columnconfigure(0, weight=1)

        script = self.getGitHubContents(path)
        for script in script:
            data = self.getScriptData(script["path"])

            frame = CTkFrame(self.contents)
            frame.grid(row=i, column=0, padx=10, pady=10, sticky="news")
            # self.list_frame.append(frame)

            btn = CTkButton(frame, text=script["name"], border_color="red", border_width=1)
            btn.configure(command=lambda event=script, frame_ref=frame, btn_ref=btn:
                          self.AddToList(event, btn_ref,
                                [var.get() if var.get() != "" else var._placeholder_text for var in frame_ref.winfo_children() if isinstance(var, CTkEntry)]),
                            )
            
            btn.grid(row=0, column=0, padx=10, pady=3, sticky="ew")
            # self.list_script_btn.append(btn)

            description = CTkLabel(frame, text=data["description"])
            description.grid(row=0, column=1, padx=10, pady=3, sticky="ew")

            if self.list_ToInstall != []:
                for src, keybind in self.list_ToInstall:
                    if src["name"] == script["name"]:
                        btn.configure(border_color="green", border_width=1)
                        for j in range(len(data["var"])):
                            var = CTkEntry(frame, placeholder_text=keybind[j])
                            var.grid(row=1, column=j, padx=10, pady=3, sticky="ew")
            else:
                for j in range(len(data["var"])):
                    var = CTkEntry(frame, placeholder_text=data["var"][j])
                    var.grid(row=1, column=j, padx=10, pady=3, sticky="ew")



            i += 1

    def create_settings_widgets(self):
        """
        Creates the widgets for the GUI.
        """
        self.delete_contents_child()

        GitTokenLabel = CTkLabel(self.contents, text="Enter you're Github Token to prevent API overload (optional)")
        GitTokenLabel.grid(row=0, column=0, padx=10, pady=10)

        GitToken = CTkEntry(self.contents, placeholder_text="Github Token")
        GitToken.grid(row=1, column=0, padx=10, pady=10)

        GitTokenBtn = CTkButton(self.contents, text="Save", command=lambda GitBtn=GitToken: self.SettingsSave(GitBtn.get()), fg_color="green")
        GitTokenBtn.grid(row=2, column=0, padx=10, pady=10)

    def SettingsSave(self, GitToken = ""):
        self.GitToken = GitToken
        if not os.path.exists("settings.txt"):
            with open("settings.txt", "w") as f:
                f.write(f"Github Token : \"{self.GitToken}\"\n")
        else:
            with open("settings.txt", "r+") as f:
                lines = f.readlines()

            for i, line in enumerate(lines):
                if line.strip().startswith('Github Token : '):
                    lines[i] = f"Github Token : \"{self.GitToken}\"\n"
                    break

            with open("settings.txt", "w") as f:
                f.writelines(lines)


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
                self.GameIsSelected.configure(text="Selected game: " + os.path.basename(self.game_path), text_color="green")
            elif os.path.exists(os.path.join(self.game_path, "js")):
                self.js_folder = os.path.join(self.game_path, "js")
                self.plugins_js = os.path.join(self.js_folder, "plugins.js")
                self.GameIsSelected.configure(text="Selected game: " + os.path.basename(self.game_path), text_color="green")
            else:
                CTkMessagebox(title="Error", message="No js or www folder found in the selected directory.")
        else:
            CTkMessagebox(title="Error", message="No game found in the selected directory.")

    def create_widgets(self):
        """
        Creates the widgets for the GUI.
        """
        self.delete_contents_child()
        self.contents.rowconfigure(0, weight=1)
        self.contents.columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        btn = CTkButton(self.contents, text="Choose game.exe directory", command=self.find_dir, height=50)
        btn.grid(row=0, column=0, padx=10, sticky="ew")

    def AddToList(self, script, btn, keybind=[]):
        if btn.cget("border_color") == "green":
            self.list_ToInstall.remove((script, keybind))
            btn.configure(border_color="red", border_width=1)
        else:
            self.list_ToInstall.append((script, keybind))
            btn.configure(border_color="green", border_width=1)

    def install_all_script(self):
        for script, keybind in self.list_ToInstall:
            # print(script, keybind)
            self.install_script(script, keybind)

    def install_script(self, script, keybind=[]):
        if self.game_path == "":
            CTkMessagebox(title="Error", message="Please select a game folder first.")
            return

        dl_link = script['download_url']

        try:
            urllib.request.urlretrieve(dl_link, os.path.join(self.js_folder, "plugins", script['name'])) # download file to the js folder
        except urllib.error.HTTPError as e:
            CTkMessagebox(title="Error", message=f"Error when downloading the script '{script['name']}': {e}")
            return

        js_file = os.path.join(self.js_folder, "plugins", script['name'])

        try:
            # change the keybind
            if keybind[0] != "":
                with open(js_file, 'r') as file:
                    lines = file.readlines()

                for i, line in enumerate(lines):
                    if line.strip().startswith('let keybind ='):
                        lines[i] = f"let keybind = {json.dumps(keybind)}; // Change keybind here\n"
                        break

                with open(js_file, 'w') as file:
                    file.writelines(lines)

            # add the script to the plugins.js
            new_plugin = {
                "name": script['name'],
                "status": True,
                "description": "",
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
        except Exception as e:
            CTkMessagebox(title="Error", message=f"Error when installing the script '{script['name']}': {e}")
        
        CTkMessagebox(title="Success", message=f"Script '{script['name']}' installed successfully !")

if __name__ == "__main__":
    app = InstallerApp()
    app.mainloop()