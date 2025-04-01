from itertools import product
from typing import Union

import numpy as np
import pulp as plp
from numpy.typing import NDArray

from mapc_optimal.constants import DATA_RATES, MAX_TX_POWER, MIN_SNRS, MIN_TX_POWER, NOISE_FLOOR
from mapc_optimal.main import Main
from mapc_optimal.pricing import Pricing
from mapc_optimal.utils import OptimizationType, dbm_to_lin, lin_to_dbm


class Solver:
    r"""
    The solver class coordinating the overall process of finding the optimal solution.
    It initializes the solver, sets up the network configuration, and manages the iterations.
    The optimization problem can be formulated in two ways:
    - the total throughput of the network is maximized,
    - the worst throughput of each node is maximized.

    Examples
    --------

    .. code-block:: python

       from mapc_optimal import Solver

       # Define your network
       # ...

       solver = Solver(stations, access_points)
       configurations, rate = solver(path_loss)


    .. note::
        The solver requires the path loss between each pair of nodes in the
        network. The reason for this is that the solver should be independent
        of the channel model used. Therefore, the path loss must be
        calculated beforehand. Note that if you do not require a specific
        channel model, you can use the provided function to calculate the
        path loss using the TGax channel model based on the positions of the
        nodes:


        .. code:: python

            import numpy as np
            from mapc_optimal import position_to_path_loss

            # Positions of the nodes as an array of `x` and `y` coordinates. `i`-th row represents the position
            # of the node with identifier `i` in the `stations` and `access_points` lists.
            pos = np.array([
              [x_0, y_0],
              [x_1, y_1],
              ...
              [x_n-1, y_n-1]
            ])

            # A matrix representing the walls in the environment (1 - wall, 0 - no wall between nodes `i` and `j`).
            walls = np.zeros((n, n))
            walls[i_0, j_0] = 1
            walls[i_1, j_1] = 1
            ...
            walls[i_m, j_m] = 1

            # n x n matrix representing the path loss between each pair of nodes.
            path_loss = position_to_path_loss(pos, walls)
    """

    def __init__(
            self,
            stations: list,
            access_points: list,
            channel_width: int = 20,
            mcs_data_rates: NDArray = None,
            min_snr: NDArray = None,
            max_tx_power: float = MAX_TX_POWER,
            min_tx_power: float = MIN_TX_POWER,
            noise_floor: float = NOISE_FLOOR,
            opt_type: OptimizationType = OptimizationType.MAX_MIN,
            max_iterations: int = 100,
            log_segments: int = 10,
            epsilon: float = 1e-5,
            solver: plp.LpSolver = None
    ) -> None:
        r"""
        .. note::
            Identifiers of the stations and APs should be unique and
            cover the range from :math:`0` to :math:`n - 1` (where :math:`n` is the
            total number of nodes in the network).

        .. note::
            The performance of the solver can significantly depend on the underlying
            mixed-integer linear programming solver. The default one is PULP_CBC,
            which is a free and open-source solver provided by the PuLP library.
            However, we recommend using a better solver, such as CPLEX.

        Parameters
        ----------
        stations: list
            Lists of numbers representing the stations.
        access_points: list
            Lists of numbers representing the access points (APs) in the network.
        channel_width: int, default=20
            The channel width used in the network (MHz).
        mcs_data_rates: NDArray, default=mapc_optimal.constants.DATA_RATES
            A list of data rates corresponding to the MCS values (Mb/s). IEEE 802.11be with 1 SS
            and 800 ns GI data rates are used by default.
        min_snr: NDArray, default=mapc_optimal.constants.MIN_SNRS
            The minimum SNR required for a successful transmission (dB) for each MCS value. Empirically 
            determined in ns-3 simulations by default.
        max_tx_power: float, default=20.0
            The maximum transmission power (dBm) available.
        min_tx_power: float, default=10.0
            The minimum transmission power (dBm) that can be used.
        noise_floor: float, default=-93.97
            The level of noise in the environment (dBm).
        opt_type: OptimizationType, default=OptimizationType.MAX_MIN
            The type of optimization problem to solve. The max min problem is solved by default.
        max_iterations: int, default=100
            The maximum number of iterations of the solver.
        log_segments: int, default=10
            The number of linear function segments used to approximate the logarithm function in proportional fairness setting.
        epsilon: float, default=1e-5
             The minimum value of the pricing objective function to continue the iterations.
        solver: pulp.LpSolver, default=pulp.PULP_CBC_CMD(msg=False)
            The solver used to solve the optimization problems.
        """

        if mcs_data_rates is None:
            mcs_data_rates = DATA_RATES[channel_width]

        if min_snr is None:
            min_snr = MIN_SNRS[channel_width]

        self.stations = stations
        self.access_points = access_points
        self.mcs_values = range(len(mcs_data_rates))
        self.mcs_data_rates = mcs_data_rates
        self.min_sinr = dbm_to_lin(min_snr)
        self.max_tx_power = dbm_to_lin(max_tx_power).item()
        self.min_tx_power = dbm_to_lin(min_tx_power).item()
        self.noise_floor = dbm_to_lin(noise_floor).item()
        self.opt_type = opt_type
        self.max_iterations = max_iterations
        self.log_approx = self._linearize_log(log_segments)
        self.epsilon = epsilon
        self.solver = solver or plp.PULP_CBC_CMD(msg=False)
        self.M = len(stations) * mcs_data_rates[-1]  # Maximum achievable throughput

        self.main = Main(
            log_approx=self.log_approx,
            opt_type=self.opt_type,
            solver=self.solver,
            M=self.M
        )
        self.pricing = Pricing(
            mcs_values=self.mcs_values,
            mcs_data_rates=self.mcs_data_rates,
            min_sinr=self.min_sinr,
            max_tx_power=self.max_tx_power,
            min_tx_power=self.min_tx_power,
            noise_floor=self.noise_floor,
            log_approx=self.log_approx,
            opt_type=self.opt_type,
            solver=self.solver
        )

    @staticmethod
    def _linearize_log(k: int, min_val: float = 0, max_val: float = 3) -> tuple[NDArray, NDArray]:
        """
        Linearizes the logarithm function by approximating it with a piecewise linear function.

        Parameters
        ----------
        k : int
            Number of segments used to approximate the logarithm function.
        min_val : float, default=0
            Minimum value of the logarithm. Note! The value is in the log10 scale.
        max_val : float, default=3
            Maximum value of the logarithm. Note! The value is in the log10 scale.

        Returns
        -------
        slopes, biases : tuple[NDArray, NDArray]
            Arrays containing the slopes and biases of the linear functions.
        """

        xs = np.logspace(min_val, max_val, k + 1, base=10)
        ys = np.log10(xs)

        xs1, xs2 = xs[:-1], xs[1:]
        ys1, ys2 = ys[:-1], ys[1:]

        slopes = (ys2 - ys1) / (xs2 - xs1)
        biases = ys1 - xs1 * slopes

        return slopes, biases

    def _tx_possible(self, path_loss: float) -> bool:
        """
        Checks if any transmission is possible for a given path loss.

        Parameters
        ----------
        path_loss : float
            Path loss between the transmitter and the receiver.

        Returns
        -------
        is_tx_possible : bool
            True if a transmission is possible, False otherwise.
        """
        
        return self.max_tx_power >= self.min_sinr[0] * path_loss * self.noise_floor

    def _generate_data(self, path_loss: NDArray, associations: dict = None) -> dict:
        """
        Generates the data required for the solver, such as the links, the stations, and the access points
        in the network, the path loss between each pair of nodes, and the maximum interference level.
        
        Parameters
        ----------
        path_loss : NDArray
            Matrix containing the path loss between each pair of nodes.
        associations : dict
            The dictionary of associations between APs and stations.

        Returns
        -------
        problem_data : dict
            Dictionary containing the data required for the solver.
        """

        links = []

        if associations is None:
            for s in self.stations:
                best_pl = float('inf')
                best_ap = None

                for a in self.access_points:
                    if path_loss[a, s] < best_pl:
                        best_pl = path_loss[a, s]
                        best_ap = a

                if self._tx_possible(best_pl):
                    links.append((f'AP_{best_ap}', f'STA_{s}'))
        else:
            for a, stations in associations.items():
                for s in stations:
                    if self._tx_possible(path_loss[a, s]):
                        links.append((f'AP_{a}', f'STA_{s}'))

        problem_data = {
            'stations': [f'STA_{s}' for s in self.stations],
            'access_points': [f'AP_{a}' for a in self.access_points],
            'links': links,
            'link_node_a': {l: l[0] for l in links},  # APs
            'link_node_b': {l: l[1] for l in links},  # STAs
        }

        link_path_loss = {(f'AP_{a}', f'STA_{s}'): path_loss[a, s].item() for a, s in product(self.access_points, self.stations)}
        max_interference = {}

        for l, m in product(links, self.mcs_values):
            max_interference[l, m] = sum(
                self.max_tx_power * (self.min_sinr[m] * link_path_loss[l] / link_path_loss[i, problem_data['link_node_b'][l]]) +
                self.min_sinr[m] * link_path_loss[l] * self.noise_floor
                for i in problem_data['access_points'] if i != problem_data['link_node_a'][l]
            )

        problem_data['link_path_loss'] = link_path_loss
        problem_data['max_interference'] = max_interference
        return problem_data

    def __call__(
            self, 
            path_loss: NDArray,
            associations: dict = None,
            baseline: dict = None,
            return_objectives: bool = False
    ) -> Union[tuple[dict, float], tuple[dict, float, list[float]]]:
        """
        Solves the MAPC C-SR problem given the path loss between each pair of nodes in the network.
        Returns the final configurations, the time shares, and the total throughput.

        Parameters
        ----------
        path_loss : NDArray
            Matrix containing the path loss between each pair of nodes.
        associations : dict
            The dictionary of associations between APs and stations.
        baseline : dict, default=None
            Dictionary containing the baseline rates of the links (only used for the max-min optimization with baseline).
        return_objectives : bool, default=False
            Flag indicating whether to return the pricing objective values.

        Returns
        -------
        result : tuple[dict, float] or tuple[dict, float, list[float]]
            Tuple containing the final configurations and the total throughput. Additionally, 
            the solver can return a list of the pricing objective values for each iteration. 
            It can be useful to check if the solver has converged.
        """

        assert not self.opt_type == OptimizationType.MAX_MIN_BASELINE or baseline is not None, \
            'Baseline rates must be provided for the max-min optimization with baseline.'

        main_baseline = None
        if baseline is not None:
            main_baseline = {sta: 0.0 for sta in baseline}

        path_loss = dbm_to_lin(path_loss)
        problem_data = self._generate_data(path_loss, associations)

        if len(problem_data['links']) == 0:
            if return_objectives:
                return {}, 0, []
            else:
                return {}, 0.

        configuration = self.pricing.initial_configuration(
            links=problem_data['links'],
            link_path_loss=problem_data['link_path_loss']
        )

        pricing_objectives = []

        for _ in range(self.max_iterations):
            main_result, main_objective = self.main(
                stations=problem_data['stations'],
                link_node_b=problem_data['link_node_b'],
                conf_links=configuration['conf_links'],
                conf_link_rates=configuration['conf_link_rates'],
                conf_total_rates=configuration['conf_total_rates'],
                confs=configuration['confs'],
                baseline=main_baseline
            )
            main_baseline = baseline

            configuration, pricing_objective = self.pricing(
                dual_alpha=main_result['alpha'],
                dual_beta=main_result['beta'],
                dual_gamma=main_result['gamma'],
                stations=problem_data['stations'],
                access_points=problem_data['access_points'],
                links=problem_data['links'],
                link_node_a=problem_data['link_node_a'],
                link_node_b=problem_data['link_node_b'],
                link_path_loss=problem_data['link_path_loss'],
                max_interference=problem_data['max_interference'],
                configuration=configuration
            )
            pricing_objectives.append(pricing_objective)

            if abs(pricing_objective) <= self.epsilon:
                break

        result = {
            'links': configuration['conf_links'],
            'link_rates': configuration['conf_link_rates'],
            'total_rates': configuration['conf_total_rates'],
            'tx_power': {c: {l: lin_to_dbm(p).item() for l, p in tx_power.items()} for c, tx_power in configuration['conf_link_tx_power'].items()},
            'shares': main_result['shares']
        }
        total_rate = sum(result['total_rates'][c] * result['shares'][c] for c in result['shares'])

        if return_objectives:
            return result, total_rate, pricing_objectives
        else:
            return result, total_rate
