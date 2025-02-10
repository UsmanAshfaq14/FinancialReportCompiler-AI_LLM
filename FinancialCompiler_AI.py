import json
from typing import Dict, List, Union
import csv
from io import StringIO

class FinancialReportCompiler:
    def __init__(self):
        self.required_fields = ['section', 'type', 'id', 'value', 'description']
        self.valid_sections = ['Revenue', 'Cost', 'Profit']

    def validate_data(self, data: List[Dict]) -> List[str]:
        errors = []
        
        for record in data:
            # Check required fields
            missing_fields = [field for field in self.required_fields if field not in record]
            if missing_fields:
                errors.append(f"Missing required fields: {', '.join(missing_fields)}")
                continue

            # Validate section
            if record['section'] not in self.valid_sections:
                errors.append(f"Invalid section: {record['section']}")

            # Validate id
            if not isinstance(record['id'], str) or not record['id'].strip():
                errors.append(f"Invalid id for record: {record}")

            # Validate value
            try:
                value = float(record['value'])
                if record['section'] == 'Revenue' and value <= 0:
                    errors.append(f"Revenue value must be greater than 0: {value}")
                elif record['section'] == 'Cost' and value < 0:
                    errors.append(f"Cost value must be 0 or greater: {value}")
            except (ValueError, TypeError):
                errors.append(f"Invalid value format: {record['value']}")

        return errors

    def parse_input(self, data: str, format_type: str) -> List[Dict]:
        if format_type == 'csv':
            csv_data = StringIO(data)
            reader = csv.DictReader(csv_data)
            return list(reader)
        elif format_type == 'json':
            try:
                json_data = json.loads(data)
                return json_data.get('records', [])
            except json.JSONDecodeError:
                raise ValueError("Invalid JSON format")
        else:
            raise ValueError("Unsupported format")

    def calculate_revenue(self, data: List[Dict]) -> Dict:
        revenue_records = [record for record in data if record['section'] == 'Revenue']
        total_revenue = sum(float(record['value']) for record in revenue_records)
        return {
            'total': total_revenue,
            'records': revenue_records
        }

    def calculate_cost(self, data: List[Dict]) -> Dict:
        cost_records = [record for record in data if record['section'] == 'Cost']
        total_cost = sum(float(record['value']) for record in cost_records)
        return {
            'total': total_cost,
            'records': cost_records
        }

    def calculate_profit(self, total_revenue: float, total_cost: float) -> float:
        return total_revenue - total_cost

    def generate_report(self, data: List[Dict]) -> str:
        revenue_data = self.calculate_revenue(data)
        cost_data = self.calculate_cost(data)
        profit = self.calculate_profit(revenue_data['total'], cost_data['total'])

        report = []
        report.append("# Financial Report\n")
        
        # Data Validation Summary
        report.append("## Data Validation Summary")
        report.append("- All records contain required fields")
        report.append("- All values are valid numbers")
        report.append("- Revenue values are greater than 0")
        report.append("- Cost values are 0 or greater\n")

        # Revenue Summary
        report.append("## Revenue Summary")
        report.append("Formula:")
        report.append("$Total\\ Revenue = \\sum_{i=1}^{n} Revenue_i$")
        report.append("\nStep-by-step calculation:")
        revenue_parts = []
        for record in revenue_data['records']:
            value = float(record['value'])
            revenue_parts.append(f"${value:,.2f}")
            report.append(f"- {record['description']}: ${value:,.2f}")
        
        report.append("\nDetailed calculation:")
        report.append(f"$Total\\ Revenue = {' + '.join(revenue_parts)} = ${revenue_data['total']:,.2f}$\n")

        # Cost Breakdown
        report.append("## Cost Breakdown")
        report.append("Formula:")
        report.append("$Total\\ Cost = \\sum_{i=1}^{n} Cost_i$")
        report.append("\nStep-by-step calculation:")
        cost_parts = []
        for record in cost_data['records']:
            value = float(record['value'])
            cost_parts.append(f"${value:,.2f}")
            report.append(f"- {record['description']}: ${value:,.2f}")
        
        report.append("\nDetailed calculation:")
        report.append(f"$Total\\ Cost = {' + '.join(cost_parts)} = ${cost_data['total']:,.2f}$\n")

        # Profit Calculation
        report.append("## Profit Calculation")
        report.append("Formula:")
        report.append("$Profit = Total\\ Revenue - Total\\ Cost$")
        report.append("\nStep-by-step calculation:")
        report.append(f"$Profit = ${revenue_data['total']:,.2f} - ${cost_data['total']:,.2f} = ${profit:,.2f}$\n")

        # Feedback Line
        report.append("## Feedback")
        report.append("Would you like detailed calculations for any specific section? Please rate this report on a scale of 1 to 5 stars.")

        return "\n".join(report)

    def process_report(self, input_data: str, format_type: str) -> str:
        try:
            data = self.parse_input(input_data, format_type)
            errors = self.validate_data(data)
            
            if errors:
                return "ERROR: Data validation failed:\n" + "\n".join(errors)
                
            return self.generate_report(data)
            
        except Exception as e:
            return f"ERROR: {str(e)}"

# Usage Example
if __name__ == "__main__":
    # Create compiler instance
    compiler = FinancialReportCompiler()

#     # Example with CSV data
#     csv_data = """section,type,id,value,description
# Revenue,summary,rev1,5000.00,Q1 Product Sales
# Revenue,summary,rev2,3000.00,Q1 Service Income
# Revenue,summary,rev3,2000.00,Q1 Consulting Fees
# Cost,breakdown,cost1,2500.00,Raw Materials
# Cost,breakdown,cost2,1800.00,Labor Costs
# Cost,breakdown,cost3,1200.00,Operating Expenses"""

#     print("Processing CSV data...\n")
#     csv_report = compiler.process_report(csv_data, 'csv')
#     print(csv_report)

    # Example with JSON data
    json_data = """
    {
  "records": [
    {"section": "Revenue", "type": "summary", "id": "R201", "value": 5000, "description": "North sector digital product sales"},
    {"section": "Revenue", "type": "summary", "id": "R202", "value": 5400, "description": "South sector software licensing"},
    {"section": "Revenue", "type": "summary", "id": "R203", "value": 4700, "description": "East sector hardware sales"},
    {"section": "Revenue", "type": "summary", "id": "R204", "value": 6200, "description": "West sector cloud service income"},
    {"section": "Revenue", "type": "summary", "id": "R205", "value": 5800, "description": "Central sector consulting revenue"},
    {"section": "Revenue", "type": "summary", "id": "R206", "value": 5100, "description": "Online platform subscriptions"},
    {"section": "Revenue", "type": "summary", "id": "R207", "value": 5300, "description": "Global e-commerce revenue"},
    {"section": "Revenue", "type": "summary", "id": "R208", "value": 6000, "description": "Regional franchise income"},
    {"section": "Revenue", "type": "summary", "id": "R209", "value": 5500, "description": "Affiliate marketing revenue"},
    {"section": "Revenue", "type": "summary", "id": "R210", "value": 5900, "description": "Licensing fees revenue"},
    {"section": "Revenue", "type": "summary", "id": "R211", "value": 5200, "description": "New product launch revenue"},
    {"section": "Cost", "type": "breakdown", "id": "C201", "value": 1500, "description": "Production material costs"},
    {"section": "Cost", "type": "breakdown", "id": "C202", "value": 900, "description": "Distribution expenses"},
    {"section": "Cost", "type": "breakdown", "id": "C203", "value": 1100, "description": "Advertising campaign costs"},
    {"section": "Cost", "type": "breakdown", "id": "C204", "value": 800, "description": "Office rental expense"},
    {"section": "Cost", "type": "breakdown", "id": "C205", "value": 750, "description": "Equipment maintenance costs"},
    {"section": "Cost", "type": "breakdown", "id": "C206", "value": 850, "description": "Employee training expenses"},
    {"section": "Cost", "type": "breakdown", "id": "C207", "value": 700, "description": "Utility and service charges"},
    {"section": "Cost", "type": "breakdown", "id": "C208", "value": 950, "description": "Logistics and shipping expenses"},
    {"section": "Cost", "type": "breakdown", "id": "C209", "value": 880, "description": "IT infrastructure costs"},
    {"section": "Cost", "type": "breakdown", "id": "C210", "value": 920, "description": "Insurance and security costs"}
  ]
}

    """

    print("\nProcessing JSON data...\n")
    json_report = compiler.process_report(json_data, 'json')
    print(json_report)

