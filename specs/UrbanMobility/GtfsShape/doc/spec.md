# GtfsShape

## Description

See
[https://developers.google.com/transit/gtfs/reference/#shapestxt](https://developers.google.com/transit/gtfs/reference/#shapestxt)

It represents a GTFS `shape`.

## Data Model

The data model is defined as shown below:

-   `id`: Entity ID

    -   It shall be `urn:ngsi-ld:GtfsShape:<shape_identifier>` being
        `shape_identifier` a value that can derived from the GTFS `shape_id`
        field.

-   `type`: Entity Type

    -   It shall be equal to `GtfsShape`

- `source` : A sequence of characters giving the source of the entity data.

    -   Attribute type: Text or URL
    -   Optional

- `dataProvider` : Specifies the URL to information about the provider of this information

    -   Attribute type: URL
    -   Optional

-   `dateCreated` : Entity's creation timestamp.

    -   Attribute type: [DateTime](https://schema.org/DateTime)
    -   Read-Only. Automatically generated.

-   `dateModified` : Last update timestamp of this Entity.

    -   Attribute type: [DateTime](https://schema.org/DateTime)
    -   Read-Only. Automatically generated.

-   `location`: The geographical shape associated to this entity encoded as GeoJSON
    `LineString` or `MultiLineString`. The coordinates shall be obtained from
    the `shapes.txt` feed file as per the value of `shape_id`, `shape_pt_lat`, `shape_pt_lon`, `shape_pt_sequence`.
    
    -   Attribute type: GeoProperty. `geo:json`
    -   Optional

### Example 1 (Normalized Format)

```json
{
    "id": "urn:ngsi-ld:GtfsShape:S234",
    "type": "GtfsShape",
    "location": {
        "type": "geo:json",
        "value": {
            "type": "LineString",
            "coordinates": [
                [-4.421394, 36.73826],
                [-4.421428, 36.73825],
                [-4.421505, 36.738186],
                [-4.421525, 36.738033]
            ]
        }
    }
}
```

### Example 2 (?options=keyValues simplified representation for data consumers)

```json
{
    "id": "urn:ngsi-ld:GtfsShape:S234",
    "type": "GtfsShape",
    "location": {
        "type": "LineString",
        "coordinates": [
            [-4.421394, 36.73826],
            [-4.421428, 36.73825],
            [-4.421505, 36.738186],
            [-4.421525, 36.738033]
        ]
    }
}
```

## Summary of mappings to GTFS

### Properties

| GTFS Field            | NGSI Attribute         | LinkedGTFS                  | Comment                                                  |
| :-------------------- | :--------------------- | :-------------------------- | :------------------------------------------------------- |
| `shape_pt_lat`        | `location`             | `geo:lat`                   | Latitude of points.                                      |
| `shape_pt_lon`        | `location`             | `geo:long`                  | Longitude of points.                                     |
| `shape_pt_sequence`   | `location`             | `gtfs:pointSequence`        | Sequence of points.                                      |

### Relationships

| GTFS Field       | NGSI Attribute     | LinkedGTFS           | Comment                                              |
| :--------------- | :----------------- | :------------------- | :--------------------------------------------------- |


## Open issues