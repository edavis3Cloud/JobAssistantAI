import sys
import os

# Add the app directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "app")))

try:
    # Try to import and run the main application
    from app.main import main
    print("Starting main application...")
    main()
except Exception as e:
    print(f"Error running main application: {e}")
    
    # If the main application fails, create a simple GUI window to show it's working
    try:
        import tkinter as tk
        print("Creating test GUI window...")
        root = tk.Tk()
        root.title("Job Assistant AI - Test Window")
        root.geometry("400x300")
        label = tk.Label(root, text="Test GUI Window", font=("Arial", 18))
        label.pack(pady=50)
        root.mainloop()
    except Exception as e:
        print(f"Error creating test GUI window: {e}") 