# -*- coding: utf-8 -*-
import os.path

from pynwb.spec import (NWBNamespaceBuilder, export_spec,
                        NWBGroupSpec, NWBAttributeSpec, NWBDatasetSpec, NWBLinkSpec)


def main():
    # these arguments were auto-generated from your cookiecutter inputs
    ns_builder = NWBNamespaceBuilder(
        name="""ndx-dbs""",
        version="""0.1.0""",
        doc="""This extension is developed to extend NWB data standards to incorporate 
        DBS(DeepBrainStimulation) experiments.""",
        author=[
            "Hamidreza Alimohammadi ([AT]DefenseCircuitsLab)",
        ],
        contact=[
            "alimohammadi.hamidreza@gmail.com",
        ],
    )

    ns_builder.include_type('DynamicTable', namespace='hdmf-common')
    ns_builder.include_type('VectorData', namespace='hdmf-common')
    ns_builder.include_type('Device', namespace='core')
    ns_builder.include_type('LabMetaData', namespace='core')

    dbs_device = NWBGroupSpec(
        neurodata_type_def='DBSDevice',
        neurodata_type_inc='Device',
        doc='Specs of the DBS device.',
        attributes=[
            NWBAttributeSpec(
                name='synchronization',
                doc='Explain the synchronization settings if the DBS device is separately connected to '
                    'another recording system.',
                dtype='text',
                required=False
            )
        ],
        groups=[
            NWBGroupSpec(
                name='electrodes_group',
                neurodata_type_inc='DBSElectrodes',
                doc='meta info on the group of electrodes used in the DBS experiment.'
            )
        ],
        links=[
            NWBLinkSpec(
                name='endpoint_recording_device',
                target_type='Device',
                doc='endpoint recording device to which the DBS device is connected.'
            )
        ]
    )

    dbs_electrodes = NWBGroupSpec(
        neurodata_type_def='DBSElectrodes',
        neurodata_type_inc='DynamicTable',
        name='electrodes_group',
        doc='Meta information of the electrodes through which the DBS is applied to the subject.',
        datasets=[
            NWBDatasetSpec(
                name='el_id',
                neurodata_type_inc='VectorData',
                dtype='text',
                doc='Reference name of the corresponding electrode.'
            ),
            NWBDatasetSpec(
                name='polarity',
                neurodata_type_inc='VectorData',
                dtype='text',
                doc='Polarity(neg/pos) of the corresponding electrode.'
            ),
            NWBDatasetSpec(
                name='impedance',
                neurodata_type_inc='VectorData',
                dtype='text',
                doc='Impedance of the corresponding electrode.'
            ),
            NWBDatasetSpec(
                name='length',
                neurodata_type_inc='VectorData',
                dtype='text',
                doc='Length of the corresponding electrode.'
            ),
            NWBDatasetSpec(
                name='tip',
                neurodata_type_inc='VectorData',
                dtype='text',
                doc='Tip surface area information of the corresponding electrode.'
            ),
            NWBDatasetSpec(
                name='material',
                neurodata_type_inc='VectorData',
                dtype='text',
                doc='Material of the corresponding electrode.'
            ),
            NWBDatasetSpec(
                name='location',
                neurodata_type_inc='VectorData',
                dtype='text',
                doc='Implementation location of the corresponding electrode.'
            ),
            NWBDatasetSpec(
                name='comment',
                neurodata_type_inc='VectorData',
                dtype='text',
                doc='Descriptive comments on the corresponding electrode'
            ),
        ]
    )

    dbs_meta = NWBGroupSpec(
        neurodata_type_def='DBSMeta',
        neurodata_type_inc='LabMetaData',
        doc='Information on the stimulation meta data, pulse specs.',
        attributes=[
            NWBAttributeSpec(
                name='stim_state',
                doc='Describe the DBS pulse state(ON/OFF) for this specific experiment session. Field information are '
                    'to be provided based on the stim_state.',
                dtype='text',
                required=False
            ),
            NWBAttributeSpec(
                name='stim_type',
                doc='Describe the DBS stimulation type(e.g. monopolar or bipolar) for this specific '
                    'experiment session.',
                dtype='text',
                required=False
            ),
            NWBAttributeSpec(
                name='stim_area',
                doc='Describe the DBS stimulation area for this specific experiment session.',
                dtype='text',
                required=False
            ),
            NWBAttributeSpec(
                name='stim_coordinates',
                doc='Describe the DBS stimulation area based on the coordinates from ATLAS for this specific experiment'
                    ' session.',
                dtype='text',
                required=False
            ),
            NWBAttributeSpec(
                name='pulse_shape',
                doc='Describe the DBS pulse shape for this specific experiment session.',
                dtype='text',
                required=False
            ),
            NWBAttributeSpec(
                name='pulse_width',
                doc='Describe the DBS pulse width for this specific experiment session.',
                dtype='text',
                required=False
            ),
            NWBAttributeSpec(
                name='pulse_frequency',
                doc='Describe the DBS pulse frequency for this specific experiment session.',
                dtype='text',
                required=False
            ),
            NWBAttributeSpec(
                name='pulse_intensity',
                doc='Describe the DBS pulse intensity for this specific experiment session.',
                dtype='text',
                required=False
            ),
            NWBAttributeSpec(
                name='charge_balance',
                doc='Describe the charge balance of the DBS stimulus pulse for this specific experiment session.',
                dtype='text',
                required=False
            )
        ]
    )

    dbs_subject = NWBGroupSpec(
        neurodata_type_def='DBSSubject',
        neurodata_type_inc='LabMetaData',
        doc='Information on the DBS subject.',
        attributes=[
            NWBAttributeSpec(
                name='model',
                doc='Describe the non-human model of a disease, e.g., 6-OHDA PD model in rats.',
                dtype='text',
                required=False
            ),
            NWBAttributeSpec(
                name='controls',
                doc='Describe the controls group in this DBS session/trial/subject.',
                dtype='text',
                required=False
            ),
            NWBAttributeSpec(
                name='comment',
                doc='Enter human-readable comments session/trial/subject.',
                dtype='text',
                required=False
            )
        ]
    )

    dbs_group = NWBGroupSpec(
        neurodata_type_def='DBSGroup',
        neurodata_type_inc='LabMetaData',
        doc='The main group to integrate necessary components of a DBS experiment. The components are a few attributes,'
            'an instance DBSDevice and DBSMeta.',
        attributes=[
            NWBAttributeSpec(
                name='DBS_phase',
                doc='Describe the DBS phase for this specific experiment session.',
                dtype='text',
                required=False
            ),
            NWBAttributeSpec(
                name='comment',
                doc='Enter human-readable comments for this specific experiment session.',
                dtype='text',
                required=False
            )
        ],
        links=[
            NWBLinkSpec(
                name='DBS_device',
                target_type='DBSDevice',
                doc='Link to the DBSDevice as a reference for DBSElectrodes and main recording device.'
            ),
            NWBLinkSpec(
                name='DBS_meta',
                target_type='DBSMeta',
                doc='Link to the DBSMeta as a reference for stimulation meta data and pulse specs.'
            ),
            NWBLinkSpec(
                name='DBS_subject',
                target_type='DBSSubject',
                doc='Link to the DBSMeta as a reference for DBSSubject.'
            )
        ]
    )

    new_data_types = [dbs_device, dbs_electrodes, dbs_meta, dbs_subject, dbs_group]

    # export the spec to yaml files in the spec folder
    output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'spec'))
    export_spec(ns_builder, new_data_types, output_dir)
    print('Spec files generated. Please make sure to rerun `pip install .` to load the changes.')


if __name__ == '__main__':
    # usage: python create_extension_spec.py
    main()

