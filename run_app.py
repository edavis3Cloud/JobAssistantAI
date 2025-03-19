import sys
import os
from PyQt5.QtWidgets import QApplication

# Add the current directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    # Try importing the main module
    from app.main import main
    
    print("Starting Job Assistant AI application...")
    sys.exit(main())
    
except Exception as e:
    print(f"Error starting application: {e}")
    import traceback
    traceback.print_exc()
    
    # If there's an error, create a simple GUI window as fallback
    try:
        import tkinter as tk
        print("Creating fallback GUI window...")
        root = tk.Tk()
        root.title("Job Assistant AI - Fallback Window")
        root.geometry("400x300")
        
        label = tk.Label(root, text="Job Assistant AI", font=("Arial", 18))
        label.pack(pady=20)
        
        error_label = tk.Label(root, text=f"Error: {str(e)}", fg="red")
        error_label.pack(pady=10)
        
        info_label = tk.Label(root, text="See console for details", font=("Arial", 10))
        info_label.pack(pady=10)
        
        root.mainloop()
    except Exception as e2:
        print(f"Error creating fallback window: {e2}") 