import addict

from ...utils import (
    AbstractAdversity,
    derive_lane_change_adversarial_command,
    get_location,
)


class LanechangeAdversity(AbstractAdversity):
    def trigger(self, obs_dict) -> bool:
        """Determine when to trigger the LanechangeAdversity module.

        Args:
            obs_dict (dict): Observation of the ego agent.

        Returns:
            bool: Flag to indicate if the LanechangeAdversity module should be triggered.
        """
        self._adversarial_command_dict = addict.Dict()
        vehicle_location = get_location(
            obs_dict["ego"]["veh_id"], obs_dict["ego"]["lane_id"]
        )
        if vehicle_location == self._location:
            adversarial_command_dict = derive_lane_change_adversarial_command(obs_dict)
            for key, command in adversarial_command_dict.items():
                adversarial_mode = command.info.get("adversarial_mode", None)
                if adversarial_mode == "LeftFoll" or adversarial_mode == "RightFoll":
                    self._adversarial_command_dict[key] = command
        if self._adversarial_command_dict:
            return True
        else:
            return False

    def derive_command(self, obs_dict) -> addict.Dict:
        """Derive the adversarial command based on the observation.

        Args:
            obs_dict (dict): Observation of the ego agent.

        Returns:
            addict.Dict: Adversarial command.
        """
        if self._probability > 0 and self.trigger(obs_dict):
            for key, command in self._adversarial_command_dict.items():
                command.prob = self._probability
                command.info.update(
                    {
                        "predicted_collision_type": self._predicted_collision_type,
                        "vehicle_location": self._location,
                    }
                )
            return self._adversarial_command_dict
        return addict.Dict()
