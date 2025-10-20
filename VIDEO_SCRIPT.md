# 🎬 VIDEO DEMO SCRIPT - LangGraph Lead Generation System

**Total Time: 5-7 minutes**  
**Style: Professional but friendly**  
**Tools: Screen recording (Windows Game Bar: Win+G)**

---

## 🎯 VIDEO STRUCTURE

### **Part 1: Introduction (30 seconds)**
### **Part 2: Show the Code (1 minute)**
### **Part 3: Explain How It Works (1.5 minutes)**
### **Part 4: Live Demo - Run It! (2 minutes)**
### **Part 5: Show Results (1 minute)**
### **Part 6: Explain Impact (30 seconds)**

---

## 📝 DETAILED SCRIPT

---

### **PART 1: INTRODUCTION (30 seconds)**

**[Screen: Your face or GitHub repo homepage]**

**YOU SAY:**
> "Hi! I'm Sai Teja from SASTRA University. For the Analytos.ai assessment, I built an autonomous lead generation system using LangGraph and AI.
>
> In the next 5 minutes, I'll show you how 7 AI agents work together to automatically find prospects, write personalized emails, send them for real, and track responses.
>
> Let me show you how it works!"

**[Screen: Transition to VS Code with project open]**

---

### **PART 2: SHOW THE CODE (1 minute)**

**[Screen: VS Code - Project structure in sidebar]**

**YOU SAY:**
> "Here's the project structure. Let me walk you through it quickly:
>
> **[Point to folders]**
> - In the `agents` folder, we have 7 autonomous agents
> - The `tools` folder has all the API integrations - SendGrid for emails, Gemini for AI
> - And `workflow.json` is the brain - it orchestrates everything
>
> **[Open workflow.json briefly]**
> This JSON file defines the entire workflow - what each agent does, in what order, and how they communicate.
>
> **[Open one agent file - outreach_content.py]**
> Here's the agent that generates emails using Google Gemini AI. It takes prospect data and creates personalized content based on their company news and technologies.
>
> Everything is modular - each agent does ONE thing really well."

**[Quick scroll through files to show organization]**

---

### **PART 3: EXPLAIN HOW IT WORKS (1.5 minutes)**

**[Screen: Draw or show the architecture diagram]**

**YOU SAY:**
> "Let me explain how the 7 agents work together:
>
> **Agent 1 - Prospect Search:**  
> Finds companies matching our ideal customer profile. For this demo, I used real data - 10 friends working at OpenAI, Google, Meta, AWS, and other tech companies.
>
> **Agent 2 - Data Enrichment:**  
> Enriches each prospect with company information - what technologies they use, recent news, growth signals.
>
> **Agent 3 - Scoring:**  
> Scores each lead from 0 to 100 based on how good a fit they are. For my demo, all friends got perfect scores.
>
> **Agent 4 - Outreach Content:**  
> This is where the magic happens! Uses Google Gemini AI to generate completely personalized emails. Each email mentions specific company news - like Google's Gemini 2 launch or OpenAI's GPT-5.
>
> **Agent 5 - Outreach Executor:**  
> Sends REAL emails via SendGrid. Not simulation - actual emails that land in inboxes.
>
> **Agent 6 - Response Tracker:**  
> Tracks who opens, who clicks, who replies - all in real-time on a dashboard.
>
> **Agent 7 - Feedback Trainer:**  
> Analyzes what worked and suggests improvements. It's a self-improving system!
>
> The entire workflow runs automatically - I just press one button."

---

### **PART 4: LIVE DEMO - RUN IT! (2 minutes)**

**[Screen: Terminal/PowerShell]**

**YOU SAY:**
> "Let me show you it running live. I'll execute the main workflow:
>
> **[Type command]**  
> `python langgraph_builder.py`
>
> **[As it runs, narrate what's happening]**
> 
> Watch this - it's loading the 7 agents... 
> 
> **[Point to logs as they appear]**
> - Agent 1 just loaded 10 prospects from my friends list
> - Agent 2 is enriching with company data
> - Agent 3 scored all of them - perfect scores because they're friends
> - Agent 4 is now generating emails with Gemini AI... see how fast it is?
> 
> **[Pause as emails generate]**
> Look at this - it's creating personalized emails:
> - For Google: mentioning Gemini 2 and TensorFlow
> - For Meta: mentioning their AI creator tools
> - For NVIDIA: mentioning Blackwell GPU architecture
> 
> Each email is unique and contextual!
> 
> **[Emails sending section]**
> And now... Agent 5 is sending real emails via SendGrid...
> 
> **[Point to success messages]**
> See that? '✅ Email sent successfully' - Status 202!
> 
> All 10 emails sent! 100% delivery rate!
> 
> The whole thing took about 30 seconds and sent 10 personalized, AI-generated emails to real people."

---

### **PART 5: SHOW RESULTS (1 minute)**

**[Screen: Open the output JSON file or tracking dashboard]**

**YOU SAY:**
> "Let me show you what was actually sent.
>
> **[Open output/workflow_results JSON]**
> Here's the complete output. Let me show you one email:
>
> **[Scroll to an email, read parts of it]**
> This email to my friend at Google:
> - Subject: 'Google AI & Sales: Maximize Team Efficiency?'
> - It mentions Gemini 2, TensorFlow, Google Cloud
> - References their recent product launch
> - And has a friendly disclaimer at the bottom explaining it's a test
> 
> **[Switch to tracking dashboard at localhost:5000]**
> And here's the tracking dashboard I built:
> - Shows 10 emails delivered
> - Tracks who opened them
> - Tracks clicks
> - All updating in real-time
> 
> I even built a simulation to test it - you can see the events flowing in.
>
> **[Show the live dashboard updating]**
> This is all running locally on my machine, but it could easily be deployed to production."

---

### **PART 6: EXPLAIN IMPACT (30 seconds)**

**[Screen: Back to you or GitHub repo]**

**YOU SAY:**
> "So what did I actually build?
> 
> A production-ready system that:
> - Uses FREE AI (Google Gemini - 2 million tokens per month)
> - Sends REAL emails via SendGrid
> - Generates personalized content automatically
> - Tracks everything in real-time
> - Learns and improves from feedback
> 
> Total cost? Zero dollars. Just using free tiers.
> Development time? About 4 hours.
> 
> The system is modular, well-documented, and ready to scale. You can find all the code on my GitHub at github.com/ladesai123/LangGraph-Lead-Generation.
> 
> Thanks for watching! I'm excited to discuss this further!"

**[End screen: Show GitHub link]**

---

## 🎥 RECORDING TIPS

### **Before Recording:**
1. ✅ Close unnecessary tabs/windows
2. ✅ Clear terminal history
3. ✅ Have VS Code open with project
4. ✅ Have browser ready with localhost:5000
5. ✅ Test your microphone
6. ✅ Wear something professional (at least on top!)

### **While Recording:**
1. **Speak clearly and slowly** - Imagine explaining to your grandma
2. **Use your mouse to point** at things on screen
3. **Pause briefly** between sections
4. **Smile** - you can hear it in your voice!
5. **Don't say "um" or "uh"** - just pause instead

### **What to Show:**
| Time | Screen | Action |
|------|--------|--------|
| 0:00-0:30 | Face/GitHub | Introduction |
| 0:30-1:30 | VS Code | Show code structure |
| 1:30-3:00 | Whiteboard/Slides | Explain architecture |
| 3:00-5:00 | Terminal | Run live demo |
| 5:00-6:00 | Browser | Show results & dashboard |
| 6:00-6:30 | Face/GitHub | Conclusion |

---

## 🎬 ALTERNATIVE: SHORTER VERSION (3 minutes)

If you want to keep it super short:

**30 sec:** "Hi, I'm Sai Teja. I built a 7-agent AI system for lead generation. Watch this."

**1 min:** [Run the workflow live, narrate as it goes]

**1 min:** [Show one generated email and explain how AI personalized it]

**30 sec:** "100% delivery rate, real emails, zero cost. All code on GitHub. Thanks!"

---

## 💡 PRO TIPS

### **Make It More Impressive:**
1. **Show your face** at the beginning - more personal
2. **Highlight the REAL emails** - this is what makes it special
3. **Point out the $0 cost** - using free tiers
4. **Mention the 100% delivery rate** - all 10 emails sent successfully
5. **Show the friendly disclaimers** - responsible AI usage

### **What NOT to Do:**
❌ Don't apologize or sound uncertain  
❌ Don't say "I tried to..." - you DID it!  
❌ Don't spend too much time on one section  
❌ Don't show your .env file with API keys!  
❌ Don't go over 7 minutes  

---

## 📊 KEY TALKING POINTS

**Emphasize these:**
1. ✅ **7 autonomous agents** working together
2. ✅ **Real emails sent** (not simulation)
3. ✅ **AI-generated content** with Google Gemini
4. ✅ **100% delivery rate** (10/10 successful)
5. ✅ **Real-time tracking** dashboard
6. ✅ **Zero cost** (free tiers only)
7. ✅ **Self-improving** feedback loop
8. ✅ **Production-ready** code

---

## 🎯 SAMPLE INTRODUCTION (Memorize This!)

> "Hi! I'm Sai Teja from SASTRA University. 
> 
> For this assessment, I built an autonomous lead generation system using 7 AI agents, Google Gemini, and SendGrid.
> 
> The system automatically finds prospects, writes personalized emails using AI, and sends them for real. I actually sent 10 emails to friends at companies like OpenAI, Google, and Meta - with 100% delivery rate.
> 
> Let me show you how it works!"

---

## 🎬 RECORDING CHECKLIST

**Before you start:**
- [ ] Script printed or on second screen
- [ ] Project opens cleanly in VS Code
- [ ] Terminal is ready with project directory
- [ ] Browser has localhost:5000 ready
- [ ] Microphone tested
- [ ] Room is quiet
- [ ] Good lighting (if showing face)

**During recording:**
- [ ] Speak clearly and confidently
- [ ] Point at important parts
- [ ] Show enthusiasm!
- [ ] Don't rush

**After recording:**
- [ ] Watch it once
- [ ] Check audio quality
- [ ] Verify everything is visible
- [ ] Upload to YouTube (unlisted)
- [ ] Test the link works

---

## 🚀 YOU GOT THIS!

Remember:
1. You built something REAL
2. You sent actual emails
3. You have proof it works
4. The code is clean and documented

**Be confident!** You accomplished in 4 hours what many people can't do in weeks!

---

**Ready to record? Follow this script and you'll nail it!** 🎥✨
