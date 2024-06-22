import json

from google.cloud import bigquery

def transfer_data(request):
    """Transfers data from App Engine to BigQuery."""

    request_json = request.get_json()
    if not request_json:
        return 'Request body must contain JSON data.', 400

    data = request_json.get('data')
    if not data:
        return 'Request body must contain a "data" field with the data to transfer.', 400

    # Replace with your BigQuery project ID, dataset ID, and table ID
    client = bigquery.Client()
    table_ref = client.dataset(dataset_id='your_dataset_id').table(table_name='your_table_name')
    errors = client.insert_rows(table_ref, data)

    if errors:
        error_string = ', '.join(str(e) for e in errors)
        return f'Errors while inserting data: {error_string}', 500

    return 'Data transferred successfully!', 200
