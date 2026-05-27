# 🔮 PureScan AI Helper - Multimodal Logistics & Ingredient Scanner

> **A Mobile-Responsive Web Application Utilizing Gemini 2.5 Flash Vision API to Instantly Translate and Inspect Foreign Product Ingredients.**

PureScan AI Helper is a zero-friction mobile companion built using Streamlit and Google's latest multimodal SDK. Engineered for international travelers and proxy shoppers, this app eradicates the anxiety of purchasing foreign pharmaceuticals or cosmetics. By utilizing mobile snapshots of back-panel ingredient descriptions, the AI acts as your pocket health shield—breaking down obscure chemical compounds, rendering explicit allergy warnings, and delivering instant color-coded safety badges.

---

## ✨ Key Features

* **👁️ Multimodal Visual Intelligence**: Zero dependency on manual OCR pipelines. Passes raw camera snapshots straight into `gemini-2.5-flash` for native multi-language visual text parsing (Japanese, English, Korean, and more).
* **🎯 Guaranteed JSON Response Schema**: Bound via strict `Pydantic` structural schemas, completely removing chatbot conversational filler to return instant, parseable data fields.
* **🚦 Color-Coded Risk Assessment Grid**: Dynamically streams response properties into high-contrast Streamlit status cards (🟢 Safe, 🟡 Warning, 🔴 Danger) optimized for high-speed offline glance visibility.
* **📱 Ultra-Lightweight Mobile Web Interface**: Configured on a single vertical layout structure (`layout="centered"`) with native viewport bindings to leverage smartphone camera modules upon canvas taps.

---

## 🛠️ Tech Stack & Architecture

* **Web UI Engineering**: `Streamlit` (Production mobile responsive layer)
* **LLM Engine & API**: `google-genai` (2025 Next-Gen Official Google SDK Wrapper)
* **Model Configuration**: `gemini-2.5-flash` (Configured with specialized `response_schema` & low 0.1 inference temperature for chemical dictionary accuracy)
* **Data Layer**: Runtime JSON deserialization fed straight into markdown block structures.

---

## Edit API ley

Goto [Google API (https://aistudio.google.com/)] apply a free Gemini API and copy-paste to line 37.


## Run
```streamlit run purescan_ai_helper.py```
---

## 介面
<img width="1170" height="1126" alt="image" src="https://github.com/user-attachments/assets/9993135e-ff51-42e5-a8aa-ac3557e722ec" />
<img width="1046" height="1565" alt="image" src="https://github.com/user-attachments/assets/4851e4c7-b537-4390-89ef-6a036c4a4a65" />

