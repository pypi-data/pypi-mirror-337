from datetime import datetime

import matplotlib.pyplot as plt
import matplotlib.dates as mdates

from .benchmark import Benchmark


class BenchmarkVisualizer:
    def __init__(self, benchmark):
        """
        Initializes the visualizer with a Benchmark instance.

        :param benchmark: Benchmark instance containing execution times and timestamps
        """
        if not isinstance(benchmark, Benchmark):
            raise ValueError("The benchmark parameter must be an instance of the Benchmark class.")

        self.benchmark = benchmark

    def visualize_execution_times(self):
        """
        Visualizes the execution times as a time series with the timestamp of each run.
        """
        times = []
        timestamps = []

        for run_data in self.benchmark.get_execution_timeseries():
            timestamps.append(run_data["sent_at"])
            times.append(float(run_data["duration"]))

        # Convert timestamps to datetime for better plotting
        timestamps = [datetime.fromisoformat(ts) for ts in timestamps]

        # Plotting the data
        plt.figure(figsize=(10, 6))
        plt.plot(timestamps, times, marker='o', linestyle='-', color='b', label='Execution Time')

        # Formatting the plot
        plt.title('Benchmark Execution Time Over Runs')
        plt.xlabel('Timestamp (UTC)')
        plt.ylabel('Execution Time (seconds)')
        plt.xticks(rotation=45)
        plt.grid(True)

        # Format x-axis to show time properly
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))
        plt.gca().xaxis.set_major_locator(mdates.HourLocator())

        # Add a legend
        plt.legend()

        # Display the plot
        plt.tight_layout()
        plt.show()

    def visualize_execution_statistics(self):
        """
        Visualizes the minimum, maximum, and average execution time.
        """
        stats = self.benchmark.get_execution_results()

        min_time = float(stats["min_time"])
        max_time = float(stats["max_time"])
        avg_time = float(stats["avg_time"])

        # Plotting the statistics
        plt.figure(figsize=(6, 4))
        plt.bar(['Min Time', 'Max Time', 'Avg Time'], [min_time, max_time, avg_time], color=['g', 'r', 'b'])
        plt.title('Benchmark Execution Time Statistics')
        plt.ylabel('Execution Time (seconds)')

        # Display the plot
        plt.tight_layout()
        plt.show()