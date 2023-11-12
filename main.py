from pkg.yafs.topology import Topology
from pkg.yafs.application import Message, Application, fractional_selectivity
from pkg.yafs.population import Statical
from pkg.yafs.distribution import deterministic_distribution
from pkg.yafs.selection import First_ShortestPath
from pkg.yafs.placement import Placement
from pkg.yafs.core import Sim

# TOPOLOGY
topology_json = {}
topology_json["entity"] = []
topology_json["link"] = []

cloud_dev = {"id": 0, "model": "cloud", "mytag": "cloud",
             "IPT": 5000 * 10 ^ 6, "RAM": 40000, "COST": 3, "WATT": 20.0}
sensor_dev = {"id": 1, "model": "sensor-device",
              "IPT": 100 * 10 ^ 6, "RAM": 4000, "COST": 3, "WATT": 40.0}
actuator_dev = {"id": 2, "model": "actuator-device",
                "IPT": 100 * 10 ^ 6, "RAM": 4000, "COST": 3, "WATT": 40.0}

link1 = {"s": 0, "d": 1, "BW": 1, "PR": 10}
link2 = {"s": 0, "d": 2, "BW": 1, "PR": 1}

topology_json["entity"].append(cloud_dev)
topology_json["entity"].append(sensor_dev)
topology_json["entity"].append(actuator_dev)
topology_json["link"].append(link1)
topology_json["link"].append(link2)

t = Topology()
t.load(topology_json)


# In YAFS, it is possible to define broadcast messages.
# APLICATION
def create_application():
    a = Application(name="SimpleCase")

    # (S) --> (ServiceA) --> (A)
    a.set_modules([
        {"Sensor": {"Type": Application.TYPE_SOURCE}},
        {"ServiceA": {"RAM": 10, "Type": Application.TYPE_MODULE}},
        {"Actuator": {"Type": Application.TYPE_SINK}}
    ])

    """
    Messages among MODULES (AppEdge in iFogSim)
    """
    m_a = Message("M.A", "Sensor", "ServiceA",
                  instructions=20*10 ^ 6, bytes=1000)
    m_b = Message("M.B", "ServiceA", "Actuator",
                  instructions=30*10 ^ 6, bytes=500)

    """
    Defining which messages will be dynamically generated # the generation is controlled by Population algorithm
    """
    a.add_source_messages(m_a)

    """
    MODULES/SERVICES: Definition of Generators and Consumers (AppEdges and TupleMappings in iFogSim)
    """
    # MODULE SERVICES
    a.add_service_module(
        "ServiceA",
        m_a,
        m_b,
        fractional_selectivity,
        threshold=1.0
    )

    return a


app = create_application("Tutorial1")

# POPULATION
pop = Statical("Statical")
pop.set_src_control({
    "model": "sensor-device",
    "number": 1,
    "message": app.get_message("M.A"),
    "distribution": deterministic_distribution,
    "param": {"time_shift": 100}
})
pop.set_sink_control({
    "model": "actuator-device",
    "number": 1,
    "module": app.get_sink_modules()
})


# SELECTOR MODEL
selectorPath = First_ShortestPath()


# PLACEMENT ALGORITHM
class CloudPlacement(Placement):
    def initial_allocation(self, sim, app_name):
        # We find the ID-nodo/resource
        value = {"mytag": "cloud"}  # or whatever tag
        id_cluster = sim.topology.find_IDs(value)
        app = sim.apps[app_name]
        services = app.services

        for module in services:
            if module in self.scaleServices:
                for rep in range(0, self.scaleServices[module]):
                    idDES = sim.deploy_module(
                        app_name, module, services[module], id_cluster)


# it defines the deployed rules: module-device
placement = CloudPlacement("onCloud")
placement.scaleService({"ServiceA": 1})


# SIMULATE
s = Sim(t)  # t is the topology
simulation_time = 100000
s.deploy_app(app, placement, pop, selectorPath)
s.run(simulation_time, show_progress_monitor=False)
