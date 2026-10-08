# AMR Project Plan

## Purpose and working agreement

This file is the project’s single source of truth for the roadmap, current milestone status, decisions, and session handoffs. Update it whenever a milestone makes progress, and bring its status and session log up to date before wrapping up each coding session. At the start of a new session, read this file first and continue from the recorded next step.

The project is a simulated differential-drive Autonomous Mobile Robot (AMR) built incrementally with ROS 2 Jazzy. Do not skip ahead to Nav2 before the robot model, simulation, motion, sensing, mapping, and localization work reliably.

### Installation approval gate

System, ROS, simulator, and other dependency installations require the project owner’s approval. Before installing anything, identify the packages, explain why they are needed, and wait for approval. Do not treat missing dependencies as permission to install them.

### Package structure principle

Keep the package structure minimal. Begin with the existing `robot_basics` package. Add a package only when a milestone introduces a distinct responsibility or reusable assets that justify separating it. The roadmap suggests likely package boundaries but does not require creating every suggested package.

### Testing principle

Introduce automated checks progressively with each feature: configuration and unit checks first, then simulator smoke checks, then repeatable integration and end-to-end scenarios. Use manual visualization and functional checks where they provide evidence that automated checks cannot reasonably provide. Do not claim acceptance until its stated criteria have been checked.

## Current project status

- **Overall status:** Roadmap approved; implementation has not started.
- **Current milestone:** Milestone 0 — Workspace baseline.
- **Last completed work:** Initial repository and ROS 2 environment reconnaissance.
- **Next step:** Begin Milestone 0 by establishing and checking the workspace build/run workflow and existing package checks.
- **Installation status:** No installation has been requested or performed. Any future installation requires explicit owner approval.
- **Working tree note from reconnaissance:** Existing uncommitted changes were observed in `src/robot_basics/package.xml`, `src/robot_basics/setup.py`, `src/robot_basics/robot_basics/status_publisher.py`, `src/robot_basics/robot_basics/status_subscriber.py`, and `.vscode/`. Preserve and inspect these changes before editing; do not assume they are disposable or authored by the implementation engineer.
- **Acceptance evidence:** No build, test, or functional acceptance checks have been run as part of the reconnaissance. The presence of ROS 2 Jazzy executables was observed; Gazebo, Nav2, and SLAM Toolbox were not found in the installed ROS package list at that time. Recheck availability when a milestone depends on them.

## Milestones

Milestone statuses use **Not started**, **In progress**, **Blocked**, or **Complete**. A milestone is complete only when its acceptance criteria have been checked and its evidence is recorded in the session log.

### Milestone 0 — Workspace baseline

- **Status:** Not started
- **Build:** Establish a repeatable build and run workflow for the existing package.
- **Why:** Later milestones depend on a reliable way to build, source, run, and check the workspace.
- **ROS 2 concepts:** Workspaces, packages, `colcon`, overlays, sourcing setup files, and package checks.
- **Packages, nodes, and interfaces:** Existing `robot_basics`; its status publisher and subscriber use `example_interfaces/String` on the `status` topic.
- **Expected files:** Initially none required. If useful and approved as project work, document workspace commands in a root README or this plan; do not introduce files without a reason.
- **Automated tests:** Run the existing package lint and test checks; add a small check only when there is meaningful behavior to verify.
- **Manual checks:** Run the publisher and subscriber in separate terminals and observe message exchange.
- **Acceptance criteria:** Workspace builds; existing package checks pass; subscriber receives messages from the publisher.
- **Dependencies:** None.

### Milestone 1 — Robot description and RViz visualization

- **Status:** Not started
- **Build:** Describe a differential-drive robot and display it in RViz2.
- **Why:** The robot model defines geometry and coordinate frames needed by simulation, sensing, and motion.
- **ROS 2 concepts:** URDF/Xacro, links, joints, fixed and movable joints, launch files, and TF.
- **Packages, nodes, and interfaces:** `robot_state_publisher`, RViz2, Xacro/URDF; add `amr_description` because a reusable robot description and its assets form a distinct responsibility.
- **Expected files:** Robot description under `urdf/`, launch files, RViz configuration, and meshes/materials only if needed.
- **Automated tests:** Check that Xacro expands and that the resulting robot description is valid.
- **Manual checks:** Display the model in RViz2 and inspect its TF tree for connected frames and sensible geometry.
- **Acceptance criteria:** Model displays correctly; its TF tree is connected; the description can be generated through the project launch workflow.
- **Dependencies:** Milestone 0.

### Milestone 2 — Simulation launch and robot spawning

- **Status:** Not started
- **Build:** Start a physics simulator with a simple world and spawn the robot into it. Spawning and visualization are the goal at this stage; motion control comes later.
- **Why:** A spawned robot in a repeatable physics environment is the foundation for simulated control and sensors.
- **ROS 2 concepts:** Simulator worlds, simulator entities, spawn workflows, ROS–simulator integration, and launch composition.
- **Packages, nodes, and interfaces:** Select a simulator and its ROS integration appropriate for Jazzy; introduce `amr_simulation` when world assets, simulator settings, or spawn launch files justify a separate package.
- **Expected files:** World description, simulator configuration, and spawn/bringup launch files, placed in the smallest suitable package structure.
- **Automated tests:** Check launch descriptions and spawn configuration; add a headless simulator smoke check that confirms the robot entity appears if the environment supports reliable headless operation.
- **Manual checks:** Start the simulator and confirm the robot appears once at the expected pose.
- **Acceptance criteria:** Simulator starts; robot spawns once at the expected pose; model is visible in the simulator. If required packages are missing, stop and request installation approval before proceeding with installation-dependent work.
- **Dependencies:** Milestone 1 and availability of the selected simulator and integration packages.

### Milestone 3 — Motion control and odometry

- **Status:** Not started
- **Build:** Accept velocity commands, move the simulated robot, and publish wheel state, odometry, and required transforms.
- **Why:** Mapping and navigation depend on controllable motion and an estimate of the robot’s movement.
- **ROS 2 concepts:** Topics, message types, parameters, controllers, odometry, and coordinate frames.
- **Packages, nodes, and interfaces:** Prefer `ros2_control` with a differential-drive controller if it integrates cleanly with the chosen simulator; use standard velocity, joint state, odometry, and TF interfaces.
- **Expected files:** Controller configuration, control-related robot description changes, and simulation launch/configuration updates.
- **Automated tests:** Check controller configuration and launch loading; verify expected topics and frames; add a short simulated motion check where practical.
- **Manual checks:** Drive forward and turn with keyboard commands; compare observed motion with odometry and TF.
- **Acceptance criteria:** Commands cause predictable motion; odometry and TF update consistently; a stop command stops the robot.
- **Dependencies:** Milestone 2.

### Milestone 4 — Simulated LiDAR

- **Status:** Not started
- **Build:** Add a simulated 2D LiDAR and expose its scans to ROS and RViz2.
- **Why:** LiDAR observations support mapping and obstacle detection.
- **ROS 2 concepts:** Sensor messages, topic inspection, frame IDs, sensor simulation, and QoS (rules governing message delivery between publishers and subscribers).
- **Packages, nodes, and interfaces:** Simulator LiDAR sensor and ROS bridge; `sensor_msgs/LaserScan`; RViz2.
- **Expected files:** Sensor configuration in the robot/simulator description and launch/configuration updates.
- **Automated tests:** Check sensor and bridge configuration, topic type, and scan frame; add a simulator smoke check that verifies scan publication.
- **Manual checks:** View `/scan` in RViz2 near known walls and obstacles; inspect message values and rate.
- **Acceptance criteria:** Scan publishes steadily, has the expected frame, and represents visible obstacles.
- **Dependencies:** Milestone 3 and the selected simulator integration.

### Milestone 5 — SLAM and saved maps

- **Status:** Not started
- **Build:** Drive through a small environment, create a 2D map, and save it.
- **Why:** The map represents the environment for later localization and route planning.
- **ROS 2 concepts:** SLAM (simultaneous localization and mapping), occupancy grids, map frames, and launch/configuration.
- **Packages, nodes, and interfaces:** SLAM Toolbox; LiDAR, odometry, TF, `nav_msgs/OccupancyGrid`, and map-saving tools.
- **Expected files:** SLAM parameters, mapping launch configuration, and a saved map with metadata.
- **Automated tests:** Check SLAM configuration and map save/load behavior; use a small repeatable simulation scenario to verify map production where practical.
- **Manual checks:** Inspect the map during and after mapping; save and reload it.
- **Acceptance criteria:** Map contains recognizable free and occupied areas, is saved with metadata, and can be loaded again.
- **Dependencies:** Milestone 4, with reliable odometry and TF from Milestone 3.

### Milestone 6 — Localization on a saved map

- **Status:** Not started
- **Build:** Load the saved map and estimate the robot’s pose as it moves.
- **Why:** Navigation needs the robot’s estimated position relative to the saved map.
- **ROS 2 concepts:** Localization, initial pose estimates, `map`/`odom`/`base_link` frames, and lifecycle nodes (nodes with explicit configure, activate, and shutdown states).
- **Packages, nodes, and interfaces:** Nav2 localization components, typically AMCL and the map server; saved map, LiDAR, odometry, and TF.
- **Expected files:** Localization parameters and launch configuration.
- **Automated tests:** Check localization configuration and launch wiring; add a repeatable startup and pose-publication simulation check.
- **Manual checks:** Initialize at a known pose, move the robot, and compare estimated pose with simulated position.
- **Acceptance criteria:** Localization settles to a plausible pose and tracks movement in the test environment without losing the robot.
- **Dependencies:** Milestone 5 and dependable scan, odometry, and TF data.

### Milestone 7 — Path planning and obstacle handling

- **Status:** Not started
- **Build:** Plan routes through the map and respond to obstacles detected by LiDAR.
- **Why:** Planning selects a route; obstacle handling adapts when objects block or approach that route.
- **ROS 2 concepts:** Nav2 costmaps (grids marking occupied or risky space), planner/controller plugins, behavior trees, and action interfaces.
- **Packages, nodes, and interfaces:** Nav2 planner, controller, costmaps, and behavior tree navigator; map, localization, TF, and sensor data.
- **Expected files:** Nav2 parameters, costmap settings, behavior tree configuration, and launch updates.
- **Automated tests:** Check Nav2 configuration and topic/action connections; add repeatable reachable-goal and blocked-route scenarios.
- **Manual checks:** Request goals and introduce obstacles; observe route planning and safe behavior.
- **Acceptance criteria:** Reachable goal produces a route; obstacles are handled safely within configured limits; impossible routes report a clear failure.
- **Dependencies:** Milestone 6 and stable velocity control.

### Milestone 8 — Autonomous goal navigation

- **Status:** Not started
- **Build:** Integrate the system so a user can send a goal and the robot navigates there, reports progress, and handles failures.
- **Why:** This joins mapping, localization, planning, control, and obstacle handling into the intended AMR workflow.
- **ROS 2 concepts:** Actions, Nav2 lifecycle management, recovery behavior, launch composition, and system-level debugging.
- **Packages, nodes, and interfaces:** Nav2 navigation action and stack; goal pose, feedback, result, and configured robot controller.
- **Expected files:** Integrated bringup launch/configuration, operator instructions, and repeatable demonstration scenarios.
- **Automated tests:** Add end-to-end scenarios for successful navigation, blocked goals, and startup/shutdown in small repeatable worlds.
- **Manual checks:** Send several goals and observe progress, completion, and failure behavior.
- **Acceptance criteria:** Reachable goals complete reliably; blocked goals fail safely with useful status; the full system starts through the documented launch workflow.
- **Dependencies:** Milestone 7.

## Decisions and open choices

- **Simulation:** Prefer a physics simulator with ROS integration appropriate for Jazzy. The exact simulator and integration must be confirmed against available packages and project constraints before Milestone 2. Installation requires owner approval.
- **Drive control:** Prefer `ros2_control` and a differential-drive controller when compatible with the selected simulation integration. A custom controller is a fallback if compatibility or learning goals justify it.
- **Package boundaries:** Keep the current package initially; likely introduce `amr_description` for the reusable model and add a simulation package only when its assets/configuration justify the boundary.
- **Navigation order:** Add Nav2 localization only after the saved-map milestone; add planning and autonomous goals only after localization and control are dependable.

## Session log

Append one entry at the end of every coding session. Record the milestone worked on, changes made, checks and their results, acceptance criteria met or still open, blockers/approval needs, and the exact next step. Keep the **Current project status** and milestone statuses synchronized with the latest entry.

### Session 0 — Roadmap and reconnaissance

- **Outcome:** Inspected the repository and ROS environment; agreed on the staged roadmap and approval/testing/package-structure rules; created this plan.
- **Changes:** Added `PROJECT_PLAN.md`. No implementation files were changed; no packages were installed.
- **Checks:** No build, tests, or functional checks run. Repository contents and available ROS executables/packages were inspected read-only.
- **Milestone status:** Milestone 0 remains **Not started**; reconnaissance alone does not satisfy its acceptance criteria.
- **Next step:** Start Milestone 0 by reviewing the existing local changes and establishing the workspace build/run workflow. Preserve the observed user changes.
