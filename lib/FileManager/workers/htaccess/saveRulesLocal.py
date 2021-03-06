import os
import traceback

from lib.FileManager.HtAccess import HtAccess
from lib.FileManager.workers.baseWorkerCustomer import BaseWorkerCustomer


class SaveRulesLocal(BaseWorkerCustomer):
    def __init__(self, path, params, session, *args, **kwargs):
        super(SaveRulesLocal, self).__init__(*args, **kwargs)

        self.path = path
        self.params = params
        self.session = session

    def run(self):
        try:
            self.preload()
            abs_path = self.get_abs_path(self.path)
            self.logger.debug("FM ReadRulesLocal worker run(), abs_path = %s" % abs_path)

            htaccess_path = os.path.join(abs_path, '.htaccess')

            if not os.path.exists(htaccess_path):
                fd = open(htaccess_path, 'x')
                fd.close()

            with open(htaccess_path, 'r') as fd:
                old_content = fd.read()

            htaccess = HtAccess(old_content, self.logger)
            content = htaccess.write_htaccess_file(self.params)

            with open(htaccess_path, 'w') as fd:
                fd.write(content)

            result = {
                    "data": self.params,
                    "error": False,
                    "message": None,
                    "traceback": None
            }

            self.on_success(result)

        except Exception as e:
            result = {
                "error": True,
                "message": str(e),
                "traceback": traceback.format_exc()
            }

            self.on_error(result)
