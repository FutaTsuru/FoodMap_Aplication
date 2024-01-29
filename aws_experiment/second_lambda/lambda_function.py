import json
import boto3
import pandas as pd
from io import StringIO

def lambda_handler(event, context):
    bucket = 'gps-bucket'
    s3 = boto3.client('s3')
    key = 'gps_info.csv'
    obj = s3.get_object(Bucket=bucket, Key=key)
    data = obj['Body'].read().decode('utf-8')
    gps_info_df = pd.read_csv(StringIO(data))
    current_latitude = gps_info_df[len(gps_info_df) - 1 : len(gps_info_df)]["latitude"].to_list()[0]
    current_longtitude = gps_info_df[len(gps_info_df) - 1 : len(gps_info_df)]["longtitude"].to_list()[0]
    
    key = "nearest_store_df.csv"
    obj = s3.get_object(Bucket=bucket, Key=key)
    data = obj['Body'].read().decode('utf-8')
    nearest_store_df = pd.read_csv(StringIO(data))
    near_store_latitude_list = nearest_store_df["latitude"].to_list()
    near_store_longtitude_list = nearest_store_df["longtitude"].to_list()
    near_store_name_list = nearest_store_df["name"].to_list()
    near_store_kind_list = nearest_store_df["kind"].to_list()
    near_store_image_list = nearest_store_df["image_url"].to_list()
    near_store_url_list = nearest_store_df["url"].to_list()
    
    key = "recommend_store_df.csv"
    obj = s3.get_object(Bucket=bucket, Key=key)
    data = obj['Body'].read().decode('utf-8')
    recommend_store_df = pd.read_csv(StringIO(data))
    recommend_store_latitude_list = recommend_store_df["latitude"].to_list()
    recommend_store_longtitude_list = recommend_store_df["longtitude"].to_list()
    recommend_store_name_list = recommend_store_df["name"].to_list()
    recommend_store_kind_list = recommend_store_df["kind"].to_list()
    recommend_store_image_list = recommend_store_df["image_url"].to_list()
    recommend_store_url_list = recommend_store_df["url"].to_list()

    
    html = f"""
    <html>
    <head>
    <meta http-equiv="content-type" charset="UTF-8">
    <link href="https://unpkg.com/maplibre-gl@3.x/dist/maplibre-gl.css" rel="stylesheet" />
    <style>
    body {{ margin: 0; }}
    #map {{ height: 100vh; }}
    </style>
    </head>
    <body>
    <div id="map" />
    <script src="https://unpkg.com/maplibre-gl@3.x/dist/maplibre-gl.js"></script>
    <script>
    const apiKey = "v1.public.eyJqdGkiOiI2ODk1OGZhYy03OTgwLTQ4MDItYjEyOS1hNDNjNGFhYzE5YzUifYDvEyWQg3mBburBrbZceh0gBb8tEZIxLbqL3ebDbe10XZWyLJLngSBdfkcL7yPZDwv9tYXcD3B60AIE0p_pHSTfMIDr_SEzxq66ldBFDkXIRlV0uxluMen9ZIk8XuMtjGLkVhS7Jk0uZvmTXQjT0uvQSP6EHsW5poR2zhFr8wUlFBpeeyzbiVvSWGAb_lEAJH5Cbba3zZB-2c6ewPENa7Jzl7bgqHh_7TrCSevW-Fe0cpaz2Y_VYFVGZzlz4Dw35jzzOZ8n7Z17gYfvd0uxfe4WuSSgPy8zdn-T5iH8msVbOmz1Y2WFVTV3zpr3nRuSl_b0r292TqJ-l1XpfebYmAA.ZWU0ZWIzMTktMWRhNi00Mzg0LTllMzYtNzlmMDU3MjRmYTkx";
    const mapName = "map_test";
    const region = "us-east-1";
    const map = new maplibregl.Map({{
    container: "map",
    style: `https://maps.geo.${{region}}.amazonaws.com/maps/v0/maps/${{mapName}}/style-descriptor?key=${{apiKey}}`,
    center: [{current_longtitude}, {current_latitude}],
    zoom: 17,
    }});
    map.once('styledata', function() {{
    for (layer of map.style.stylesheet.layers) {{
    if(map.style._serializedLayers[layer.id].layout &&
    map.style._serializedLayers[layer.id].layout['text-field']){{
    map.setLayoutProperty(layer.id, 'text-field', '{{_name_ja}}');
    }}
    }}
    }});
    map.addControl(new maplibregl.NavigationControl(), "top-left");
    var popup = new maplibregl.Popup().setHTML('<h2>現在地</h2>');
    current_location_marker = new maplibregl.Marker({{
    color: '#ff0000',
    scale: 1.5
    }}).setLngLat([{current_longtitude}, {current_latitude}]).setPopup(popup).addTo(map);
    near_marker_0 = new maplibregl.Marker({{color: '#ee82ee'}}).setLngLat([{near_store_longtitude_list[0]}, {near_store_latitude_list[0]}]).setPopup(new maplibregl.Popup({{offset: 0,}}).setHTML('<html>近くの飲食店<p><h2>{near_store_name_list[0]}</h2></p><p><{near_store_kind_list[0]}></p><p><a href={near_store_url_list[0]}>{near_store_url_list[0]}</a></p><p><img src="{near_store_image_list[0]}" alt="show image" width="300" height="200"></p></html>')).addTo(map);
    near_marker_1 = new maplibregl.Marker({{color: '#ee82ee'}}).setLngLat([{near_store_longtitude_list[1]}, {near_store_latitude_list[1]}]).setPopup(new maplibregl.Popup({{offset: 0,}}).setHTML('<html>近くの飲食店<p><h2>{near_store_name_list[1]}</h2></p><p><{near_store_kind_list[1]}></p><p><a href={near_store_url_list[1]}>{near_store_url_list[1]}</a></p><p><img src="{near_store_image_list[1]}" alt="show image" width="300" height="200"></p></html>')).addTo(map);
    near_marker_2 = new maplibregl.Marker({{color: '#ee82ee'}}).setLngLat([{near_store_longtitude_list[2]}, {near_store_latitude_list[2]}]).setPopup(new maplibregl.Popup({{offset: 0,}}).setHTML('<html>近くの飲食店<p><h2>{near_store_name_list[2]}</h2></p><p><{near_store_kind_list[2]}></p><p><a href={near_store_url_list[2]}>{near_store_url_list[2]}</a></p><p><img src="{near_store_image_list[2]}" alt="show image" width="300" height="200"></p></html>')).addTo(map);
    near_marker_3 = new maplibregl.Marker({{color: '#ee82ee'}}).setLngLat([{near_store_longtitude_list[3]}, {near_store_latitude_list[3]}]).setPopup(new maplibregl.Popup({{offset: 0,}}).setHTML('<html>近くの飲食店<p><h2>{near_store_name_list[3]}</h2></p><p><{near_store_kind_list[3]}></p><p><a href={near_store_url_list[3]}>{near_store_url_list[3]}</a></p><p><img src="{near_store_image_list[3]}" alt="show image" width="300" height="200"></p></html>')).addTo(map);
    near_marker_4 = new maplibregl.Marker({{color: '#ee82ee'}}).setLngLat([{near_store_longtitude_list[4]}, {near_store_latitude_list[4]}]).setPopup(new maplibregl.Popup({{offset: 0,}}).setHTML('<html>近くの飲食店<p><h2>{near_store_name_list[4]}</h2></p><p><{near_store_kind_list[4]}></p><p><a href={near_store_url_list[4]}>{near_store_url_list[4]}</a></p><p><img src="{near_store_image_list[4]}" alt="show image" width="300" height="200"></p></html>')).addTo(map);
    recommend_marker_0 = new maplibregl.Marker({{color: '#0000ff'}}).setLngLat([{recommend_store_longtitude_list[0]}, {recommend_store_latitude_list[0]}]).setPopup(new maplibregl.Popup({{offset: 0,}}).setHTML('<html>あなたにおすすめな飲食店<p><h2>{recommend_store_name_list[0]}</h2></p><p><{recommend_store_kind_list[0]}></p><p><a href={recommend_store_url_list[0]}>{recommend_store_url_list[0]}</a></p><p><img src="{recommend_store_image_list[0]}" alt="show image" width="300" height="200"></p></html>')).addTo(map);
    recommend_marker_1 = new maplibregl.Marker({{color: '#0000ff'}}).setLngLat([{recommend_store_longtitude_list[1]}, {recommend_store_latitude_list[1]}]).setPopup(new maplibregl.Popup({{offset: 0,}}).setHTML('<html>あなたにおすすめな飲食店<p><h2>{recommend_store_name_list[1]}</h2></p><p><{recommend_store_kind_list[1]}></p><p><a href={recommend_store_url_list[1]}>{recommend_store_url_list[1]}</a></p><p><img src="{recommend_store_image_list[1]}" alt="show image" width="300" height="200"></p></html>')).addTo(map);
    recommend_marker_2 = new maplibregl.Marker({{color: '#0000ff'}}).setLngLat([{recommend_store_longtitude_list[2]}, {recommend_store_latitude_list[2]}]).setPopup(new maplibregl.Popup({{offset: 0,}}).setHTML('<html>あなたにおすすめな飲食店<p><h2>{recommend_store_name_list[2]}</h2></p><p><{recommend_store_kind_list[2]}></p><p><a href={recommend_store_url_list[2]}>{recommend_store_url_list[2]}</a></p><p><img src="{recommend_store_image_list[2]}" alt="show image" width="300" height="200"></p></html>')).addTo(map);
    recommend_marker_3 = new maplibregl.Marker({{color: '#0000ff'}}).setLngLat([{recommend_store_longtitude_list[3]}, {recommend_store_latitude_list[3]}]).setPopup(new maplibregl.Popup({{offset: 0,}}).setHTML('<html>あなたにおすすめな飲食店<p><h2>{recommend_store_name_list[3]}</h2></p><p><{recommend_store_kind_list[3]}></p><p><a href={recommend_store_url_list[3]}>{recommend_store_url_list[3]}</a></p><p><img src="{recommend_store_image_list[3]}" alt="show image" width="300" height="200"></p></html>')).addTo(map);
    recommend_marker_4 = new maplibregl.Marker({{color: '#0000ff'}}).setLngLat([{recommend_store_longtitude_list[4]}, {recommend_store_latitude_list[4]}]).setPopup(new maplibregl.Popup({{offset: 0,}}).setHTML('<html>あなたにおすすめな飲食店<p><h2>{recommend_store_name_list[4]}</h2></p><p><{recommend_store_kind_list[4]}></p><p><a href={recommend_store_url_list[4]}>{recommend_store_url_list[4]}</a></p><p><img src="{recommend_store_image_list[4]}" alt="show image" width="300" height="200"></p></html>')).addTo(map);
    const params = {{
    CalculatorName: 'TestRoute',
    DeparturePosition: [{current_longtitude}, {current_latitude}],
    DestinationPosition: [{recommend_store_longtitude_list[0]}, {recommend_store_latitude_list[0]}],
    IncludeLegGeometry: true,
    DepartNow: true,
    TravelMode: Walk
    }};
    client.calculateRoute(params, (err, data) => {{
    const routes = data.Legs[0].Geometry.LineString
    // ルートデータ表示
    map.on('load', function () {{
    // ライン設定
    map.addSource('route_sample', {{
    'type': 'geojson',
    'data': {{
    'type': 'Feature',
    'properties': {{}},
    'geometry': {{
    'type': 'LineString',
    'coordinates': routes
    }}
    }}
    }});
    }}
    map.addLayer({{
    'id': 'route_sample',
    'type': 'line',
    'source': 'route_sample',
    'layout': {{
    'line-join': 'round',
    'line-cap': 'round'
    }},
    'paint': {{
    'line-color': '#FF0000',
    'line-width': 10,
    'line-opacity': 0.5
    }}
    }});
    }});
    </script>
    </body>
    </html>
    """
    return html