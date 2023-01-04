from app import db
from flask import url_for, jsonify


class Datatable(object):
    model = ''
    api_url = ''

    def __init__(self, db_model, api_url):
        self.model = db_model
        self.api_url = api_url

    def getRecords(self, displayable_columns, request):

        operator = request.args.get('operator')
        request_value = request.args.get('value')
        search_column = request.args.get('column')
        limit = request.args.get('limit')

        if search_column and operator and request_value:
            search_query = {
                'equals': lambda value: "= '" + value + "'",
                'contains': lambda value: "like '%" + value + "%'",
                'ends': lambda value: "like '%" + value + "'",
                'starts': lambda value: "like '" + value + "%'",
            }[operator](request_value)

            query_args = search_column + ' ' + search_query

            return self.getFilteredRecords(query_args, displayable_columns, limit)

        query = self.model.query.paginate(1, int(limit), False)
        return self.results(query, displayable_columns)

    def getFilteredRecords(self, filter_args, displayable_columns, limit):
        # you can use the like parameter from filter_args i.e User.phone_number.like('0' + "%")
        query = self.model.query.filter(filter_args).paginate(1, int(limit), False)

        return self.results(query, displayable_columns)

    def getRecordsWithRelationships(self, relationship_model, relationship_enitites, displayable_columns, request, search_column):
        operator = request.args.get('operator')
        request_value = request.args.get('value')
        limit = request.args.get('limit')

        if search_column and operator and request_value:
            search_query = {
                'equals': lambda value: "= '" + value + "'",
                'contains': lambda value: "like '%" + value + "%'",
                'ends': lambda value: "like '%" + value + "'",
                'starts': lambda value: "like '" + value + "%'",
            }[operator](request_value)

            query_args = search_column + ' ' + search_query

            query = self.model.query.filter(query_args).join(
                relationship_model).with_entities(*relationship_enitites).paginate(1, int(limit), False)

            return self.results(query, displayable_columns)

        return self.results(query, displayable_columns)

    def getRecord(self, displayable_columns, id):
        query = self.model.query.get(id)
        return self.result(query, displayable_columns)

    def update(self, updatable_columns, data, id):
        # 1.get record
        query = self.model.query.get(id)
        # 2.check which columns are updatable
        for field in updatable_columns:
            if field in data:
                setattr(query, field, data[field])
        db.session.add(query)
        db.session.commit()
        return self.result(query, updatable_columns)

    def results(self, query_results, columns):

        results = [{col: getattr(d, col)
                    for col in columns} for d in query_results.items]

        # create paginate results
        next_url = url_for(self.api_url, page=query_results.next_num)\
            if query_results.has_next else None
        prev_url = url_for(self.api_url, page=query_results.prev_num)\
            if query_results.has_prev else None

        return jsonify({"columns": columns, "data": results, "prev_url": prev_url, "next_url": next_url, "limit": len(results)})

    def result(self, query_result, columns):
        result = [{col: getattr(query_result, col)
                   for col in columns}]

        return result
