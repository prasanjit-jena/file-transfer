from django.shortcuts import render, redirect
from django.http import HttpResponse, FileResponse,StreamingHttpResponse
from .forms import UploadFileForm
import pandas as pd
import plotly.express as px
import os
from django.conf import settings
from io import BytesIO
from .models import ProcessedData

def handle_uploaded_file(files):
    # Load the master file
    master_path = "C:/Users/Prasanjit Jena/Downloads/master.xlsx"
    master = pd.ExcelFile(master_path)

    # Read the master data
    name_df = master.parse('name')
    lob_df = master.parse('lob')
    category_df = master.parse('category')
    month_df = master.parse('month')

    # Function to process each input sheet
    def process_sheet(sheet_name, excel_file):
        if sheet_name == 'Health Portfolio' or sheet_name== 'Liability Portfolio':
            df = excel_file.parse(sheet_name,skiprows=2)
        else:
            df = excel_file.parse(sheet_name,skiprows=1)
        # df = excel_file.parse(sheet_name)
        # Ensure there are at least 3 rows to drop the first two and have headers
        # df = df.dropna(subset=[df.columns[0]])  # Drop rows where the first column is NaN
        # df.columns = df.iloc[1]  # Use the second row as header
        # df = df.drop([0, 1])  # Drop the first two rows
        df = df.rename(columns={df.columns[0]: 'insurer'})
        df = df.melt(id_vars=['insurer'], var_name='Product', value_name='Value')
        return df

    # Process each sheet from input1 and input2 and concatenate
    input1 = pd.ExcelFile(files['input1'])
    input2 = pd.ExcelFile(files['input2'])

    input1_dfs = [process_sheet(sheet, input1) for sheet in input1.sheet_names]
    input2_dfs = [process_sheet(sheet, input2) for sheet in input2.sheet_names]

    input1_combined = pd.concat(input1_dfs, ignore_index=True)
    input2_combined = pd.concat(input2_dfs, ignore_index=True)

    # Combine input1 and input2 data
    combined_df = pd.concat([input1_combined, input2_combined], ignore_index=True)

    # Merge with master data
    combined_df = combined_df.merge(name_df, how='left', left_on='insurer', right_on='insurer')
    combined_df = combined_df.merge(category_df, how='left', on='clubbed_name')
    combined_df = combined_df.dropna()
    # print(combined_df)
    # Add month data
    output_df = pd.DataFrame()

    for month in month_df['month']:
        month_num = month_df[month_df['month'] == month]['month_num'].values[0]
        temp_df = combined_df.copy()
        temp_df['Year'] = 2022  # Assuming the year is 2022
        temp_df['Month'] = month
        temp_df['month_num'] = month_num
        output_df = pd.concat([output_df, temp_df], ignore_index=True)

    # Select and reorder columns
    output_df = output_df[['Year', 'Month', 'category', 'clubbed_name', 'Product', 'Value']]
    for _, row in output_df.head(1000).iterrows():
        ProcessedData.objects.create(
            year=row['Year'],
            month=row['Month'],
            category=row['category'],
            clubbed_name=row['clubbed_name'],
            product=row['Product'],
            value=row['Value']
        )

    # Generate output file
    output_file_path = os.path.join(settings.MEDIA_ROOT, 'output.xlsx')
    output_df.to_excel(output_file_path, index=False)

    return output_file_path

def upload_file(request):
    # ProcessedData.objects.all().delete() 
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            input1_file = request.FILES['input1']
            input2_file = request.FILES['input2']
            output_file_path = handle_uploaded_file({'input1': input1_file, 'input2': input2_file})
            request.session['output_file_path'] = output_file_path
            return redirect('generate_output')
    else:
        form = UploadFileForm()
    return render(request, 'upload.html', {'form': form})

def generate_output(request):
    output_file_path = request.session.get('output_file_path')
    if not output_file_path or not os.path.exists(output_file_path):
        return HttpResponse("Output file not found.", status=404)

    # Generate a plot
    plot_data = pd.read_excel(output_file_path)
    # print(plot_data)
    fig = px.bar(plot_data, x='clubbed_name', y='Value', title='Bar Graph', labels={'Value': 'Value'}, color_discrete_sequence=['blue','red','green'])

    # Convert Plotly figure to HTML
    plot_html = fig.to_html(full_html=False)

    # Save plot_data to a new Excel file for download
    plot_data_output_path = os.path.join(settings.MEDIA_ROOT, 'plot_data.xlsx')
    plot_data.to_excel(plot_data_output_path, index=False)
    request.session['plot_data_output_path'] = plot_data_output_path

    return render(request, 'output.html', {'plot_html': plot_html, 'plot_data': plot_data.head(1000).to_html(classes='table table-bordered')})


def download_output_file(request):
    plot_data_output_path = request.session.get('plot_data_output_path')
    if not plot_data_output_path or not os.path.exists(plot_data_output_path):
        return HttpResponse("Output file not found.", status=404)
    
    response = StreamingHttpResponse(open(plot_data_output_path, 'rb'))
    response['Content-Disposition'] = 'attachment; filename="plot_data.xlsx"'
    return response
