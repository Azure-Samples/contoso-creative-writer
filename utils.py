import tkinter as tk
import urllib.request
import logging

def show_privacy_consent() -> bool:
    """Display a pop-up window to obtain user consent for data collection and privacy."""
    def on_accept():
        user_consent.set(True)
        root.destroy()
    def on_decline():
        user_consent.set(False)
        root.destroy()
    root = tk.Tk()
    root.title("Data Permission and Privacy")
    message = ("We value your privacy. By using this application, you consent to the collection and use of your data "
               "as described in our privacy policy. Do you agree to proceed?")
    label = tk.Label(root, text=message, wraplength=400, justify="left")
    label.pack(padx=20, pady=20)
    button_frame = tk.Frame(root)
    button_frame.pack(pady=10)
    accept_button = tk.Button(button_frame, text="Accept", command=on_accept)
    accept_button.pack(side="left", padx=10)
    decline_button = tk.Button(button_frame, text="Decline", command=on_decline)
    decline_button.pack(side="right", padx=10)
    user_consent = tk.BooleanVar()
    root.mainloop()
    return user_consent.get()

def download_database(url: str, file_path: str) -> None:
    """Download the database file from the given URL."""
    try:
        logging.info(f"Downloading database from {url}...")
        urllib.request.urlretrieve(url, file_path)
        logging.info("Download complete.")
    except urllib.error.URLError as e:
        logging.error(f"Error: Failed to download database. {e}")
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
