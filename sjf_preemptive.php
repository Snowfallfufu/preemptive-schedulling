<!DOCTYPE html>
<html>
<head>
  <title>Preemptive Shortest Job First</title>
  <style>
    .container {
      max-width: 1150px;
      margin: 0 auto;
      padding: 20px;
      text-align: center;
    }

    h1 {
      margin-bottom: 20px;
    }

    textarea {
      width: 100%;
      resize: vertical;
      margin-bottom: 10px;
    }

    input[type="submit"] {
      padding: 10px 20px;
      background-color: #0047AB;
      color: white;
      border: none;
      cursor: pointer;
    }

    table {
      margin-top: 20px;
      width: 100%;
      border-collapse: collapse;
    }

    th, td {
      padding: 8px;
      text-align: left;
      border-bottom: 1px solid #ddd;
    }

    th {
      background-color: #0047AB;
      color: white;
    }

    .gantt {
      margin-top: 20px;
      display: flex;
      align-items: center;
	  justify-content: center;
    }

    .gantt-bar {
      height: 20px;
      background-color: #0047AB;
      margin-right: 4px;
      position: relative;
    }

    .gantt-text {
      position: absolute;
      top: 50%;
      left: 50%;
      transform: translate(-50%, -50%);
      color: white;
    }

    .gantt-timeline {
      display: flex;
      justify-content: center;
      margin-top: 8px;
    }

    .gantt-timeline-item {
      margin-right: 20px;
    }

    .time {
      display: flex;
      justify-content: center;
      margin-top: 8px;
    }

    .time-item {
      margin-right: 20px;
    }
  </style>
</head>
<body>
  <div class="container">
    <h1>Preemptive Shortest Job First</h1>
    <form action="<?php echo htmlspecialchars($_SERVER["PHP_SELF"]); ?>" method="post">
      <label for="processes">Enter process information:</label>
      <textarea id="processes" name="processes" rows="4" cols="50" placeholder="Enter processes in the format: ProcessName ArrivalTime BurstTime"><?php echo isset($_POST["processes"]) ? htmlspecialchars($_POST["processes"]) : ""; ?></textarea>
      <br>
      <input type="submit" value="Run">
    </form>

    <?php
	if ($_SERVER["REQUEST_METHOD"] == "POST") {
	  //Get the input processes
	  $processesInput = $_POST["processes"];

	  //Parse the input into an array of processes
	  $processesArray = explode("\n", $processesInput);
	  $processes = array();

	  foreach ($processesArray as $processString) {
		$processData = explode(" ", $processString);
		$processes[] = array(
		  "name" => $processData[0],
		  "arrivalTime" => intval($processData[1]),
		  "burstTime" => intval($processData[2])
		);
	  }

	  //Sort the processes based on their arrival time
	  usort($processes, function($a, $b) {
		return $a["arrivalTime"] - $b["arrivalTime"];
	  });

	  //Preemptive Shortest Job First algorithm
	  $completionTimes = array();
	  $turnaroundTimes = array();
	  $waitingTimes = array();
	  $remainingTimes = array();
	  $ganttChart = array();
	  $ganttStartTimes = array();
	  $finalCompletedProcess = 0;

	  foreach ($processes as $process) {
		$remainingTimes[$process["name"]] = $process["burstTime"];
	  }

	  $time = 0;
	  $completedProcesses = 0;

	  while ($completedProcesses < count($processes)) {
		$nextProcess = null;
		$shortestBurst = PHP_INT_MAX;

		foreach ($processes as $process) {
		  if ($process["arrivalTime"] <= $time && $remainingTimes[$process["name"]] < $shortestBurst && $remainingTimes[$process["name"]] > 0) {
			$nextProcess = $process["name"];
			$shortestBurst = $remainingTimes[$process["name"]];
		  }
		}

		if ($nextProcess == null) {
		  $time++;
		  continue;
		}

		$remainingTimes[$nextProcess]--;

		if (!isset($ganttChart[$time])) {
		  $ganttChart[$time] = $nextProcess;
		} else {
		  $ganttChart[$time] .= "<br>$nextProcess";
		}

		if ($remainingTimes[$nextProcess] == 0) {
		  $completionTimes[$nextProcess] = $time + 1;
		  $turnaroundTimes[$nextProcess] = $time + 1 - $processes[array_search($nextProcess, array_column($processes, 'name'))]['arrivalTime'];
		  $waitingTimes[$nextProcess] = $turnaroundTimes[$nextProcess] - $processes[array_search($nextProcess, array_column($processes, 'name'))]['burstTime'];
		  $completedProcesses++;
		  $finalCompletedProcess = $time + 1;
		}

		$time++;
	  }

	  //Output the completion times, turnaround times, and waiting times
	  echo "<h2>Table</h2>";
	  echo "<table>";
	  echo "<tr><th>Process</th><th>Arrival Time</th><th>Burst Time</th><th>Completion Time</th><th>Turnaround Time</th><th>Waiting Time</th></tr>";

	  foreach ($processes as $process) {
		$processName = $process["name"];
		$arrivalTime = $process["arrivalTime"];
		$burstTime = $process["burstTime"];
		$completionTime = isset($completionTimes[$processName]) ? $completionTimes[$processName] : "N/A";
		$turnaroundTime = isset($turnaroundTimes[$processName]) ? $turnaroundTimes[$processName] : "N/A";
		$waitingTime = isset($waitingTimes[$processName]) ? $waitingTimes[$processName] : "N/A";


		echo "<tr><td>$processName</td><td>$arrivalTime</td><td>$burstTime</td><td>$completionTime</td><td>$turnaroundTime</td><td>$waitingTime</td></tr>";
	  }

	  echo "<tr><th colspan='4'>Average</th><th>" . array_sum($turnaroundTimes) / count($turnaroundTimes) . "</th><th>" . array_sum($waitingTimes) / count($waitingTimes) . "</th></tr>";

	  echo "</table>";

	  //Ganttcharttable
      echo "<h2>Gantt Chart</h2>";
      echo "<table>";
      echo "<tr><th>Process</th>";

		// process names
		foreach ($ganttChart as $time => $process) {
		echo "<th>$process</th>";
		}
		echo "</tr>";
		echo "<tr><td>Time</td>";
		// time
		foreach ($ganttChart as $time => $process) {
		echo "<td>$time</td>";
		}
		echo "</tr>";


      echo "</table>";
	}
	?>

  </div>
</body>
</html>
