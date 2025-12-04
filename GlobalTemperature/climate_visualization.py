import csv
import datetime
import matplotlib.pyplot as plt
import os

# Step 1: Load and process the data
print("Step 1: Loading the global temperature data...")
data = []
dates = []
temperatures = []

# Read the CSV file
with open('GlobalTemperatures.csv', 'r') as file:
    csv_reader = csv.reader(file)
    header = next(csv_reader)  # Skip header
    
    for row in csv_reader:
        if len(row) > 1 and row[1]:  # Check if temperature data exists
            date_str = row[0]
            temp_str = row[1]
            
            try:
                # Parse date and temperature
                date = datetime.datetime.strptime(date_str, '%Y-%m-%d')
                temp = float(temp_str)
                
                # Store the data
                dates.append(date)
                temperatures.append(temp)
                data.append((date, temp))
            except (ValueError, IndexError):
                continue

print(f"Loaded {len(data)} temperature records.")

# Step 2: Create annual averages for trend analysis
print("Step 2: Creating annual averages...")
annual_data = {}

for date, temp in data:
    year = date.year
    if year not in annual_data:
        annual_data[year] = []
    annual_data[year].append(temp)

# Calculate annual averages
annual_averages = {}
for year, temps in annual_data.items():
    annual_averages[year] = sum(temps) / len(temps)

# Sort by year
years = sorted(annual_averages.keys())
avg_temps = [annual_averages[year] for year in years]

# Step 3: Create basic temperature trend visualization
print("Step 3: Creating temperature trend visualization...")
plt.figure(figsize=(12, 6))
plt.plot(years, avg_temps, 'r-', linewidth=2)
plt.title('Global Land Temperature Trend (1750-Present)', fontsize=16)
plt.xlabel('Year', fontsize=12)
plt.ylabel('Temperature (°C)', fontsize=12)
plt.grid(True, alpha=0.3)

# Add reference lines for important climate events
plt.axvline(x=1850, color='gray', linestyle='--', alpha=0.7, label='Industrial Revolution')
plt.axvline(x=1950, color='darkgray', linestyle='--', alpha=0.7, label='Post-WWII Industrial Boom')
plt.axvline(x=1980, color='black', linestyle='--', alpha=0.7, label='Accelerated Warming')
plt.legend()

# Save the figure
plt.tight_layout()
plt.savefig('temperature_trend.png')
plt.close()

# Step 4: Create decadal temperature change visualization
print("Step 4: Creating decadal temperature change visualization...")
# Group data by decades
decades = {}
for year, temp in annual_averages.items():
    decade = (year // 10) * 10
    if decade not in decades:
        decades[decade] = []
    decades[decade].append(temp)

# Calculate average temperature for each decade
decade_averages = {}
for decade, temps in decades.items():
    decade_averages[decade] = sum(temps) / len(temps)

# Sort decades
sorted_decades = sorted(decade_averages.keys())
decade_temps = [decade_averages[decade] for decade in sorted_decades]

# Create the visualization
plt.figure(figsize=(12, 6))
bars = plt.bar([str(decade) for decade in sorted_decades], decade_temps, color='blue')

# Add a horizontal line for the overall average
overall_avg = sum(avg_temps) / len(avg_temps)
plt.axhline(y=overall_avg, color='red', linestyle='-', label=f'Overall Average: {overall_avg:.2f}°C')

# Customize the plot
plt.title('Average Temperature by Decade', fontsize=16)
plt.xlabel('Decade', fontsize=12)
plt.ylabel('Temperature (°C)', fontsize=12)
plt.grid(True, axis='y', alpha=0.3)
plt.legend()

# Add value labels on top of bars
for bar in bars:
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2., height + 0.05,
             f'{height:.2f}°C',
             ha='center', va='bottom', fontsize=9)

# Save the figure
plt.tight_layout()
plt.savefig('temperature_by_decade.png')
plt.close()

# Step 5: Create a simple dashboard combining both visualizations
print("Step 5: Creating a simple dashboard...")
plt.figure(figsize=(15, 10))

# Plot 1: Annual temperature trend
plt.subplot(2, 1, 1)
plt.plot(years, avg_temps, 'r-', linewidth=2)
plt.title('Global Land Temperature Trend (1750-Present)', fontsize=14)
plt.xlabel('Year', fontsize=10)
plt.ylabel('Temperature (°C)', fontsize=10)
plt.grid(True, alpha=0.3)
plt.axvline(x=1850, color='gray', linestyle='--', alpha=0.7, label='Industrial Revolution')
plt.axvline(x=1950, color='darkgray', linestyle='--', alpha=0.7, label='Post-WWII Industrial Boom')
plt.axvline(x=1980, color='black', linestyle='--', alpha=0.7, label='Accelerated Warming')
plt.legend(fontsize=8)

# Plot 2: Temperature by decade
plt.subplot(2, 1, 2)
bars = plt.bar([str(decade) for decade in sorted_decades], decade_temps, color='blue')
plt.axhline(y=overall_avg, color='red', linestyle='-', label=f'Overall Average: {overall_avg:.2f}°C')
plt.title('Average Temperature by Decade', fontsize=14)
plt.xlabel('Decade', fontsize=10)
plt.ylabel('Temperature (°C)', fontsize=10)
plt.grid(True, axis='y', alpha=0.3)
plt.legend(fontsize=8)

# Add a title for the entire dashboard
plt.suptitle('Global Temperature Analysis Dashboard', fontsize=18, y=0.98)

# Save the dashboard
plt.tight_layout(rect=[0, 0, 1, 0.96])
plt.savefig('climate_dashboard.png')
plt.close()

print("\nVisualization complete! The following files have been created:")
print("1. temperature_trend.png - Shows the long-term temperature trend")
print("2. temperature_by_decade.png - Shows average temperatures by decade")
print("3. climate_dashboard.png - A dashboard combining both visualizations")
print("\nThese visualizations help understand how global temperatures have changed over time.")