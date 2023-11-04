#ifndef CODEGEN_H
#define CODEGEN_H

#ifdef __cplusplus
extern "C" {
#endif

// ====================================================================================================
// Dependencies
// ====================================================================================================
#include <stdint.h>

// ====================================================================================================
// Function prototypes
// ====================================================================================================
void control(double goal_x, double goal_y, double x, double y, double theta, double * wheel_speeds);

#ifdef __cplusplus
}
#endif

#endif /* CODEGEN_H */