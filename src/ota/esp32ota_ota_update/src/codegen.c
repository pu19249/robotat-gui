#include "codegen.h"
#include <math.h>
#include <stdio.h>


volatile float v_result;
volatile float w_result;


void control(double goal_x, double goal_y, double x0, double y0, double theta0, double *wheel_speeds)
{
    v_result =  20.0 - 20.0*pow(2.7182818284590451, -9*pow(pow(goal_x - x0, 2) + pow(goal_y - y0, 2), 1.0));
    w_result =  15.02*atan2(-sin(theta0 - atan2(goal_y - y0, goal_x - x0)), cos(theta0 - atan2(goal_y - y0, goal_x - x0)));

    wheel_speeds[0] = v_result;
    wheel_speeds[1] = w_result;

}
