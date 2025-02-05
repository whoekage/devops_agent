from kubernetes import client, config

def view_pod_logs(namespace: str, pod_name: str, container: str = None) -> str:
    """
    Получает логи указанного пода в заданном неймспейсе.

    Args:
        namespace (str): Namespace, где находится под.
        pod_name (str): Имя пода.
        container (str, optional): Имя контейнера (если в поде несколько контейнеров).

    Returns:
        str: Логи пода или сообщение об ошибке.
    """
    try:
        try:
            config.load_kube_config()
        except Exception:
            config.load_incluster_config()
        v1 = client.CoreV1Api()
        log = v1.read_namespaced_pod_log(name=pod_name, namespace=namespace, container=container)
        print(f"[DEBUG] Получены логи пода '{pod_name}' в неймспейсе '{namespace}': {log}")
        return log
    except Exception as e:
        return f"Ошибка получения логов: {str(e)}"

def add_two_numbers(a: int, b: int) -> int:
    """
    Складывает два целых числа.

    Args:
        a (int): Первое число.
        b (int): Второе число.

    Returns:
        int: Сумма двух чисел.
    """
    return a + b
