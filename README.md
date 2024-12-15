# How to Run This Project Locally  

1. **Check Python Installation**  
   - Open your terminal and run:  
     ```bash
     python -V
     ```  
   - If a Python version is displayed, Python is installed on your system.  
   - If you see an error, [download and install Python](https://www.python.org/downloads/).  

2. **Set Up a Virtual Environment**  
   - Run the following command to create a virtual environment:  
     ```bash
     python -m venv .venv
     ```  
     If you're using macOS, you may need to use `python3`:  
     ```bash
     python3 -m venv .venv
     ```  

3. **Activate the Virtual Environment**  
   - On **Windows**, run:  
     ```bash
     .venv\Scripts\activate.bat
     ```  
   - On **Linux/macOS**, run:  
     ```bash
     source .venv/bin/activate
     ```  

4. **Install Dependencies**  
   - Run the following command to install the required dependencies:  
     ```bash
     pip install -r requirements.txt
     ```  

5. **Start the Project**  
   - Launch the application with:  
     ```bash
     python main.py
     ```  
     On macOS, you may need to use:  
     ```bash
     python3 main.py
     ```  

---

# Running Tests  

- To run tests, execute the following command in your terminal:  
  ```bash
  python game_test.py
  ```  