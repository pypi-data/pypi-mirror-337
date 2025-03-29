import boto3
import csv
import os
from datetime import datetime
from io import StringIO
import tempfile

class ExpenseExporter:
    """
    This library queries dynamodb for expense records within a date range
    and exports them to a CSV file for download.
    """
    
    def __init__(self, table_name, region_name='us-east-1'):
        """
        Initialize the Class.
        """
        self.dynamodb = boto3.resource('dynamodb', region_name=region_name)
        self.table = self.dynamodb.Table(table_name)
    
    def get_expenses_by_date_range(self, user_id, start_date, end_date):
        """
        Fetch expense records from dynamodb for a specific user within a date range.
        """
        # date formats validation
        try:
            datetime.fromisoformat(start_date)
            datetime.fromisoformat(end_date)
        except ValueError:
            raise ValueError("Dates must be in ISO format (YYYY-MM-DD)")
            
        # using the user-date-index for query by date range
        response = self.table.query(
            IndexName='user-date-index',
            KeyConditionExpression='PK = :pk AND #date BETWEEN :start_date AND :end_date',
            ExpressionAttributeNames={
                '#date': 'date'
            },
            ExpressionAttributeValues={
                ':pk': f"USER-{user_id}",
                ':start_date': start_date,
                ':end_date': end_date
            }
        )
        
        return response.get('Items', [])
    
    def export_to_csv(self, expenses):
        """
        Convert expense items to CSV format with specific columns.
        """
        if not expenses:
            raise ValueError("No expenses found to export")
            
        fieldnames = ['amount', 'bill_id', 'date', 'vendor']
        
        csv_output = StringIO()
        writer = csv.DictWriter(csv_output, fieldnames=fieldnames)
        writer.writeheader()
        
        for expense in expenses:
            filtered_expense = {
                'amount': expense.get('amount', ''),
                'bill_id': expense.get('bill_id', ''),
                'date': expense.get('date', ''),
                'vendor': expense.get('vendor', '')
            }
            writer.writerow(filtered_expense)
            
        csv_output.seek(0)
        return csv_output
    
    def save_to_file(self, csv_data, filename):
        """
        Saving CSV to a file with the specified filename.
        """
        temp_dir = tempfile.gettempdir()
        
        file_path = os.path.join(temp_dir, filename)
        
        with open(file_path, 'w', newline='') as temp_file:
            temp_file.write(csv_data.getvalue())
    
        return file_path
    
    def generate_expense_report(self, user_id, start_date, end_date, filename=None):
        """
        Generate an expense report for a user within a specified date range.
        """
        # fetch expense data
        expenses = self.get_expenses_by_date_range(user_id, start_date, end_date)
        
        if not expenses:
            return {
                'success': False,
                'message': f"No expenses found between {start_date} and {end_date}",
                'count': 0
            }
    
        csv_data = self.export_to_csv(expenses)
        if not filename:
            filename = f"expenses_summary.csv"
        
        file_path = self.save_to_file(csv_data, filename)
        
        total_expenses = len(expenses)
        return {
            'success': True,
            'file_path': file_path,
            'count': total_expenses,
            'start_date': start_date,
            'end_date': end_date
        }