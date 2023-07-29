#include <ros/ros.h>
#include <geometry_msgs/PoseStamped.h>

int main(int argc, char** argv) {
    ros::init(argc, argv, "manual_control");
    ros::NodeHandle n;

    ros::Publisher pub = n.advertise<geometry_msgs::PoseStamped>("/move_base_simple/goal", 10);

    // Wait for the publisher to connect to subscribers
    ros::Rate rate(1);
    while (pub.getNumSubscribers() == 0) {
        rate.sleep();
    }

    // Create the goal message
    geometry_msgs::PoseStamped goal;
    goal.header.stamp = ros::Time::now();
    goal.header.frame_id = "world";
    goal.pose.position.x = -5.0; // Set your desired x coordinate
    goal.pose.position.y = 4.0; // Set your desired y coordinate
    goal.pose.position.z = 0.0; // Set your desired z coordinate
    goal.pose.orientation.w = 1.0;

    // Publish the goal message
    pub.publish(goal);
    ros::spinOnce();
    ros::Duration(1.0).sleep(); // Sleep for a short period to ensure the message is published

    return 0;
}
