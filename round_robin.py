class RoundRobin:
    def processData(self, no_of_processes, time_quantum):
        process_data = []
        for i in range(no_of_processes):
            process_id = int(input("Enter Process ID: "))
            arrival_time = int(input(f"Enter Arrival Time for Process {process_id}: "))
            burst_time = int(input(f"Enter Burst Time for Process {process_id}: "))
            process_data.append([process_id, arrival_time, burst_time, burst_time, 0])
        self.schedulingProcess(process_data, time_quantum)

    def schedulingProcess(self, process_data, time_quantum):
        total_time = sum(p[2] for p in process_data)

        gantt_chart = []
        current_time = 0

        while True:
            is_completed = True
            for process in process_data:
                if process[3] > 0:
                    is_completed = False
                    if process[3] > time_quantum:
                        current_time += time_quantum
                        process[3] -= time_quantum
                    else:
                        current_time += process[3]
                        process[3] = 0
                    gantt_chart.append((process[0], current_time))

            if is_completed:
                break

        self.printGanttChart(gantt_chart)
        t_time = self.calculateTurnaroundTime(process_data)
        w_time = self.calculateWaitingTime(process_data)
        self.printData(process_data, t_time, w_time)

    def calculateTurnaroundTime(self, gantt_chart):
        process_ids = set(entry[0] for entry in gantt_chart)
        turnaround_times = {}
        for process_id in process_ids:
            arrival_time = gantt_chart[0][1]
            completion_time = gantt_chart[-1][1]
            for entry in reversed(gantt_chart):
                if entry[0] == process_id:
                    completion_time = entry[1]
                    break
            turnaround_time = completion_time - arrival_time
            turnaround_times[process_id] = turnaround_time
        average_turnaround_time = sum(turnaround_times.values()) / len(turnaround_times)
        return average_turnaround_time

    def calculateWaitingTime(self, gantt_chart):
        process_ids = set(entry[0] for entry in gantt_chart)
        waiting_times = {}
        for process_id in process_ids:
            burst_time = 0
            completion_time = 0
            for entry in gantt_chart:
                if entry[0] == process_id:
                    burst_time += entry[1] - completion_time
                    completion_time = entry[1]
            waiting_time = burst_time
            waiting_times[process_id] = waiting_time
        average_waiting_time = sum(waiting_times.values()) / len(waiting_times)
        return average_waiting_time

    def printGanttChart(self, gantt_chart):
        print("Gantt Chart:")
        print("+" + "-" * (len(gantt_chart) * 6) + "+")
        for entry in gantt_chart:
            print(f"|  P{entry[0]}  ", end="")
        print("|")
        print("+" + "-" * (len(gantt_chart) * 6) + "+")
        print("0", end="")
        for entry in gantt_chart:
            print(f"     {entry[1]}", end="")
        print("\n")

    def printData(self, process_data, average_turnaround_time, average_waiting_time):
        process_data.sort(key=lambda x: x[0])  # Sort processes according to the Process ID

        print("Process_ID  Arrival_Time  Burst_Time   Completion_Time  Turnaround_Time  Waiting_Time")

        for i in range(len(process_data)):
            for j in range(len(process_data[i])):
                print(process_data[i][j], end="              ")
            print()

        print(f'Average Turnaround Time: {average_turnaround_time}')
        print(f'Average Waiting Time: {average_waiting_time}')

if __name__ == "__main__":
    no_of_processes = int(input("Enter number of processes: "))
    time_quantum = int(input("Enter the time quantum: "))
    round_robin = RoundRobin()
    round_robin.processData(no_of_processes, time_quantum)
