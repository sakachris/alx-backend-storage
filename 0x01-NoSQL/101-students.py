#!/usr/bin/env python3
''' 101-students.py '''

from pymongo import MongoClient


def top_students(mongo_collection):
    '''
    returns all students sorted by average score
    '''
    students = list(mongo_collection.find())

    for student in students:
        scores = [topic['score'] for topic in student['topics']]
        student['averageScore'] = (
                sum(scores) / len(scores) if len(scores) > 0 else 0
        )

    return sorted(students, key=lambda s: s['averageScore'], reverse=True)
