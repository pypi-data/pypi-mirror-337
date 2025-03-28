import mosaik_api_v3
from midas.util.dict_util import bool_from_dict
from midas.util.logging import set_and_init_logger

from . import LOG
from .csv_model import CSVModel
from .meta import META


class MidasCSVStore(mosaik_api_v3.Simulator):
    """ """

    def __init__(self):
        super().__init__(META)

        self.sid = None
        self.eid = "Database-0"
        self.database = None
        self.filename = None
        self.step_size = None
        self.current_size = 0
        self.buffer_size = None
        self.saved_rows = 0
        self.finalized = False
        self.keep_old_files = True
        self._worker = None

    def init(self, sid, **sim_params):
        self.sid = sid
        self.step_size = sim_params.get("step_size", 900)

        return self.meta

    def create(self, num, model, **model_params):
        if num > 1 or self.database is not None:
            errmsg = (
                "You should really not try to instantiate more than one "
                "database. If your need another database, create a new "
                "simulator as well."
            )
            raise ValueError(errmsg)

        self.database = CSVModel(
            model_params.get("filename", ""),
            path=model_params.get("path", None),
            unique_filename=bool_from_dict(
                model_params, "unique_filename", False
            ),
            keep_old_files=bool_from_dict(
                model_params, "keep_old_files", False
            ),
        )

        return [{"eid": self.eid, "type": model}]

    def step(self, time, inputs, max_advance=0):
        data = inputs.get(self.eid, {})

        if not data:
            LOG.info(
                "Did not receive any inputs. "
                "Did you connect anything to the store?"
            )

        for attr, src_ids in data.items():
            for src_id, val in src_ids.items():
                sid, eid = src_id.split(".")
                self.database.to_memory(sid, eid, attr, val)

        self.database.step()

        return time + self.step_size

    def get_data(self, outputs):
        return {}

    def finalize(self):
        self.database.finalize()


if __name__ == "__main__":
    set_and_init_logger(0, "store-logfile", "midas-store.log", replace=True)

    mosaik_api_v3.start_simulation(MidasCSVStore())
