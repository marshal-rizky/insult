# Vibecode Roast: The Crime Scene Suite

A brutally honest, zero-tolerance custom skill for Google Deepmind's Antigravity (and Gemini) agent. 

This skill overrides your AI assistant's standard polite persona, replacing it with an elitist Principal Engineer who is deeply offended by "vibecoding" (writing code purely based on vibes with no structural integrity).

When triggered, the AI executes the included internally-bundled `diagnostic_suite.py` to extract `git blame` author data, commit timestamps, and basic code complexity metrics. It then uses this hard data as ammunition to deliver a devastating "**Code Crime Report**."

## Installation

To install this custom skill so your agent can use it:

1. **Download this repository:**
   You can either `git clone` this repository via terminal or simply download it as a `.ZIP` file from the main page.
   ```bash
   git clone https://github.com/marshal-rizky/insult.git
   ```

2. **Move it to your skills directory:**
   Copy the `vibecode-roast` folder into your Antigravity skills directory. Depending on your Operating System, this is located at:
   - **Windows:** `C:\Users\<YourUsername>\.gemini\antigravity\skills\`
   - **Mac/Linux:** `~/.gemini/antigravity/skills/`

## How to Trigger It

Once installed, simply ask Gemini to review your code, evaluate your architecture, or mention that you "vibecoded" something. 

Examples:
- *"Review `src/app.js`, I've been vibecoding it all night."*
- *"Can you run the vibecode roaster on my project?"*
- *"Act as my code reviewer for my latest commits."*

The AI will automatically handle executing the diagnostic scripts to acquire the necessary historical/Git context and will format its response to humiliate you. Good luck.
