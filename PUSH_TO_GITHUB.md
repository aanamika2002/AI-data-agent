# How to push this repo to GitHub (recommended)

Option A — Using GitHub CLI (recommended)
1. Install GitHub CLI: https://cli.github.com/
2. Authenticate: `gh auth login`
3. Create repo: `gh repo create YOUR_GITHUB_USERNAME/ai-data-agent --public --source=. --remote=origin`
4. Push: `git push -u origin main`

Option B — Manual
1. Create a new repository on github.com
2. In your local folder:
    git init
    git add .
    git commit -m "Initial commit"
    git branch -M main
    git remote add origin https://github.com/YOUR_USERNAME/ai-data-agent.git
    git push -u origin main
