# 📊 Data Cleaning & Analysis App

A beginner-friendly **interactive data cleaning and analysis web application** built with **Streamlit**, **Pandas**, **NumPy**, and **Matplotlib**.
The app allows users to upload datasets, clean them automatically, explore statistics, and generate visualizations without writing code.

---

## 🚀 Features

* Upload **CSV** or **JSON** datasets
* Preview raw data instantly
* Detect and display missing values
* Automatically clean data:

  * Fill missing numeric values with mean
  * Fill missing categorical values with mode
  * Remove duplicate rows
  * Convert columns to appropriate data types
* Perform exploratory data analysis:

  * Dataset shape (rows & columns)
  * Column data types
  * Descriptive statistics
  * Unique value counts
  * Correlation matrix
* Generate visualizations:

  * Histograms for numeric columns
  * Bar charts for categorical columns
* Interactive UI with sidebar upload and dynamic controls

---

## 🧠 How the App Works (High-Level Flow)

1. User uploads a CSV or JSON file
2. Dataset is loaded into a Pandas DataFrame
3. Missing values are analyzed and displayed
4. User clicks **Clean Data**
5. Cleaned data is stored in session memory
6. Analysis and visualizations are generated from cleaned data
7. Results update dynamically based on user selections

---

## 🗂️ Project Structure

```
data-cleaner-app/
│
├── app.py              # Main Streamlit application
├── requirements.txt    # Python dependencies
└── README.md           # Project documentation
```

---

## 🧩 Requirements

### 1️⃣ Python Version

* **Python 3.9 – 3.11 (recommended)**

Check your version:

```bash
python --version
```

---

### 2️⃣ Required Python Libraries

The app depends on the following libraries:

* `streamlit` – Web application framework
* `pandas` – Data manipulation and analysis
* `numpy` – Numerical computations
* `matplotlib` – Data visualization
* `io` – File handling (standard library)

---

### 3️⃣ Installation

#### Step 1: (Optional) Create a Virtual Environment

```bash
python -m venv venv
```

Activate it:

* **Windows**

```bash
venv\Scripts\activate
```

* **macOS / Linux**

```bash
source venv/bin/activate
```

---

#### Step 2: Install Dependencies

```bash
pip install streamlit pandas numpy matplotlib
```

Or using `requirements.txt`:

```bash
pip install -r requirements.txt
```

---

## ▶️ How to Run the App

From the project directory:

```bash
streamlit run app.py
```

After running, Streamlit will open the app in your browser, usually at:

```
http://localhost:8501
```

---

## 📂 Supported File Types

| File Type | Supported |
| --------- | --------- |
| CSV       | ✅ Yes     |
| JSON      | ✅ Yes     |
| Excel     | ❌ No      |
| TXT       | ❌ No      |

---

## 🧪 Data Cleaning Logic Explained

### Numeric Columns

* Missing values → replaced with **mean**
* Automatically detected using NumPy data types

### Categorical Columns

* Missing values → replaced with **mode**
* If no mode exists, values remain unchanged

### Other Cleaning Steps

* Duplicate rows are removed
* Index is reset
* Columns are converted to:

  * Numeric (if possible)
  * Datetime (if detected)

---

## 📈 Visualizations

### Histogram

* User selects a numeric column
* Displays value distribution
* Uses 20 bins by default

### Bar Chart

* User selects a categorical column
* Displays top 20 most frequent values
* X-axis labels rotate automatically for readability

---

## ⚠️ Limitations

* No file export (cleaned data is not downloadable)
* No advanced ML models
* Large datasets may affect performance
* No persistent storage (session-based only)

---

## 🔮 Possible Improvements

* Add data download (CSV export)
* Add boxplots and scatter plots
* Add outlier detection
* Add feature selection
* Add machine learning models
* Replace Streamlit with FastAPI + frontend

---

## 👨‍💻 Intended Audience

* Students learning **Data Analysis**
* Beginners in **Python & Pandas**
* Anyone needing quick dataset inspection
* Academic and demo projects

---

## 📜 License

This project is open-source and free to use for educational and personal projects.

---

## 🙌 Author Notes

This app demonstrates:

* Practical data cleaning techniques
* Exploratory Data Analysis (EDA)
* Interactive Python dashboards
* Clean and readable code structure

---


