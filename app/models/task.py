from app import db, app
from datetime import datetime
import time
from sqlalchemy.types import TypeDecorator, VARCHAR
import json
from app.models.JSONRPCModel import JSONRPCModel, RPCModelMeta, JSONRPCUtils


class Task(db.Model, JSONRPCModel, metaclass=RPCModelMeta):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    title = db.Column(db.UnicodeText())
    description = db.Column(db.UnicodeText())
    due_time = db.Column(db.DateTime(timezone=True), nullable=True)
    completion_time = db.Column(db.DateTime(timezone=True), nullable=True)

    def _create_parameters(self):
        return {
            "required": {"user_id": None, "title": None,},
            "optional": {"description": None, "due_time": JSONRPCUtils.from_iso_str},
        }

    def _update_parameters(self):
        return {
            "required": {"target_id": None},
            "optional": {
                "title": None,
                "description": None,
                "due_time": JSONRPCUtils.from_iso_str,
                "completion_time": JSONRPCUtils.from_iso_str,
            },
        }

    def transform_json_values(self):
        return {
            "due_time": JSONRPCUtils.to_iso_str,
            "completion_time": JSONRPCUtils.to_iso_str,
        }
