import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os

# sanitize function to create valid filenames
def sanitize(name):
    return name.replace('/', '_').replace(' ', '_')

# define the file paths and their corresponding languages and implementation types
files = [
    ("Project/python/python1_results.csv", "python", "Naive"),
    ("Project/python/python2_results.csv", "python", "Optimized"),
    ("Project/python/python3_results.csv", "python", "Parallel"),
    ("Project/Julia/julia1_results.csv", "julia", "Naive"),
    ("Project/Julia/julia2_results.csv", "julia", "Optimized"),
    ("Project/Julia/julia3_results.csv", "julia", "Parallel"),
    ("Project/c++/cpp1_results.csv", "c/c++", "Naive"),
    ("Project/c++/cpp2_results.csv", "c/c++", "Optimized"),
    ("Project/c++/cpp3_results.csv", "c/c++", "Parallel"),
    ("Project/Chapel/chapel1_results.csv", "chapel", "Naive"),
    ("Project/Chapel/chapel2_results.csv", "chapel", "Optimized"),
    ("Project/Chapel/chapel3_results.csv", "chapel", "Parallel"),
]

# read and annotate dataframes
dataframes = []
for file_path, language, impl_type in files:
    if not os.path.exists(file_path):
        print(f"warning: file not found: {file_path}")
        continue
    df = pd.read_csv(file_path)

    # normalize and fix column names
    df.columns = [col.strip().lower().replace("(s)", "").replace(" ", "_") for col in df.columns]

    # rename any common variations
    df = df.rename(columns={
        'matrixsize': 'matrix_size',
        'meantime': 'mean_time',
        'meantime_': 'mean_time',
        'meantime_s': 'mean_time',
        'mean_time(s)': 'mean_time',
        'mean_time_': 'mean_time',
        'mean_time_s': 'mean_time',
    })

    # skip if essential columns missing
    if 'matrix_size' not in df.columns or 'mean_time' not in df.columns:
        print(f"skipping {file_path} due to missing required columns.")
        continue

    # convert to numeric safely
    df['matrix_size'] = pd.to_numeric(df['matrix_size'], errors='coerce')
    df['mean_time'] = pd.to_numeric(df['mean_time'], errors='coerce')
    df = df.dropna(subset=['matrix_size', 'mean_time'])

    # annotate
    df['language'] = language
    df['implementation_type'] = impl_type
    df['row_label'] = f"{language} - {impl_type}"

    dataframes.append(df)

# combine all cleaned and labeled dataframes
results = pd.concat(dataframes, ignore_index=True)

# sort orders
matrix_size_order = sorted(results['matrix_size'].unique())
impl_order = ["Naive", "Optimized", "Parallel"]
lang_order = sorted(results['language'].unique())
row_order = [f"{lang} - {impl}" for impl in impl_order for lang in lang_order]

# pivot the data
pivot = results.pivot_table(
    index='row_label',
    columns='matrix_size',
    values='mean_time',
    aggfunc='mean'
)

# reorder rows and columns
pivot = pivot.reindex(index=row_order)
pivot = pivot[matrix_size_order]

# apply log transform
pivot_logged = np.log10(pivot.replace(0, np.nan))

# plot heatmap
plt.figure(figsize=(10, 8))
sns.set(style="whitegrid")
sns.heatmap(
    pivot_logged,
    cmap="YlGnBu",
    annot=True,
    fmt=".2f",
    linewidths=0.5,
    linecolor='gray',
    cbar_kws={"label": "log10(mean time [s])"},
    mask=pivot_logged.isnull()
)

plt.title("heatmap of log10 mean execution time by language and matrix size", fontsize=16)
plt.xlabel("matrix size")
plt.ylabel("language - implementation type")
plt.tight_layout()
plt.savefig("heatmap_organized.png")
plt.show()

# bar charts for singular comparisons 
for matrix_size in matrix_size_order:
    plt.figure(figsize=(10, 6))
    sub_data = results[results['matrix_size'] == matrix_size]
    
    # create bar chart
    sns.barplot(x='row_label', y='mean_time', hue='implementation_type', data=sub_data, palette=["#FFB6C1", "#FF69B4", "#FF1493"])  
    
    # plot detaisl
    plt.title(f"comparison of execution times for matrix size {matrix_size}", fontsize=14)
    plt.xlabel('language - implementation type')
    plt.ylabel('mean time (seconds)')
    plt.xticks(rotation=45, ha='right')
    plt.legend(title="implementation type")
    plt.tight_layout()
    
    # save the plot as a png file
    plt.savefig(f"bar_chart_matrix_size_{matrix_size}.png")
    plt.show()

# compare across a specific language
for language in lang_order:
    plt.figure(figsize=(12, 8))
    sub_data = results[results['language'] == language]
    
    # create bar chart
    sns.barplot(x='matrix_size', y='mean_time', hue='implementation_type', data=sub_data, palette=["#FFB6C1", "#FF69B4", "#FF1493"])  # girly pink shades
    
    #  plot details
    plt.title(f"execution time comparison for {language.capitalize()}", fontsize=14)
    plt.xlabel('matrix size')
    plt.ylabel('mean time (seconds)')
    plt.legend(title="implementation type")
    plt.tight_layout()
    
     # sanitize the filename and save the plot
    sanitized_filename = sanitize(f"bar_chart_{language}.png")
    plt.savefig(sanitized_filename)
    plt.show()
