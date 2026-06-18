# Quick Start Guide - Run the Application

## 🚀 Easiest Way (Windows)

Simply **double-click** the `run.bat` file in the project folder. This will:
1. Create a virtual environment (if needed)
2. Install all dependencies automatically
3. Start the application
4. Open it in your browser

## 📋 Manual Steps (All Platforms)

### Step 1: Open Terminal/Command Prompt

**Windows:**
- Press `Win + R`, type `cmd`, press Enter
- Navigate to project folder:
  ```bash
  cd c:\MEGA\Professinoal\Amansour\GitHub\ai-powered-content-creation
  ```

**Mac/Linux:**
- Open Terminal
- Navigate to project folder:
  ```bash
  cd /path/to/ai-powered-content-creation
  ```

### Step 2: Create Virtual Environment (First Time Only)

```bash
python -m venv venv
```

### Step 3: Activate Virtual Environment

**Windows:**
```bash
venv\Scripts\activate
```

**Mac/Linux:**
```bash
source venv/bin/activate
```

You should see `(venv)` at the start of your command prompt.

### Step 4: Install Dependencies (First Time Only)

```bash
pip install -r requirements.txt
```

This will take 5-10 minutes to download and install all required packages.

### Step 5: Run the Application

```bash
streamlit run app.py
```

The application will automatically open in your default browser at:
```
http://localhost:8501
```

## ✅ What You Should See

1. **Browser Opens** - The app loads in your browser
2. **Home Page** - You see "AI-Powered Educational Content Creator"
3. **Green Checkmark** - "✓ API Configured" in the sidebar
4. **Ready to Use** - You can click "New Project" to start

## 🎯 First Steps in the App

1. **Click "New Project"** in the sidebar
2. **Fill in details:**
   - Title: "My First Video"
   - Topic: "Pythagorean Theorem"
   - Level: "High School"
3. **Click "Create Project"**
4. The AI will start generating content!

## ⚠️ Troubleshooting

### "Python not found"
- Install Python 3.9+ from [python.org](https://www.python.org/downloads/)
- Make sure to check "Add Python to PATH" during installation

### "pip not found"
- Python should include pip. Try:
  ```bash
  python -m pip --version
  ```

### "Module not found" errors
- Make sure virtual environment is activated (you see `(venv)`)
- Reinstall dependencies:
  ```bash
  pip install -r requirements.txt
  ```

### Port already in use
- Another app is using port 8501
- Stop other Streamlit apps or use different port:
  ```bash
  streamlit run app.py --server.port 8502
  ```

### API Key issues
- Check `.env` file exists in project root
- Verify API key is correct
- Go to Settings in the app to reconfigure

## 🛑 Stopping the Application

Press `Ctrl + C` in the terminal where the app is running.

## 📱 Accessing from Other Devices

If you want to access the app from another device on your network:

```bash
streamlit run app.py --server.address 0.0.0.0
```

Then access from other devices using:
```
http://YOUR_COMPUTER_IP:8501
```

## 💡 Tips

- **Keep terminal open** - Don't close it while using the app
- **Refresh browser** - If something looks wrong, refresh the page
- **Check terminal** - Error messages appear in the terminal
- **Save often** - Use the "Save Project" button regularly

## 📚 Next Steps

Once the app is running:
1. Read the in-app Help section
2. Check USER_GUIDE.md for detailed tutorials
3. Explore the example workflows
4. Create your first educational video!

## 🆘 Need More Help?

- Check SETUP_GUIDE.md for detailed installation
- Review TECHNICAL_SPECIFICATION.md for advanced topics
- Open an issue on GitHub
- Check the troubleshooting section in USER_GUIDE.md

---

**Ready to create amazing educational content!** 🎓✨