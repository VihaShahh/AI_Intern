import gradio as gr
import pandas as pd
import PyPDF2

# Function to process CSV file
def process_csv(file):
    df = pd.read_csv(file.name)
    return df

# Function to process PDF file
def process_pdf(file):
    pdf_reader = PyPDF2.PdfReader(file.name)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

# Function to filter CSV data
def filter_csv_data(df, column_name, filter_value):
    filtered_df = df[df[column_name] == filter_value]
    return filtered_df

# Function to handle questions and outputs
def ask_question(question, file, file_type, column_name, filter_value):
    if file_type == "CSV":
        df = process_csv(file)
        if column_name and filter_value:
            df = filter_csv_data(df, column_name, filter_value)
        
        # Attempt to determine the column of interest from the question
        for col in df.columns:
            if col.lower() in question.lower():
                return df[[col]].to_string(index=False)

        # If no specific column is identified, return the filtered data
        return df.to_string()

    elif file_type == "PDF":
        text = process_pdf(file)
        if question:
            # Simple keyword search in the text
            if question.lower() in text.lower():
                return "The keyword was found in the document."
            else:
                return "The keyword was not found in the document."
        else:
            return text
    else:
        return "Unsupported file type"

# Gradio Interface
file_upload = gr.File(label="Upload CSV or PDF", file_types=["csv", "pdf"])
file_type = gr.Dropdown(choices=["CSV", "PDF"], label="Select File Type")
question_box = gr.Textbox(label="Ask a question")
column_name_box = gr.Textbox(label="Column Name (for CSV filtering)")
filter_value_box = gr.Textbox(label="Filter Value (for CSV filtering)")
output_box = gr.Textbox(label="Output", lines=10)

interface = gr.Interface(
    fn=ask_question,
    inputs=[question_box, file_upload, file_type, column_name_box, filter_value_box],
    outputs=output_box,
    title="Document Analyzer",
    description="Upload a CSV or PDF file, ask questions, and filter data.",
)

interface.launch()
