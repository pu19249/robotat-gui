#include "codegen.h"
#include <math.h>
#include <stdio.h>

void control(double goal_x, double goal_y, double x0, double y0, double theta0, double *wheel_speeds)
{
    volatile float phi_ell = 0; // en rpm
    volatile float phi_r = 0; // en rpm
    float MAX_WHEEL_VELOCITY = 100;          // Velocidad máxima en ruedas
    float WHEEL_RADIUS = (0.32 / 2);         // radio de las ruedas (en cm)
    float DISTANCE_FROM_CENTER = (0.96 / 2); // distancia a ruedas (en cm)
    // Velocidad lineal máxima (en cm/s)
    float MAX_SPEED = WHEEL_RADIUS * MAX_WHEEL_VELOCITY;
    double v_result;
    v_result = 0.11 * sqrt(pow(goal_x - x0, 2) + pow(goal_y - y0, 2)) - 0.10000000000000001 * sin(theta0 - (goal_y - y0) / (goal_x - x0)) / cos(theta0 - (goal_y - y0) / (goal_x - x0));
    double w_result;
    w_result = -0.21000000000000002 * sin(theta0 - (goal_y - y0) / (goal_x - x0)) / cos(theta0 - (goal_y - y0) / (goal_x - x0));

    phi_ell = (v_result - w_result*DISTANCE_FROM_CENTER) / WHEEL_RADIUS; //rad/s;
    phi_r = (v_result + w_result*DISTANCE_FROM_CENTER) / WHEEL_RADIUS; //rad/s;

    phi_ell = phi_ell * (60.0 / (2 * 3.14159265 )); //rpm
    phi_r = phi_r * (60.0 / (2 * 3.14159265 )); //rpm
    if((phi_ell || phi_r) > 200){
      phi_ell = 0;
      phi_r = 0;

    }
    wheel_speeds[0] = phi_ell;
    wheel_speeds[1] = phi_r;

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