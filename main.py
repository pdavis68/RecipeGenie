import tkinter as tk
from tkinter import ttk, scrolledtext, filedialog, messagebox
import json
import os
import sys
import traceback
import pyperclip  # For clipboard functionality
from recipe_generator import RecipeGenerator
from recipe_printer import print_recipe
from debug_utils import log_error, save_recipe_data

class RecipeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Recipe Genie")
        self.root.geometry("600x400")
        self.root.minsize(600, 400)  
        
        self.config = self.load_config()
        self.recipe_generator = RecipeGenerator(self.config)
        
        self.create_main_window()
    
    def load_config(self):
        """Load configuration from config.json file"""
        config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config.json')
        try:
            with open(config_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            messagebox.showerror("Error", "config.json file not found. Please create one.")
            sys.exit(1)
        except json.JSONDecodeError:
            messagebox.showerror("Error", "Invalid config.json file.")
            sys.exit(1)
    
    def create_main_window(self):
        """Create the main input window"""
        # Create a frame for the form
        form_frame = ttk.Frame(self.root, padding="20")
        form_frame.pack(fill=tk.BOTH, expand=True)
        
        # Store references to input widgets for enabling/disabling
        self.input_widgets = []
        
        # Cuisine selection
        ttk.Label(form_frame, text="Cuisine:").grid(column=0, row=0, sticky=tk.W, pady=5)
        self.cuisine_var = tk.StringVar()
        self.cuisine_combo = ttk.Combobox(form_frame, textvariable=self.cuisine_var, width=30)
        self.input_widgets.append(self.cuisine_combo)
        self.cuisine_combo['values'] = [
            "American", "American (Cajun)", "American (California Style)", "American (Creole)", 
            "American (Hawaiian)", "American (Midwestern)",  "American (New England)", "American (Pacific Northwest)", 
            "American (Soul Food)", "American (Southern)",  "American (Southwestern)", "American (Tex-Mex)", 
            "Argentinian", "Australian", "Brazilian", "British", "Caribbean", "Chinese", "Chinese (Cantonese)", 
            "Chinese (Szechuan)", "Chinese (Hunan)",  "Cuban", "Dutch", "Estonian", "Ethiopian", "Filipino", "Finnish" 
            "French", "Fusion", "German",  "Greek", "Indian", "Indian (Northern)", "Indian (Southern)", "Indian (Eastern)", 
            "Indian (Western)", "Indonesian", "Irish", "Italian", "Italian (Northern)", "Italian (Central)", 
            "Italian (Southern)", "Jamaican", "Japanese", "Korean", "Lebanese", "Malaysian", "Mediterranean", 
            "Mexican (authentic)", "Mexican (Oaxacan)", "Mexican (Michoacan)", "Mexican (Yucatan)",
            "Mexican (Vera Cruz)", "Mexican (Puebla)", "Mexican (Jalisco)", "Mexican (Chiapas)", 
            "Mexican (Guerrero)", "Mexican (Northern)", "Middle Eastern", "Moroccan", "New England", 
            "New Zealand", "Peruvian", "Polish", "Russian", "Sardinian", "Scandinavian", "Sicilian", 
            "South African", "Spanish", "Taiwanese","Thai", "Thai (Northern)", "Thai (Central)", "Thai (Southern)", 
            "Turkish", "Vietnamese"
        ]
        self.cuisine_combo.grid(column=1, row=0, sticky=(tk.W, tk.E), pady=5)
        
        # Main ingredient
        ttk.Label(form_frame, text="Main Ingredient:").grid(column=0, row=1, sticky=tk.W, pady=5)
        self.centerpiece_var = tk.StringVar()
        centerpiece_entry = ttk.Entry(form_frame, textvariable=self.centerpiece_var, width=30)
        centerpiece_entry.grid(column=1, row=1, sticky=(tk.W, tk.E), pady=5)
        self.input_widgets.append(centerpiece_entry)
        
        # Calories
        ttk.Label(form_frame, text="Calories per Serving:").grid(column=0, row=2, sticky=tk.W, pady=5)
        self.calories_var = tk.StringVar(value="500")
        calories_entry = ttk.Entry(form_frame, textvariable=self.calories_var, width=30)
        calories_entry.grid(column=1, row=2, sticky=(tk.W, tk.E), pady=5)
        self.input_widgets.append(calories_entry)
        
        # Servings
        ttk.Label(form_frame, text="Number of Servings:").grid(column=0, row=3, sticky=tk.W, pady=5)
        self.servings_var = tk.StringVar(value="4")
        servings_entry = ttk.Entry(form_frame, textvariable=self.servings_var, width=30)
        servings_entry.grid(column=1, row=3, sticky=(tk.W, tk.E), pady=5)
        self.input_widgets.append(servings_entry)
        
        # Maximum Prep Time
        ttk.Label(form_frame, text="Maximum Prep Time (minutes):").grid(column=0, row=4, sticky=tk.W, pady=5)
        self.prep_time_var = tk.StringVar(value="30")
        prep_time_entry = ttk.Entry(form_frame, textvariable=self.prep_time_var, width=30)
        prep_time_entry.grid(column=1, row=4, sticky=(tk.W, tk.E), pady=5)
        self.input_widgets.append(prep_time_entry)
        
        # Additional information
        ttk.Label(form_frame, text="Additional Information:").grid(column=0, row=5, sticky=tk.W, pady=5)
        self.additional_info_text = scrolledtext.ScrolledText(form_frame, width=40, height=6, wrap=tk.WORD)  # Reduced height
        self.additional_info_text.grid(column=0, row=6, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        self.input_widgets.append(self.additional_info_text)
        
        # Generate button
        self.generate_button = ttk.Button(form_frame, text="Generate Recipe", command=self.generate_recipe)
        self.generate_button.grid(column=0, row=7, columnspan=2, pady=10)  # Reduced padding
        self.input_widgets.append(self.generate_button)
        
        # Configure grid weights
        form_frame.columnconfigure(1, weight=1)
        
    def create_results_window(self, recipe_data):
        """Create the results window to display the generated recipe"""
        results_window = tk.Toplevel(self.root)
        results_window.title(recipe_data["title"])
        results_window.geometry("700x700")
        results_window.minsize(700, 700)
        
        # Create a frame for the content
        content_frame = ttk.Frame(results_window, padding="20")
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        # Recipe title
        title_label = ttk.Label(content_frame, text=recipe_data["title"], font=("Arial", 16, "bold"))
        title_label.pack(anchor=tk.W, pady=(0, 10))
        
        # Recipe description
        desc_label = ttk.Label(content_frame, text=recipe_data["description"], wraplength=650)
        desc_label.pack(anchor=tk.W, pady=(0, 15))
        
        # Recipe details
        time_info = ""
        if "prep_time_minutes" in recipe_data:
            time_info = f" | Prep: {recipe_data['prep_time_minutes']} min"
        if "cook_time_minutes" in recipe_data:
            time_info += f" | Cook: {recipe_data['cook_time_minutes']} min"
            
        details_text = f"Cuisine: {recipe_data['cuisine']} | Servings: {recipe_data['servings']} | Calories: {recipe_data['calories_per_serving']} per serving{time_info}"
        details_label = ttk.Label(content_frame, text=details_text)
        details_label.pack(anchor=tk.W, pady=(0, 15))
        
        # Recipe content
        recipe_text = scrolledtext.ScrolledText(content_frame, width=80, height=25, wrap=tk.WORD)
        recipe_text.pack(fill=tk.BOTH, expand=True, pady=(0, 15))
        
        # Format the recipe text
        formatted_recipe = self.format_recipe_text(recipe_data)
        recipe_text.insert(tk.END, formatted_recipe)
        recipe_text.config(state=tk.DISABLED)  # Make it read-only
        
        # Buttons frame
        buttons_frame = ttk.Frame(content_frame)
        buttons_frame.pack(fill=tk.X, pady=(0, 10))
        
        # New Recipe button
        new_recipe_btn = ttk.Button(buttons_frame, text="New Recipe", 
                                   command=results_window.destroy)
        new_recipe_btn.pack(side=tk.LEFT, padx=5)
        
        # Print button
        print_btn = ttk.Button(buttons_frame, text="Print", 
                              command=lambda: print_recipe(recipe_data, formatted_recipe))
        print_btn.pack(side=tk.LEFT, padx=5)
        
        # Copy to Clipboard button
        copy_btn = ttk.Button(buttons_frame, text="Copy to Clipboard", 
                             command=lambda: self.copy_to_clipboard(recipe_data, formatted_recipe))
        copy_btn.pack(side=tk.LEFT, padx=5)
        
        # Export button
        export_btn = ttk.Button(buttons_frame, text="Export...", 
                               command=lambda: self.export_recipe(recipe_data, formatted_recipe))
        export_btn.pack(side=tk.LEFT, padx=5)
        
        # Store recipe data for later use
        self.current_recipe = recipe_data
        self.formatted_recipe = formatted_recipe
    
    def generate_recipe(self):
        """Generate a recipe using the LLM based on user inputs"""
        # Get values from form
        cuisine = self.cuisine_var.get().strip()
        centerpiece = self.centerpiece_var.get().strip()
        calories = self.calories_var.get().strip()
        servings = self.servings_var.get().strip()
        prep_time = self.prep_time_var.get().strip()
        additional_info = self.additional_info_text.get("1.0", tk.END).strip()
        
        # Validate inputs
        if not cuisine or not centerpiece or not calories or not servings or not prep_time:
            messagebox.showerror("Error", "Please fill in all required fields.")
            return
        
        try:
            calories = int(calories)
            servings = int(servings)
            prep_time = int(prep_time)
        except ValueError:
            messagebox.showerror("Error", "Calories, servings, and prep time must be numbers.")
            return
        
        # Show loading indicator and disable controls
        self.set_busy_state(True)
        
        try:
            # Generate recipe
            recipe_data = self.recipe_generator.generate_recipe(
                cuisine, centerpiece, calories, servings, prep_time, additional_info
            )
            
            # Save recipe data for debugging
            save_recipe_data(recipe_data)
            
            # Validate recipe data before displaying
            if not isinstance(recipe_data, dict):
                error_msg = f"Invalid recipe data format: {type(recipe_data)}"
                log_error(error_msg, recipe_data)
                raise ValueError(error_msg)
            
            required_keys = ["title", "description", "cuisine", "servings", 
                            "calories_per_serving", "ingredients", "instructions", "nutrition"]
            missing_keys = [key for key in required_keys if key not in recipe_data]
            if missing_keys:
                error_msg = f"Recipe data missing required keys: {', '.join(missing_keys)}"
                log_error(error_msg, recipe_data)
                raise ValueError(error_msg)
            
            # Display results
            self.create_results_window(recipe_data)
        except Exception as e:
            error_message = f"Failed to generate recipe: {str(e)}"
            print(f"Error: {error_message}")
            print(traceback.format_exc())
            log_error(error_message, traceback.format_exc())
            messagebox.showerror("Error", error_message)
        finally:
            # Reset cursor and re-enable controls
            self.set_busy_state(False)
    
    def format_recipe_text(self, recipe_data):
        """Format the recipe data as readable text"""
        text = "TIME REQUIRED:\n"
        text += "=" * 50 + "\n"
        text += f"Preparation: {recipe_data['prep_time_minutes']} minutes\n"
        text += f"Cooking: {recipe_data['cook_time_minutes']} minutes\n"
        text += f"Total: {recipe_data['prep_time_minutes'] + recipe_data['cook_time_minutes']} minutes\n\n"
        
        text += "INGREDIENTS:\n"
        text += "=" * 50 + "\n"
        for ingredient in recipe_data["ingredients"]:
            text += f"• {ingredient['amount']} {ingredient['name']}\n"
        
        text += "\n\nINSTRUCTIONS:\n"
        text += "=" * 50 + "\n"
        for i, step in enumerate(recipe_data["instructions"], 1):
            text += f"{i}. {step}\n\n"
        
        text += "NUTRITION INFORMATION:\n"
        text += "=" * 50 + "\n"
        nutrition = recipe_data["nutrition"]
        text += f"Calories: {nutrition['calories']} per serving\n"
        text += f"Protein: {nutrition['protein_g']}g\n"
        text += f"Fat: {nutrition['fat_g']}g\n"
        text += f"Carbohydrates: {nutrition['carbohydrates_g']}g\n"
        
        return text
    
    def copy_to_clipboard(self, recipe_data, formatted_text):
        """Copy the recipe to the clipboard"""
        clipboard_text = f"{recipe_data['title']}\n\n"
        clipboard_text += f"{recipe_data['description']}\n\n"
        clipboard_text += formatted_text
        
        try:
            pyperclip.copy(clipboard_text)
            messagebox.showinfo("Success", "Recipe copied to clipboard!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to copy to clipboard: {str(e)}")
    
    def set_busy_state(self, is_busy):
        """Set the busy state of the application
        
        Args:
            is_busy (bool): True to show busy cursor and disable controls, False to restore normal state
        """
        if is_busy:
            # Set busy cursor for all widgets
            self.root.config(cursor="watch")
            for widget in self.root.winfo_children():
                widget.config(cursor="watch")
            
            # Disable all input widgets
            for widget in self.input_widgets:
                if isinstance(widget, ttk.Button):
                    widget.state(['disabled'])
                elif isinstance(widget, scrolledtext.ScrolledText):
                    widget.config(state=tk.DISABLED)
                else:
                    widget.config(state="disabled")
        else:
            # Reset cursor for all widgets
            self.root.config(cursor="")
            for widget in self.root.winfo_children():
                widget.config(cursor="")
            
            # Re-enable all input widgets
            for widget in self.input_widgets:
                if isinstance(widget, ttk.Button):
                    widget.state(['!disabled'])
                elif isinstance(widget, scrolledtext.ScrolledText):
                    widget.config(state=tk.NORMAL)
                else:
                    widget.config(state="normal")
        
        # Force update to show changes immediately
        self.root.update()
    
    def export_recipe(self, recipe_data, formatted_text):
        """Export the recipe to a text file"""
        filename = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
            initialfile=f"{recipe_data['title'].replace(' ', '_')}.txt"
        )
        
        if filename:
            try:
                with open(filename, 'w') as f:
                    f.write(f"{recipe_data['title']}\n\n")
                    f.write(f"{recipe_data['description']}\n\n")
                    f.write(formatted_text)
                messagebox.showinfo("Success", "Recipe exported successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to export recipe: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = RecipeApp(root)
    root.mainloop()
