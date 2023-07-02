# coding: utf-8

import sys
sys.path.append('/home/dharal1/forcepoint/')    # path to config.py file
from config import api_url, api_key, api_version, api_port        # for SMC API access
from smc import session     # for SMC API login logout
from smc_monitoring.monitors.logs import LogQuery   # for get logs
from smc_monitoring.models.filters import InFilter  # add filter for query
from smc_monitoring.models.values import FieldValue, ConstantValue  # use values of SMC API
from smc_monitoring.models.constants import LogField, Alerts, Actions   # use constants of SMC API
from prometheus_client import start_http_server, REGISTRY
from prometheus_client.core import GaugeMetricFamily  # metrics prometheus
from time import sleep
from datetime import datetime, timedelta
import logging  # for debugging

# debugging
logging.getLogger()
logging.basicConfig(
    level=logging.DEBUG, format='%(asctime)s %(levelname)s %(name)s.%(funcName)s: %(message)s')

# constant of metrics
DATE_TIME = 0
SRC_ADDR = 1
SEVERITY = 2
DST_ADDR = 3
DST_PORT = 4
SITUATION = 5
H_REF = 6
ATTACKER_IP = 7
TARGET_IP = 8
FACILITY = 9
EVENT_ID = 10
METRICS_VALUES = 11

# logs history
previous_logs = []
# first execution
is_first_query = True


class Collector(object):
    # Class role is to collect prometheus metrics on logs Forcepoint Firewall SMC

    def __init__(self):
        pass

    # fill metrics with the value of the reference (only if reference exist)
    def __add_metrics_values__(self, log_ref, metrics, value):
        ref = {
            "Src Addr": SRC_ADDR,
            "Severity": SEVERITY,
            "Situation": SITUATION,
            "Creation Time": DATE_TIME,
            "Dst Port": DST_PORT,
            "Dst Addr": DST_ADDR,
            "acknowledge_href": H_REF,
            "Attacker IP": ATTACKER_IP,
            "Target IP": TARGET_IP,
            "Facility": FACILITY,
            "Event ID": EVENT_ID
        }

        if log_ref in ref:
            metrics[ref.get(log_ref)] = value

    def collect(self):
        global is_first_query, previous_logs

        # login to session SMC API Forcepoint
        session.login(url=api_url()+":"+api_port(),     # IP address of SMC API
                      api_key=api_key(),        # API key to login session
                      api_version=api_version(),  # version of API
                      verify=False)             # no certificate needed

        # logs query configuration
        query = LogQuery(fetch_size=None,       # max size allowed
                         fetch_type="stored",   # stored on SMC
                         backwards=True)        # lasted in last (in the result)
        query.time_range.last_hour()
        query.format.timezone("CET")    # Central European Time - (UTC + 1)
        query.add_and_filter([          # severity: critical and action: terminate
            InFilter(
                FieldValue(LogField.ALERTSEVERITY),
                [ConstantValue(Alerts.CRITICAL)]
            ),
            InFilter(
                FieldValue(LogField.ACTION),
                [ConstantValue(Actions.TERMINATE)]
            )
        ])

        # metric definition for total event number
        metric_total_event = GaugeMetricFamily(
            "forcepoint_total_event", "Nombre total d'alertes",
            labels=["nombre_event"])
        # metrics definition for alert details
        metric_priority_event = GaugeMetricFamily("forcepoint_priority_event", "Détails des alertes",
                                                  labels=["date_time",
                                                          "src_addr",
                                                          "severity",
                                                          "dst_addr",
                                                          "situation",
                                                          "h_ref",
                                                          "attacker_ip",
                                                          "target_ip",
                                                          "facility",
                                                          "event_id"])

        # current time
        now = datetime.today()
        # logs recovery date
        last_time = now - timedelta(days=0, hours=1)
        # string of current time
        now_str = now.strftime("%Y-%m-%d %H:%M:%S")
        # string of last time
        last_time_str = last_time.strftime(
            "%Y-%m-%d %H:%M:%S")
        # total of logs
        nb_alerts = 0

        # set to good format
        last_time = last_time.strptime(
            last_time_str, "%Y-%m-%d %H:%M:%S")

        # execute the query
        query_result = list(query.fetch_raw())

        for log in query_result:
            for elem in log:  # read each alerts
                # index of the value inside the alert
                index = 0
                # final metrics tab of the alert
                metrics_values = [''] * METRICS_VALUES
                # the alert
                str_elem = str(elem)

                # parse alert fields
                str_elem = str_elem.replace("\'}", '')
                str_tab_elem_priority = str_elem.split("\', \'")

                while index < len(str_tab_elem_priority):
                    # get each values inside alert field
                    str_tab_elem_values = str_tab_elem_priority[index].split(
                        "\': \'")

                    # fill metrics tab the log metrics values we want to transform
                    self.__add_metrics_values__(
                        log_ref=str_tab_elem_values[0], # name of the value
                        metrics=metrics_values,         # tab we want to fill
                        value=str_tab_elem_values[1]    # the value
                    )

                    index += 1  # switch to next field inside the alert

                new_metrics = False  # considering current log will be not adding to prometheus
                if is_first_query == True:
                    # add in logs history the current log
                    previous_logs.append(metrics_values)
                    # adding log to prometheus on first function call
                    new_metrics = True
                elif is_first_query == False:
                    # considering the current log is not in previous logs list
                    in_previous_logs = False
                    # verify if the current logs is in previous logs list
                    for previous_log in previous_logs:
                        # comparing event ID
                        if metrics_values[EVENT_ID] in previous_log:
                            in_previous_logs = True  # current log is in previous log

                    # adding current log that is not in previous logs in previous logs list
                    if in_previous_logs == False:
                        # add in the list of previous logs the new log
                        previous_logs.append(metrics_values)
                        new_metrics = True  # set 'True' to be added in prometheus

                if new_metrics == True:
                    # add metrics in prometheus
                    metric_priority_event.add_metric(
                        labels=[metrics_values[DATE_TIME],
                                metrics_values[SRC_ADDR],
                                metrics_values[SEVERITY],
                                metrics_values[DST_ADDR],
                                metrics_values[SITUATION],
                                metrics_values[H_REF],
                                metrics_values[ATTACKER_IP],
                                metrics_values[TARGET_IP],
                                metrics_values[FACILITY],
                                metrics_values[EVENT_ID]
                                ],
                        value=str(metrics_values[DST_PORT]))

                nb_alerts += 1  # next alert

        # only on not first function call
        if is_first_query == False:
            index = 1  # index in previous logs
            for log in previous_logs[:]:
                # covert log date to datetime type
                log_date = datetime.strptime(
                    log[DATE_TIME], "%Y-%m-%d %H:%M:%S (CET)")
                # delete outdated log
                if log_date < last_time:
                    del previous_logs[previous_logs.index(log)]

        # for debugging
        for log in previous_logs:
            print(log)
        print("")
        print(f"nb alertes: {nb_alerts}\n")

        # add metric for alerts number
        metric_total_event.add_metric(labels=["1h"], value=nb_alerts)

        # after the first function call this boolean is set on False for the rest of the execution
        is_first_query = False

        session.logout()  # quit session

        # Collector() return all metrics
        yield metric_total_event
        yield metric_priority_event


if __name__ == "__main__":
    start_http_server(9401)  # http server on localhost and port :9401
    REGISTRY.register(Collector())
    while True:
        sleep(60)
