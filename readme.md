# Holiday Support Email Program

<p align="center">
  <img src="logo.png" alt="4day" width="40%" height="40" />
</p>

## Purpose
Many veterans and service members feel especially isolated during the 4 day weekend and holiday season.  
This project was built to send **messages of support, care, and encouragement** during these long holiday weekends —  
a reminder that they are **never forgotten, always valued, and never alone**.  

By registering with the system, users can receive automated supportive emails during major holidays.  

---

## Features
- **Automated Emails**: Sends warm, supportive messages during long holiday breaks  
- **Web Interface**: Simple pages for users to **register** or **unregister** from the mailing list  
- **Respectful & Secure**: No spam — only meaningful holiday outreach  
- **SMTP Integration**: Currently sends test emails, with full holiday scheduling in development  

---

## Tech Stack
- **Flask** – lightweight backend framework for the web app  
- **HTML/CSS** – simple UI for register/unregister pages  
- **smtplib** – for sending automated emails  
- **dotenv** – environment variables for secure credential handling  

---

## How It Works
1. User registers through the website form  
2. Email is stored securely in the system (data.json not inlcuded in this repository for security purposes)
3. On holidays (currently test emails, soon holiday-triggered emails):  
   - The system sends a supportive, prewritten message via email  
   - Example message:  

   > *“During this holiday season, please know you are not forgotten.  
   > Your courage, sacrifice, and strength are deeply appreciated.  
   > Wishing you peace, warmth, and a gentle reminder that your presence matters.”*  

---

## Roadmap
- Basic email sending (test messages)  
- User register/unregister system  
- Holiday scheduling for automated outreach  
- Database integration for scalability and persistence  
- Expand with personalized messages and optional volunteer submissions  

---

## Why This Matters
This project is more than code — it’s a way to reach out to those who may feel isolated when others are celebrating.  
A small reminder can mean the world.  