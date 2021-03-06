import sys
from software.app_files.classes import Doctor
from software.app_files.classes import Nurse
from software.app_files.classes import AdminStaff
from software.app_files import database as db
import pytest

db.connectDB()

def setup_module():
    # reset db
    f = open('test_db_files/proj_tables.sql','r')
    sql = f.read()
    db.c.executescript(sql)
    f = open('test_db_files/test_data.sql','r')
    sql = f.read()
    db.c.executescript(sql)
    db.conn.commit()

def teardown_module():
    # reset db
    f = open('test_db_files/proj_tables.sql','r')
    sql = f.read()
    db.c.executescript(sql)
    f = open('test_db_files/test_data.sql','r')
    sql = f.read()
    db.c.executescript(sql)
    db.conn.commit()

'''
Passes
'''
# CareStaff Tests
def test_getCharts(capsys):
    doc = Doctor(db.getUser('RwiNqxg:', 'Vjgug"Pggf"Jcujkpi'))
    patient = doc.getPatient("15384")
    doc.getCharts(patient['hcno'])
    out=capsys.readouterr()
    print(out)
    assert out[0] == 'Charts for patient with health care number 15384:\nChart 1:\n- adate: 2015-01-06 12:24:56\n- name: Angelina Jolie\n- edate: 2015-02-13 10:35:42\n- phone: 7801234567\n- hcno: 15384\n- address: 123-120 ST, Edmonton, Alberta\n- chart_id: 10001\n- emg_phone: 7801234567\n- age_group: 18-39\n'
'''
Passes
'''
def test_printChartEntries(capsys):
    doc = Doctor(db.getUser('RwiNqxg:', 'Vjgug"Pggf"Jcujkpi'))
    patient = doc.getPatient("15384")
    print (doc.printChartEntries(patient['hcno'], "10001"))
    out=capsys.readouterr()
    print (out)
    assert out[0] == 'Symptom 1:\n- chart_id: 10001\n- obs_date: 2015-01-08 18:22:55\n- staff_id: 37225\n- symptom: Nausea\n- hcno: 15384\nDiagnosis 1:\n- chart_id: 10001\n- diagnosis: Ebola\n- staff_id: 14334\n- ddate: 2015-01-11 14:06:01\n- hcno: 15384\nMedication 1:\n- staff_id: 14334\n- mdate: 2015-01-12 02:20:09\n- hcno: 15384\n- drug_name: ZMapp\n- amount: 8\n- start_med: 2015-01-12 19:50:32\n- end_med: 2015-02-21 02:51:33\n- chart_id: 10001\nTrue\n'
'''
    Passes
'''
def test_getPatient():
    doc = Doctor(db.getUser('RwiNqxg:', 'Vjgug"Pggf"Jcujkpi'))
    patient = doc.getPatient("15384")
    assert patient['hcno'] == "15384"
    assert patient['name'] == "Angelina Jolie"
    assert patient['phone'] == "7801234567"
    assert patient['address'] == "123-120 ST, Edmonton, Alberta"
    assert patient['emg_phone'] == "7801234567"
    assert patient['age_group'] == "18-39"
'''
Passes
'''
def test_addSymptom():
    # TODO
    doc = Doctor(db.getUser('RwiNqxg:', 'Vjgug"Pggf"Jcujkpi'))
    doc.addSymptom("15384","10001","00001","Flu")
    entry = db.symptomsForPatientAndChart("15384", "10001")
    assert entry[0]["hcno"] == "15384"
    assert entry[0]["chart_id"] == '10001'
    assert entry[0]["staff_id"] == '37225'
    assert entry[0]["obs_date"] == "2015-01-08 18:22:55"
    assert entry[0]["symptom"] == "Nausea"

# Doctor Tests
'''
Passes
'''
def test_docIntroduce():
    doc = Doctor(db.getUser('RwiNqxg:', 'Vjgug"Pggf"Jcujkpi'))
    assert doc.introduce() == "I'm a Doctor"
'''
Passes
'''
def test_addDiagnosis():
    doc = Doctor(db.getUser('RwiNqxg:', 'Vjgug"Pggf"Jcujkpi'))
    doc.addDiagnosis("15384", '10001', '14334', 'Flu')
    entry = db.diagnosesForPatientAndChart("15384", "10001");
    assert entry[0]['hcno'] == "15384"
    assert entry[0]['chart_id'] == "10001"
    assert entry[0]['diagnosis'] == "Ebola"
    assert entry[0]['staff_id'] == "14334"

'''
Passes!
'''
def test_checkMedicationAmountValid():
    doc = Doctor(db.getUser('RwiNqxg:', 'Vjgug"Pggf"Jcujkpi'))
    assert doc.checkMedicationAmountValid("ZMapp", "10", "18-39") == False
    assert doc.checkMedicationAmountValid("ZMapp", "5", "18-39") == True

'''
Passes
'''
def test_getValidMedicationAmount():
    doc = Doctor(db.getUser('RwiNqxg:', 'Vjgug"Pggf"Jcujkpi'))
    validMedicationAmount = doc.getValidMedicationAmount("ZMapp", "18-39")
    assert validMedicationAmount['drug_name'] == "ZMapp"
    assert validMedicationAmount['age_group'] == "18-39"
    assert validMedicationAmount['sug_amount'] == 8

'''
Passes
'''
def test_checkPatientAllergicToDrug():
    doc = Doctor(db.getUser('RwiNqxg:', 'Vjgug"Pggf"Jcujkpi'))

    assert doc.checkPatientAllergicToDrug("15384", "Tamiflu") == True
    assert doc.checkPatientAllergicToDrug("15384", "ZMapp") == False

'''
 Passes!
    
'''
def test_checkInferredAllergyToDrug():

    doc = Doctor(db.getUser('RwiNqxg:', 'Vjgug"Pggf"Jcujkpi'))
    inferred = doc.checkInferredAllergyToDrug('15384', "ZMapp")
    
    assert inferred == None


'''
Fails:
assert 'ZMapp' == 'Viread'

'''
def test_addMedication():
    doc = Doctor(db.getUser('RwiNqxg:', 'Vjgug"Pggf"Jcujkpi'))
    doc.addMedication("15384", '10001', '14334', "2015-01-22 19:50:32", "2015-02-22 02:51:33", "Viread", "8")

    entry = db.medicationsForPatientAndChart("15384", "10001")
    #assert entry['hcno'] == '15384'
    assert entry[0]['chart_id'] == '10001'
    assert entry[0]['staff_id'] == '14334'
    assert entry[0]['mdate'] == "2015-01-12 02:20:09"
    assert entry[0]['start_med'] == "2015-01-12 19:50:32"
    assert entry[0]['end_med'] == "2015-02-21 02:51:33"
    assert entry[0]['amount'] == 8
    assert entry[0]['drug_name'] == "Viread"


# Nurse Tests
'''
Passes!
'''
def test_nurIntroduce():
    nur = Nurse(db.getUser('Lq{3', 'Lq{345'))
    assert nur.introduce() == "I'm a Nurse"

'''
Passes!
'''
def test_newChart():

    nur = Nurse(db.getUser('Lq{3', 'Lq{345'))
    newChart = nur.newChart("15384")
    print(newChart)
    assert newChart == 10010

'''
Passes!
'''
def test_newPatient():

    nur = Nurse(db.getUser('Lq{3', 'Lq{345'))
    newpatient = nur.newPatient("3", "Aaron", "18-39", "The zoo",
                             "000000000", "000000")
    patient = db.getPatientWithHcno('3')
    
    assert patient["hcno"] == '3'
    assert patient["name"] == 'Aaron'
    assert patient["phone"] =='000000000'
    assert patient["address"] == "The zoo"
'''
Passes!
    
'''
def test_checkIfPatientHasOpenChart():
    nur = Nurse(db.getUser('Lq{3', 'Lq{345'))
    assert nur.checkIfPatientHasOpenChart("20195") == "10009"
    assert nur.checkIfPatientHasOpenChart("15384") == None


'''
Passes!
'''
def test_closeChart():
    nur = Nurse(db.getUser('Lq{3', 'Lq{345'))

    chart_id = db.createNewChartForPatient("15384")
    if db.isChartOpenForPatient("15384") != None: 
        nur.closeChart(chart_id)
        assert db.isChartOpenForPatient("15384") == '10010'

'''
passes!

'''
# Admin tests
def test_listDrugAmtForEachDoctor(capsys):
    start = "2015-01-11 19:50:32"
    end = "2015-01-13 19:50:32"
    adm = AdminStaff(db.getUser('Lgtkejq', 'sygtv{'))
    adm.listDrugAmtForEachDoctor(start, end)
    out=capsys.readouterr()
    print (out)
    assert out[0] == 'Report: Drug Amount Prescribed For Each Doctor Between 2015-01-11 19:50:32 and 2015-01-13 19:50:32:\n-----------------------\n- drug_name: Retrovir\n- DoctorName: Mehmet Oz\n- total_amount: 85\n-----------------------\n- drug_name: Viread\n- DoctorName: Phil McGraw\n- total_amount: 16\n'

'''
Passes!
'''

def test_listDrugAmtForEachCategory(capsys):
    start = "2015-01-11 19:50:32"
    end = "2015-01-13 19:50:32"
    adm = AdminStaff(db.getUser('Lgtkejq', 'sygtv{'))
    adm.listDrugAmtForEachCategory(start, end)
    out=capsys.readouterr()
    print (out)
    assert out[0] == 'Report Part 1: Drug Amount Prescribed For Each Category Between 2015-01-11 19:50:32 and 2015-01-13 19:50:32\n-----------------------\n- category: anti-Ebola\n- drug_name: ZMapp\n- amount: 8\n-------------------------------------------------\nReport Part 2: Total Amount Prescribed For Each Category Between 2015-01-11 19:50:32 and 2015-01-13 19:50:32\n-----------------------\n- category: anti-Ebola\n- total: 8\n'


'''
Fails!
    
'''
def test_listMedicationsForDiagnosis():
    diagnosis = "Ebola"
    adm = AdminStaff(db.getUser('Lgtkejq', 'sygtv{'))
    assert adm.listMedicationsForDiagnosis(diagnosis) == True

    diagnosis = "DoesNotExist"
    assert adm.listMedicationsForDiagnosis(diagnosis) == False

'''
  Fails!
    
'''
def test_listDiagnosesMadeBeforePrescribingDrug():
    drug_name = "ZMapp"
    adm = AdminStaff(db.getUser('Lgtkejq', 'sygtv{'))
    assert adm.listDiagnosesMadeBeforePrescribingDrug(drug_name) == True
    drug_name = "Heroin"
    assert adm.listDiagnosesMadeBeforePrescribingDrug(drug_name) == False

