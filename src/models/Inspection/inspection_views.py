from flask import Blueprint, render_template, json, request, redirect, session, url_for, jsonify
from bson.json_util import dumps
from src.common.database import Database
from src.models.Inspection.createInsItem import resetInspections
from src.models.Inspection.employee import Employee
from src.models.Inspection.inspection import Inspection
from src.models.Inspection.inspectionEmployee import InspectionEmployee
from src.models.Inspection.inspectionItem import InspectionItem
from src.models.Inspection.inspectionScore import InspectionScore
from src.models.Inspection.score import Score

import sendgrid, os
from sendgrid.helpers.mail import *

inspection_bp = Blueprint('inspection', __name__)
collection = 'inspections'


@inspection_bp.route('/empList')
def getEmployeeList():
    return dumps(Database.findAll('employees'))


@inspection_bp.route('/newInspection', methods=['GET', 'POST'])
def startNewInspection():
    data = request.json
    inspection = data[0]
    ids = data[1]
    roomNum = inspection['room_number']
    day = inspection['day']
    month = inspection['month']
    year = inspection['year']
    newId = Inspection(roomNum, day, month, year, 0).insertOne()
    for id in ids:
        InspectionEmployee(newId.inserted_id, id).insert()
    insItems = InspectionItem.getAllItemsByGroup()
    return jsonify({'id': newId.inserted_id}, insItems)


@inspection_bp.route('/inspectionResult', methods=['POST'])
def createInspectionResult():
    data = request.json
    id = data[0]['id']
    scores = data[1]
    comments = data[2]
    totalScore = 0
    count = 0
    for key in scores:
        score = scores[key]
        if score != -1:
            totalScore += float(score)
            count = count + 1
        if key not in comments:
            comment = ''
        else:
            comment = comments[key]
        InspectionScore(id, key, score, comment).insert()
    inspection = Inspection.get_by_id(id)
    inspection.score = totalScore / count
    inspection.updateSelf()
    insEmployees = InspectionEmployee.get_by_ins_id(inspection._id)
    for employee in insEmployees:
        emp = Employee.get_by_id(employee['empId'])
        if emp.avg_score == 0:
            emp.avg_score = inspection.score
        else:
            emp.avg_score = (float(emp.avg_score) + float(inspection.score)) / 2.0
        emp.num_inspections += 1
        emp.update()
        empScore = Score.get_by_emp_id(employee['empId'], inspection.month)
        if empScore is None:
            Score(employee['empId'], inspection.month, inspection.year, inspection.score).insert()
        else:
            empScoreData = Score(**empScore)
            empScoreData.score = (float(empScoreData.score) + float(inspection.score)) / 2.0
            empScoreData.num_inspections += 1
            Score.updateScore(employee['empId'], inspection.month, inspection.score, empScoreData.json())
    return jsonify({'text': 'Inspection Recorded'})


@inspection_bp.route('/employeeInspections/<empID>')
def getEmployeeInspections(empID):
    return Employee.getMonthlyInspections(empID)


@inspection_bp.route('/resetInspections')
def reset():
    resetInspections()
    return jsonify({'text': 'Inspections Reset Successfully'})


@inspection_bp.route('/getInspections/<empID>')
def getInpsections(empID):
    return Employee.getEmployeeInspections(empID)


@inspection_bp.route('/getInspection', methods=['POST'])
def getInpsection():
    inspection = request.json
    insId = inspection['_id']
    day = inspection['day']
    month = inspection['month']
    year = inspection['year']
    return Inspection.getInspectionItems(insId, day, month, year)


@inspection_bp.route('/deleteInspection/<insId>/<month>/<year>')
def deleteInspection(insId, month, year):
    Inspection.remove(insId)
    insEmps = Database.DATABASE['ins_employees'].find({"insId": insId})
    for emp in insEmps:
        Employee.calculateMonthlyAvg(emp['empId'], month, year)
        Employee.calculateAllAvg(emp['empId'])
    InspectionEmployee.remove_by_insId(insId)
    InspectionScore.remove_by_insId(insId)
    return jsonify({"text": "Inspection Deleted"})


@inspection_bp.route('/deleteMonthlyInspections/<empID>', methods=['POST'])
def deleteMonthlyInspections(empID):
    data = request.json
    month = data['month']
    year = data['year']
    Score.remove_by_month_and_year(month, year)
    inspections = Inspection.get_by_month_and_year(month, year)
    Inspection.remove_by_month_and_year(month, year)
    for ins in inspections:
        InspectionScore.remove_by_insId(ins['_id'])
        InspectionEmployee.remove_by_insId(ins['_id'])
    Employee.calculateAvgForAllEmployees(month, year)
    return jsonify({"text": "Inspections Deleted"})
