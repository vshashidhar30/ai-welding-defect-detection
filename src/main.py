#in this gui for selecting process and final image in gui ,also info saved in txt file and also displyed in final gui 

import os
import cv2 # type: ignore
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk # type: ignore
from ultralytics import YOLO # type: ignore
# importing modules #

# Load the YOLO model
model_path = "../models/best.pt"
model = YOLO(model_path)

# Default output folder
output_folder = "../output_images"
results_file_path = "../results/results.txt"
test_folder=r'E:\shashi_files\My Projects\My Python Projects\python practise\defect detection system\our project\testimg'

os.makedirs(output_folder, exist_ok=True)

welding_defects = {
    "Porosity": {
        "Meaning": "Porosity is the presence of small cavities or gas pockets in the weld metal.",
        "Causes": [
            "Contaminants like moisture, oil, or rust on the base metal.",
            "Improper shielding gas flow or gas contamination.",
            "Excessive welding speed causing gas entrapment.",
            "Poor electrode storage leading to moisture absorption."
        ],
        "Solutions": [
            "Clean the base metal thoroughly before welding.",
            "Ensure proper shielding gas flow and quality.",
            "Use dry and properly stored electrodes.",
            "Control welding speed to allow gas escape."
        ]
    },
    "Spatter": {
        "Meaning": "Spatter refers to small molten metal droplets scattered around the weld area.",
        "Causes": [
            "High welding current causing excessive melting.",
            "Incorrect electrode angle or poor technique.",
            "Contaminants on the base metal.",
            "Improper gas shielding leading to arc instability."
        ],
        "Solutions": [
            "Use the correct current settings based on the material and process.",
            "Maintain a proper electrode angle and distance.",
            "Clean the workpiece surface before welding.",
            "Optimize gas shielding to stabilize the arc."
        ]
    },
    "Underfill": {
        "Meaning": "Underfill occurs when the weld bead is below the surface of the base metal, creating a weak joint.",
        "Causes": [
            "Insufficient filler metal deposition.",
            "Low heat input resulting in poor fusion.",
            "Incorrect welding speed (too fast).",
            "Inconsistent electrode positioning."
        ],
        "Solutions": [
            "Use adequate filler metal to achieve full joint penetration.",
            "Increase heat input while maintaining proper technique.",
            "Adjust welding speed to ensure proper metal flow.",
            "Ensure consistent and stable electrode positioning."
        ]
    }
}


# Global variables
image_list = []
current_index = 0
output_window = None
label_img = None
label_path = None
label_defects = None

def select_welding_folder():
    global image_list, current_index
    folder_path = filedialog.askdirectory(title="Select Welding Images Folder")
    if folder_path:
        image_list = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.lower().endswith(('jpg', 'png', 'jpeg'))]
        current_index = 0
        if image_list:
            process_images()
        else:
            messagebox.showwarning("No Images", "No valid images found in the selected folder.")

def process_images():
    with open(results_file_path, "w") as results_file:
        for image_file in os.listdir(test_folder):
            if image_file.lower().endswith(('.jpg', '.png', '.jpeg')):  
                image_path = os.path.join(test_folder, image_file)
                results = model(image_path, conf=0.3)  

                # Read image
                image = cv2.imread(image_path)

                # Process detection results
                detected_defects = set()
                for result in results:
                    for box in result.boxes:
                        x1, y1, x2, y2 = map(int, box.xyxy[0])  
                        class_id = int(box.cls[0]) if box.cls.nelement() > 0 else -1
                        label = result.names[class_id] if class_id >= 0 else "Unknown"
                        detected_defects.add(label)
                        cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
                        cv2.putText(image, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

                # Save processed image
                output_path = os.path.join(output_folder, image_file)
                cv2.imwrite(output_path, image)

                # Write results to file
                results_file.write(f"Image: {image_file}\n")
                results_file.write(f"Path: {image_path}\n")
                
                if detected_defects:
                    results_file.write("Detected Defects:\n")
                    for defect in detected_defects:
                        defect_name = defect.capitalize()  # Ensure first letter is capitalized
                        results_file.write(f" - {defect_name}\n")

                        if defect_name in welding_defects:
                            results_file.write(f"Meaning: {welding_defects[defect_name]['Meaning']}\n")
                            results_file.write("Causes:\n")
                            for cause in welding_defects[defect_name]['Causes']:
                                results_file.write(f"    - {cause}\n")
                            results_file.write("Solutions:\n")
                            for solution in welding_defects[defect_name]['Solutions']:
                                results_file.write(f"    - {solution}\n")
                            results_file.write("\n")
                    results_file.write("\n" + "-"*50 + "\n\n")
                else:
                    results_file.write("No defects detected.\n")
                    results_file.write("\n" + "-"*50 + "\n\n")

    messagebox.showinfo("Info",'A copy of results is saved in current directory as "results.txt" .')


    global output_window, label_img, label_path, label_defects, current_index
    if not image_list:
        return

    if output_window is None:
        output_window = tk.Toplevel()
        output_window.title("Welding Defect Detection Result")
        output_window.geometry("600x600")

        label_img = tk.Label(output_window)
        label_img.pack(pady=10)

        label_path = tk.Label(output_window, font=("Arial", 10), wraplength=550, justify="left")
        label_path.pack(pady=5)

        label_defects = tk.Label(output_window, font=("Arial", 10), wraplength=550, justify="left")
        label_defects.pack(pady=5)

        btn_frame = tk.Frame(output_window)
        btn_frame.pack(pady=10)

        btn_prev = tk.Button(btn_frame, text="Previous", command=lambda: navigate_images(-1))
        btn_prev.pack(side=tk.LEFT, padx=10)
        
        btn_next = tk.Button(btn_frame, text="Next", command=lambda: navigate_images(1))
        btn_next.pack(side=tk.RIGHT, padx=10)
    
    update_image()

def update_image():
    global current_index, label_img, label_path, label_defects
    image_path = image_list[current_index]
    results = model(image_path, conf=0.3)
    
    image = cv2.imread(image_path)
    detected_defects = set()
    
    for result in results:
        for box in result.boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            class_id = int(box.cls[0]) if box.cls.nelement() > 0 else -1
            label = result.names[class_id] if class_id >= 0 else "Unknown"
            detected_defects.add(label)
            cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(image, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
    
    output_path = os.path.join(output_folder, os.path.basename(image_path))
    cv2.imwrite(output_path, image)
    
    img = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    img = Image.fromarray(img)
    img.thumbnail((550, 400))
    img = ImageTk.PhotoImage(img)
    
    label_img.configure(image=img)
    label_img.image = img
    
    label_path.configure(text=f"Image: {os.path.basename(image_path)}")
    
    defect_info = "No defects detected."
    if detected_defects:
        defect_info = "Detected Defects:\n" + "\n".join([f" - {d}" for d in detected_defects])
        for defect in detected_defects:
            if defect.capitalize() in welding_defects:
                details = welding_defects[defect.capitalize()]
                defect_info += f"\nMeaning: {details['Meaning']}\nCauses:\n" + "\n".join([f"  - {c}" for c in details['Causes']])
                defect_info += f"\nSolutions:\n" + "\n".join([f"  - {s}" for s in details['Solutions']])
    
    label_defects.configure(text=defect_info)

def navigate_images(direction):
    global current_index
    if 0 <= current_index + direction < len(image_list):
        current_index += direction
        update_image()

root = tk.Tk()
root.title("Defect Detection System")
root.geometry("300x200")
root.resizable(False, False)

label = tk.Label(root, text="Select a Process", font=("Arial", 14, "bold"))
label.pack(pady=10)
def show_message(process_name):
    messagebox.showinfo("Info", f"{process_name} - Need Further Development")

buttons = [
    ("Welding", select_welding_folder),
    ("Casting", lambda: show_message("Casting")),
    ("Deep Drawing", lambda: show_message("Deep Drawing")),
]

for text, command in buttons:
    btn = tk.Button(root, text=text, font=("Arial", 12), width=25, command=command)
    btn.pack(pady=5)

root.mainloop()
