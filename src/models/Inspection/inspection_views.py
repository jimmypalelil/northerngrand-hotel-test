from flask import Blueprint, request, jsonify, json
from bson.json_util import dumps
from src.common.database import Database
from src.models.Inspection.createInsItem import resetInspections
from src.models.Inspection.employee import Employee
from src.models.Inspection.inspection import Inspection
from src.models.Inspection.inspectionEmployee import InspectionEmployee
from src.models.Inspection.inspectionItem import InspectionItem
from src.models.Inspection.inspectionScore import InspectionScore
from src.models.Inspection.employeemonthlyscore import EmployeeMonthlyScore

inspection_bp = Blueprint('inspection', __name__)
collection = 'inspections'


@inspection_bp.route('/empList')
def get_emp_list():
    return dumps(Database.findAll('employees'))


@inspection_bp.route('/newInspection', methods=['GET', 'POST'])
def start_new_inspection():
    data = request.json
    inspection = data[0]
    emp_ids = data[1]
    room_num = inspection['room_number']
    day = inspection['day']
    month = inspection['month']
    year = inspection['year']
    new_id = Inspection(room_num, day, month, year, 0, len(emp_ids)).insert_one()
    for emp_id in emp_ids:
        InspectionEmployee(new_id.inserted_id, emp_id, month, year).insert()
    ins_items = InspectionItem.getAllItemsByGroup()
    return jsonify({'id': new_id.inserted_id}, ins_items)


@inspection_bp.route('/inspectionResult', methods=['POST'])
def create_inspection_result():
    data = request.json
    ins_id = data[0]['_id']['id']
    month = data[0]['month']
    year = data[0]['year']
    scores = data[1]
    comments = data[2]
    ins_emps = data[3]
    total_score = 0
    count = 0
    for key in scores:
        score = float(scores[key])
        if score >= 0:
            total_score += score
            count += 1
        if key not in comments:
            comment = ''
        else:
            comment = comments[key]
    # items = InspectionItem.getAllItems()
    # for item in items:
    #     key = item['_id']
    #     score = -1
    #     if key in scores:
    #         score = float(scores[key])
    #         if score >= 0:
    #             total_score += score
    #             count += 1
    #     if key not in comments:
    #         comment = ''
    #     else:
    #         comment = comments[key]
        for emp in ins_emps:
            InspectionScore(ins_id, emp['_id'], key, month, year, score, comment).insert()

    if count == 0:
        count = 1
    ins_score = total_score / count
    Inspection.set_ins_score(ins_id, ins_score)
    for employee in ins_emps:
        Employee.update_emp_score(employee['_id'], ins_score, 1)
        emp_month_score = EmployeeMonthlyScore.get_by_emp_id_month_year(employee['_id'], month, year)
        if emp_month_score is None:
            EmployeeMonthlyScore(employee['_id'], month, year, ins_score).insert()
        else:
            EmployeeMonthlyScore.update_monthly_score_and_num_inspections(employee['_id'], month,
                                                                          year, ins_score, 1)
    return jsonify({'text': 'Inspection Recorded'})


@inspection_bp.route('/getEmployeeMonthlyInspections/<emp_id>')
def get_emp_monthly_inspections(emp_id):
    return Employee.get_monthly_inspections(emp_id)


@inspection_bp.route('/resetInspections')
def reset():
    resetInspections()
    return jsonify({'text': 'Inspections Reset Successfully'})


@inspection_bp.route('/getEmployeeInspections', methods=['POST'])
def get_inspections():
    data = request.json
    emp_id = data['emp_id']
    month = data['month']
    year = data['year']
    return dumps(Employee.get_emp_month_inspections(emp_id, month, year))


@inspection_bp.route('/getEmployeeInspection/<ins_id>/<emp_id>')
def getInpsection(ins_id, emp_id):
    return dumps(Inspection.get_inspection_items(ins_id, emp_id))


@inspection_bp.route('/deleteInspection', methods=['POST'])
def delete_inspection():
    data = request.json
    inspection = data['inspection']['inspections']
    ins_id = inspection['_id']
    emp_id = data['emp_id']
    total_emps = inspection['num_employees']

    score_to_deduct = inspection['score'] * -1
    Employee.update_emp_score(emp_id, score_to_deduct, -1)
    Employee.calculate_emp_monthly_avg(emp_id, inspection['month'], inspection['year'], score_to_deduct, -1)

    if total_emps == 1:
        Inspection.remove(ins_id)
    else:
        Inspection.set_num_emps(ins_id, -1)
    InspectionScore.remove_by_ins_id_emp_id(ins_id, emp_id)
    InspectionEmployee.remove_by_ins_id_and_emp_id(ins_id, emp_id)

    return jsonify({"text": "Inspection Deleted"})


@inspection_bp.route('/deleteMonthlyInspections/<emp_id>', methods=['POST'])
def delete_monthly_inspections(emp_id):
    data = request.json
    month = data['month']
    year = data['year']
    score_to_deduct = data['score'] * -1
    num_inspections_to_deduct = data['num_inspections'] * -1

    Employee.calculate_emp_avg(emp_id, score_to_deduct, num_inspections_to_deduct)
    EmployeeMonthlyScore.remove_by_emp_id_and_month_and_year(emp_id, month, year)
    InspectionScore.remove_by_emp_id_month_year(emp_id, month, year)
    InspectionEmployee.remove_by_emp_id_month_year(emp_id, month, year)
    Inspection.remove_by_month_and_year(month, year)
    return jsonify({"text": "Inspections Deleted"})
