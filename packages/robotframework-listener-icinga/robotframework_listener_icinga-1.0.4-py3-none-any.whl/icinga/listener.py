import json
import os
import socket
import urllib.parse
from datetime import datetime, timezone

from lib.base import get_state
from lib.base import get_table
from lib.base import state2str
from lib.globals import STATE_CRIT
from lib.globals import STATE_OK
from lib.globals import STATE_UNKNOWN
from lib.icinga import api_post
from lib.icinga import get_service
from lib.txt import pluralize
from RPA.Robocorp.Vault import Vault


class icinga:

    ROBOT_LISTENER_API_VERSION = 2
    ROBOT_LIBRARY_SCOPE = "GLOBAL"

    def __init__(self, api_user=None, api_pass=None, icinga_fqdn=None, host_name=None, service_name=None, ignore_keywords=True, ttl=300):

        self.ROBOT_LIBRARY_LISTENER = self
        self.fqdn = socket.getfqdn().lower()

        self.ignore_keywords = ignore_keywords

        if api_user is None:
            VAULT = Vault()
            _vault_icinga = VAULT.get_secret("icinga")
            api_user = _vault_icinga["api_user"]
        self.api_user = api_user

        if api_pass is None:
            api_pass = _vault_icinga["api_pass"]
        self.api_password = api_pass

        env_icinga_fqdn = os.getenv("ICINGA_FQDN", default=False)
        if icinga_fqdn is None and env_icinga_fqdn:
            icinga_fqdn = env_icinga_fqdn
        self.icinga = icinga_fqdn

        env_icinga_host_name = os.getenv("ICINGA_HOST_NAME", default=False)
        if host_name is None:
            if env_icinga_host_name:
                self.host_name = env_icinga_host_name
            else:
                self.host_name = self.fqdn

        env_icinga_service_name = os.getenv("ICINGA_SERVICE_NAME", default=False)
        if service_name is None and env_icinga_service_name:
            service_name = env_icinga_service_name
        self.service_name = service_name

        env_icinga_ttl = os.getenv("ICINGA_TTL", default=False)
        if ttl == 300 and env_icinga_ttl:
            ttl = env_icinga_ttl
        self.ttl = ttl

        current_time = datetime.now(tz=timezone.utc)
        self.current_ts = int(current_time.timestamp()) * 1000

        self.current_suite = {}
        self.current_test = {}
        self.current_keyword = {}

        self.icinga_status = STATE_UNKNOWN
        self.icinga_message = ""
        self.icinga_perfdata = []
        self.suit_status = []
        self.test_status = []
        self.keyword_status = []
        self.failed_keywords = []
        self.table_cols = ["Suite", "Test", "Keyword", "Reason", "Robot Framework Status", "Icinga Status"]
        self.table_data_keywords = []
        self.table_data_tests = []
        self.table_data_suites = []
        # print(sys.path)
        self.service_thresholds = self.get_service_thresholds()

    def get_service_thresholds(self):
        try:
            uri = f"https://{self.icinga}:5665"
            service_name = urllib.parse.quote(f"{self.host_name}!{self.service_name}")
            print(service_name)
            return_code, result = get_service(
                uri, self.api_user, self.api_password, servicename=f"{self.host_name}!{self.service_name}", attrs="vars"
            )
            return json.loads(result["results"][0]["attrs"]["vars"]["robot_framework_thresholds"])
        except Exception as e:
            return {}

    def set_service_status(
        self, performance_data=False, check_command=False, check_source=False, execution_start=False, execution_end=False, ttl=False
    ):
        uri = f"https://{self.icinga}:5665/v1/actions/process-check-result"
        data = {
            "type": "Service",
            "filter": "host.name==host_name && service.name==service_name",
            "filter_vars": {"host_name": self.host_name, "service_name": self.service_name},
            "exit_status": self.icinga_status,
            "plugin_output": self.icinga_message,
        }
        if self.icinga_perfdata:
            # print(self.icinga_perfdata)
            data["performance_data"] = self.icinga_perfdata
        data["check_command"] = self.__class__.__name__
        data["check_source"] = self.fqdn
        if execution_start:
            data["execution_start"] = execution_start
        if execution_end:
            data["execution_end"] = execution_end
        if self.ttl:
            data["ttl"] = self.ttl
        # print("Icinga: set_service_status(): ", data)
        return_code, result = api_post(uri=uri, username=self.api_user, password=self.api_password, data=data)
        if return_code:
            print("Icinga: set_service_status(): successfull")
        else:
            print("Icinga: set_service_status(): failed", return_code, result)
            return False
        return True

    def get_metric_name(self, event_type):
        if event_type == "keyword":
            metric_name = ".".join([self.current_test["suite"], self.current_test["test"], self.current_keyword["keyword"]])
        elif event_type == "test":
            metric_name = ".".join([self.current_test["suite"], self.current_test["test"]])
        elif event_type == "suite":
            metric_name = self.current_suite["suite"]
        return metric_name
    
    def get_statistics(self):
        suite_statistics_len = len(self.suit_status)
        suite_statistics_title = pluralize("suite", suite_statistics_len)
        suite_statistics = f"{suite_statistics_len} {suite_statistics_title}, {self.suit_status.count(0)} ok, {self.suit_status.count(1)} warning, {self.suit_status.count(2)} critical, {self.suit_status.count(3)} unknown"
        test_statistics_len = len(self.test_status)
        test_statistics_title = pluralize('test', test_statistics_len)
        test_statistics = f"{test_statistics_len} {test_statistics_title}, {self.test_status.count(0)} ok, {self.test_status.count(1)} warning, {self.test_status.count(2)} critical, {self.test_status.count(3)} unknown"
        if self.ignore_keywords:
            statistics = f"Statistics: {suite_statistics}; {test_statistics}"
        else:
            keyword_statistics_len = len(self.keyword_status)
            keyword_statistics_title = pluralize("keyword", keyword_statistics_len)
            keyword_statistics = f"{keyword_statistics_len} {keyword_statistics_title}, {self.keyword_status.count(0)} ok, {self.keyword_status.count(1)} warning, {self.keyword_status.count(2)} critical, {self.keyword_status.count(3)} unknown"
            statistics = f"Statistics: {suite_statistics}; {test_statistics}; {keyword_statistics}"
        return statistics
    
    def append_table_row(self, list, row):
        row_dict = {}
        for idx, val in enumerate(row):
            row_dict[self.table_cols[idx]] = val
        list.append(row_dict)

    def process_data(self, name, event_type, attrs):
        if event_type == "close":
            # build final output for icinga listener
            self.icinga_status = max([max(self.suit_status), max(self.test_status), max(self.keyword_status, default=0)])
            result = "" if self.icinga_status == 0 else f" => {state2str(self.icinga_status)}"
            self.icinga_message = f"Robot listener {self.__class__.__name__}: {self.get_statistics()}{result}"
            self.icinga_message += "\n" + get_table(self.table_data_suites, self.table_cols, header=self.table_cols)
            return
        reasons = []
        # try to find a meaningfull descriptor
        if attrs["doc"] == "":
            lable = name
        else:
            lable = attrs["doc"]
        # if the icinga service has thresholds defined use them
        processed_status = STATE_OK # let's be optimistic for a change and make sure the var exists
        metric = self.get_metric_name(event_type)
        if metric in self.service_thresholds:
            d = self.service_thresholds[metric]
            warn = d["warning"]
            crit = d["critical"]
            if "status" in d:
                status = d["status"]
            else:
                status = "PASS"
            icinga_status = get_state(attrs["elapsedtime"], warn, crit, _operator="range")
            if icinga_status != STATE_OK:
                reasons.append(
                    {
                        "text": "- value={}, warning={}, critical={}".format(attrs["elapsedtime"], warn, crit),
                        "rf_status": "",
                        "status": state2str(icinga_status),
                        "type": "service_thresholds-threshold_violation",
                    }
                )
            self.icinga_perfdata.append(
                "{lable}={value}{unit};{warning};{critical}".format(
                    lable=lable, value=attrs["elapsedtime"], unit="ms", warning=warn, critical=crit
                )
            )
            # print(lable, self.service_thresholds, attrs['elapsedtime'], warn, crit, self.icinga_status)
            if attrs["status"] != status:
                robot_framework_status = STATE_CRIT
                reasons.append(
                    {
                        "text": "- status={}, expected={}".format(attrs["status"], status),
                        "rf_status": "",
                        "status": state2str(robot_framework_status),
                        "type": "service_thresholds-status_violation",
                    }
                )
            else:
                robot_framework_status = STATE_OK
            # go with the worse status
            processed_status = robot_framework_status if robot_framework_status >= icinga_status else icinga_status
        else:
            # no thresholds and not state overwrites only PASS or FAIL
            self.icinga_perfdata.append("'{lable}'={value}{unit}".format(lable=lable, value=attrs["elapsedtime"], unit="ms"))
            processed_status = STATE_OK if attrs["status"] == "PASS" else STATE_CRIT
        
        if processed_status == STATE_CRIT and len(self.failed_keywords) > 0 and self.ignore_keywords:
            # add keyword trace if keywords are ignored
            for failed_keyword in self.failed_keywords:
                #print(failed_keyword)
                reasons.append(
                    {
                        "text": "- keyword={}, line={}".format(failed_keyword["name"], failed_keyword["attrs"]["lineno"]),
                        "rf_status": failed_keyword["attrs"]["status"],
                        "status": state2str(processed_status),
                        "type": "keyword-failed",
                    }
                )
        # prepare data for table
        # for suite in suites
        # add suite
        # for reasons in suite
        # add reason
        # for tests in suite
        # add test
        # for reasons in test
        # add reason
        # for keywords in test
        # add keyword
        # for reasons in keyword
        # add reason
        if event_type == "keyword":
            self.keyword_status.append(processed_status)
            if processed_status != STATE_OK:
                # only add to table if not OK
                if len(reasons) == 0:
                    reason = "Robot Framework status"
                else:
                    reason = "Icinga threshold or status overwrite violation:"
                self.append_table_row(self.table_data_keywords, ["", "", lable, reason, attrs["status"], state2str(processed_status)])
                for r in reasons:
                    self.append_table_row(self.table_data_keywords, ["", "", "", r["text"], r["rf_status"], r["status"]])
        elif event_type == "test":
            self.test_status.append(processed_status)
            if processed_status != STATE_OK:
                # only add to table if not OK
                table_data_tests = []
                if len(reasons) == 0:
                    reason = "Robot Framework status"
                else:
                    reason = "Icinga threshold or status overwrite violation:"
                self.append_table_row(table_data_tests, ["", lable, "", reason, attrs["status"], state2str(processed_status)])
                for r in reasons:
                    self.append_table_row(table_data_tests, ["", "", "", r["text"], r["rf_status"], r["status"]])
                # reset keyword table
                self.table_data_tests = self.table_data_tests + table_data_tests + self.table_data_keywords
                # reset keyword table and failed keywords
                self.table_data_keywords = []
                self.failed_keywords = []
        elif event_type == "suite":
            self.suit_status.append(processed_status)
            # previous_messages = self.icinga_message
            if processed_status != STATE_OK:
                # only add to table if not OK
                table_data_suites = []
                if len(reasons) == 0:
                    reason = "Robot Framework status"
                else:
                    reason = "Icinga threshold or status overwrite violation:"
                self.append_table_row(table_data_suites, [attrs["longname"], "", "", reason, attrs["status"], state2str(processed_status)])
                for r in reasons:
                    self.append_table_row(table_data_suites, ["", "", "", r["text"], r["rf_status"], r["status"]])
                # reset test table
                self.table_data_suites = self.table_data_suites + table_data_suites + self.table_data_tests
                self.table_data_tests = []

    def start_suite(self, name, attrs):
        self.current_suite = {"suite": name, "attrs": attrs}

    def start_test(self, name, attrs):
        self.current_test = {"suite": self.current_suite["suite"], "test": name, "attrs": attrs}

    def start_keyword(self, name, attrs):
        self.current_keyword = {"suite": self.current_suite["suite"], "test": self.current_test["test"], "keyword": name, "attrs": attrs}

    def end_keyword(self, name, attrs):
        # print('keyword: ', name, attrs)
        # check for failed and add to queue - try to match to test (record test_test?)
        if attrs["status"] == "FAIL":
            # don't use attrs from start_keyword!
            self.failed_keywords.append(
                {"suite": self.current_suite["suite"], "test": self.current_test["test"], "name": name, "attrs": attrs}
            )
        if self.ignore_keywords:
            return
        self.process_data(name, "keyword", attrs)

    def end_test(self, name, attrs):
        # print('test: ', name, attrs)
        self.process_data(name, "test", attrs)

    def end_suite(self, name, attrs):
        # print('suite: ', name, attrs)
        self.process_data(name, "suite", attrs)

    def close(self):
        self.process_data("close", "close", {})
        self.set_service_status()
        print("failed keyword: ", self.failed_keywords)

    def message(self, message):
        # print('message: ', message)
        pass
