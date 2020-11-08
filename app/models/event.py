# from app import db, app
# from datetime import datetime
# import time
# from sqlalchemy.types import TypeDecorator, VARCHAR
# import json
# import datetime
# from app.models.JSONRPCModel import JSONRPCModel, RPCModelMeta
#
# class JSONEncodedDict(TypeDecorator):
#     """Represents an immutable structure as a json-encoded string.
#
#     Usage::
#
#         JSONEncodedDict(255)
#
#     """
#
#     impl = VARCHAR
#
#     def process_bind_param(self, value, dialect):
#         if value is not None:
#             value = json.dumps(value)
#         return value
#
#     def process_result_value(self, value, dialect):
#         if value is not None:
#             value = json.loads(value)
#         return value
#
#
# class Event(db.Model, JSONRPCModel, metaclass=RPCModelMeta):
#     id = db.Column(db.Integer, primary_key=True)
#     user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
#     creation_time = db.Column(
#         db.DateTime(timezone=True), server_default=db.func.now(), nullable=False
#     )
#
#     event_time = db.Column(
#         db.DateTime(timezone=True),
#         nullable=True
#         )
#     name = db.Column(db.UnicodeText())
#     data = db.Column(JSONEncodedDict)
#     #
#     def __init__(self):
#         JSONRPCModel.__init__(self)
#
#         # super(JSONRPCModel, self).__init__()
#
#
#     # @property
#     # @abstractmethod
#     def _rpc_model_base(self):
#         return "events"
#
#     # @abstractmethod
#     def _rpc_create(self, params):
#         if (
#             not params
#             or not "user_id" in params
#             or not "name" in params
#             or not "data" in params
#         ):
#             raise JSONRPC.InvalidRequestException()
#
#         return Event.create(
#             params['user_id'],
#             params['name'],
#             params['data'],
#             params.get('event_time_iso').to_json()
#
#     # @abstractmethod
#     def _rpc_update(self, params):
#         ...
#
#     def set_fields(self, updates):
#         for field in updates:
#             new_value = updates[field]
#             if field == "name":
#                 self.name = new_value
#             if field == "event-time":
#                 event_time = datetime.datetime.strptime(new_value, "%Y-%m-%dT%H:%M:%S.%fZ")
#                 self.event_time = event_time
#             if field == "data":
#                 self.data = new_value
#         db.session.add(self)
#         db.session.commit()
#
#     def __repr__(self):
#         return "<Event {}>".format(self.id)
#
#     def to_json(self):
#         return {
#             "id": self.id,
#             "user-id": self.user_id,
#             "name": self.name,
#             "data": self.data,
#             "creation-time": self.creation_time,
#             "date": self.event_time.strftime('%Y-%m-%d')
#         }
#
#
#     @staticmethod
#     def create(user_id, name, data, event_time_iso=None):
#         event_time = None
#         if event_time_iso:
#             event_time = datetime.datetime.strptime(event_time_iso, "%Y-%m-%dT%H:%M:%S.%fZ")
#         e = Event(user_id=user_id, name=name, data=data, event_time=event_time)
#         db.session.add(e)
#         db.session.commit()
#         return e
