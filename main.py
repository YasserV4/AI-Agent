import openai
import os
import json
import pandas as pd
import numpy as np
from dotenv import load_dotenv
from excel_handler import ExcelHandler

load_dotenv()

def convert_numpy_types(obj):
    """Convert numpy/pandas types to Python native types"""
    if isinstance(obj, np.integer):
        return int(obj)
    elif isinstance(obj, np.floating):
        return float(obj)
    elif isinstance(obj, np.ndarray):
        return obj.tolist()
    elif pd.isna(obj):
        return None
    elif hasattr(obj, 'item'):
        return obj.item()
    return obj

class MedicalClaimsChat:
    def __init__(self):
        self.client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.excel_handler = ExcelHandler(os.getenv("EXCEL_FILE_PATH"))
        self.conversation_history = []
        
    def get_system_prompt(self) -> str:
        data_summary = self.excel_handler.get_data_summary()
        
        try:
            column_info = self.excel_handler.get_column_info()
            column_info_str = json.dumps(column_info, indent=2, default=convert_numpy_types)
        except Exception as e:
            column_info_str = "Column info unavailable due to data type issues"
        
        return f"""You are a helpful assistant analyzing medical claims data. 

DATA CONTEXT:
{data_summary}

COLUMN DETAILS:
{column_info_str}

You can help users understand and analyze this medical claims dataset. When users ask questions:
1. Provide clear, accurate answers based on the data
2. Suggest specific queries they might want to run
3. Explain medical claims terminology when needed
4. Be helpful in guiding them to insights
5. If the questions need excute queries on the data, excute it then print the result to the user
6. answer question in Arabic or English based on the user language

Based on the data I can see, this appears to be a comprehensive medical claims dataset with:
- Patient information (patient_id, name, Gender)
- Healthcare provider details (doctor_id, doctor_name, hospital_id, hospital_name)
- Insurance information (insurance_provider_id, insurance_provider_name)
- Medical details (MedicalCondition, admission_date, discharge_date, medication, test_results)
- Financial information (billing_amount)
- Administrative data (admission_type, Length_of_Stay)

If you need specific calculations or data analysis, I can help query the dataset.
"""

    def query_data_for_llm(self, user_question: str) -> str:
        user_question_lower = user_question.lower()
        
        context_data = []
        
        # Add basic summary
        context_data.append("DATA SUMMARY:")
        context_data.append(self.excel_handler.get_data_summary())
        
        # Add sample data if asking for examples
        if any(word in user_question_lower for word in ["example", "sample", "show me"]):
            context_data.append("\nSAMPLE DATA:")
            context_data.append(self.excel_handler.query_data("sample_data", rows=3))
        
        # Handle count/total questions directly
        if any(word in user_question_lower for word in ["how many", "total", "count"]):
            total_records = len(self.excel_handler.df)
            context_data.append(f"\nDIRECT ANSWER: There are {total_records} medical claims in the dataset.")
        
        # Add statistics if asking about numbers/stats (but handle errors)
        if any(word in user_question_lower for word in ["average", "statistics", "mean", "median"]):
            try:
                basic_stats = self.excel_handler.query_data("basic_stats")
                context_data.append("\nBASIC STATISTICS:")
                context_data.append(basic_stats)
            except Exception:
                context_data.append("\nNote: Statistical analysis available upon request for specific columns.")
        
        return "\n".join(context_data)

    def chat(self, user_message: str) -> str:
        """Main chat function"""
        # Get relevant data context
        data_context = self.query_data_for_llm(user_message)
        
        # Prepare messages for ChatGPT
        messages = [
            {"role": "system", "content": self.get_system_prompt()},
            {"role": "user", "content": f"DATA CONTEXT:\n{data_context}\n\nUSER QUESTION: {user_message}"}
        ]
        
        messages.extend(self.conversation_history[-6:])
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=messages,
                max_tokens=1000,
                temperature=0.7
            )
            
            assistant_response = response.choices[0].message.content
            
            self.conversation_history.append({"role": "user", "content": user_message})
            self.conversation_history.append({"role": "assistant", "content": assistant_response})
            
            return assistant_response
            
        except Exception as e:
            return f"Error communicating with ChatGPT: {str(e)}"

def main():
    print("Medical Claims Data Chat Interface")
    print("Type 'quit' to exit\n")
    
    try:
        chat_bot = MedicalClaimsChat()
        print("System initialized successfully!")
        print("You can now ask questions about your medical claims data.\n")
        
        while True:
            user_input = input("You: ").strip()
            
            if user_input.lower() in ['quit', 'exit', 'bye']:
                print("Goodbye!")
                break
            
            if not user_input:
                continue
            
            print("Assistant: ", end="")
            response = chat_bot.chat(user_input)
            print(response)
            print()
            
    except Exception as e:
        print(f"Error initializing system: {e}")
        print("Please check your .env file and Excel file path.")
        print(f"Full error details: {type(e).__name__}: {str(e)}")

if __name__ == "__main__":
    main()