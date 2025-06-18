# Medical Claims AI Agent

Application that connects medical claims data with LLM, enabling natural language queries and intelligent data analysis for healthcare datasets.

## 📋 Solution Description

### Problem Statement
Traditional medical claims analysis requires technical expertise in data manipulation and SQL queries. This solution bridges the gap by allowing healthcare professionals to query medical claims data using natural language, making data insights accessible without technical barriers.

### Model Selection and Rationale

**Selected Model: OpenAI GPT-4o**

**Justification:**
1. **Natural Language Understanding**: GPT-4o excels at interpreting complex medical terminology and healthcare contexts
2. **Reasoning Capabilities**: Superior performance in multi-step analytical reasoning required for healthcare data queries
3. **Context Handling**: Can maintain conversation context across multiple related queries
4. **Medical Domain Knowledge**: Pre-trained on extensive medical literature and terminology
5. **Structured Data Integration**: Effectively processes and analyzes structured Excel data when provided with proper context

**Alternative Models Considered:**
- **Qwen3**: Strong open-source LLM capable of handling such tasks
- **Claude**: Strong analytical capabilities but limited API accessibility
- **Local LLMs**: Privacy benefits but insufficient medical domain knowledge

## 📊 Dataset Description

- **Dataset link**: https://www.kaggle.com/datasets/mohammedalsubaie/medical-claims

### Source Data: HealthCare_Claims.xlsx
- **Total Records**: 12,684 medical claims
- **Columns**: 18 data fields
- **Format**: Excel (.xlsx)
- **Language**: Mixed Arabic/English healthcare data

### Data Structure
| Column | Type | Description |
|--------|------|-------------|
| `encounter_id` | String | Unique claim identifier |
| `patient_id` | String | Patient identifier |
| `name` | String | Patient name (Arabic) |
| `Gender` | String | Patient gender |
| `doctor_id` | String | Doctor identifier |
| `doctor_name` | String | Doctor name (Arabic) |
| `hospital_id` | String | Hospital identifier |
| `hospital_name` | String | Hospital name (Arabic) |
| `insurance_provider_id` | String | Insurance provider ID |
| `insurance_provider_name` | String | Insurance provider name (Arabic) |
| `MedicalCondition` | String | Medical condition/diagnosis |
| `admission_date` | Date | Date of admission |
| `discharge_date` | Date | Date of discharge |
| `billing_amount` | Float | Claim amount |
| `admission_type` | String | Type of admission (Urgent/Emergency/Elective) |
| `medication` | String | Prescribed medications |
| `test_results` | String | Test results |
| `Length_of_Stay` | Integer | Duration of stay in days |

### Data Characteristics
- **Healthcare Providers**: 7 unique hospitals
- **Insurance Coverage**: 7 different insurance providers
- **Admission Types**: 3 categories (Urgent, Emergency, Elective)
- **Billing Range**: Up to 614,988.22 in claim amounts
- **Multilingual**: Arabic names and institutions with English medical terms

## 🚀 Installation and Setup

### Prerequisites
- **Python**: 3.8 or higher
- **OpenAI Account**: Valid API key and credits required

### 1. Project Structure
```
medical_claims_ai_agent/
├── main.py                 # Main application entry point
├── excel_handler.py        # Excel data processing logic
├── .env                    # Environment variables
├── requirements.txt        # Python dependencies
├── README.md              # Documentation
├── AI-agent.ipynb         # Performance verification notebook
└── HealthCare_Claims.xlsx  # Medical claims dataset
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

Or install manually:
```bash
pip install openai pandas openpyxl python-dotenv
```

### 3. Environment Configuration
Create `.env` file:
```env
OPENAI_API_KEY=sk-your_actual_api_key_here
EXCEL_FILE_PATH=C:\path\to\your\HealthCare_Claims.xlsx
```

### 4. Run Application
```bash
python main.py
```

## 📈 Performance Report

### Model Performance Evaluation

**Test Queries and Results:**

| Query Type | Input | Expected Output | Actual Output | Accuracy |
|------------|-------|----------------|---------------|----------|
| Data Count | "How many medical claims are in the dataset?" | 12,684 | 12,684 | ✅ 100% |
| Provider Analysis | "Which doctor has the most patients?" | الدكتور برهان سلومي (403 patients) | الدكتور برهان سلومي (403 patients) | ✅ 100% |
| Statistical Analysis | "What is the highest billing amount?" | 614,988.22 | 614,988.22 | ✅ 100% |
| Entity Listing | "List all insurance providers" | 7 providers (Arabic names) | 7 providers correctly listed | ✅ 100% |
| Entity Listing | "List all hospitals" | 7 hospitals (Arabic names) | 7 hospitals correctly listed | ✅ 100% |
| Distribution Analysis | "What's the distribution of admission types?" | Urgent: 4,260, Emergency: 4,260, Elective: 4,164 | **Incorrect distribution reported** | ❌ 0% |

### Performance Metrics
- **Simple Queries**: 100% accuracy (5/5)
- **Complex Analytics**: 0% accuracy (0/1)
- **Overall Accuracy**: 83.3% (5/6)
- **Response Time**: 2-5 seconds average
- **Multilingual Support**: ✅ Handles Arabic text correctly

### Strengths
1. **Perfect Basic Data Retrieval**: Accurately handles count, max/min, and entity listing queries
2. **Multilingual Processing**: Correctly processes and displays Arabic healthcare provider names
3. **Medical Context Understanding**: Properly interprets medical terminology and healthcare concepts
4. **Conversation Continuity**: Maintains context across multiple related queries

### Weaknesses
1. **Complex Aggregation Errors**: Fails on distribution and grouping queries
2. **Statistical Analysis Limitations**: Struggles with multi-dimensional data analysis
3. **Data Processing Inconsistency**: Unreliable when combining multiple data operations

## 🔍 Error Analysis

### Critical Error: Distribution Query Failure

**Query**: "What's the distribution of admission types?"
**Expected**: Accurate count breakdown by admission type
**Actual**: Incorrect distribution values reported

### Root Cause Analysis
1. **Context Window Limitations**: Large dataset summaries may exceed optimal context length
2. **JSON Serialization Problems**: Pandas data type conversion issues affecting statistical calculations
3. **Query Processing Logic**: The system may be using cached or sample data instead of full dataset

### Error Categories Identified
1. **Type 1 - Data Aggregation Errors**: 16.7% of queries (1/6)
   - Impact: Critical for analytical insights
   - Frequency: Affects complex statistical queries
   
2. **Type 2 - Context Processing**: Potential issue with large dataset handling
   - Impact: May affect reliability at scale
   - Frequency: Observable in complex multi-step analyses

### Recommended Improvements

#### Immediate Fixes
1. **Enhanced Data Validation**: Implement verification layer for statistical calculations
2. **Improved Error Handling**: Add try-catch blocks around pandas operations
3. **Query Result Verification**: Cross-validate LLM responses with direct data queries

#### System Enhancements
1. **Hybrid Processing**: Combine LLM reasoning with deterministic statistical functions
2. **Query Decomposition**: Break complex queries into verified sub-components
3. **Result Auditing**: Implement automatic accuracy checking for numerical results

#### Long-term Optimizations
1. **Specialized Medical LLM**: Fine-tune model on healthcare analytics tasks
2. **Database Integration**: Replace Excel processing with database queries
3. **Multi-model Ensemble**: Combine multiple LLMs for improved accuracy

## 🎯 Usage Examples

### Verified Working Queries
```bash
# Data Overview
"How many medical claims are in the dataset?"
"What columns do you have?"

# Entity Analysis  
"List all insurance providers"
"List all hospitals in the data"
"Which doctor has the most patients?"

# Financial Analysis
"What is the highest billing amount?"
```

## 🔧 Technical Configuration

### Model Parameters
```python
model="gpt-4o"
max_tokens=1000
temperature=0.7
```

### Environment Variables
| Variable | Description |
|----------|-------------|
| `OPENAI_API_KEY` | OpenAI API authentication key |
| `EXCEL_FILE_PATH` | Full path to medical claims Excel file |


## 🔄 Future Development

### Planned Improvements
1. **Statistical Query Validation**: Implement automated accuracy verification
2. **Enhanced Analytics**: Add data visualization capabilities
3. **Performance Monitoring**: Real-time accuracy tracking
4. **Web Interface**: Streamlit-based user interface for broader accessibility

### Research Directions
1. **Medical Domain Fine-tuning**: Specialized model training for healthcare analytics
2. **Multi-modal Integration**: Combine structured data analysis with medical literature
3. **Privacy-Preserving Analytics**: Local processing options for sensitive healthcare data