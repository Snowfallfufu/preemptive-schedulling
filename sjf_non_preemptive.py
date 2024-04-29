class SJF:

    def processData(self, no_of_processes):
        process_data = []
        for i in range(no_of_processes):
            temporary = []
            process_id = int(input("Enter Process ID: "))
            arrival_time = int(input(f"Enter Arrival Time for Process {process_id}: "))
            burst_time = int(input(f"Enter Burst Time for Process {process_id}: "))
            temporary.extend([process_id, arrival_time, burst_time, 0])
            process_data.append(temporary)
        self.schedulingProcess(process_data)

    def schedulingProcess(self, process_data):
        start_time = []
        exit_time = []
        s_time = 0
        process_data.sort(key=lambda x: x[1])

        for i in range(len(process_data)):
            ready_queue = []
            temp = []
            normal_queue = []

            for j in range(len(process_data)):
                if (process_data[j][1] <= s_time) and (process_data[j][3] == 0):
                    temp.extend([process_data[j][0], process_data[j][1], process_data[j][2]])
                    ready_queue.append(temp)
                    temp = []
                elif process_data[j][3] == 0:
                    temp.extend([process_data[j][0], process_data[j][1], process_data[j][2]])
                    normal_queue.append(temp)
                    temp = []

            if len(ready_queue) != 0:
                ready_queue.sort(key=lambda x: x[2])
                '''
                Sort the processes according to the Burst Time
                '''
                start_time.append(s_time)
                s_time = s_time + ready_queue[0][2]
                e_time = s_time
                exit_time.append(e_time)
                for k in range(len(process_data)):
                    if process_data[k][0] == ready_queue[0][0]:
                        break
                process_data[k][3] = 1
                process_data[k].append(e_time)

            elif len(ready_queue) == 0:
                if s_time < normal_queue[0][1]:
                    s_time = normal_queue[0][1]
                start_time.append(s_time)
                s_time = s_time + normal_queue[0][2]
                e_time = s_time
                exit_time.append(e_time)
                for k in range(len(process_data)):
                    if process_data[k][0] == normal_queue[0][0]:
                        break
                process_data[k][3] = 1
                process_data[k].append(e_time)

        t_time = self.calculateTurnaroundTime(process_data)  # Call the method after the scheduling loop
        w_time = self.calculateWaitingTime(process_data)
        self.printData(process_data, t_time, w_time)


    def calculateTurnaroundTime(self, process_data):
        total_turnaround_time = 0
        for i in range(len(process_data)):
            turnaround_time = process_data[i][4] - process_data[i][1]
            '''
            turnaround_time = completion_time - arrival_time
            '''
            total_turnaround_time = total_turnaround_time + turnaround_time
            process_data[i].append(turnaround_time)
        average_turnaround_time = total_turnaround_time / len(process_data)
        '''
        average_turnaround_time = total_turnaround_time / no_of_processes
        '''
        return average_turnaround_time


    def calculateWaitingTime(self, process_data):
        total_waiting_time = 0
        for i in range(len(process_data)):
            waiting_time = process_data[i][5] - process_data[i][2]
            '''
            waiting_time = turnaround_time - burst_time
            '''
            total_waiting_time = total_waiting_time + waiting_time
            process_data[i].append(waiting_time)
        average_waiting_time = total_waiting_time / len(process_data)
        '''
        average_waiting_time = total_waiting_time / no_of_processes
        '''
        return average_waiting_time


    def printData(self, process_data, average_turnaround_time, average_waiting_time):
        
        process_data.sort(key=lambda x: x[6])  # Sort based on completion time
        
        print("\nShortest Job First Non Preemptive")

        print("\nGantt Chart")
        ganttWidths = [process_data[i][6] - process_data[i][1] for i in range(len(process_data))]

        print("+", end="")
        for width in ganttWidths:
            print("-" * 4 * width, end="+")
        print()

        print("|", end="")
        for i in range(len(process_data)):
            width = ganttWidths[i]
            process_id = process_data[i][0]
            print(" " * (4 * width - 3), f"P{process_id}", " " * (4 * width - 3), end="|")
        print()

        print("+", end="")
        for width in ganttWidths:
            print("-" * 4 * width, end="+")
        print()

        ganttStartTimes = [0] + [process_data[i][6] for i in range(len(process_data))]
        print(ganttStartTimes[0], end="")
        for i in range(len(process_data)):
            width = ganttWidths[i]
            print(" " * (4 * width), ganttStartTimes[i + 1], end="")
        print()
        prev_exit_time = 0
        for i in range(len(process_data)):
            process_id = process_data[i][0]
            start_time = process_data[i][6]
            end_time = process_data[i][6] + process_data[i][2]

            # Print spaces for idle time (if any) before this process starts
            if start_time > prev_exit_time:
                print(" " * (start_time - prev_exit_time), end="")

            # Print the process ID for its duration
            print("-" * (end_time - start_time), end="")
            prev_exit_time = end_time

        print("\n")
        print("Process_ID  Arrival_Time  Burst_Time      Completed  Completion_Time  Turnaround_Time  Waiting_Time")

        for i in range(len(process_data)):
            for j in range(len(process_data[i])):
                print(process_data[i][j], end=" " * (15 - len(str(process_data[i][j]))))
            print()

        print(f'Average Turnaround Time: {average_turnaround_time}')
        print(f'Average Waiting Time: {average_waiting_time}')



if __name__ == "__main__":
    no_of_processes = int(input("Enter number of processes: "))
    sjf = SJF()
    sjf.processData(no_of_processes)