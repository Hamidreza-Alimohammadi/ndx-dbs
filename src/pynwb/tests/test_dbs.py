from pynwb.testing import TestCase, remove_test_file

from pynwb import NWBHDF5IO, NWBFile
from datetime import datetime
from uuid import uuid4
import numpy as np
from dateutil.tz import tzlocal
from hdmf.common import DynamicTable

from ndx_dbs import (
    DBSDevice,
    DBSElectrodes,
    DBSMeta,
    DBSSubject,
    DBSGroup
)


def set_up_nwbfile(nwbfile: NWBFile = None):

    nwbfile = NWBFile(
        session_description='DBS mock session',
        identifier=str(uuid4()),
        session_start_time=datetime.now(tzlocal()),
        experimenter='experimenter',
        lab='ChiWangLab',
        institution='UKW',
        experiment_description='',
        session_id='',
    )

    # define an endpoint main recording device
    nwbfile.create_device(
        name='endpoint_recording_device',
        description='description_of_the_ERD',  # ERD: Endpoint recording device
        manufacturer='manufacturer_of_the_ERD'
    )

    return nwbfile


class TestDBSRoundtrip(TestCase):

    def setUp(self):
        self.nwbfile = set_up_nwbfile()
        self.path = "test.nwb"

    def tearDown(self):
        remove_test_file(self.path)

    def test_roundtrip(self):

        # creating an DBS electrodes table as a DynamicTable
        dbs_electrodes_table = DBSElectrodes(
            description='descriptive meta-data on DBS stimulus electrodes'
        )

        # add electrodes
        dbs_electrodes_table.add_row(
            el_id='el_0',
            polarity='negative electrode (stimulation electrode, cathode)',
            impedance='0.8 MOhm',
            length='X cm',
            tip='tip surface ~ XX micrometer sq',
            material='platinum/iridium',
            location='STN',
            comment='none',
        )
        dbs_electrodes_table.add_row(
            el_id='el_1',
            polarity='positive electrode (reference electrode, anode)',
            impedance='1 MOhm',
            length='Y cm',
            tip='tip surface ~ YY micrometer sq',
            material='platinum/iridium',
            location='scalp surface',
            comment='distance D from el_0',
        )
        # adding the object of DynamicTable
        self.nwbfile.add_acquisition(dbs_electrodes_table)  # storage point for DT

        # define an DBSDevice-type device for ecg recording
        dbs_device = DBSDevice(
            name='DBS_device',
            description='cable-bound multichannel systems stimulus generator; TypeSTG4004',
            manufacturer='MultichannelSystems, Reutlingen, Germany',
            synchronization='taken care of via ...',
            electrodes_group=dbs_electrodes_table,
            endpoint_recording_device=self.nwbfile.get_device('endpoint_recording_device')
        )
        # adding the object of DBSDevice
        self.nwbfile.add_device(dbs_device)

        dbs_meta_group = DBSMeta(
            name='DBS_meta',
            stim_state='ON',
            stim_type='unipolar',
            stim_area='STN',
            stim_coordinates='–3.6mmAP, either–2.5mm (right) or 12.5mm(left)ML, and–7.7mmDV',
            pulse_shape='rectangular',
            pulse_width='60 micro-seconds',
            pulse_frequency='130 Hz',
            pulse_intensity='50 micro-Ampere',
            charge_balance='pulse symmetric; set to be theoretically zero',
        )
        # adding the object of DBSMeta
        self.nwbfile.add_lab_meta_data(dbs_meta_group)  # storage point for custom LMD

        dbs_subject_group = DBSSubject(
            name='DBS_subject',
            model='6-OHDA',
            controls='specific control on this trial',
            comment='any comments on this subject',
        )
        # adding the object of DBSSubject
        self.nwbfile.add_lab_meta_data(dbs_subject_group)  # storage point for custom LMD

        dbs_main_group = DBSGroup(
            name='DBS_main_container',
            DBS_phase='first phase after implementation recovery',
            DBS_device=dbs_device,
            DBS_meta=dbs_meta_group,
            DBS_subject=dbs_subject_group,
            comment='any comments ...',
        )
        # adding the object of DBSSubject
        self.nwbfile.add_lab_meta_data(dbs_main_group)  # storage point for custom LMD

        # writing the nwbfile on disk
        with NWBHDF5IO(self.path, mode='w') as io:
            io.write(self.nwbfile)

        # reading and asserting
        with NWBHDF5IO(self.path, mode="r", load_namespaces=True) as io:
            read_nwbfile = io.read()
            # DBSElectrodes
            self.assertContainerEqual(dbs_electrodes_table, read_nwbfile.acquisition['electrodes_group'])
            self.assertContainerEqual(dbs_electrodes_table, read_nwbfile.devices['DBS_device'].electrodes_group)
            # DBSDevice
            self.assertContainerEqual(dbs_device, read_nwbfile.devices['DBS_device'])
            self.assertContainerEqual(dbs_device, read_nwbfile.lab_meta_data['DBS_main_container'].DBS_device)
            # DBSMeta
            self.assertContainerEqual(dbs_meta_group, read_nwbfile.lab_meta_data['DBS_meta'])
            self.assertContainerEqual(dbs_meta_group, read_nwbfile.lab_meta_data['DBS_main_container'].DBS_meta)
            # DBSSubject
            self.assertContainerEqual(dbs_subject_group, read_nwbfile.lab_meta_data['DBS_subject'])
            self.assertContainerEqual(dbs_subject_group, read_nwbfile.lab_meta_data['DBS_main_container'].DBS_subject)
            # DBSMain
            self.assertContainerEqual(dbs_main_group, read_nwbfile.lab_meta_data['DBS_main_container'])

