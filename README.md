# ndx-dbs Extension for NWB

This extension is developed to extend NWB data standards to incorporate required (meta)data for DBS experiments. `DBSGroup`, the main neurodata-type in this extension, in fact extends the `LabMetaData` which itself extends the NWBContainer base type and incorporates data types of `DBSMeta`(as an extension of LabMetaData), `DBSSubject`(as an extension of LabMetaData) and `DBSDevice`(as an extension of Device) which itself includes `DBSElectrodes`(as an extension of DynamicTable). Instances of these data types are interlinked to each other to account for the comprehensiveness of all the required meta(data) in a general experiment including DBS.

