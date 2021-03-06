from random import randint

from flask import Blueprint, request
from flask.ext.utils.serialization import jsonify
from flask.ext.utils.args import arg_int

from nomenklatura.views.pager import query_pager
#from nomenklatura import authz
from nomenklatura.model.matching import find_matches
from nomenklatura.model import Dataset, Entity


section = Blueprint('matching', __name__)


@section.route('/match', methods=['GET'])
def match():
    dataset_arg = request.args.get('dataset')
    dataset = Dataset.find(dataset_arg)
    matches = find_matches(dataset,
        request.args.get('name'),
        filter=request.args.get('filter'),
        exclude=arg_int('exclude'))
    return query_pager(matches)


@section.route('/datasets/<dataset>/review', methods=['GET'])
def review(dataset):
    entities = Entity.all()
    dataset = Dataset.find(dataset)
    entities = entities.filter_by(dataset=dataset)
    entities = entities.filter(Entity.reviewed==False)
    review_count = entities.count()
    if review_count == 0:
        return jsonify(None)
    entities = entities.offset(randint(0, review_count-1))
    return jsonify(entities.first())
