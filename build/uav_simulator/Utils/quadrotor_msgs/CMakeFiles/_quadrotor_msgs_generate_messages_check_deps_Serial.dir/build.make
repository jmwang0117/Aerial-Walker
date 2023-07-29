# CMAKE generated file: DO NOT EDIT!
# Generated by "Unix Makefiles" Generator, CMake Version 3.26

# Delete rule output on recipe failure.
.DELETE_ON_ERROR:

#=============================================================================
# Special targets provided by cmake.

# Disable implicit rules so canonical targets will work.
.SUFFIXES:

# Disable VCS-based implicit rules.
% : %,v

# Disable VCS-based implicit rules.
% : RCS/%

# Disable VCS-based implicit rules.
% : RCS/%,v

# Disable VCS-based implicit rules.
% : SCCS/s.%

# Disable VCS-based implicit rules.
% : s.%

.SUFFIXES: .hpux_make_needs_suffix_list

# Command-line flag to silence nested $(MAKE).
$(VERBOSE)MAKESILENT = -s

#Suppress display of executed commands.
$(VERBOSE).SILENT:

# A target that is always out of date.
cmake_force:
.PHONY : cmake_force

#=============================================================================
# Set environment variables for the build.

# The shell in which to execute make rules.
SHELL = /bin/sh

# The CMake executable.
CMAKE_COMMAND = /usr/local/lib/python3.8/dist-packages/cmake/data/bin/cmake

# The command to remove a file.
RM = /usr/local/lib/python3.8/dist-packages/cmake/data/bin/cmake -E rm -f

# Escaping for special characters.
EQUALS = =

# The top-level source directory on which CMake was run.
CMAKE_SOURCE_DIR = /home/melodic/Aerial-Walker/src

# The top-level build directory on which CMake was run.
CMAKE_BINARY_DIR = /home/melodic/Aerial-Walker/build

# Utility rule file for _quadrotor_msgs_generate_messages_check_deps_Serial.

# Include any custom commands dependencies for this target.
include uav_simulator/Utils/quadrotor_msgs/CMakeFiles/_quadrotor_msgs_generate_messages_check_deps_Serial.dir/compiler_depend.make

# Include the progress variables for this target.
include uav_simulator/Utils/quadrotor_msgs/CMakeFiles/_quadrotor_msgs_generate_messages_check_deps_Serial.dir/progress.make

uav_simulator/Utils/quadrotor_msgs/CMakeFiles/_quadrotor_msgs_generate_messages_check_deps_Serial:
	cd /home/melodic/Aerial-Walker/build/uav_simulator/Utils/quadrotor_msgs && ../../../catkin_generated/env_cached.sh /usr/bin/python2 /opt/ros/melodic/share/genmsg/cmake/../../../lib/genmsg/genmsg_check_deps.py quadrotor_msgs /home/melodic/Aerial-Walker/src/uav_simulator/Utils/quadrotor_msgs/msg/Serial.msg std_msgs/Header

_quadrotor_msgs_generate_messages_check_deps_Serial: uav_simulator/Utils/quadrotor_msgs/CMakeFiles/_quadrotor_msgs_generate_messages_check_deps_Serial
_quadrotor_msgs_generate_messages_check_deps_Serial: uav_simulator/Utils/quadrotor_msgs/CMakeFiles/_quadrotor_msgs_generate_messages_check_deps_Serial.dir/build.make
.PHONY : _quadrotor_msgs_generate_messages_check_deps_Serial

# Rule to build all files generated by this target.
uav_simulator/Utils/quadrotor_msgs/CMakeFiles/_quadrotor_msgs_generate_messages_check_deps_Serial.dir/build: _quadrotor_msgs_generate_messages_check_deps_Serial
.PHONY : uav_simulator/Utils/quadrotor_msgs/CMakeFiles/_quadrotor_msgs_generate_messages_check_deps_Serial.dir/build

uav_simulator/Utils/quadrotor_msgs/CMakeFiles/_quadrotor_msgs_generate_messages_check_deps_Serial.dir/clean:
	cd /home/melodic/Aerial-Walker/build/uav_simulator/Utils/quadrotor_msgs && $(CMAKE_COMMAND) -P CMakeFiles/_quadrotor_msgs_generate_messages_check_deps_Serial.dir/cmake_clean.cmake
.PHONY : uav_simulator/Utils/quadrotor_msgs/CMakeFiles/_quadrotor_msgs_generate_messages_check_deps_Serial.dir/clean

uav_simulator/Utils/quadrotor_msgs/CMakeFiles/_quadrotor_msgs_generate_messages_check_deps_Serial.dir/depend:
	cd /home/melodic/Aerial-Walker/build && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /home/melodic/Aerial-Walker/src /home/melodic/Aerial-Walker/src/uav_simulator/Utils/quadrotor_msgs /home/melodic/Aerial-Walker/build /home/melodic/Aerial-Walker/build/uav_simulator/Utils/quadrotor_msgs /home/melodic/Aerial-Walker/build/uav_simulator/Utils/quadrotor_msgs/CMakeFiles/_quadrotor_msgs_generate_messages_check_deps_Serial.dir/DependInfo.cmake --color=$(COLOR)
.PHONY : uav_simulator/Utils/quadrotor_msgs/CMakeFiles/_quadrotor_msgs_generate_messages_check_deps_Serial.dir/depend

