# Building

## Description

This entity contains a harmonised description of a Building. This entity is
associated with the vertical segments of smart homes, smart cities, industry and
related IoT applications.

This data model has been partially developed in cooperation with mobile
operators and the [GSMA](https://www.gsma.com/iot/iot-big-data/),
compared to GSMA data model following changes are introduced:

-   the reference to `BuildingType` is removed, since `BuildingType` compared to
    `category` attribute does not introduce significant information.

-   `category` attribute is required.

-   `openingHours` is introduced following schema.org data model to allow
    fine-grained on building opening times. GSMA supported this as free text in
    the `notes` attribute (removed as well).

-   `refSubscriptionService` is not supported, since `SubscriptionService` model
    is not supported currently.

## Data Model

For a full description of the following attributes refer to GSMA
[IoT Big Data Harmonised Data Model](https://github.com/GSMADeveloper/NGSI-LD-Entities)

-   `id`

-   `type`

-   `source` : A sequence of characters giving the source of the entity data.

    -   Attribute type: Text or URL
    -   Optional

-   `dataProvider` : Specifies the URL to information about the provider of this
    information

    -   Attribute type: URL
    -   Optional

-   `dateModified` : Last update timestamp of this entity.

    -   Attribute type: [DateTime](https://schema.org/DateTime)
    -   Read-Only. Automatically generated.

-   `dateCreated` : Entity's creation timestamp.

    -   Attribute type: [DateTime](https://schema.org/DateTime)
    -   Read-Only. Automatically generated.

-   `owner`

    -   Optional

-   `category`

    -   Required

-   `location`

    -   Optional.

-   `containedInPlace`

    -   Optional.

-   `address`

    -   Required

-   `description`

    -   Optional

-   `occupier`

    -   Optional

-   `floorsAboveGround`

    -   Optional

-   `floorsBelowGround`

    -   Optional

-   `refMap`
    -   Optional

The following attribute has been introduced:

-   `openingHours` : The number of floors above ground level in this building.
    -   Attribute type: List of [Opening Hours](http://schema.org/openingHours)
    -   Optional

**Note**: JSON Schemas are intended to capture the data type and associated
constraints of the different Attributes, regardless their final representation
format in NGSI(v2, LD).

## Examples

### Normalized Example

Normalized NGSI response

```json
{
    "id": "building-a85e3da145c1",
    "type": "Building",
    "category": {
        "value": ["office"]
    },
    "floorsBelowGround": {
        "value": 0
    },
    "description": {
        "value": "Office block"
    },
    "floorsAboveGround": {
        "value": 7
    },
    "occupier": {
        "type": "Relationship",
        "value": ["9830f692-7677-11e6-838b-4f9fb3dc5a4f"]
    },
    "mapUrl": {
        "type": "URL",
        "value": "http://www.example.com"
    },
    "dateCreated": {
        "type": "DateTime",
        "value": "2016-08-08T10:18:16Z"
    },
    "source": {
        "value": "http://www.example.com"
    },
    "location": {
        "type": "geo:json",
        "value": {
            "type": "Polygon",
            "coordinates": [[[100, 0], [101, 0], [101, 1], [100, 1], [100, 0]]]
        }
    },
    "address": {
        "type": "PostalAddress",
        "value": {
            "addressLocality": "London",
            "postalCode": "EC4N 8AF",
            "streetAddress": "25 Walbrook"
        }
    },
    "owner": {
        "type": "Relationship",
        "value": [
            "cdfd9cb8-ae2b-47cb-a43a-b9767ffd5c84",
            "1be9cd61-ef59-421f-a326-4b6c84411ad4"
        ]
    },
    "openingHours": {
        "value": [
            {
                "dayOfWeek": "http://schema.org/Sunday",
                "closes": "17:00:00",
                "opens": "09:00:00"
            },
            {
                "dayOfWeek": "http://schema.org/Saturday",
                "closes": "17:00:00",
                "opens": "09:00:00"
            },
            {
                "dayOfWeek": "http://schema.org/Thursday",
                "closes": "17:00:00",
                "opens": "09:00:00"
            },
            {
                "dayOfWeek": "http://schema.org/Tuesday",
                "closes": "17:00:00",
                "opens": "09:00:00"
            },
            {
                "dayOfWeek": "http://schema.org/Friday",
                "closes": "17:00:00",
                "opens": "09:00:00"
            },
            {
                "dayOfWeek": "http://schema.org/Monday",
                "closes": "17:00:00",
                "opens": "09:00:00"
            },
            {
                "dayOfWeek": "http://schema.org/Wednesday",
                "closes": "17:00:00",
                "opens": "09:00:00"
            }
        ]
    },
    "dataProvider": {
        "value": "OperatorA"
    },
    "dateModified": {
        "type": "DateTime",
        "value": "2016-08-08T10:18:16Z"
    },
    "containedInPlace": {
        "value": {
            "type": "Polygon",
            "coordinates": [[[100, 0], [101, 0], [101, 1], [100, 1], [100, 0]]]
        }
    }
}
```

### key-value pairs Example

Sample uses simplified representation for data consumers `?options=keyValues`

```json
{
    "id": "building-a85e3da145c1",
    "type": "Building",
    "dateCreated": "2016-08-08T10:18:16Z",
    "dateModified": "2016-08-08T10:18:16Z",
    "source": "http://www.example.com",
    "dataProvider": "OperatorA",
    "category": ["office"],
    "containedInPlace": {
        "type": "Polygon",
        "coordinates": [[[100, 0], [101, 0], [101, 1], [100, 1], [100, 0]]]
    },
    "location": {
        "type": "Polygon",
        "coordinates": [[[100, 0], [101, 0], [101, 1], [100, 1], [100, 0]]]
    },
    "address": {
        "addressLocality": "London",
        "postalCode": "EC4N 8AF",
        "streetAddress": "25 Walbrook"
    },
    "owner": [
        "cdfd9cb8-ae2b-47cb-a43a-b9767ffd5c84",
        "1be9cd61-ef59-421f-a326-4b6c84411ad4"
    ],
    "occupier": ["9830f692-7677-11e6-838b-4f9fb3dc5a4f"],
    "floorsAboveGround": 7,
    "floorsBelowGround": 0,
    "description": "Office block",
    "mapUrl": "http://www.example.com",
    "openingHours": [
        {
            "closes": "17:00:00",
            "dayOfWeek": "http://schema.org/Sunday",
            "opens": "09:00:00"
        },
        {
            "closes": "17:00:00",
            "dayOfWeek": "http://schema.org/Saturday",
            "opens": "09:00:00"
        },
        {
            "closes": "17:00:00",
            "dayOfWeek": "http://schema.org/Thursday",
            "opens": "09:00:00"
        },
        {
            "closes": "17:00:00",
            "dayOfWeek": "http://schema.org/Tuesday",
            "opens": "09:00:00"
        },
        {
            "closes": "17:00:00",
            "dayOfWeek": "http://schema.org/Friday",
            "opens": "09:00:00"
        },
        {
            "closes": "17:00:00",
            "dayOfWeek": "http://schema.org/Monday",
            "opens": "09:00:00"
        },
        {
            "closes": "17:00:00",
            "dayOfWeek": "http://schema.org/Wednesday",
            "opens": "09:00:00"
        }
    ]
}
```

## Test it with a real service

T.B.D.
