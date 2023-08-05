# probe-format

This readme describes specifications for describing electrophysiology **probes** and **probe insertions** as well as standard formats for sharing **anatomical data** about a probe insertion.

The individual folders in this repository contain the relevant files for the probes used in [Pinpoint](https://github.com/virtualBrainLab/pinpoint).

## Probe

A probe is a 3D object, usually shaped like a needle, with one or more shanks which each have electrode sites on them.

File | Description
---|---
probe.json | probe metadata, in JSON format
probe_model.obj | 3D model of the probe shanks and any attached silicon, the tip of the reference shank is at the origin
probe_hardware.obj | (optional) 3D model of additional hardware attached to the probe, replace "hardware" with the name of (e.g. "Sensapex_probe_holder")
probe_channel_map.csv | coordinates of electrode surface relative to the tip and selection layers

### probe.json

Field | Type | Example
---|---|---
name | string | Neuropixels 1.0
producer | string | imec
channels | int | 960
shanks | int | 1
reference-shank | int | 0

Example for Neuropixels 1.0:

```
{
  "name":"Neuropixels 1.0",
  "producer":"imec",
  "channels":"960",
  "shanks":"1",
  "reference-shank":"0"
}
```

### probe_model.obj

3D model of the probe with the tip at the origin. If the probe has depth, the origin should be placed at the surface of the probe.

### probe_channel_map.csv

Fields: index, x, y, z, w, h, d, default, layer1, layer2, ...

Example for Neuropixels 1.0:

| index     | x   | y   | z | w  | h  | d  | default | all | bank0 | double_length |
|-----------|-----|-----|---|----|----|----|---------|-----|-------|---------------|
| 0         | -14 | 200 | 0 | 12 | 12 | 24 | 1       | 1   | 1     | 0             |
| 1         | 18  | 200 | 0 | 12 | 12 | 24 | 1       | 1   | 1     | 1             |
| 2         | -30 | 220 | 0 | 12 | 12 | 24 | 1       | 1   | 1     | 0             |
| 3         | 2   | 220 | 0 | 12 | 12 | 24 | 1       | 1   | 1     | 1             |

## Probe Insertion

A probe insertion describes the position of the tip of a probe and its angles within a reference atlas. The (ap, ml, dv) coordinates will be relative to the calibration coordinate in the reference-atlas and atlas-transform. A (yaw, pitch, roll) of (0,0,0) is a probe pointing down (ventral) with its electrode sites facing forward (anterior). 

Example shown is the IBL repeated site.

Field | Type | Example
---|---|---
ap | float (um) | 2000
ml | float (um) | 2243
dv | float (um) | 960
yaw | float (deg) | 1
pitch | float (deg) | 15
roll | float (deg) | 0
reference-atlas | string | CCF
atlas-transform | string | Qiu2018

## Anatomical data API

An anatomical data message is a string for communicating between applications that support per-channel anatomical data.

File | Description
---|---
probe.json | probe metadata, in JSON format
probe_model.obj | 3D model of the probe shanks and any attached silicon, the tip of the reference shank is at the origin
probe_hardware.obj | (optional) 3D model of the additional hardware
probe_channel_map.csv | coordinates of electrode surface relative to the tip and selection layers

### Uncompressed format

The uncompressed format sends data for every channel as a single string, with the format:

"probe-name;channel-data"

Where the channel-data string has the format:

"index,acronym,hex-color;..."

For example:

"ProbeA;0,ACAv,40A666;1,ACAv,40A666;...;958,-,000000;959,-,000000"

### Compressed format

Channels with identical acronyms are compressed, using the first format "indexFirst-indexLast"

"ProbeA;0-27,ACAv,40A666;28-77,ACAd,40A666;78-175,-,000000;176-959,-,000000"
