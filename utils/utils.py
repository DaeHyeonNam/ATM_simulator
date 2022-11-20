import json

class Utility:
    @staticmethod
    def make_success_response(data):
        return json.dumps({"success": True, 'data': data})


    @staticmethod
    def make_failure_response(error):
        return json.dumps({"success": False, 'error': error})