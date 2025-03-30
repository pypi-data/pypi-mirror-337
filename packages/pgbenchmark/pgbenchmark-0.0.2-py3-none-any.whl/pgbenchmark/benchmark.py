import os
import time
import psycopg2
from psycopg2.extras import execute_values
from datetime import datetime, timezone


class Benchmark:
    def __init__(self, db_connection=None, number_of_runs=1):
        """
        Initialize the benchmark with a database connection and configuration.

        :param db_connection: psycopg2 database connection
        :param number_of_runs: Number of times to execute the query
        """
        self.sql_query = None
        self.db_connection = db_connection
        self.number_of_runs = number_of_runs
        self.execution_times = []
        self._paused = False
        self._run_timestamps = []  # Store timestamps of each run

    def set_sql(self, query: str):
        """
        Sets the SQL query to be benchmarked. If a file path is provided, it reads the SQL from the file.

        :param query: File path or raw SQL query
        """
        if os.path.isfile(query):
            with open(query, "r", encoding="utf-8") as file:
                self.sql_query = file.read().strip()
        else:
            self.sql_query = query

    def get_sql(self):
        """Returns the currently set SQL query."""
        return self.sql_query

    # TODO: WIP
    # def pause(self):
    #     """Pauses the benchmark execution."""
    #     self._paused = True
    #     print("Benchmark paused. Call resume() to continue.")
    #
    # def resume(self):
    #     """Resumes the benchmark execution."""
    #     self._paused = False
    #     print("Benchmark resumed.")

    def execute_benchmark(self):
        """
        Executes the SQL query multiple times and records execution time, allowing for pausing.
        """
        if not self.db_connection:
            raise ValueError("Database connection is not set.")
        if not self.sql_query:
            raise ValueError("SQL query is not set.")

        cursor = self.db_connection.cursor()

        self.execution_times = []
        self._run_timestamps = []
        for i in range(self.number_of_runs):
            while self._paused:
                time.sleep(0.1)
            start_time = time.time()
            timestamp_sent = datetime.now(timezone.utc)
            cursor.execute(self.sql_query)
            self.db_connection.commit()
            end_time = time.time()
            self.execution_times.append(end_time - start_time)
            self._run_timestamps.append({
                "sent_at": timestamp_sent.isoformat(),
                "duration": format(end_time - start_time, '.6f').rstrip('0').rstrip('.')
            })

        cursor.close()

    def get_execution_results(self):
        """Returns a summary of execution times with fixed decimal formatting (6 decimal places)."""
        if not self.execution_times:
            raise ValueError("Benchmark has not been run yet.")

        return {
            "runs": self.number_of_runs,
            "min_time": format(min(self.execution_times), '.6f').rstrip('0').rstrip('.'),
            "max_time": format(max(self.execution_times), '.6f').rstrip('0').rstrip('.'),
            "avg_time": format(sum(self.execution_times) / self.number_of_runs, '.6f').rstrip('0').rstrip('.')
        }

    def get_execution_timeseries(self):
        """
        Generator that yields benchmark run data with timestamp and duration
        when number_of_runs is more than 1000.
        """
        if not self.execution_times:
            raise ValueError("Benchmark has not been run yet.")
        # if self.number_of_runs <= 1000:
        #     raise ValueError("Number of runs must be greater than 1000 to get timeseries.")
        if len(self._run_timestamps) != self.number_of_runs:
            raise ValueError("Internal error: run timestamps not recorded correctly.")

        for run_data in self._run_timestamps:
            yield run_data
