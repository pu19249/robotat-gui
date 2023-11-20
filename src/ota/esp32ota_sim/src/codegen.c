#include "codegen.h"
#include <math.h>
#include <stdio.h>


float MAX_WHEEL_VELOCITY = 100; // Velocidad máxima en ruedas

volatile float v_result;
volatile float w_result;


void control(double goal_x, double goal_y, double x0, double y0, double theta0, double *wheel_speeds)
{
    v_result = 15.01*sqrt(pow(goal_x - x0, 2) + pow(goal_y - y0, 2)) + 0.01*atan2(-sin(theta0 - (goal_y - y0)/(goal_x - x0)), cos(theta0 - (goal_y - y0)/(goal_x - x0)));
    w_result = 15.02*atan2(-sin(theta0 - (goal_y - y0)/(goal_x - x0)), cos(theta0 - (goal_y - y0)/(goal_x - x0)));

    wheel_speeds[0] = v_result;
    wheel_speeds[1] = w_result;

}
