from datetime import datetime
import socket
from lib.icinga import api_post
from lib.globals import STATE_CRIT, STATE_OK, STATE_UNKNOWN, STATE_WARN

__version__ = "0.0.3"

class icinga:

    ROBOT_LISTENER_API_VERSION = 2
    ROBOT_LIBRARY_SCOPE = "GLOBAL"

    def __init__(self, api_user="", api_pass="", icinga_fqdn="", host_name=None, service_name="", ttl=300):
        self.ROBOT_LIBRARY_LISTENER = self

        current_time = datetime.now()
        self.current_ts = int(current_time.timestamp()) * 1000

        self.api_user = api_user
        self.api_password = api_pass
        self.icinga = icinga_fqdn
        self.fqdn = socket.getfqdn().lower()
        if host_name is None:
            self.host_name = self.fqdn
        else:
            self.host_name = host_name
        self.service_name = service_name
        self.ttl = ttl
        self.service_name_suite = ''
        self.icinga_status = STATE_OK
        self.icinga_message = ''
        self.icinga_perfdata = ''
        self.last_failed_keyword = ''
        self.last_failed_test = ''
        pass

    def set_service_status(self,
                    performance_data=False,
                    check_command=False,
                    check_source=False,
                    execution_start=False,
                    execution_end=False,
                    ttl=False):
        uri = "https://{}:5665/v1/actions/process-check-result".format(
            self.icinga)
        data = {
            'type': 'Service',
            'filter': 'host.name==host_name && service.name==service_name',
            'filter_vars': {
                'host_name': self.host_name,
                'service_name': self.service_name
            },
            'exit_status': self.icinga_status,
            'plugin_output': self.icinga_message
        }
        if self.icinga_perfdata:
            data['performance_data'] = self.icinga_perfdata
        data['check_command'] = self.__class__.__name__
        data['check_source'] = self.fqdn
        if execution_start:
            data['execution_start'] = execution_start
        if execution_end:
            data['execution_end'] = execution_end
        if self.ttl:
            data['ttl'] = self.ttl
        #print("Icinga: set_service_status(): ", data)
        return_code, result = api_post(
            uri=uri,
            username=self.api_user,
            password=self.api_password,
            data=data)
        if return_code:
            print("Icinga: set_service_status(): successfull")
        else:
            print("Icinga: set_service_status(): failed")
            print("Icinga: set_service_status(): ", return_code, result)
            return False
        return True

    def end_keyword(self, name, attrs):
        #print("end_keyword", name)
        #print(attrs)
        if attrs['doc'] == '':
            lable = name
        else:
            lable = attrs['doc']
        self.icinga_perfdata += " '{lable}'={value}{unit}".format(
            lable = lable,
            value = attrs['elapsedtime'],
            unit = 'ms'
        )
        if attrs['status'] != 'PASS':
            self.icinga_status = STATE_CRIT
            self.last_failed_keyword = "{} {}: {}\n".format(lable, attrs['args'], attrs['status'] )
        pass

    def end_test(self, name, attrs):
        #print("end_test", name)
        #print(attrs)
        if attrs['doc'] == '':
            lable = name
        else:
            lable = attrs['doc']
        if attrs['status'] != 'PASS':
            self.last_failed_test = "{} {}: {}\n".format(lable, attrs['args'], attrs['status'] )
            self.icinga_message = "{}\n{}".format(self.last_failed_test, self.last_failed_keyword)
        pass

    def end_suite(self, name, attrs):
        #print("end_suite", name)
        #print(attrs)
        if attrs['status'] == 'PASS':
            self.icinga_message = "Test Suite {}: {} {}".format(attrs['longname'], attrs['statistics'], attrs['status'])
        else:
            self.icinga_message = "Test Suite {}: {} {}\n{}\n{}".format(attrs['longname'], attrs['statistics'], attrs['status'], self.last_failed_test, self.last_failed_keyword)
        pass

    def close(self):
        self.set_service_status()
        pass