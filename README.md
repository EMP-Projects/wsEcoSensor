# wsEcoSensor

Web Service to read EcoSensor air quality data for certain geographical coordinates.

## How to use

```bash
curl --location 'http://127.0.0.1:8000/air-quality/40.7896/16.9247'
```

```json
{
    "layer": {
        "regionName": "Puglia",
        "regionCode": 16,
        "provName": "Bari",
        "provCode": 72,
        "cityCode": 72021,
        "cityName": "Gioia del Colle",
        "typeMonitoringData": 0,
        "id": 1,
        "entityKey": "cd616122-fba1-429d-8e96-f25b605b3714"
    },
    "location": {
        "Label": "Via Federico II di Svevia, 70023, Gioia del Colle, Bari, ITA",
        "Geometry": {
            "Point": [
                16.925687304198,
                40.78976397905
            ]
        },
        "Municipality": "Gioia del Colle",
        "SubRegion": "Bari",
        "Region": "Puglia",
        "Country": "ITA",
        "PostalCode": "70023",
        "Interpolated": false,
        "Categories": [
            "StreetType"
        ]
    },
    "data": [
        {
            "Lat": 0.0,
            "Lng": 0.0,
            "Value": 158.0,
            "Unit": "μg/m³",
            "Date": "2024-10-04T18:00:00Z",
            "Elevation": 331.0,
            "EuropeanAqi": 30,
            "PollutionText": "Monossido di carbonio",
            "SourceText": "OpenMeteo Api",
            "Source": 0,
            "Pollution": 0,
            "GisId": 12,
            "Color": "",
            "TypeMonitoringData": 0,
            "Id": 1389,
            "TimeStamp": "0001-01-01T00:00:00"
        },
        {
            "Lat": 0.0,
            "Lng": 0.0,
            "Value": 4.5,
            "Unit": "μg/m³",
            "Date": "2024-10-04T18:00:00Z",
            "Elevation": 331.0,
            "EuropeanAqi": 2,
            "PollutionText": "Diossido di azoto",
            "SourceText": "OpenMeteo Api",
            "Source": 0,
            "Pollution": 1,
            "GisId": 12,
            "Color": "#47EEE0",
            "TypeMonitoringData": 0,
            "Id": 1437,
            "TimeStamp": "0001-01-01T00:00:00"
        },
        {
            "Lat": 0.0,
            "Lng": 0.0,
            "Value": 74.0,
            "Unit": "μg/m³",
            "Date": "2024-10-04T18:00:00Z",
            "Elevation": 331.0,
            "EuropeanAqi": 30,
            "PollutionText": "Ozono",
            "SourceText": "OpenMeteo Api",
            "Source": 0,
            "Pollution": 3,
            "GisId": 12,
            "Color": "#47EEE0",
            "TypeMonitoringData": 0,
            "Id": 1413,
            "TimeStamp": "0001-01-01T00:00:00"
        },
        {
            "Lat": 0.0,
            "Lng": 0.0,
            "Value": 7.2,
            "Unit": "μg/m³",
            "Date": "2024-10-04T18:00:00Z",
            "Elevation": 331.0,
            "EuropeanAqi": 10,
            "PollutionText": "Particelle sull'aria (PM10)",
            "SourceText": "OpenMeteo Api",
            "Source": 0,
            "Pollution": 4,
            "GisId": 12,
            "Color": "#47EEE0",
            "TypeMonitoringData": 0,
            "Id": 1341,
            "TimeStamp": "0001-01-01T00:00:00"
        },
        {
            "Lat": 0.0,
            "Lng": 0.0,
            "Value": 4.0,
            "Unit": "μg/m³",
            "Date": "2024-10-04T18:00:00Z",
            "Elevation": 331.0,
            "EuropeanAqi": 10,
            "PollutionText": "Particelle sull'aria (PM2.5)",
            "SourceText": "OpenMeteo Api",
            "Source": 0,
            "Pollution": 5,
            "GisId": 12,
            "Color": "#47EEE0",
            "TypeMonitoringData": 0,
            "Id": 1365,
            "TimeStamp": "0001-01-01T00:00:00"
        }
    ]
}
```