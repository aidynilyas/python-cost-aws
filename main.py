import boto3
from datetime import datetime

# Input from user
granularity = input("How do you want to group the costs? (DAILY / MONTHLY): ").upper()

# Validate granularity
if granularity not in ["DAILY", "MONTHLY"]:
    print("Invalid granularity. Must be DAILY or MONTHLY.")
    exit(1)

startDate = input("Enter Start Date (FORMAT MUST BE = YYYY-MM-DD): ")
endDate = input("Enter End Date (FORMAT MUST BE = YYYY-MM-DD): ")

# Validate date format (optional, basic check)
try:
    datetime.strptime(startDate, "%Y-%m-%d")
    datetime.strptime(endDate, "%Y-%m-%d")
except ValueError:
    print("Invalid date format. Use YYYY-MM-DD.")
    exit(1)

# Create Cost Explorer client
client = boto3.client('ce')

# Get cost and usage
response = client.get_cost_and_usage(
    TimePeriod={
        'Start': startDate,
        'End': endDate
    },
    Granularity=granularity,
    Metrics=['UnblendedCost'],
    GroupBy=[{
        'Type': 'DIMENSION',
        'Key': 'SERVICE'
    }]
)

# Print results
print(f"\nAWS Cost from {startDate} to {endDate} grouped by {granularity}:\n")
for time_period in response['ResultsByTime']:
    print(f"{time_period['TimePeriod']['Start']} to {time_period['TimePeriod']['End']}:")
    for group in time_period['Groups']:
        service = group['Keys'][0]
        amount = float(group['Metrics']['UnblendedCost']['Amount'])
        print(f"  • {service}: ${amount:.5f}")
    print()
