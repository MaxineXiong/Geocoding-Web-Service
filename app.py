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


app = Flask(__name__)
app.secret_key = secrets.token_hex()

ArcGIS().timeout = 1000

@app.route('/')
def home():
    for temporary_csv_file in glob.glob('*.csv'):
        os.remove(temporary_csv_file)

    for temporary_excel_file in glob.glob('*.xlsx'):
        os.remove(temporary_excel_file)

    for temporary_map_file in glob.glob('./templates/map_*.html'):
        os.remove(temporary_map_file)

    session['output_file_name'] = None

    return render_template('index.html')


@app.route('/file_processed.html', methods=['POST', 'GET'])
def process_file():
    if request.method == 'POST':
        input_file = request.files['uploaded_file']

        temporary_file_name = secure_filename('uploaded_{}'.format(input_file.filename))
        input_file.save(temporary_file_name)

        file_type = None
        if input_file.filename[-4:] == '.csv':
            file_type = 'csv'
            df = pd.read_csv(temporary_file_name)
        if input_file.filename[-5:] == '.xlsx':
            file_type = 'xlsx'
            df = pd.read_excel(temporary_file_name, sheet_name=0)

        cols = df.columns

        if not any('address' in col.lower() for col in cols):
            return render_template('invalid_file_uploaded.html')

        for col in cols:
            if 'address' in col.lower():
                lat_col = col + '_latitude'
                lon_col = col + '_longitude'
                map_col = col + '_map'
                df[lat_col] = df[col].apply(lambda x: ArcGIS().geocode(x).latitude \
                                            if ArcGIS().geocode(x) else None)
                df[lon_col] = df[col].apply(lambda x: ArcGIS().geocode(x).longitude \
                                            if ArcGIS().geocode(x) else None)

                full_map = folium.Map(
                                location=(df.iloc[0][lat_col], df.iloc[0][lon_col]),
                                zoom_start=15, tiles='openstreetmap',
                                control_scale=True
                                      )
                fg = folium.FeatureGroup(name='all_points')
                for row_index in range(len(df)):
                    row = df.iloc[row_index]
                    lat = row[lat_col]
                    lon = row[lon_col]
                    if (not math.isnan(lat)) and (not math.isnan(lon)):
                        marker = folium.Marker(
                                       location=(lat, lon),
                                       popup=folium.Popup(row[col], parse_html=True),
                                       icon=folium.Icon(color='blue')
                                                )
                        fg.add_child(marker)

                full_map.add_child(fg)

                list_map_url = []
                for row_index in range(len(df)):
                    row = df.iloc[row_index]
                    lat = row[lat_col]
                    lon = row[lon_col]
                    if (not math.isnan(lat)) and (not math.isnan(lon)):
                        full_map.location = [lat, lon]

                        map_url = 'map_{}_lat={}_lon={}.html'  \
                                  .format(col.replace(' ', '_'), lat, lon)

                        full_map.save('./templates/'+map_url)

                        list_map_url.append(map_url)
                    else:
                        list_map_url.append(None)

                df[map_col] = list_map_url

        df.rename(columns={'Unnamed: 0': ''}, inplace=True)

        data_table_html = df.to_html(index=False)   \
                            .replace('<thead>', '<thead class="thead">') \
                            .replace('<tbody>', '<tbody class="tbody">')

        data_table_html = re.sub(r'<td>(map_\S+_lat=[-\d\.]+_lon=[-\d\.]+\.html)</td>',
                            r"<td><a target='_blank' href='/\1'>Show on Map</a></td>",
                            data_table_html)

        map_cols = [col for col in df.columns if '_map' in col]
        df.drop(map_cols, axis=1, inplace=True)

        session['output_file_name'] = 'geocoded_' + input_file.filename
        if file_type == 'csv':
            df.to_csv(session['output_file_name'], index=False)
        if file_type == 'xlsx':
            df.to_excel(session['output_file_name'], index=False)

        return render_template('file_processed.html',
                                filename=session['output_file_name'],
                                table=data_table_html)
    else:
        return 'Something went wrong. Please try again!'


@app.route('/file_downloaded.html', methods=['POST', 'GET'])
def download_file():
    if request.method == 'POST':
        return send_file(session['output_file_name'], as_attachment=True,
                         download_name=session['output_file_name'])
    else:
        return 'Something went wrong. Please try again!'


@app.route('/example.html')
def show_example():
    return render_template('example.html')


@app.route('/<string:map_url>')
def map(map_url):
    return render_template(map_url)



if __name__ == '__main__':
    app.run(debug=True)
