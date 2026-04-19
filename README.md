# 🧠 SkillGapAI

> Semantic resume × job description matcher using Azure ML + NLP transformer embeddings.

Built with Python, Streamlit, sentence-transformers, and deployed on Azure App Service.

---

## 📁 Project Structure

```
SkillGapAI/
├── app.py                      ← Main Streamlit UI
├── src/
│   ├── __init__.py
│   ├── resume_parser.py        ← PDF text extraction (pdfplumber + PyMuPDF)
│   ├── skill_extractor.py      ← NLP skill detection
│   └── matcher.py              ← Semantic similarity matching
├── .github/
│   └── workflows/
│       └── deploy.yml          ← GitHub Actions → Azure CI/CD
├── .streamlit/
│   └── config.toml             ← Streamlit server config
├── requirements.txt
├── startup.txt                 ← Azure App Service startup command
└── README.md
```

---

## ⚡ Local Setup (VS Code)

### 1. Clone / Open in VS Code

```bash
# If you already have this folder:
code /path/to/SkillGapAI

# OR clone from GitHub after pushing:
git clone https://github.com/<YOUR_USERNAME>/SkillGapAI.git
cd SkillGapAI
code .
```

### 2. Create Virtual Environment

```bash
python -m venv venv

# Activate:
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

> ⚠️ `sentence-transformers` will download ~80MB model on first run. That's normal.

### 4. Run Locally

```bash
streamlit run app.py
```

Open `http://localhost:8501` in your browser.

---

## 🐙 Push to GitHub

```bash
# Step 1: Initialize git (if not already)
git init

# Step 2: Add all files
git add .

# Step 3: Commit
git commit -m "Initial commit: SkillGapAI with semantic matching"

# Step 4: Create repo on GitHub → https://github.com/new
# Name it: SkillGapAI  (public, no README)

# Step 5: Add remote and push
git remote add origin https://github.com/<YOUR_USERNAME>/SkillGapAI.git
git branch -M main
git push -u origin main
```

---

## ☁️ Deploy on Azure (Step-by-Step)

### Prerequisites
- Azure account → https://portal.azure.com (free tier works)
- Azure CLI installed → https://learn.microsoft.com/en-us/cli/azure/install-azure-cli

### Step 1: Login to Azure CLI

```bash
az login
```

### Step 2: Create Resource Group

```bash
az group create --name SkillGapAI-RG --location eastus
```

### Step 3: Create App Service Plan (Free tier)

```bash
az appservice plan create \
  --name SkillGapAI-Plan \
  --resource-group SkillGapAI-RG \
  --sku B1 \
  --is-linux
```

### Step 4: Create Web App

```bash
az webapp create \
  --resource-group SkillGapAI-RG \
  --plan SkillGapAI-Plan \
  --name skillgapai-<YOUR_UNIQUE_NAME> \
  --runtime "PYTHON:3.11"
```

> Replace `<YOUR_UNIQUE_NAME>` — must be globally unique (e.g., `skillgapai-john2024`)

### Step 5: Configure Startup Command

```bash
az webapp config set \
  --resource-group SkillGapAI-RG \
  --name skillgapai-<YOUR_UNIQUE_NAME> \
  --startup-file "streamlit run app.py --server.port 8000 --server.address 0.0.0.0 --server.headless true"
```

### Step 6: Set Port Environment Variable

```bash
az webapp config appsettings set \
  --resource-group SkillGapAI-RG \
  --name skillgapai-<YOUR_UNIQUE_NAME> \
  --settings WEBSITES_PORT=8000
```

### Step 7: Deploy from GitHub (CI/CD)

In Azure Portal:
1. Go to your Web App → **Deployment Center**
2. Source: **GitHub**
3. Authorize → Select your repo `SkillGapAI` → branch `main`
4. Save → Azure will build and deploy automatically on every push!

**OR deploy manually via ZIP:**

```bash
zip -r deploy.zip . -x "venv/*" ".git/*" "__pycache__/*"
az webapp deployment source config-zip \
  --resource-group SkillGapAI-RG \
  --name skillgapai-<YOUR_UNIQUE_NAME> \
  --src deploy.zip
```

### Step 8: Set GitHub Secrets for Actions CI/CD

In your GitHub repo → Settings → Secrets → Actions:

| Secret Name | Value |
|---|---|
| `AZURE_WEBAPP_NAME` | `skillgapai-<YOUR_UNIQUE_NAME>` |
| `AZURE_PUBLISH_PROFILE` | Download from Azure Portal → Web App → Get publish profile |

Now every push to `main` auto-deploys! 🚀

---

## 🔗 Your App URL

```
https://skillgapai-<YOUR_UNIQUE_NAME>.azurewebsites.net
```

---

## 📝 Resume-Worthy Description

> Built **SkillGapAI** — an NLP-powered resume analyzer deployed on Azure App Service. Extracts skills from PDFs using `pdfplumber`, performs semantic skill matching with `sentence-transformers` (cosine similarity, threshold 0.70), and visualizes skill gaps with interactive Plotly charts. CI/CD pipeline via GitHub Actions. Stack: Python · Streamlit · Azure · Transformers.

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| UI | Streamlit |
| PDF Parsing | pdfplumber + PyMuPDF |
| NLP Matching | sentence-transformers (MiniLM-L6-v2) |
| Visualization | Plotly |
| Cloud | Microsoft Azure App Service |
| CI/CD | GitHub Actions |