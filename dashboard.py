import tkinter as tk
from tkinter import ttk, messagebox
from agents.farmer_advisor import FarmerAdvisor

# Load your trained advisor model
advisor = FarmerAdvisor("dataset_farming/farmer_advisor_dataset.csv")

# Dashboard class
class FarmingDashboard:
    def __init__(self, root):
        self.root = root
        self.root.title("AI-Driven Farming Advisor")
        self.root.geometry("650x500")
        self.root.configure(bg="#f4f4f4")
        
        title = tk.Label(root, text="🌾 AI-Driven Farming Advisor", font=("Helvetica", 20, "bold"), bg="#f4f4f4", fg="#2c3e50")
        title.pack(pady=20)

        # Input frame
        frame = tk.Frame(root, bg="#ffffff", bd=2, relief=tk.GROOVE)
        frame.pack(padx=30, pady=10, fill="both", expand=True)

        # Input fields
        self.entries = {}
        labels = ["Farm ID", "Crop Type", "Crop Yield (ton)", "Fertilizer Usage (kg)", "Pesticide Usage (kg)"]
        keys = ["farm_id", "crop_type", "crop_yield_ton", "fertilizer_usage_kg", "pesticide_usage_kg"]

        for i, (label, key) in enumerate(zip(labels, keys)):
            tk.Label(frame, text=label + ":", font=("Helvetica", 12), anchor="w", bg="#ffffff").grid(row=i, column=0, padx=15, pady=10, sticky="w")
            entry = ttk.Entry(frame, font=("Helvetica", 12))
            entry.grid(row=i, column=1, padx=15, pady=10)
            self.entries[key] = entry

        # Submit button
        self.result_text = tk.StringVar()
        submit_btn = ttk.Button(root, text="Get Recommendation", command=self.predict_crop)
        submit_btn.pack(pady=10)

        # Result
        result_label = tk.Label(root, textvariable=self.result_text, font=("Helvetica", 14, "bold"), fg="green", bg="#f4f4f4")
        result_label.pack(pady=10)

    def predict_crop(self):
        try:
            input_data = {
                "farm_id": int(self.entries["farm_id"].get()),
                "crop_type": self.entries["crop_type"].get(),
                "crop_yield_ton": float(self.entries["crop_yield_ton"].get()),
                "fertilizer_usage_kg": float(self.entries["fertilizer_usage_kg"].get()),
                "pesticide_usage_kg": float(self.entries["pesticide_usage_kg"].get())
            }

            result = advisor.get_recommendations(input_data)

            if "error" in result:
                self.result_text.set("⚠️ " + result["error"])
            else:
                self.result_text.set(f"🌱 Recommended Crop: {result['prediction']} ({result['confidence']}% confidence)")

        except Exception as e:
            messagebox.showerror("Input Error", str(e))

# Run dashboard
if __name__ == "__main__":
    root = tk.Tk()
    app = FarmingDashboard(root)
    root.mainloop()
