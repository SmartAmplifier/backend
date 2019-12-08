# backend

[![Build Status](https://travis-ci.org/SmartAmplifier/backend.svg?branch=master)](https://travis-ci.org/SmartAmplifier/backend)

## Register new amplifier
Type: `POST`

    /register/new/amplifier

body:
```
{
    "amplifier": <amplifier-id>
}
```

## Pair new amplifier
Type: `POST`

    /pair/new/amplifier

body:
```
{
    "amplifier": <amplifier-id>,
    "email": <email-to-pair-with>
}
```

## Change volume by id
Type: `POST`

    /change/volume/by/id

body:
```
{
    "amplifier": <amplifier-id>,
    "volume": <volume>
}
```

## Change volume by email
Type: `POST`

    /change/volume/by/email

body:
```
{
    "email": <paired-email>
    "volume": <volume>
}
```

## Get paired amplifier
Type: `GET`

    /get/paired/amplifier/<email>

Response:
```
{
    "amplifier": <amplifier-id>
}
```

## Get volume by id
Type: `GET`

    /get/volume/by/id/<id>

Response:
```
{
    "volume": <volume>
}
```

## Get volume by email
Type: `GET`

    /get/volume/by/email/<email>

Response:
```
{
    "volume": <volume>
}
```