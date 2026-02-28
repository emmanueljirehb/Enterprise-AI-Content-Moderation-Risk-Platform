# Enterprise AI Content Moderation Risk Platform



What i actually built over 3 months is not just “a content moderator.”
It evolved through **three engineering phases**:

1. **Phase 1 – Local ML Stack**
   (CLIP + Toxic-BERT + Presidio + FastAPI + MySQL)

2. **Phase 2 – Production Hardening**
   (False-positive reduction, entity aggregation, Vault integration, stability fixes)

3. **Phase 3 – Cloud-Native LLM Architecture**
   (AWS Bedrock – LLaMA 3.x, token tracking, cost awareness, structured outputs, parallelism)

And finally expanded into:

4. **Counterfeit & Fraud Risk Engine (Multi-factor Scoring + Bedrock reasoning)**

Instead of showing them separately, I merged everything into **one clean, Director-level master documentation** that:

* Shows evolution
* Shows ownership
* Shows measurable impact
* Shows architecture thinking
* Shows cost awareness
* Shows debugging maturity
* Shows scalability
* Shows security practices
* Shows business alignment


---

# 🛡️ Enterprise AI Content Moderation & Risk Intelligence System

### She-Jobs Tech – AI Internship (3-Month Engineering Project)

A production-ready, scalable AI-powered moderation and risk detection platform designed to protect marketplace ecosystems from:

* 🔞 NSFW / Violent Images
* ⚠️ Toxic / Threatening Text
* 🔐 PII Exposure
* 🏷️ Counterfeit & Fraud Signals
* 📊 Seller Risk Anomalies

This system evolved from a local ML prototype into a **cloud-native, cost-aware, LLM-powered moderation engine using AWS Bedrock (LLaMA 3.x models).**

---

# 🚀 Executive Summary

Over the course of 3 months, this project progressed through:

| Phase   | Architecture                            | Focus                      |
| ------- | --------------------------------------- | -------------------------- |
| Phase 1 | CLIP + Toxic-BERT + Presidio            | Functional ML moderation   |
| Phase 2 | FastAPI + Aggregation + FP Optimization | Production hardening       |
| Phase 3 | AWS Bedrock (LLaMA 3.x)                 | Cloud-native scalable AI   |
| Phase 4 | Multi-Factor Risk & Counterfeit Engine  | Advanced risk intelligence |

Final Outcome:

* ✅ False Positive Rate reduced to **<5%**
* ✅ Token-level cost tracking implemented
* ✅ Fully modular, scalable architecture
* ✅ Production-grade error handling
* ✅ Audit-ready structured moderation reports
* ✅ Parallel processing for performance optimization

---

# 🎯 Business Objectives

The system was built to:

* Automate manual moderation workflows
* Reduce legal & compliance risks
* Maintain platform safety
* Provide explainable moderation reasoning
* Track AI usage cost per record
* Scale efficiently for batch processing

---

# 🏗️ Final Production Architecture

```
MySQL Database (Paginated Fetch)
        ↓
Text Aggregation
        ↓
Bedrock LLaMA 3.2 3B (Toxicity + PII)
        ↓
Image Processing (Resize + Compression)
        ↓
Bedrock LLaMA 3.2 11B Vision (NSFW / Violence)
        ↓
Counterfeit Risk Engine
        ↓
Seller Anomaly Detection
        ↓
Risk Scoring & Aggregation
        ↓
Token Usage Tracking
        ↓
Final Moderation CSV Report
```

---

# 🤖 AI Models Used

## 📝 Text Moderation

* Model: **LLaMA 3.2 3B Instruct (AWS Bedrock)**
* Used for:

  * Toxicity detection
  * PII extraction
* Chosen for:

  * Cost efficiency
  * Fast inference
  * Structured JSON outputs

---

## 🖼️ Vision Moderation

* Model: **LLaMA 3.2 11B Vision (AWS Bedrock)**
* Used for:

  * NSFW detection
  * Violent image detection
* Upgrade path available to 90B if required.

---

# 🧠 Core Detection Modules

## 1️⃣ Toxicity Detection

* Violent & threatening language scoring
* Threshold tuning (calibrated to reduce FP)
* Structured JSON enforcement

---

## 2️⃣ PII Detection

* Strict pattern-based + LLM validation
* Emails, phone numbers, Aadhaar patterns
* Prevents over-flagging descriptions
* Reduces false positives drastically

---

## 3️⃣ NSFW & Violent Image Detection

* Image resizing (max 512px)
* RGB conversion
* JPEG compression
* Base64 encoding
* LLM reasoning-based classification

Avoids false positives for:

* Logos
* Question papers
* Invoices
* Brand product images
* Screenshots

---

## 4️⃣ Counterfeit & Fraud Risk Engine

Multi-factor scoring based on:

| Signal              | Description                 |
| ------------------- | --------------------------- |
| Brand Mention       | Luxury brand detection      |
| Price Anomaly       | <30% of market median       |
| Suspicious Keywords | “Replica”, “Inspired”, etc. |
| Image Duplication   | pHash-based matching        |
| Seller Risk         | Bulk suspicious listings    |
| Review Signals      | “Fake” complaints           |

Classification:

* SAFE
* REVIEW
* FAKE

---

# 📊 Risk Scoring Logic

Entity marked **UNSAFE** if any:

* Toxicity detected
* PII detected
* NSFW image detected
* Fraud risk score ≥ threshold

False Positive % dynamically calculated:

```
false_positive_percent = (incorrect_flags / total_processed) * 100
```

System blocks deployment if FP > 5%.

---

# ⚡ Performance Optimizations

### ✅ Parallel Image Processing

* Multi-threading
* Up to 10 concurrent image evaluations
* ~5–10x speed improvement

### ✅ Token Usage Tracking

Each record stores:

```
{
  "input_tokens": X,
  "output_tokens": Y,
  "total_tokens": Z
}
```

Enables:

* Cost forecasting
* Budget control
* Leadership reporting
* Model optimization decisions

---

# 🔒 Security & Compliance

* IAM-based Bedrock access
* Vault integration for DB credentials
* No hardcoded secrets
* Environment variable isolation
* No raw PII stored in output
* Region-locked AWS configuration

---

# 🧪 Major Challenges Solved

* 67% → <5% false positives
* Presidio over-detection
* CLIP tensor mismatch errors
* MySQL connection pool issues
* Vault authentication errors
* LLM malformed JSON outputs
* Region mismatch (us-east-2 vs us-east-1)
* Dependency conflicts (NumPy / SpaCy ABI)
* Duplicate image row merging
* Token cost invisibility

---

# 📄 Final Output Format

Generated file: `review_final.csv`

Columns:

```
entity_id
type
content
reason_of_reporting
score_summary
admin_check
admin_comment
token_usage
false_positive_percentage
```

Only flagged records exported.

Audit-ready.

---

# 🧠 Engineering Skills Demonstrated

* Cloud-native AI integration
* AWS Bedrock orchestration
* Vision + Text LLM pipelines
* Prompt engineering
* Token accounting & cost control
* Multi-threaded processing
* False positive calibration
* Modular system architecture
* Secure secret management
* Database stability engineering
* Production debugging under constraints
* Multi-factor risk scoring design

---

# 📈 Measurable Outcomes

* False positives reduced below 5%
* Improved violent image detection reliability
* Eliminated system crashes from malformed AI responses
* Reduced infra complexity by migrating to managed AI
* Enabled cost transparency per moderation batch
* Reduced manual moderation workload significantly

---

# 🔮 Future Enhancements

* Async Bedrock invocation
* A/B model testing (3B vs 11B vs 90B)
* Confidence calibration dashboard
* Real-time monitoring & alerts
* Admin moderation UI
* Isolation Forest for price anomaly detection
* Slack/email governance automation

---

# 👨‍💻 Internship Impact

This project demonstrates the ability to:

* Build from prototype to production
* Redesign systems for scalability
* Optimize cost-aware AI pipelines
* Balance rule-based logic with LLM reasoning
* Solve real-world production debugging challenges
* Deliver measurable business value

---

# 🏁 Final Status

✅ Fully Operational
✅ Production-Ready
✅ Cost-Tracked
✅ Scalable
✅ Secure
✅ Architecturally Modular

# Project Hilights

## execution speed improved from 6hrs to less than "3 minutes"
---

<img width="641" height="428" alt="image" src="https://github.com/user-attachments/assets/e6d0089f-a61b-444e-ae0c-e6ca1563afee" />

## detected following images from DB
---

<img width="416" height="465" alt="image" src="https://github.com/user-attachments/assets/4635bb68-b527-47ab-a18a-6fb0c07c5ca2" />

## added fake and real images of every category to db
---
<img width="635" height="426" alt="image" src="https://github.com/user-attachments/assets/8ba75833-1efd-4546-b5d0-e611087412b9" />

<img width="625" height="419" alt="image" src="https://github.com/user-attachments/assets/e4014ab6-56f9-4442-8794-3aa4624ce9f6" />

<img width="520" height="367" alt="image" src="https://github.com/user-attachments/assets/c02b4bc6-f1b1-4061-a6ab-628763f00b06" />

<img width="409" height="437" alt="image" src="https://github.com/user-attachments/assets/8dcb9619-97bf-415e-8763-e02e20d7711c" />

<img width="380" height="395" alt="image" src="https://github.com/user-attachments/assets/be25ec54-338f-4b6e-ac5f-0b65321054b2" />

## deteced them successfully

<img width="958" height="530" alt="image" src="https://github.com/user-attachments/assets/66878c07-d582-459c-affd-952d003cf9c1" />

content moderator readme
