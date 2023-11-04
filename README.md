# electrophysiology probe specifications

This readme describes specifications for describing electrophysiology **probes** and **probe insertions** as well as standard formats for sharing **anatomical data** about a probe insertion. These formats are intended for use in visualization software and for sharing data between applications.

The individual folders in this repository contain the relevant files for the probes used in [Pinpoint](https://github.com/virtualBrainLab/pinpoint) and examples of the insertion and anatomical data files. 

## Probe

A probe is a 3D object with one or more shanks which each have electrode sites on them.

File | Description
---|---
metadata.json | probe metadata, in JSON format
model.obj | 3D model of the probe shanks and any attached silicon, the tip of the reference shank is at the origin
hardware.obj | (optional) 3D model of additional hardware attached to the probe, replace "hardware" with the name of (e.g. "Sensapex_probe_holder")
channel_map.csv | coordinates of electrode surface relative to the tip and selection layers

### metadata.json

Field | Type | Example
---|---|---
name | string | Neuropixels 1.0
type | int | 1
producer | string | imec
channels | int | 960
shanks | int | 1
reference-shank | int | 0
hardware-files | list of string | ["hardware", "holder"]

Example for Neuropixels 1.0:

```
{
  "name":"Neuropixels 1.0",
  "type":"1"
  "producer":"imec",
  "channels":"960",
  "shanks":"1",
  "reference-shank":"0",
  "hardware-files": ["hardware", "sensapex_holder", "new_scale_holder"],
}
```

### model.obj

3D model of the probe with the surface of the tip at the origin.

#### hardware.obj

Additional 3D model files can be included. For example, you may want a 3D model for the circuit boards that are often attached to the actual probe shanks, or for the parts that connect the probe to a micro-manipulator. 

### channel_map.csv

Fields: index, x, y, z, w, h, d, default, layer1, layer2, ...

Example for Neuropixels 1.0:

| index     | x   | y   | z | w  | h  | d  | default | all | bank0 | double_length |
|-----------|-----|-----|---|----|----|----|---------|-----|-------|---------------|
| 0         | -14 | 200 | 0 | 12 | 12 | 24 | 1       | 1   | 1     | 0             |
| 1         | 18  | 200 | 0 | 12 | 12 | 24 | 1       | 1   | 1     | 1             |
| 2         | -30 | 220 | 0 | 12 | 12 | 24 | 1       | 1   | 1     | 0             |
| 3         | 2   | 220 | 0 | 12 | 12 | 24 | 1       | 1   | 1     | 1             |

## Probe Insertion

A probe insertion describes the position of the tip of a probe and its angles within a reference atlas. The (ap, ml, dv) coordinates and positive directions will be relative to the calibration coordinate and axes defined by the reference-atlas and atlas-transform. A (yaw, pitch, roll) of (0,0,0) is a probe pointing down (ventral) with its electrode sites facing forward (anterior). Positive yaw rotates clockwise, positive pitch brings the probe up toward horizontal, and positive roll rotates clockwise. A blank atlas-transform means the insertion is defined the reference atlas space.

Example shown is the IBL repeated site.

Field | Type | Example
---|---|---
AP | float (mm) | 2.000
ML | float (mm) | 2.243
DV | float (mm) | -2.92
Yaw | float (deg) | -90
Pitch | float (deg) | 15
Roll | float (deg) | 0
AtlasName | string | CCF
TransformName | string | Qiu2018
RefAP | float (mm) | 5.200
RefML | float (mm) | 5.700
RefDV | float (mm) | 0.330

Example

```
{
  "AP":"2.000",
  "ML":"2.243",
  "Dv":"-2.92",
  "Yaw":"Neuropixels 1.0",
  "Pitch":"imec",
  "Roll":"960",
  "ReferenceAtlasName":"CCF",
  "AtlasTransformName":"Qiu2018"
}
```

Note that the (AP, ML, DV) tip coordinate is relative to to the reference, so to reconstruct the coordinate in raw CCF space you need to add the reference coordinate to the un-transformed (AP, ML , DV) position. 

## Atlas

A reference atlas is an annotated representation of a brain. We don't define a schema for atlas information but instead rely on the BrainGlobe Atlas API. For more information, see github.com/virtualBrainLab/brainAtlas/ or https://github.com/brainglobe/bg-atlasapi 

The following atlases are defined in Pinpoint

Name | Prefix | Resolution(s) | Species - strain | Reference
---|---|---|---|---
CCF | ccf | 25 | Mouse - C57BL/6J | Wang et al. 2020
Waxholm | wxh | 39, 78 | Rat - Sprague Dawley | Papp et al. 2014

## Atlas Transform

An atlas transform defines an Affine Transformation or Nonlinear Deformation Field. 

### Affine Transform

Affine transformations are applied as an Euler rotation (Yaw, then Pitch, then Roll) around Bregma followed by scaling and axis inversion (if needed). The scaling values go from the Atlas to the Transform.

Field | Type | Description
---|---|---
Yaw | float (deg) | Clockwise rotation around DV axis
Pitch | float (deg) | Clockwise rotation around ML axis
Roll | float (deg) | Clockwise rotation around AP axis
ScaleAP | float | Change in scale on AP
ScaleML | float | Change in scale on ML
ScaleDV | float | Change in scale on DV
SignAP | int | Axis direction for AP (relative to Atlas)
SignML | int | Axis direction for ML (relative to Atlas)
SignDV | int | Axis direction for DV (relative to Atlas)
Name | string | Name

Example

```
{
  "Name":"Qiu2018",
  "Yaw":"0",
  "Pitch":"-5",
  "Roll":"0",
  "ScaleAP":"1.031",
  "ScaleML":"0.952",
  "ScaleDV":"0.885",
  "SignAP":"-1",
  "SignML":"1",
  "SignDV":"-1"
}
```

### Non-Linear Deformation Field

todo

## Rig Object

Rig objects are 3D models that can be placed in the scene. Their origin should be relative to the Reference coordinate.

File | Description
---|---
model.obj | 3D model of the rig object, the origin will be placed at the active reference coordinate

## Scene

A scene is a JSON object that contains string references to the names of the active Atlas and rig objects, as well as serialized JSON copies of the probe insertions, atlas transform, and any other metadata (e.g. Settings).

Field | Type | Description
---|---|---
AtlasName | string | Name of active atlas
AtlasTransform | string | AtlasTransform JSON
Data | Array of {"type":"jsondata"} | Other data about the scene

### Data Types

Data can include "probes", "settings", and anything else that is needed to reconstruct a scene representation.

## Anatomical data API

An anatomical data message is a string for communicating between applications that support per-channel anatomical data. Multiple probes can be sent in one string as an array `"[probe-string-0,probe-string1,...]"`

### Uncompressed format

The uncompressed format sends data for every channel as a single string, with the format:

`"probe-name;channel-data"`

Where the channel-data string has the format:

`"index,acronym,hex-color;..."`

For example:

```
"ProbeA;0,ACAv,40A666;1,ACAv,40A666;...;958,-,000000;959,-,000000"
```

### Compressed format

Channels with identical acronyms are compressed, using the first format "indexFirst-indexLast"

```
"ProbeA;0-27,ACAv,40A666;28-77,ACAd,40A666;78-175,-,000000;176-959,-,000000"
```
