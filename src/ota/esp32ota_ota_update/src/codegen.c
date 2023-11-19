#include "codegen.h"
#include <math.h>
#include <stdio.h>

// volatile float phi_ell = 0; // en rpm
// volatile float phi_r = 0; // en rpm
float MAX_WHEEL_VELOCITY = 100;          // Velocidad máxima en ruedas
// double WHEEL_RADIUS = (0.032/ 2);         // radio de las ruedas (en m)
// double DISTANCE_FROM_CENTER = (0.096 / 2); // distancia a ruedas (en m)
// Velocidad lineal máxima (en cm/s)
// float MAX_SPEED = WHEEL_RADIUS * MAX_WHEEL_VELOCITY;
volatile float v_result;
volatile float w_result;
// double phi_left;
// double phi_right;

void control(double goal_x, double goal_y, double x0, double y0, double theta0, double *wheel_speeds)
{
    v_result = 15.01*sqrt(pow(goal_x - x0, 2) + pow(goal_y - y0, 2)) + 0.01*atan2(-sin(theta0 - (goal_y - y0)/(goal_x - x0)), cos(theta0 - (goal_y - y0)/(goal_x - x0)));
    //v_result = 0;
    w_result = 15.02*atan2(-sin(theta0 - (goal_y - y0)/(goal_x - x0)), cos(theta0 - (goal_y - y0)/(goal_x - x0)));
     // phi_left = (v_result*0 - w_result*DISTANCE_FROM_CENTER) / WHEEL_RADIUS; //rad/s;
    // phi_right = (v_result*0 + w_result*DISTANCE_FROM_CENTER) / WHEEL_RADIUS; //rad/s;

    // phi_left = phi_left * (60.0 / (2 * 3.14159265 )); //rpm
    // phi_right = phi_right * (60.0 / (2 * 3.14159265 )); //rpm    
    wheel_speeds[0] = v_result;
    wheel_speeds[1] = w_result;

}

// double v(double goal_x, double goal_y, double theta0, double x0, double y0) {
//    double v_result;
//    v_result = 0.11*sqrt(pow(goal_x - x0, 2) + pow(goal_y - y0, 2)) - 0.10000000000000001*sin(theta0 - (goal_y - y0)/(goal_x - x0))/cos(theta0 - (goal_y - y0)/(goal_x - x0));
//    return v_result;
// }

// double w(double goal_x, double goal_y, double theta0, double x0, double y0) {
//    double w_result;
//    w_result = -0.21000000000000002*sin(theta0 - (goal_y - y0)/(goal_x - x0))/cos(theta0 - (goal_y - y0)/(goal_x - x0));
//    return w_result;
// }