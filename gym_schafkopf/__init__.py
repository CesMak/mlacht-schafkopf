from gym.envs.registration import register

register(
    id="gym_schafkopf/Schafkopf-v0",
    entry_point="gym_schafkopf.envs:SchafkopfEnv",
)
