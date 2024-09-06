import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

class EDAAnalysis:
    def __init__(self, data):
        self.data = data.copy()

    def describe_variables(self):
        """Describe dataset variables and their data types."""
        print("Dataset columns and their data types:")
        print(self.data.dtypes)
        return self.data.head()

    def segment_users_by_decile(self):
        """Segment users into decile classes based on total session duration and compute total data."""
        self.data['total_data'] = self.data['Total DL (Bytes)'] + self.data['Total UL (Bytes)']
        self.data['decile_class'] = pd.qcut(self.data['Dur. (ms)'], 10, labels=False)
        total_data_per_decile = self.data.groupby('decile_class')['total_data'].sum()

        plt.figure(figsize=(10, 6))
        sns.barplot(x=total_data_per_decile.index, y=total_data_per_decile.values, palette='Blues_d')
        plt.title('Total Data (DL + UL) per Decile Class')
        plt.xlabel('Decile Class')
        plt.ylabel('Total Data (Bytes)')
        plt.show()

    def analyze_basic_metrics(self):
        """Analyze basic metrics: mean, median, etc."""
        metrics = self.data[['Dur. (ms)', 'Total DL (Bytes)', 'Total UL (Bytes)']].describe()
        print(metrics)

        plt.figure(figsize=(12, 8))
        self.data[['Dur. (ms)', 'Total DL (Bytes)', 'Total UL (Bytes)']].hist(bins=30, layout=(2, 2), figsize=(12, 8))
        plt.suptitle('Histograms of Session Duration, Total DL, and Total UL')
        plt.show()

    def compute_dispersion_parameters(self):
        """Compute and print dispersion parameters for the data."""
        variance = self.data[['Dur. (ms)', 'Total DL (Bytes)', 'Total UL (Bytes)']].var()
        std_dev = self.data[['Dur. (ms)', 'Total DL (Bytes)', 'Total UL (Bytes)']].std()
        print("Variance:\n", variance)
        print("\nStandard Deviation:\n", std_dev)

    def plot_univariate_analysis(self):
        """Generate box plots for univariate analysis."""
        plt.figure(figsize=(12, 6))
        sns.boxplot(data=self.data[['Dur. (ms)', 'Total DL (Bytes)', 'Total UL (Bytes)']])
        plt.title('Box Plots of Session Duration, Total DL, and Total UL')
        plt.show()

    def bivariate_analysis(self):
        """Explore relationships between application data and total data."""
        # Create a new column for total data (DL + UL)
        self.data['total_data'] = self.data['Total DL (Bytes)'] + self.data['Total UL (Bytes)']

        # List of application columns to compare against total data
        applications = ['Social Media DL (Bytes)', 'Google DL (Bytes)', 'Email DL (Bytes)', 
                        'Youtube DL (Bytes)', 'Netflix DL (Bytes)', 'Gaming DL (Bytes)', 'Other DL (Bytes)']

        # Iterate over each application column to create a scatter plot
        for app in applications:
            plt.figure(figsize=(10, 6))  # Set the figure size for each plot
            sns.scatterplot(x=self.data[app], y=self.data['total_data'])
            plt.title(f'Relationship between {app} and Total Data (Bytes)')
            plt.xlabel(app)
            plt.ylabel('Total Data (Bytes)')
            plt.show()  # Display the plot for each application

    def correlation_analysis(self):
        """Generate correlation matrix for application data."""
        app_data = self.data[['Social Media DL (Bytes)', 'Google DL (Bytes)', 'Email DL (Bytes)', 'YouTube DL (Bytes)', 
                              'Netflix DL (Bytes)', 'Gaming DL (Bytes)', 'Other DL (Bytes)']]
        correlation_matrix = app_data.corr()

        plt.figure(figsize=(10, 6))
        sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm')
        plt.title('Correlation Matrix of Application Data')
        plt.show()

    def pca_analysis(self):
        """Perform PCA and plot the components."""
        app_data = self.data[['Social Media DL (Bytes)', 'Google DL (Bytes)', 'Email DL (Bytes)', 'YouTube DL (Bytes)', 
                              'Netflix DL (Bytes)', 'Gaming DL (Bytes)', 'Other DL (Bytes)']]
        scaler = StandardScaler()
        scaled_data = scaler.fit_transform(app_data)

        pca = PCA(n_components=2)
        pca_components = pca.fit_transform(scaled_data)

        plt.figure(figsize=(10, 6))
        plt.scatter(pca_components[:, 0], pca_components[:, 1], c='blue', edgecolor='k', s=50)
        plt.title('PCA of Application Data')
        plt.xlabel('Principal Component 1')
        plt.ylabel('Principal Component 2')
        plt.show()

        print("Explained variance ratio:", pca.explained_variance_ratio_)
