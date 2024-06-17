from flask import Flask, render_template, request, send_file, session
from werkzeug.utils import secure_filename
import pandas as pd
from geopy.geocoders import ArcGIS
import folium
import os
import glob
import secrets
import math
import re



# Initialize the Flask application
app = Flask(__name__)
# Generate a random secret key for the session
app.secret_key = secrets.token_hex()

# Set the timeout for the ArcGIS geocoder
ArcGIS().timeout = 1000


# Define a route for the Home page of the flask app
@app.route('/')
def home():
    # Delete all CSV files in the root directory to free space
    for temporary_csv_file in glob.glob('*.csv'):
        os.remove(temporary_csv_file)

    # Delete all Excel XLSX files in the root directory to free space
    for temporary_excel_file in glob.glob('*.xlsx'):
        os.remove(temporary_excel_file)

    # Remove all temporary HTML map files from the 'templates' directory
    for temporary_map_file in glob.glob('./templates/map_*.html'):
        os.remove(temporary_map_file)

    # Reset the session variable 'output_file_name' to None
    session['output_file_name'] = None

    # Render and return the 'index.html' template to display the home page
    return render_template('index.html')


# Define a route for the 'file_processed.html' page, to which the app navigates ...
# ... after user submits a file for processing
@app.route('/file_processed.html', methods=['POST', 'GET'])
def process_file():
    # Check if the request method is POST
    if request.method == 'POST':
        # Retrieve the uploaded file object from the form
        input_file = request.files['uploaded_file']

        # Create a secure filename for saving the input file
        temporary_file_name = secure_filename('uploaded_{}'.format(input_file.filename))
        # Save the uploaded file object as a local temporary file
        input_file.save(temporary_file_name)

        # Initialize the file_type to None
        file_type = None
        # Check if the file type is CSV and read it into a DataFrame
        if input_file.filename[-4:] == '.csv':
            file_type = 'csv'
            df = pd.read_csv(temporary_file_name)
        # Check if the file type is Excel XLSX and read the first sheet into a DataFrame
        if input_file.filename[-5:] == '.xlsx':
            file_type = 'xlsx'
            df = pd.read_excel(temporary_file_name, sheet_name=0)

        # Retrieve the column names of the DataFrame
        cols = df.columns

        # Check if none of the columns contain the keyword 'address'
        if not any('address' in col.lower() for col in cols):
            # If so, render and return the 'invalid_file_uploaded.html' template
            return render_template('invalid_file_uploaded.html')

        # Iterate over each column in the DataFrame
        for col in cols:
            # Check if the column contains 'address' in its name
            if 'address' in col.lower():
                # Define the names for latitude column, longitude column, and map column
                lat_col = col + '_latitude'
                lon_col = col + '_longitude'
                map_col = col + '_map'
                # Add two new columns to the DataFrame for geocoding outputs
                # Apply geocoding to each address in the dataframe to get the latitude
                df[lat_col] = df[col].apply(lambda x: ArcGIS().geocode(x).latitude \
                                            if ArcGIS().geocode(x) else None)
                # Apply geocoding to each address in the dataframe to get the longitude
                df[lon_col] = df[col].apply(lambda x: ArcGIS().geocode(x).longitude \
                                            if ArcGIS().geocode(x) else None)

                # Create a Folium map centered on the first geocoded address
                full_map = folium.Map(
                                location=(df.iloc[0][lat_col], df.iloc[0][lon_col]),
                                zoom_start=14, tiles='openstreetmap',
                                control_scale=True
                                      )
                # Create a Folium feature group for collecting markers for all addresses
                fg = folium.FeatureGroup(name='all_points')

                # Iterate over each row in the DataFrame
                for row_index in range(len(df)):
                    # Get the current row
                    row = df.iloc[row_index]
                    # Extract the latitude value
                    lat = row[lat_col]
                    # Extract the longitude value
                    lon = row[lon_col]
                    # Check if latitude and longitude values are valid
                    if (not math.isnan(lat)) and (not math.isnan(lon)):
                        # Create a default blue marker for the current coordinate
                        default_marker = folium.Marker(
                                           location=(lat, lon),
                                           popup=folium.Popup(row[col], parse_html=True),
                                           icon=folium.Icon(color='blue')
                                                       )
                        # Add the marker to the feature group
                        fg.add_child(default_marker)

                # Add the feature group carrying all markers to the Folium map
                full_map.add_child(fg)

                # Create an empty list for collecting all the map HTML templates
                list_map_url = []
                # Iterate over each row in the DataFrame
                for row_index in range(len(df)):
                    # Get the current row
                    row = df.iloc[row_index]
                    # Extract the latitude value
                    lat = row[lat_col]
                    # Extract the longitude value
                    lon = row[lon_col]
                    # Check if latitude and longitude values are valid
                    if (not math.isnan(lat)) and (not math.isnan(lon)):
                        # Create a featured red marker to highlight the current coordinate
                        featured_marker = folium.Marker(
                                               location=(lat, lon),
                                               popup=folium.Popup(row[col], parse_html=True),
                                               icon=folium.Icon(color='red')
                                                        )
                        # Add the featured red marker to the Folium map
                        full_map.add_child(featured_marker)

                        # Set the center of the map view to the current coordinate
                        full_map.location = [lat, lon]
                        # Define a file name for the map HTML template
                        map_url = 'map_{}_lat={}_lon={}.html'  \
                                  .format(col.replace(' ', '_'), lat, lon)
                        # Save the Folium map as a HTML template file
                        full_map.save('./templates/'+map_url)

                        # Create another default blue marker
                        default_marker = folium.Marker(
                                           location=(lat, lon),
                                           popup=folium.Popup(row[col], parse_html=True),
                                           icon=folium.Icon(color='blue')
                                                       )
                        # Place the default blue marker to overlay the red featured marker
                        full_map.add_child(default_marker)

                        # Add the map URL to the list
                        list_map_url.append(map_url)

                    else:
                        # If the current latitude or longitude values are NaN ...
                        # ... add None to the list
                        list_map_url.append(None)

                # Add a new column to the DataFrame to display the address on the map
                df[map_col] = list_map_url

        # Rename 'Unnamed: 0' column to ''
        df.rename(columns={'Unnamed: 0': ''}, inplace=True)

        # Convert the DataFrame to HTML and apply custom styles to the table elements
        data_table_html = df.to_html(index=False)   \
                            .replace('<thead>', '<thead class="thead">') \
                            .replace('<tbody>', '<tbody class="tbody">')
        # Replace the table data cells containing map URLs with clickable links
        data_table_html = re.sub(r'<td>(map_\S+_lat=[-\d\.]+_lon=[-\d\.]+\.html)</td>',
                            r"<td><a target='_blank' href='/\1'>Show on Map</a></td>",
                            data_table_html)

        # Remove map columns from the DataFrame as they are no longer needed
        map_cols = [col for col in df.columns if '_map' in col]
        df.drop(map_cols, axis=1, inplace=True)

        # Set the output file name for use in the download view
        session['output_file_name'] = 'geocoded_' + input_file.filename
        # Save the DataFrame to either CSV or Excel file based on the input file type
        if file_type == 'csv':
            df.to_csv(session['output_file_name'], index=False)
        if file_type == 'xlsx':
            df.to_excel(session['output_file_name'], index=False)

        # Render and return the 'file_processed.html' template that is formatted ...
        # ... with the output file name and HTML of the DataFrame
        return render_template('file_processed.html',
                                filename=session['output_file_name'],
                                table=data_table_html)

    else:
        # If the request method is GET, simply return the error message
        return 'Something went wrong. Please try again!'


# Define a route for the 'file_downloaded.html' page
@app.route('/file_downloaded.html', methods=['POST', 'GET'])
def download_file():
    # Check if the request method is POST
    if request.method == 'POST':
        # If so, send the output file for downloading
        return send_file(session['output_file_name'], as_attachment=True,
                         download_name=session['output_file_name'])
    else:
        # If the request method is GET, simply return the error message
        return 'Something went wrong. Please try again!'


# Define a route for the 'example.html' page
@app.route('/example.html')
def show_example():
    # Render and return the 'example.html' template
    return render_template('example.html')


# Define a route that accepts a dynamic string parameter 'map_url'
@app.route('/<string:map_url>')
def map(map_url):
    # Render and return the HTML template corresponding to the map URL ...
    # ... provided in the route
    return render_template(map_url)



# Check if this script is being run directly (and not imported as a module)
if __name__ == '__main__':
    # Run the Flask web app with debug mode ON
    app.run(debug=True)
