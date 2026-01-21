# How to Run Glue Jobs in VS Code

## ⚠️ IMPORTANT: Don't use "Run Python File"

The default "Run Python File" button (▶️) in VS Code runs Python directly in your venv, which will **NOT work** for Glue jobs because `awsglue` libraries only exist in Docker.

## ✅ CORRECT WAY: Use Run and Debug Panel

### Method 1: Run and Debug Panel (Recommended)

1. **Open the Run and Debug panel:**
   - Click the **Run and Debug** icon in the left sidebar (play button with bug icon)
   - OR press `Cmd+Shift+D`

2. **Select a configuration from the dropdown:**
   - `Run Current Glue Job in Docker` - Runs the currently open .py file
   - `Run simple_glue_job.py` - Runs the simple job
   - `Run sample_etl_job.py` - Runs the ETL job
   - `Start Glue Jupyter Notebook` - Opens Jupyter in browser
   - `Start Glue PySpark Shell` - Opens interactive shell

3. **Click the green play button** or press `F5`

### Method 2: Command Palette

1. Press `Cmd+Shift+P` (or `F1`)
2. Type: `Tasks: Run Task`
3. Select: `Run Glue Job in Docker`

### Method 3: Terminal (Always Works)

```bash
cd sample-PySpark-project/scripts
./run_glue_job.sh simple_glue_job.py
./run_glue_job.sh sample_etl_job.py
```

## 🎯 Step-by-Step Visual Guide

### Step 1: Open Run and Debug
![Screenshot: Click the play-with-bug icon on the left sidebar]

### Step 2: Choose Configuration
![Screenshot: Click the dropdown at the top of the panel]

### Step 3: Click the Green Play Button
![Screenshot: Click the green triangle next to the dropdown]

## 🚫 Common Mistakes

### ❌ WRONG: Clicking "Run Python File"
This runs Python in your venv → `ModuleNotFoundError: No module named 'awsglue'`

### ✅ RIGHT: Using Run and Debug panel
This runs the job inside Docker → Success!

## 📝 Why This Happens

- AWS Glue libraries (`awsglue`, `pyspark` configured for Glue) only exist in the Docker container
- Your local venv doesn't have these libraries (and they're not available via pip)
- All Glue jobs must run inside the Docker container using the provided scripts

## 🔍 Troubleshooting

**Q: I don't see "Run Current Glue Job in Docker" in the dropdown**
- Make sure you're in the Run and Debug panel (Cmd+Shift+D)
- Check that `.vscode/launch.json` exists
- Try reloading VS Code window: `Cmd+Shift+P` → `Reload Window`

**Q: The job still runs in venv**
- Don't use the "Run Python File" button
- Use the Run and Debug panel instead

**Q: Can I debug the code?**
- Direct debugging inside Docker is complex
- Use print statements for debugging
- Or use Jupyter notebook: `./start_jupyter.sh`
