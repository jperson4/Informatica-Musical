import tkinter as tk
from tkinter import ttk

class SynthGUI(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Synth Control Panel")
        self.geometry("600x300")
        self.configure(padx=10, pady=10)

        self.knob_options = [
            "None", "Frequency", "Amplitude", "Attack", "Decay", "Sustain", "Release"
        ]
        self.waveforms = ["Sine", "Square", "Triangle", "Sawtooth"]

        self.create_widgets()

    def create_widgets(self):
        # Comboboxes for knob assignments
        self.knob_selectors = []
        for i in range(8):
            combo = ttk.Combobox(self, values=self.knob_options, state="readonly")
            combo.set(f"Knob {i+1}")
            combo.grid(row=i//4, column=i%4, padx=10, pady=10)
            self.knob_selectors.append(combo)

        # Waveform selection
        ttk.Label(self, text="Base Waveform:").grid(row=2, column=0, pady=10, sticky="w")
        self.waveform_selector = ttk.Combobox(self, values=self.waveforms, state="readonly")
        self.waveform_selector.set("Sine")
        self.waveform_selector.grid(row=2, column=1, pady=10, sticky="w")

        # Amplitude modulation options
        self.amp_mod_var = tk.BooleanVar()
        self.amp_mod_check = ttk.Checkbutton(
            self, text="Enable Amplitude Modulation", variable=self.amp_mod_var,
            command=self.toggle_amp_mod_selector
        )
        self.amp_mod_check.grid(row=3, column=0, columnspan=2, sticky="w")

        ttk.Label(self, text="Modulation Waveform:").grid(row=3, column=2, pady=10, sticky="e")
        self.mod_wave_selector = ttk.Combobox(self, values=self.waveforms, state="disabled")
        self.mod_wave_selector.set("Sine")
        self.mod_wave_selector.grid(row=3, column=3, sticky="w")

        # Button to add more waveforms
        self.add_waveform_button = ttk.Button(
            self, text="Add Waveform", command=self.add_waveform
        )
        self.add_waveform_button.grid(row=4, column=0, pady=10, sticky="w")

        # List to store dynamically added waveform comboboxes
        self.additional_waveform_selectors = []

    def toggle_amp_mod_selector(self):
        if self.amp_mod_var.get():
            self.mod_wave_selector.configure(state="readonly")
        else:
            self.mod_wave_selector.configure(state="disabled")

    def add_waveform(self):
        # Add a new combobox for waveform selection
        new_waveform_selector = ttk.Combobox(self, values=self.waveforms, state="readonly")
        new_waveform_selector.set("Sine")
        new_waveform_selector.grid(row=5 + len(self.additional_waveform_selectors), column=0, pady=10, sticky="w")
        self.additional_waveform_selectors.append(new_waveform_selector)

    def get_values(self):
        # Retrieve knob assignments
        knob_values = [combo.get() for combo in self.knob_selectors]

        # Retrieve waveform selection
        base_waveform = self.waveform_selector.get()

        # Retrieve amplitude modulation settings
        amp_mod_enabled = self.amp_mod_var.get()
        mod_waveform = self.mod_wave_selector.get() if amp_mod_enabled else None

        # Retrieve additional waveforms
        additional_waveforms = [combo.get() for combo in self.additional_waveform_selectors]

        return {
            "knob_values": knob_values,
            "base_waveform": base_waveform,
            "amp_mod_enabled": amp_mod_enabled,
            "mod_waveform": mod_waveform,
            "additional_waveforms": additional_waveforms
        }

    def show_gui(self):
        self.mainloop()
