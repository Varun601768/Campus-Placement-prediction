# visualization.py
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt

def generate_salary_visualization():
    df = pd.read_csv('train_mca_with_skills.csv')  # Ensure correct path

    # Calculate mean and median salary
    mean_salary = df['salary'].mean()
    median_salary = df['salary'].median()

    # Plot histogram
    plt.hist(df['salary'], bins=40, edgecolor='black')
    plt.axvline(mean_salary, color='red', linestyle='dashed', linewidth=2, label=f'Mean: {mean_salary:.2f}')
    plt.axvline(median_salary, color='blue', linestyle='dashed', linewidth=2, label=f'Median: {median_salary:.2f}')
    plt.xlabel('Salary')
    plt.ylabel('Frequency')
    plt.title('Salary Distribution')
    plt.legend()

    # Save the plot to a file
    plt.savefig('static/salary_distribution.png')  # Save it in static folder to display in the app
    plt.close()

    # Save gender distribution
    plt.figure(figsize=(6, 4))
    sns.histplot(data=df, x='gender')
    plt.title("Gender Distribution")
    plt.xticks([0, 1], labels=["Male", "Female"])
    plt.savefig("static/gender_distribution.png")
    plt.close()

    # Save pairplot (warning: this might be slow if dataset is large)
    sns.pairplot(data=df, hue='gender')
    plt.savefig("static/pairplot.png")
    

    # Save box plots
    mkt_hr_data = df[df['specialisation'] == 'Iot']
    mkt_fin_data = df[df['specialisation'] == 'DataScience']
    mkt_m_data = df[df['specialisation'] == 'MernStack']
    mkt_c_data = df[df['specialisation'] == 'CyberSecurity']
    
    for col in ['ssc_p', 'hsc_p', 'degree_p', 'mca_p']:
        plt.figure(figsize=(6, 4))
        sns.boxplot(x='specialisation', y=col, data=pd.concat([mkt_hr_data, mkt_fin_data,mkt_m_data,mkt_c_data]))
        plt.title(f'Box Plot of {col} for Iot,DataScience,Mernstack,Cybersecirity')
        plt.xlabel('Specialization')
        plt.ylabel(col)
        plt.savefig(f"static/{col}_boxplot.png")
        plt.close()

    # Save placement status distributions
    plt.figure(figsize=(6, 4))
    sns.histplot(data=df, x='status', hue='gender')
    plt.title('Placement Status Distribution with Gender')
    plt.xlabel('Placement Status')
    plt.savefig("static/placement_status_gender.png")
    plt.close()

    plt.figure(figsize=(6, 4))
    sns.histplot(data=df, x='status', hue='workex')
    plt.title('Placement Status Distribution with Work Experience')
    plt.xlabel('Placement Status')
    plt.savefig("static/placement_status_workex.png")
    plt.close()

    # Save pie chart for specializations
    plt.figure(figsize=(6, 6))
    plt.pie(df['specialisation'].value_counts(), labels=df['specialisation'].value_counts().index, autopct='%1.1f%%')
    plt.title("Pie chart of Specialization")
    plt.savefig("static/specialization_pie.png")
    plt.close()

    # Save salary distribution
    placed_data = df[df['status'] == 'Placed']
    plt.figure(figsize=(6, 4))
    sns.histplot(placed_data['salary'], kde=True, bins=20)
    plt.title('Salary Distribution for Placed Candidates')
    plt.xlabel('Salary')
    plt.ylabel('Count')
    plt.savefig("static/salary_distribution.png")
    plt.close()
