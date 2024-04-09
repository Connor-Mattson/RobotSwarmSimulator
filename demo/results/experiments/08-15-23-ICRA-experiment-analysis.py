import yaml
from src.novel_swarms.world.simulate import main as sim
from src.novel_swarms.config.AgentConfig import AgentConfigFactory
from src.novel_swarms.config.WorldConfig import RectangularWorldConfig

if __name__ == "__main__":
    # Load env from yaml
    with open("../out/Homoge-Fixed-1/n10-t4000-fixed/env.yaml") as yaml_config:
        env = yaml.safe_load(yaml_config)

    # Load Agent Config
    print(env["agent_config"])
    agent_conf = AgentConfigFactory.create(env["agent_config"])

    #########################
    # Play with Agent-Level Variables Here
    #########################
    agent_conf.turning_rate = -0.1
    agent_conf.forward_rate = 15.0
    ##########################

    if "init_type" in env and "file" in env["init_type"]:
        env["init_type"]["file"] = f'../../../{env["init_type"]["file"]}'

    # Load World
    world_conf = RectangularWorldConfig.from_dict(env)
    world_conf.addAgentConfig(agent_conf)
    world_conf.stop_at = None

    print(world_conf.init_type.as_dict())

    #########################
    # Play with World-Level Variables Here
    #########################
    # None
    ##########################

    # Simulate
    sim(world_config=world_conf)
