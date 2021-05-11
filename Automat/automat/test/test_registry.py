from automat.registry import Registry, Heartbeat
import time

def test_registry():
    age = 1

    r = Registry(age=age)
    heart_beat = Heartbeat(host="url", port="80", tag="someKP")
    r.refresh(heart_beat)
    response = r.get_registry()
    # shoule
    assert len(response) > 0
    assert response[heart_beat.tag]['status'] == Registry.LABELS[Registry.TTL_ALIVE]
    time.sleep(Registry.TTL_WARNING + r.age)
    response = r.get_registry()
    assert response[heart_beat.tag]['status'] == Registry.LABELS[Registry.TTL_WARNING]
    time.sleep(Registry.TTL_OFFLINE + r.age)
    response = r.get_registry()
    assert response[heart_beat.tag]['status'] == Registry.LABELS[Registry.TTL_OFFLINE]
    time.sleep(Registry.TTL_DELETE_ENTRY + r.age)
    response = r.get_registry()
    #
    response = r.get_registry()
    assert len(response) == 0