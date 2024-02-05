from pytube import YouTube, Playlist
import customtkinter as ctk
import os
import getpass
from tkinter import filedialog, messagebox
    
class downloader(ctk.CTk):
    user_input = ""
    output_folder = ""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.title("YouTube music downloader")
        self.geometry("400x400")
        
        self.grid_columnconfigure([i for i in range(1,11)], weight= 1, uniform= "yes")
        self.grid_rowconfigure([i for i in range(1, 11)], weight= 1, uniform= "yes")
        
        self.hi_message = ctk.CTkLabel(master = self,
                                       corner_radius= 20,
                                       text = f"Hi {getpass.getuser()} !")
        self.hi_message.grid(row = 1, column = 4, columnspan = 3)
        
        self.let_the_user_know_what_we_accept = ctk.CTkLabel(master= self,
                                                             corner_radius= 20,
                                                             text = "Enter a YouTube link or click on 'Select text docuemnt'.\n After that, please select a folder where the music will be saved.")
        self.let_the_user_know_what_we_accept.grid(row = 2, column = 1, columnspan = 10)

        self.path_link = ctk.CTkEntry(master= self,
                                      placeholder_text= "Enter YT link or path to .txt")
        self.path_link.grid(row = 3, column = 1, columnspan = 10, sticky = "news")
        
        self.path_to_txt = ctk.CTkButton(master= self, 
                                         text= "Click here to select a .txt file with links",
                                         command= self.select_text_file)
        self.path_to_txt.grid(row = 4, column = 1, columnspan = 10)
        
        self.button_output_path = ctk.CTkButton(master = self,
                                                text = "Click here to select destination",
                                                command= self.select_output_path)
        self.button_output_path.grid(row = 5, column = 1, columnspan = 10)
        
        self.run_button = ctk.CTkButton(master = self,
                                        text = "Run",
                                        command= self.run)
        self.run_button.grid(row = 6, column = 5)
        
        self._yes_this_program_does_something = ctk.CTkLabel(master= self,
                                                             text = "Input:" + self.user_input + "\n" "Output: " + self.output_folder)
        self._yes_this_program_does_something.grid(row= 7, rowspan = 3, column = 1, columnspan = 10, sticky = "news")
        
    def select_text_file(self):
        self.user_input = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        self.we_do_not_sleep()

    def select_output_path(self):
        self.output_folder = filedialog.askdirectory(title="Select a directory")
        self.we_do_not_sleep()

    def run(self):
        try:
            main(user_input = self.user_input, output_folder = self.output_folder)
        except:
            if self.path_link.get() == "" and self.user_input == "":
                messagebox.showerror("Error", "Please select a YT link or select a .txt file with links")
            if self.output_folder == "":
                messagebox.showerror("Error", "Please select an output directory")

    def we_do_not_sleep(self):
        self._yes_this_program_does_something.configure(text = "Input:" + self.user_input + "\n" "Output: " + self.output_folder)
        
    
        
def download_video(url, output_path="."):
    try:
        yt = YouTube(url)
        title = yt.title
        duration = yt.length
        print(f"Downloading: {title}")


        if duration >= 150 and "Interview" not in title:
            audio_stream = yt.streams.filter(only_audio=True).first()
            audio_stream.download(output_path)
            print(f"Finished downloading: {title}")
        else:
            print(f"Skipped: {title} (Doesn't meet requirements)")
    except Exception as e:
        print(f"Error: {e}")

def download_playlist(url, output_path="."):
    try:
        playlist = Playlist(url)
        for video_url in playlist.video_urls:
            download_video(video_url, output_path)
    except Exception as e:
        print(f"Error: {e}")
        
def download_from_txt(file_path, output_path="."):
    try:
        with open(file_path, 'r') as file:
            for line in file:
                url = line.strip()
                if url:
                    if "&list=" in url.lower():
                        download_playlist(url, output_path)
                    elif "watch" in url.lower() and "&list=" not in url.lower():
                        download_video(url, output_path)
                    else:
                        downloader.doing_something = f"Invalid YouTube link in the file: {url}"
                        downloader.we_do_not_sleep()
    except Exception as e:
        print(f"Error reading from file: {e}")

def main(user_input, output_folder):
    if user_input.lower().endswith('.txt'):
        download_from_txt(user_input, output_folder)
    else:
        if "&list=" in user_input.lower():
            download_playlist(user_input, output_folder)
        elif "watch" in user_input.lower() and "&list=" not in user_input.lower():
            download_video(user_input, output_folder)
        else:
            print("Invalid YouTube link or file path.")
        
if __name__ == "__main__":
    program = downloader()
    program.mainloop()
