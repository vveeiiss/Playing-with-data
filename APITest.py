import tkinter as tk
import csv
import requests

API_URL = "https://api-inference.huggingface.co/models/gpt2"
API_TOKEN = "TOKEN" #HF API Token

headers = {"Authorization": f"Bearer {API_TOKEN}"}


feedback_labels = [
        "How did you like the assistance?",
        "Did the generated text make sense?",
        "In scale of 1-10 how helpful the assistance was?",
        "Will you use the plug-in again?",
        "Do you find the generated material accurate?"]

def generate_paragraph(question):
    payload = {"inputs": f"{question}","options": {"use_cache": False}}
    response = requests.post(API_URL, headers=headers, json=payload)
    data = response.json()

    if data and 'generated_text' in data[0]:
        return data[0]['generated_text'].strip()
    else:
        return "no response"

def on_button_click():
    question = prompt_entry.get()
    generated_paragraph_text = generate_paragraph(question)
    result_text.config(state="normal")
    result_text.delete("1.0", tk.END)
    result_text.insert(tk.END, generated_paragraph_text)
    result_text.config(state="disabled")

    with open("inputs.txt", "w") as input_file:
        input_file.write(question)
    with open("gen_text.txt", "w") as gen_text_file:
        gen_text_file.write(generated_paragraph_text)


def on_feedback_click():
    feedback_window = tk.Toplevel(window)
    feedback_window.title("Feedback")
    feedback_window.geometry("600x400")

    feedback_labels = [
        "How did you like the assistance?",
        "Did the generated text make sense?",
        "In scale of 1-10 how helpful the assistance was?",
        "Will you use the plug-in again?",
        "Do you find the generated material accurate?"]
    feedback_entries = []

    for label_text in feedback_labels:
        feedback_label = tk.Label(feedback_window, text=label_text)
        feedback_label.pack()

        feedback_entry = tk.Entry(feedback_window, width=40)
        feedback_entry.pack()
        feedback_entries.append(feedback_entry)

    feedback_button = tk.Button(feedback_window, text="Submit Feedback",
                                command=lambda: on_submit_feedback(feedback_entries, feedback_window),
                                bg="yellow") # color not working
    feedback_button.pack(pady=10)

def on_close_click():
    window.destroy()

def on_submit_feedback(entries, feedback_window):
    feedback_values = [entry.get() for entry in entries]

    feedback_file = "feedbacks.csv"
    with open(feedback_file, "a", newline="") as csvfile:
        feedback_writer = csv.writer(csvfile)
        if csvfile.tell() == 0:
            feedback_writer.writerow([
        "How did you like the assistance?",
        "Did the generated text make sense?",
        "In scale of 1-10 how helpful the assistance was?",
        "Will you use the plug-in again?",
        "Do you find the generated material accurate?"])
        feedback_writer.writerow(feedback_values)

    feedback_window.destroy()
    window.destroy()

window = tk.Tk()
window.title("Generator")
window.geometry("600x400")

prompt_label = tk.Label(window, text="Enter Text:")
prompt_label.pack()

prompt_entry = tk.Entry(window, width=40)
prompt_entry.pack()

generate_button = tk.Button(window, text="Generate", command=on_button_click)
generate_button.pack(pady=10)
generate_button.configure(bg="blue") #not working fo no reason


result_text = tk.Text(window, height=5, width=40, state="disabled")
result_text.pack()


feedback_button = tk.Button(window, text="Feedback", command=on_feedback_click)
feedback_button.pack(pady=10)
feedback_button.configure(bg="yellow") #not working

window.mainloop()
