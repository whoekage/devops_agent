import time
import json
from kubernetes import client, config, watch
from core.transport import ZeroMQTransport
from core.config import load_config

class KubernetesAgent:
    def __init__(self, zmq_address):
        self.transport = ZeroMQTransport(zmq_address)
        self.config = load_config()

        # Загружаем конфигурацию Kubernetes (локально или в кластере)
        config.load_kube_config()  # Для локального тестирования
        # config.load_incluster_config()  # Если агент работает внутри пода

        self.v1 = client.CoreV1Api()
        self.custom_api = client.CustomObjectsApi()

    def get_pods_status(self):
        """Получает информацию о подах во всех namespace"""
        print("[K8s Agent] Получаем список подов...")
        pods = self.v1.list_pod_for_all_namespaces(watch=False)
        pod_list = [
            {
                "namespace": pod.metadata.namespace,
                "name": pod.metadata.name,
                "status": pod.status.phase,
                "node": pod.spec.node_name,
                "restarts": sum(c.restart_count for c in pod.status.container_statuses or [])
            }
            for pod in pods.items
        ]
        return pod_list

    def get_nodes_usage(self):
        """Получает нагрузку на ноды (CPU/RAM)"""
        print("[K8s Agent] Получаем использование ресурсов нод...")
        metrics = self.custom_api.list_cluster_custom_object("metrics.k8s.io", "v1beta1", "nodes")
        node_usage = [
            {
                "name": node["metadata"]["name"],
                "cpu": node["usage"]["cpu"],
                "memory": node["usage"]["memory"],
            }
            for node in metrics["items"]
        ]
        return node_usage

    def get_events(self):
        """Получает последние события Kubernetes"""
        print("[K8s Agent] Получаем события Kubernetes...")
        events = self.v1.list_event_for_all_namespaces()
        event_list = [
            {
                "message": event.message,
                "reason": event.reason,
                "source": event.source.component,
                "timestamp": str(event.metadata.creation_timestamp)
            }
            for event in events.items
        ]
        return event_list

    def monitor_cluster(self):
        """Запускает сбор информации о кластере"""
        print("[K8s Agent] Запуск мониторинга Kubernetes...")

        # Собираем данные
        pods_status = self.get_pods_status()
        nodes_usage = self.get_nodes_usage()
        events = self.get_events()

        # Отправляем через ZeroMQ
        self.transport.send({"agent": "k8s_agent", "type": "pods_status", "data": pods_status})
        self.transport.send({"agent": "k8s_agent", "type": "nodes_usage", "data": nodes_usage})
        self.transport.send({"agent": "k8s_agent", "type": "events", "data": events})

    def monitor_events(self):
        """Слушает real-time события Kubernetes через Watch API"""
        print("[K8s Agent] Запуск live-мониторинга событий...")
        w = watch.Watch()

        for event in w.stream(self.v1.list_event_for_all_namespaces):
            event_data = {
                "agent": "k8s_agent",
                "type": event['type'],
                "message": event['object'].message,
                "reason": event['object'].reason,
                "source": event['object'].source.component,
                "timestamp": str(event['object'].metadata.creation_timestamp),
            }
            print(f"[K8s Agent] Новое событие: {event_data['message']}")
            self.transport.send(event_data)

    def run(self):
        """Основной цикл работы агента"""
        while True:
            try:
                self.monitor_cluster()
                print("[K8s Agent] Ожидание перед следующим запуском...")
                time.sleep(60)  # Запускаем проверку раз в минуту
            except Exception as e:
                print(f"[K8s Agent] Ошибка: {str(e)}")
                time.sleep(5)  # Пауза перед повторной попыткой