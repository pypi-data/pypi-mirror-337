import torch
import random
import numpy
import pickle

from typing import List, Union


class Save:
    def __init__(self) -> None:
        self.np_random_state = None
        self.np_random_state_path = "numpy_random_state.pkl"
        self.init_np_random_state()

    def init_np_random_state(self):
        if os.path.exists(self.np_random_state_path):
            with open(self.np_random_state_path, "rb") as f:
                self.np_random_state = np.load(f, allow_pickle=True)
                np.random.set_state(self.np_random_state)

    def dump_np_random_state(self):
        with open("client_manager.pkl", "wb") as f:
            pickle.dump(self.np_random_state, f)

    def numbers(self):
        print_random()
        # update random state
        self.np_random_state = np.random.get_state()


class Checkpoint:
    def __init__(
        self,
        numpy_flag: bool = True,
        random_flag: bool = True,
        torch_flag: bool = True,
        cuda_devices: Union[List[int], List[str], List[torch.device]] = None,
        RNG_state_path: str = "rng_state.pkl",
    ) -> None:
        """
        check point for state of model, PRNG
        """
        self.numpy_flag = numpy_flag
        self.random_flag = random_flag
        self.torch_flag = torch_flag
        self.cuda_devices = cuda_devices

        self.numpy_random_state = None
        self.random_random_state = None
        self.torch_random_state = [None for _ in range(1 + len(cuda_devices))]

        self.RNG_state_path = RNG_state_path

    def save_RNG_state(self):
        if self.numpy_flag:
            self.save_numpy_RNG_state()
        if self.random_flag:
            self.save_random_RNG_state()
        if self.torch_flag:
            self.save_torch_RNG_state()

    def save_RNG_state_to_file(self):
        data = [
            self.numpy_random_state,
            self.random_random_state,
            [tensor.numpy() for tensor in self.torch_random_state],
        ]
        with open(self.RNG_state_path, "wb") as f:
            pickle.dump(data, f)

    def save_numpy_RNG_state(self):
        # tuple
        self.numpy_random_state = numpy.random.get_state()

    def save_random_RNG_state(self):
        # tuple
        self.random_random_state = random.getstate()

    def save_torch_RNG_state(self):
        self.torch_random_state[0] = torch.random.get_rng_state()
        for index, cuda_device in enumerate(self.cuda_devices):
            self.torch_random_state[index + 1] = torch.cuda.random.get_rng_state(
                cuda_device
            )

    def load(self):
        pass
