import pandas as pd
import json
from typing import Dict, Any, List

class ExcelHandler:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.df = None
        self.load_data()
    
    def load_data(self):
        """Load Excel file into pandas DataFrame"""
        try:
            self.df = pd.read_excel(self.file_path)
            print(f"Loaded {len(self.df)} rows and {len(self.df.columns)} columns")
            print(f"Columns: {list(self.df.columns)}")
        except Exception as e:
            print(f"Error loading Excel file: {e}")
            raise
    
    def get_data_summary(self) -> str:
        """Get basic summary of the data"""
        if self.df is None:
            return "No data loaded"
        
        missing_values = {}
        for col in self.df.columns:
            missing_count = self.df[col].isnull().sum()
            missing_values[col] = int(missing_count) if hasattr(missing_count, 'item') else missing_count
        
        summary = f"""
Medical Claims Data Summary:
- Total Records: {len(self.df)}
- Total Columns: {len(self.df.columns)}
- Columns: {', '.join(self.df.columns)}
- Data Types: {dict(self.df.dtypes.astype(str))}
- Missing Values: {missing_values}
"""
        return summary
    
    def query_data(self, query_type: str, **kwargs) -> str:
        """Execute specific queries on the data"""
        if self.df is None:
            return "No data available"
        
        try:
            if query_type == "basic_stats":
                return self.df.describe().to_string()
            elif query_type == "sample_data":
                rows = kwargs.get('rows', 5)
                return self.df.head(rows).to_string()
            elif query_type == "column_values":
                column = kwargs.get('column')
                if column in self.df.columns:
                    return f"Unique values in {column}: {self.df[column].unique()[:20]}"
                return f"Column {column} not found"
            elif query_type == "filter_data":
                column = kwargs.get('column')
                value = kwargs.get('value')
                if column in self.df.columns:
                    filtered = self.df[self.df[column] == value]
                    return f"Found {len(filtered)} records matching {column}={value}"
                return f"Column {column} not found"
            else:
                return "Unknown query type"
        except Exception as e:
            return f"Error executing query: {str(e)}"
    
    def get_column_info(self) -> Dict[str, Any]:
        """Get detailed column information"""
        if self.df is None:
            return {}
        
        column_info = {}
        for col in self.df.columns:
            sample_values = self.df[col].dropna().unique()[:5]
            sample_values_converted = []
            for val in sample_values:
                if pd.isna(val):
                    sample_values_converted.append(None)
                elif hasattr(val, 'item'): 
                    sample_values_converted.append(val.item())
                else:
                    sample_values_converted.append(str(val))
            
            column_info[col] = {
                'type': str(self.df[col].dtype),
                'non_null_count': int(self.df[col].count()),  
                'unique_values': int(self.df[col].nunique()),
                'sample_values': sample_values_converted
            }
        return column_info