from flask import Flask, request, jsonify, send_file
import pandas as pd
import base64
import io

app = Flask(__name__)

@app.route('/upload', methods=['POST'])
def upload_file():
    try:
        # Get JSON data from request
        json_data = request.get_json()

        # Extract file data and additional parameters
        base64_file_data = json_data.get('file')
        sheet_names = json_data.get('sheet_names')
        compare_index = json_data.get('compare_index')

        # Decode base64 file data
        file_data = base64.b64decode(base64_file_data)

        # Convert the raw data to a BytesIO stream
        data_stream = io.BytesIO(file_data)

        # Read the Excel file from the BytesIO stream
        df_dict = pd.read_excel(data_stream, sheet_name=sheet_names, engine='openpyxl')

        results = {}

        # Function to compare data
        def compare_data(source, target, index):
            identical = []
            source_only = []
            target_only = []
            different = []

            for i in range(len(source)):
                source_value = source.iloc[i, index]
                target_value = target.iloc[i, index] if i < len(target) else None

                if pd.isnull(source_value) and pd.notnull(target_value):
                    source_only.append(source.iloc[i].to_dict())
                elif pd.notnull(source_value) and pd.isnull(target_value):
                    target_only.append(target.iloc[i].to_dict())
                elif source_value == target_value:
                    identical.append(source.iloc[i].to_dict())
                else:
                    different.append({
                        'source': source.iloc[i].to_dict(),
                        'target': target.iloc[i].to_dict() if i < len(target) else {}
                    })

            return {
                'identical': identical,
                'source_only': source_only,
                'target_only': target_only,
                'different': different
            }

        for sheet_name, sheet_df in df_dict.items():
            # Process each sheet from the 15th row to the end
            data = sheet_df.iloc[14:].reset_index(drop=True)

            # Split data into pairs
            source_df = data.iloc[::2].reset_index(drop=True)
            target_df = data.iloc[1::2].reset_index(drop=True)

            # Perform the comparison
            result = compare_data(source_df, target_df, compare_index)
            results[sheet_name] = result

        # Create Excel file with summary and details
        output = io.BytesIO()
        writer = pd.ExcelWriter(output, engine='xlsxwriter')

        # Write summary sheet
        summary_df = pd.DataFrame(columns=['sheet_name', 'total_count', 'identical_count', 'source_only_count', 'target_only_count', 'different_count'])
        
        for sheet_name, result in results.items():
            summary_df = summary_df.append({
                'sheet_name': sheet_name,
                'total_count': len(result['identical']) + len(result['source_only']) + len(result['target_only']) + len(result['different']),
                'identical_count': len(result['identical']),
                'source_only_count': len(result['source_only']),
                'target_only_count': len(result['target_only']),
                'different_count': len(result['different'])
            }, ignore_index=True)

        summary_df.to_excel(writer, sheet_name='summary', index=False)

        # Write detail sheets
        for sheet_name, result in results.items():
            detail_df = pd.DataFrame(result['identical'])
            detail_df['Type'] = 'identical'
            detail_df.to_excel(writer, sheet_name=sheet_name+'_identical', index=False)

            detail_df = pd.DataFrame(result['source_only'])
            detail_df['Type'] = 'source_only'
            detail_df.to_excel(writer, sheet_name=sheet_name+'_source_only', index=False)

            detail_df = pd.DataFrame(result['target_only'])
            detail_df['Type'] = 'target_only'
            detail_df.to_excel(writer, sheet_name=sheet_name+'_target_only', index=False)

            detail_df = pd.DataFrame(result['different'])
            detail_df['Type'] = 'different'
            detail_df.to_excel(writer, sheet_name=sheet_name+'_different', index=False)

        writer.save()
        output.seek(0)

        # Return Excel file to the frontend
        return send_file(output, attachment_filename='comparison_results.xlsx', as_attachment=True)

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
