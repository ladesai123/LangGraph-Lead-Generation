# 🚀 WHAT TO RUN IN YOUR VIDEO - Complete Guide

## 🎯 THE MAIN COMMAND (This is what matters!)

### **THE ONE COMMAND FOR YOUR DEMO:**

```powershell
python langgraph_builder.py
```

**That's it!** This runs the ENTIRE pipeline (all 7 agents automatically).

---

## 🎬 COMPLETE VIDEO DEMO SEQUENCE

### **STEP-BY-STEP: What to Run and When**

---

### **1. PREPARATION (Before Recording)**

Open PowerShell and navigate to project:

```powershell
cd "C:\Users\LADE SAI TEJA\OneDrive\Desktop\LeadGenerator"
```

Clear the screen for a clean demo:

```powershell
cls
```

**DON'T RECORD YET!** This is just setup.

---

### **2. START RECORDING (Win + Alt + R)**

Now press **Win + Alt + R** to start recording!

---

### **3. SHOW PROJECT STRUCTURE (Optional)**

**OPTIONAL:** Show files in the project (makes it look professional):

```powershell
Get-ChildItem
```

**Say while it runs:**
> "Here's my project. You can see the agents folder, tools folder, and all the configuration files."

**Time: 10 seconds**

---

### **4. MAIN DEMO - RUN THE PIPELINE! ⭐⭐⭐**

### **THIS IS THE MAIN EVENT:**

```powershell
python langgraph_builder.py
```

**Say BEFORE you run it:**
> "Now watch the entire pipeline run. All 7 agents will execute automatically, generate personalized emails with AI, and send them for real. Let's go!"

**Then press Enter and watch!**

**While it runs, narrate what you see:**
> "Look at this:
> - Loading the 7 agents...
> - Agent 1: Found 10 prospects
> - Agent 2: Enriching data...
> - Agent 3: Scoring... all approved!
> - Agent 4: Generating emails with Gemini AI... see how fast?
> - Agent 5: Sending real emails via SendGrid...
> - Email 1... Status 202 ✅
> - Email 2... Status 202 ✅
> - All 10 sent successfully!
> - Agent 6 and 7: Tracking and learning...
> - Done! 100% success rate!"

**Time: 1-2 minutes** (including your narration)

---

### **5. SHOW THE OUTPUT FILE**

After the pipeline finishes, show the results:

```powershell
Get-ChildItem output | Sort-Object LastWriteTime -Descending | Select-Object -First 1
```

**Say:**
> "The results were saved to this output file. Let me show you what's inside."

**Then open the file in VS Code:**

```powershell
code (Get-ChildItem output | Sort-Object LastWriteTime -Descending | Select-Object -First 1).FullName
```

**OR just open it manually in VS Code and scroll through!**

**Say while showing:**
> "Here you can see all 10 emails that were generated. Each one is personalized with AI - mentioning the company, their technologies, recent news. Look at this one for Google - it talks about Gemini 2 and TensorFlow!"

**Time: 1 minute**

---

### **6. SHOW THE TRACKING DASHBOARD**

**If webhook server is running**, open browser and show:

**Navigate to:**
```
http://localhost:5000
```

**Say:**
> "And here's the real-time tracking dashboard. You can see all 10 emails delivered, who opened them, who clicked - all tracked live!"

**Time: 30 seconds**

---

### **7. STOP RECORDING**

Press **Win + Alt + R** to stop recording.

---

## 📋 COMPLETE RUN SEQUENCE (COPY-PASTE READY)

**Here's everything in order - you can copy this whole block:**

```powershell
# BEFORE RECORDING - Setup
cd "C:\Users\LADE SAI TEJA\OneDrive\Desktop\LeadGenerator"
cls

# START RECORDING NOW (Win + Alt + R)

# 1. Show project structure (optional)
Get-ChildItem

# 2. RUN THE MAIN PIPELINE ⭐⭐⭐
python langgraph_builder.py

# 3. Show the output file
Get-ChildItem output | Sort-Object LastWriteTime -Descending | Select-Object -First 1

# 4. Open the results in VS Code
code (Get-ChildItem output | Sort-Object LastWriteTime -Descending | Select-Object -First 1).FullName

# 5. Open tracking dashboard in browser
# Go to: http://localhost:5000

# STOP RECORDING (Win + Alt + R)
```

---

## 🎯 MINIMAL VERSION (If Short on Time)

**Just run ONE command:**

```powershell
python langgraph_builder.py
```

That's literally all you need! Everything else is bonus.

---

## ⚠️ TROUBLESHOOTING

### **Problem: "python is not recognized"**

**Solution:** Use full path:

```powershell
python.exe langgraph_builder.py
```

### **Problem: Dependencies missing**

**Run this BEFORE recording:**

```powershell
pip install -r requirements.txt
```

### **Problem: .env file not found**

**Make sure .env exists with your API keys:**

```powershell
Get-Content .env
```

Should show:
```
GEMINI_API_KEY=...
SENDGRID_API_KEY=...
FROM_EMAIL=126156075@sastra.ac.in
```

---

## 🎬 WHAT TO SHOW IN VS CODE (Side by Side)

**Split screen recommended:**

**LEFT SIDE:** VS Code showing:
- `langgraph_builder.py` (the main file)
- OR `workflow.json` (the configuration)
- OR `agents/` folder (show the 7 agents)

**RIGHT SIDE:** Terminal running:
- `python langgraph_builder.py`

**As terminal runs, point to VS Code:**
> "See? The code is running here, and these are the agents executing one by one."

---

## 🎥 ALTERNATIVE: Show Testing Scripts

**If you want to show more capabilities:**

### **Test 1: Verify Setup**

```powershell
python test_gemini.py
```

**Say:**
> "First, let me verify the AI is working..."

### **Test 2: Run Main Pipeline**

```powershell
python langgraph_builder.py
```

**Say:**
> "Now let's run the full pipeline..."

### **Test 3: Show Tracking**

```powershell
python test_webhook.py
```

**Say:**
> "And here's how the tracking system works..."

**But honestly? Just running `langgraph_builder.py` is enough!**

---

## 💡 PRO TIPS FOR RECORDING

### **Before You Run:**

1. **Test it first** (not while recording):
   ```powershell
   python langgraph_builder.py
   ```
   Make sure it works!

2. **Clear terminal**:
   ```powershell
   cls
   ```

3. **Check .env**:
   ```powershell
   Get-Content .env
   ```
   Make sure API keys are there!

### **While Recording:**

1. **Speak BEFORE running commands**
   - ❌ Don't: Run command, then explain
   - ✅ Do: Explain, then run command

2. **Let commands finish**
   - Don't interrupt the output
   - Let viewers see "Status 202" for each email

3. **Point with mouse**
   - Move cursor to highlight important parts
   - Circle around "✅ Email sent successfully"

---

## 🎯 THE ABSOLUTE MINIMUM

**If you only have 3 minutes:**

```powershell
# Setup
cd "C:\Users\LADE SAI TEJA\OneDrive\Desktop\LeadGenerator"
cls

# Start recording (Win + Alt + R)

# Say: "Watch this - 7 AI agents sending 10 real emails"
python langgraph_builder.py

# Say: "10 out of 10 delivered! Here's what was sent:"
code (Get-ChildItem output | Sort-Object LastWriteTime -Descending | Select-Object -First 1).FullName

# Stop recording (Win + Alt + R)
```

**That's it! 3 minutes, shows everything!**

---

## 📊 WHAT YOU'LL SEE WHEN IT RUNS

**Expected output from `langgraph_builder.py`:**

```
Loading workflow from workflow.json...
Initializing 7 agents...

[Agent 1: Prospect Search]
✅ Found 10 prospects from real_leads_data.json

[Agent 2: Data Enrichment]
✅ Enriched 10 prospects with company data

[Agent 3: Scoring]
✅ Scored 10 prospects (10 approved, 0 rejected)

[Agent 4: Outreach Content]
🤖 Generating personalized emails with Gemini AI...
✅ Generated 10 unique emails

[Agent 5: Outreach Executor]
📧 Sending email to rahul.sharma@example.com... Status: 202 ✅
📧 Sending email to priya.patel@example.com... Status: 202 ✅
[... 8 more ...]
✅ All 10 emails sent successfully!

[Agent 6: Response Tracker]
✅ Tracking initialized for 10 emails

[Agent 7: Feedback Trainer]
✅ Performance analysis complete

Pipeline execution completed successfully!
Results saved to: output/workflow_results_20251020_XXXXXX.json
```

**This is what you'll narrate over!**

---

## ✅ FINAL CHECKLIST

**Before you hit record:**

- [ ] Terminal is open in project directory
- [ ] Screen is clean (no personal tabs open)
- [ ] .env file has API keys
- [ ] You tested `python langgraph_builder.py` already
- [ ] You know what to say while it runs
- [ ] Microphone is on (Win + G settings)
- [ ] You're ready to be enthusiastic!

---

## 🚀 READY? HERE'S YOUR SCRIPT:

**SAY THIS:**

> "Hi! I'm Sai Teja. Let me show you my LangGraph lead generation system.
> 
> **[Show VS Code with project open]**
> 
> Here's the code. 7 agents working together.
> 
> **[Switch to terminal]**
> 
> Watch this - I'm going to run the entire pipeline with one command:
> 
> **[Type: python langgraph_builder.py]**
> 
> This will automatically find prospects, enrich data, score leads, generate personalized emails with AI, and send them for REAL via SendGrid.
> 
> **[Press Enter and narrate as it runs]**
> 
> See that? Agent 1 found 10 prospects... Agent 2 enriching... Agent 3 scoring... Agent 4 generating with AI... Agent 5 sending... Status 202, success! Another one... another one...
> 
> **[Wait for completion]**
> 
> Done! 10 out of 10 emails delivered. 100% success rate. Zero dollars cost.
> 
> **[Show output file]**
> 
> Here's what was generated - personalized emails for each person.
> 
> **[Show one email]**
> 
> Look at this - mentions their company, their technology stack, recent news. All generated by AI.
> 
> That's it! Complete autonomous lead generation. All code on GitHub. Thanks!"

---

## 🎬 YOU'RE READY!

**The command:** `python langgraph_builder.py`

**That's all you need!** Everything else is extra.

**NOW GO RECORD IT!** 🚀
