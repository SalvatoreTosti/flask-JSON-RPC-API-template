from app import db
from abc import ABC, abstractmethod
import datetime
from app.rpc.JSONRPCExceptions import InvalidRequestException


class JSONRPCModel(ABC):
    def _crud_dispaches(self):
        self.add_dispatch("create", self._rpc_create)
        self.add_dispatch("read", self._rpc_read)
        self.add_dispatch("read_all", self._rpc_read_all)
        self.add_dispatch("update", self._rpc_update)
        self.add_dispatch("delete", self._rpc_delete)

    def __repr__(self):
        return f"<{type(self)} {self.id}>, endpoint: {self._rpc_model_base()}"

    # Optional override to apply transformations to output values (eg. datetimes)
    def transform_json_values(self):
        return {}

    def to_json(self):
        x = {}
        for k in dir(self):
            v = getattr(self, k)
            if (
                not callable(v)
                and not k.startswith("_")
                and k not in ("metadata", "query")
            ):
                x[k] = v

        return self._transform_parameters(x, self.transform_json_values())

    def _rpc_model_base(self):
        return type(self).__name__.lower()

    def add_dispatch(self, action, fn):
        self._dispatch_dict[self._rpc_model_base() + "." + action] = fn

    def dispatches(self):
        self._dispatch_dict = {}
        self._crud_dispaches()
        return self._dispatch_dict

    def _validate_params(self, params=None, required_params=None, optional_params=None):
        if not params:
            params = {}

        if not required_params:
            required_params = []

        if not optional_params:
            optional_params = []

        for required_param in required_params:
            if required_param not in params:
                raise InvalidRequestException()

        _all_params = []
        _all_params.extend(required_params)
        _all_params.extend(optional_params)
        valid_params = {}
        for k, v in params.items():
            if k in _all_params:
                valid_params[k] = v

        return valid_params

    @classmethod
    def read_cls(cls, target_id):
        return cls.query.filter_by(id=target_id).first()

    def read_restrictions(self):
        return True

    def read(self, target_id):
        if not self.read_restrictions():
            raise InvalidRequestException()
        return type(self).read_cls(target_id)

    def _rpc_read(self, params):
        target_id = params["target_id"]
        return self.read(target_id).to_json()

    def read_all_restrictions(self):
        return True

    def read_all(self):
        if not self.read_all_restrictions():
            raise InvalidRequestException()
        return type(self).query.all()

    def _rpc_read_all(self, params):
        return [target.to_json() for target in self.read_all()]

    def _transform_parameters(self, params, transformation_dict):
        for k, v in params.items():
            if k in transformation_dict.keys():
                fn = transformation_dict[k]
                params[k] = fn(v)
        return params

    def _generate_transform_dict(self, parameter_description_dict):
        all_params = {}
        all_params.update(parameter_description_dict.get("required", {}))
        all_params.update(parameter_description_dict.get("optional", {}))

        valid_transformations = {}
        for k, v in all_params.items():
            if v:
                valid_transformations[k] = v
        return valid_transformations

    @abstractmethod
    def _create_parameters(self):
        ...

    def create(self, dictionary):
        dictionary = self._transform_parameters(
            dictionary, self._generate_transform_dict(self._create_parameters())
        )
        target = type(self)(**dictionary)
        db.session.add(target)
        db.session.commit()
        return target

    def create_restrictions(self, dictionary):
        return True

    def _rpc_create(self, params):
        params = self._validate_params(
            params,
            self._create_parameters().get("required").keys(),
            self._create_parameters().get("optional").keys(),
        )
        if not self.create_restrictions(params):
            raise InvalidRequestException()
        return self.create(params).to_json()

    @abstractmethod
    def _update_parameters(self):
        ...

    def update(self, dictionary):
        updates = self._transform_parameters(
            dictionary, self._generate_transform_dict(self._update_parameters())
        )
        print(updates)
        for k, v in updates.items():
            setattr(self, k, v)
        db.session.add(self)
        db.session.commit()

    def update_restrictions(self, dictionary):
        return True

    def _rpc_update(self, params):
        params = self._validate_params(
            params,
            self._update_parameters().get("required").keys(),
            self._update_parameters().get("optional").keys(),
        )
        if not self.update_restrictions(params):
            print("raising ex")
            raise InvalidRequestException()
        target = self.read(params["target_id"])
        target.update(params)
        return target.to_json()

    def delete_restrictions(self):
        return True

    # Override for specific class behavior
    def delete(self):
        if not self.delete_restrictions():
            raise InvalidRequestException()
        db.session.delete(target)
        db.session.commit()
        return {}

    def update_restrictions(self, dictionary):
        return True

    def _rpc_delete(self, params):
        target_id = params["target_id"]
        target = self.read(target_id)
        if not target:
            return {}
        return target.delete()


class JSONRPCUtils:
    @staticmethod
    def from_iso_str(value):
        if value:
            return datetime.datetime.strptime(value, "%Y-%m-%dT%H:%M:%S.%fZ")
        return value

    @staticmethod
    def to_iso_str(value):
        if value:
            return value.isoformat() + "Z"
        return value


class RPCModelMeta(type(JSONRPCModel), type(db.Model)):
    ...
