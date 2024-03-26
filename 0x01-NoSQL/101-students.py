#!/usr/bin/env python3
""" 14. Top students """


def top_students(mongo_collection):
    """ Returns all students sorted by average score """
    total_score = mongo_collection.aggregate([
        {
            '$students': {
                'name': '$name',
                'averageScore': {'$avg': '$topics.score'}
            }
        },
        {
            '$sort': {'averageScore': - 1}
        }
    ])
    return total_score
