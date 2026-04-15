import time
import threading
from typing import Callable, List
from dataclasses import dataclass

@dataclass
class AlertRule:
    metric: str
    threshold: float
    operator: str

class BlockchainMonitor:
    def __init__(self, check_interval: int = 60):
        self.check_interval = check_interval
        self.alert_rules: List[AlertRule] = []
        self.alert_callbacks: List[Callable] = []
        self.running = False

    def register_alert(self, metric: str, threshold: float, operator: str) -> None:
        self.alert_rules.append(AlertRule(metric, threshold, operator))

    def add_alert_callback(self, callback: Callable) -> None:
        self.alert_callbacks.append(callback)

    def check_metric(self, metric: str, value: float) -> List[AlertRule]:
        triggered = []
        for rule in self.alert_rules:
            if rule.metric != metric:
                continue
            if rule.operator == "gt" and value > rule.threshold:
                triggered.append(rule)
            elif rule.operator == "lt" and value < rule.threshold:
                triggered.append(rule)
            elif rule.operator == "eq" and value == rule.threshold:
                triggered.append(rule)
        return triggered

    def start_monitor(self) -> None:
        self.running = True
        thread = threading.Thread(target=self._monitor_loop)
        thread.daemon = True
        thread.start()

    def stop_monitor(self) -> None:
        self.running = False

    def _monitor_loop(self) -> None:
        while self.running:
            self._run_checks()
            time.sleep(self.check_interval)

    def _run_checks(self) -> None:
        pass
