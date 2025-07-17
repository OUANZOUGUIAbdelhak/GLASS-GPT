# 🧪 Predicting Initial Dissolution Rates of Glasses Using AI

Welcome! This repository documents a complete AI-driven workflow developed during a **one-year gap-year internship**, focused on **automating data extraction from scientific articles** to create a database for modeling the **initial dissolution rate of glasses**—a critical property for materials used in **nuclear waste containment**.

> 🧠 **Goal**: Extract and structure glass composition and experimental parameters from PDF articles using **LLMs, Langflow, OCR, and custom Python scripts**, and use this data to **train a model to predict the initial dissolution rate** of glass under various conditions.

---

## 📌 Table of Contents

* [🔬 Project Background](#-project-background)
* [🧰 Technologies Used](#-technologies-used)
* [🧠 AI/ML Techniques](#-aiml-techniques)
* [📁 Repository Structure](#-repository-structure)
* [🚀 Getting Started](#-getting-started)
* [⚙️ Project Workflow](#-project-workflow)
* [📊 Final Dataset & Modeling](#-final-dataset--modeling)
* [📎 License & Citation](#-license--citation)
* [📚 References](#-references)

---

## 🔬 Project Background

In the context of nuclear waste storage, glass is used to immobilize radioactive materials. Predicting how this glass alters (dissolves) over time in various conditions is essential for long-term safety.

The **initial dissolution rate** is one of the key metrics, but gathering experimental data on this is difficult due to:

* Scattered information across decades of publications
* Lack of structured datasets
* Variability in composition formats and testing conditions

---

## 🧰 Technologies Used

| Category        | Tools / Technologies             |
| --------------- | -------------------------------- |
| AI/LLM Workflow | Langflow (v1.2.0)                |
| Language Models | Mistral Small 22B (internal API) |
| Development     | Python, VS Code 1.96.2           |
| Data Parsing    | PDFMiner, PyMuPDF                |
| OCR             | Docling, Lab OCR Scanner         |
| Database        | SQLite + SQLAlchemy              |
| ML Modeling     | Scikit-learn                     |
| Visualization   | matplotlib, seaborn              |

---

## 🧠 AI/ML Techniques

* **Document Question Answering** via Langflow
* **LLM Prompt Engineering** to validate articles
* **OCR preprocessing** for scanned papers
* **Structured information extraction** from PDFs
* **Unit conversion and normalization** of compositions
* **Tabular data organization** for ML
* **Neural network modeling** of the dissolution rate

---

## 📁 Repository Structure

```bash
glass-ai-dissolution-rate/
├── README.md
├── LICENSE
├── requirements.txt
├── data/
│   ├── raw_articles/             # Original collected articles (PDFs)
│   ├── processed_articles/       # OCR-corrected articles
│   └── final_dataset.csv         # 107-column dataset ready for ML
├── articles/
│   └── valid_articles_metadata.json
├── scripts/
│   ├── run_langflow_pipeline.py  # Executes the full Langflow pipeline
│   └── convert_composition.py    # Converts composition to mol% of elements
├── notebooks/
│   ├── 01_article_validation.ipynb
│   ├── 02_extraction_flow.ipynb
│   └── 03_model_training.ipynb
├── models/
│   └── trained_model.pkl         # Final regression model
├── langflow/
│   └── flows/                    # Langflow JSON files for each step
├── docs/
│   ├── architecture.png          # Visual pipeline diagram
│   └── explanation.md            # Additional written explanations
```

---

## 🚀 Getting Started

### 1. Clone the repo

```bash
git clone https://github.com/your-username/glass-ai-dissolution-rate.git
cd glass-ai-dissolution-rate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Prepare Langflow

> Install and run Langflow locally:

```bash
pip install langflow==1.2.0
langflow run
```

Then import JSON flows from `/langflow/flows/`.

### 4. Run the workflow

Use the included Python scripts and notebooks to execute the Langflow pipeline for:

* Validating article relevance
* Extracting compositions
* Converting to mol%
* Extracting experimental parameters
* Populating the SQL database
* Training the ML model

---

## ⚙️ Project Workflow

### Step 1: Article Collection & OCR

* Collected \~50+ articles from:

  * ScienceDirect
  * Google Scholar
  * Web of Science
  * Supervisor suggestions
* Used **Docling** and a lab OCR printer to digitize 3 scanned papers

### Step 2: Relevance Check via LLM Prompting

Used Langflow + LLM with a strict **specification sheet prompt** to ensure each article includes:

* Full glass composition (\~100%)
* Explicit initial dissolution rate (with unit)
* At least one experimental parameter (e.g., pH, temperature)

📄 **Output**: `articles/valid_articles_metadata.json`
🟢 20 valid articles (out of 50+ reviewed)

### Step 3: Glass List Extraction

Extracted names of glasses with valid data using LLM, e.g.:

```
1. glass_1: NBS14/18
2. glass_2: NBSA
3. glass_3: NBSC
...
```

### Step 4: Composition Extraction & Conversion

LLM prompts extract **composition in various units** → then converted using:

* `convert_composition.py`
* Output: **mol% of elements** (Si, O, B, Na, etc.)

### Step 5: Full Parameter Extraction

For each test on each glass:

* Composition (mol%)
* Experimental conditions
* Initial rate (V₀ or r₀)
* Other metadata (irradiation, polishing, BET surface...)

🔢 Output: structured row for each glass-test combination (107 parameters)

### Step 6: Populate the Database

* All cleaned data is inserted into an SQL database
* Converted to CSV: `data/final_dataset.csv`

### Step 7: Model Training

* Used `notebooks/03_model_training.ipynb`
* Feature engineering on mol% + key conditions
* Trained regression model (e.g., RandomForestRegressor)
* Output: `models/trained_model.pkl`

---

## 📊 Final Dataset & Modeling

* ✅ 20 validated papers
* 🧪 70+ unique tests on glasses
* 🧾 107 parameters per test
* 📈 Model performance: \[to be filled after training]

---

## 📎 License & Citation

### 📜 License

```text
This project is licensed under the Creative Commons Attribution-NonCommercial 4.0 International License.
You may not use this project for commercial purposes or publish derived works without attribution.

To view a copy of this license, visit:
http://creativecommons.org/licenses/by-nc/4.0/
```

### 📌 Citation Policy

If you use any part of this repository—including the workflow, prompts, dataset, or model—for **research or publication**, you must cite this work as:

```bibtex
@misc{ouanzougui2025glass,
  author       = {OUANZOUGUI},
  title        = {Predicting Glass Dissolution Rates with AI: A Langflow-Based Workflow},
  year         = 2025,
  url          = {https://github.com/your-username/glass-ai-dissolution-rate}
}
```

---

## 📚 References

1. Gin, S., et al. *Can a simple topological-constraints-based model predict the initial dissolution rate of borosilicate and aluminosilicate glasses?* npj Materials Degradation, 2020.
2. \[List of all 20 article titles and DOIs here, if permitted]

