#include "phylib.h"
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include <stdio.h>


phylib_object *phylib_new_still_ball(unsigned char number, phylib_coord *pos) {
    //allocate memory for object
    phylib_object *obj = (phylib_object *)calloc(1, sizeof(phylib_object));
    if (obj != NULL) {
        //initialize values
        obj->type = PHYLIB_STILL_BALL;
        obj->obj.still_ball.number = number;
        obj->obj.still_ball.pos = *pos;
    } else {
        return NULL;
    }
    return obj;
}

phylib_object *phylib_new_rolling_ball(unsigned char number, phylib_coord *pos, phylib_coord *vel, phylib_coord *acc) {
    //repeat logic for following functions when declaring
    phylib_object *obj = (phylib_object *)calloc(1, sizeof(phylib_object));
    if (obj != NULL) {
        obj->type = PHYLIB_ROLLING_BALL;
        obj->obj.rolling_ball.number = number;
        obj->obj.rolling_ball.pos = *pos;
        obj->obj.rolling_ball.vel = *vel;
        obj->obj.rolling_ball.acc = *acc;
    } else {
        return NULL;
    }
    return obj;
}

phylib_object *phylib_new_hole(phylib_coord *pos) {
    phylib_object *obj = (phylib_object *)calloc(1, sizeof(phylib_object));
    if (obj != NULL) {
        obj->type = PHYLIB_HOLE;
        obj->obj.hole.pos = *pos;
    } else {
        return  NULL;
    }
    return obj;
}

phylib_object *phylib_new_hcushion(double y) {
    phylib_object *obj = (phylib_object *)calloc(1, sizeof(phylib_object));
    if (obj != NULL) {
        obj->type = PHYLIB_HCUSHION;
        obj->obj.hcushion.y = y;
    } else {
        return NULL;
    }
    return obj;
}

phylib_object *phylib_new_vcushion(double x) {
    phylib_object *obj = (phylib_object *)calloc(1, sizeof(phylib_object));
    if (obj != NULL) {
        obj->type = PHYLIB_VCUSHION;
        obj->obj.vcushion.x = x;
    } else {
        return NULL;
    }
    return obj;
}

phylib_table *phylib_new_table(void) {
    phylib_table *table = (phylib_table *)calloc(1, sizeof(phylib_table));
    if (table != NULL) {
        table->time = 0.0;
        
        // Initialize each table object accordingly 
        table->object[0] = phylib_new_hcushion(0.0);
        table->object[1] = phylib_new_hcushion(PHYLIB_TABLE_LENGTH);
        table->object[2] = phylib_new_vcushion(0.0);
        table->object[3] = phylib_new_vcushion(PHYLIB_TABLE_WIDTH);

        table->object[4] = phylib_new_hole(&(phylib_coord){0.0, 0.0});
        
        table->object[5] = phylib_new_hole(&(phylib_coord){0.0, PHYLIB_TABLE_LENGTH / 2.0});

        table->object[6] = phylib_new_hole(&(phylib_coord){0.0, PHYLIB_TABLE_LENGTH});
        table->object[7] = phylib_new_hole(&(phylib_coord){PHYLIB_TABLE_WIDTH, 0.0});
        table->object[8] = phylib_new_hole(&(phylib_coord){PHYLIB_TABLE_WIDTH, PHYLIB_TABLE_LENGTH / 2.0});
        table->object[9] = phylib_new_hole(&(phylib_coord){PHYLIB_TABLE_WIDTH, PHYLIB_TABLE_LENGTH});


        //deal with remaining pointers and set them as null
        for (int i = 10; i < PHYLIB_MAX_OBJECTS; i++) {
            table->object[i] = NULL;
        }
    } else {
        return NULL;
    }
    return table;
}

void phylib_copy_object(phylib_object **dest, phylib_object **src) {
    if (*src == NULL) {
        *dest = NULL;
        return;
    }

    *dest = (phylib_object *)calloc(1, sizeof(phylib_object));
    //copy the memory for the object
    if (*dest != NULL) {
        memcpy(*dest, *src, sizeof(phylib_object));
    }
}

phylib_table *phylib_copy_table(phylib_table *table) {
    if (table == NULL) {
        return NULL;
    }

    phylib_table *new_table = (phylib_table *)calloc(1, sizeof(phylib_table));
    //copy the table and each object as well as the time into the new table
    if (new_table != NULL) {
        for (int i = 0; i < PHYLIB_MAX_OBJECTS; i++) {
            phylib_copy_object(&(new_table->object[i]), &(table->object[i]));
        }
        new_table->time = table->time;
    }
    return new_table;
}

void phylib_add_object(phylib_table *table, phylib_object *object) {
    if (table == NULL || object == NULL) {
        return;
    }

    //loop through until null object is found and add object
    for (int i = 0; i < PHYLIB_MAX_OBJECTS; i++) {
        if (table->object[i] == NULL) {
            table->object[i] = object;
            break;
        }
    }
}

void phylib_free_table(phylib_table *table) {
    if (table == NULL) {
        return;
    }
    //free each object

    for (int i = 0; i < PHYLIB_MAX_OBJECTS; ++i) {
        if (table->object[i] != NULL) {
            free(table->object[i]);
        }
    }
    //free the table
    free(table);
}

phylib_coord phylib_sub( phylib_coord c1, phylib_coord c2 ) {
    phylib_coord result;
    result.x = c1.x - c2.x;
    result.y = c1.y - c2.y;
    return result;
}

double phylib_length( phylib_coord c ) {
    //return vector
    return sqrt(c.y * c.y + c.x * c.x);
}

double phylib_dot_product(phylib_coord a, phylib_coord b) {
    return a.x * b.x + a.y * b.y;
}

double phylib_distance(phylib_object *obj1, phylib_object *obj2) {
    //if either object is null then we return a negative double
    if (obj1 == NULL || obj2 == NULL) {
        return -1.0;
    }
    //ensure first object type is a rolling ball before continuing in function
    if (obj1->type != PHYLIB_ROLLING_BALL) {
        return -1.0;
    }
    //save center of first ball
    phylib_coord center1 = obj1->obj.rolling_ball.pos;
    //do different operations depending on the type of the second object
    switch (obj2->type) {
        case PHYLIB_STILL_BALL: {
            phylib_coord center2 = obj2->obj.still_ball.pos;
            double distance = phylib_length(phylib_sub(center1, center2)) - PHYLIB_BALL_DIAMETER;
            return distance;
        }
        case PHYLIB_ROLLING_BALL: {
            phylib_coord center2 = obj2->obj.rolling_ball.pos;
            double distance = phylib_length(phylib_sub(center1, center2)) - PHYLIB_BALL_DIAMETER;
            return distance;
        }
        case PHYLIB_HOLE: {
            phylib_coord hole_center = obj2->obj.hole.pos;
            double distance = phylib_length(phylib_sub(center1, hole_center)) - PHYLIB_HOLE_RADIUS;
            return distance;
        }
        case PHYLIB_HCUSHION: {
            double cushion_y = obj2->obj.hcushion.y;
            double distance = fabs(center1.y - cushion_y) - PHYLIB_BALL_RADIUS;
            return distance;
        }
        case PHYLIB_VCUSHION: {
            double cushion_x = obj2->obj.vcushion.x;
            double distance = fabs(center1.x - cushion_x) - PHYLIB_BALL_RADIUS;
            return distance;
        }
        default:
            return -1.0;
    }
}

void phylib_roll( phylib_object *new, phylib_object *old, double time ) {
    if (new->type != PHYLIB_ROLLING_BALL && old->type != PHYLIB_ROLLING_BALL) {
        return;
    }
    //calculate mathematic functions
    new->obj.rolling_ball.pos.x = old->obj.rolling_ball.pos.x + (old->obj.rolling_ball.vel.x * time) + (time * time * 0.5 * old->obj.rolling_ball.acc.x);
    new->obj.rolling_ball.pos.y = old->obj.rolling_ball.pos.y + (old->obj.rolling_ball.vel.y * time) + (time * time * 0.5 * old->obj.rolling_ball.acc.y);
    new->obj.rolling_ball.vel.x = old->obj.rolling_ball.vel.x + old->obj.rolling_ball.acc.x * time;
    new->obj.rolling_ball.vel.y = old->obj.rolling_ball.vel.y + old->obj.rolling_ball.acc.y * time;

    //if two values are multiplied and the value is negative, then directions were absolutely changed
    if ((new->obj.rolling_ball.vel.x * old->obj.rolling_ball.vel.x) < 0.0) {
        new->obj.rolling_ball.vel.x = 0.0;
        new->obj.rolling_ball.acc.x = 0.0;
    }
    if ((new->obj.rolling_ball.vel.y * old->obj.rolling_ball.vel.y) < 0.0) {
        new->obj.rolling_ball.vel.y = 0.0;
        new->obj.rolling_ball.acc.y = 0.0;
    }
}

unsigned char phylib_stopped(phylib_object *object) {
    if (object->type != PHYLIB_ROLLING_BALL) {
        return 0;
    }

    double speed = phylib_length(object->obj.rolling_ball.vel);
    //remembering to carry on the position and number values as they don't transfer without doing so 
    if (speed < PHYLIB_VEL_EPSILON) {
        object->type = PHYLIB_STILL_BALL;
        object->obj.still_ball.pos.x = object->obj.rolling_ball.pos.x;
        object->obj.still_ball.pos.y = object->obj.rolling_ball.pos.y;
        object->obj.still_ball.number = object->obj.rolling_ball.number;
        return 1;
    }

    return 0;
}

void phylib_bounce(phylib_object **a, phylib_object **b) {
    switch ((*b)->type) {
        case PHYLIB_HCUSHION:
            // Reverse y values
            (*a)->obj.rolling_ball.vel.y = -((*a)->obj.rolling_ball.vel.y);
            (*a)->obj.rolling_ball.acc.y = -((*a)->obj.rolling_ball.acc.y);
            break;
        case PHYLIB_VCUSHION:
            // Reverse x values
            (*a)->obj.rolling_ball.vel.x = -((*a)->obj.rolling_ball.vel.x);
            (*a)->obj.rolling_ball.acc.x = -((*a)->obj.rolling_ball.acc.x);
            break;
        case PHYLIB_HOLE:
            free(*a);
            *a = NULL;
            break;
        case PHYLIB_STILL_BALL: {
            //change still ball to rolling ball whilst moving values
            phylib_coord new_ball;
            new_ball.x = 0.0;
            new_ball.y = 0.0;
            
            (*b)->type = PHYLIB_ROLLING_BALL;

            (*b)->obj.rolling_ball.number = (*b)->obj.still_ball.number;
            (*b)->obj.rolling_ball.pos = (*b)->obj.still_ball.pos;
            (*b)->obj.rolling_ball.vel = new_ball;
            (*b)->obj.rolling_ball.acc = new_ball;
            //no break statement to allow entrance to rolling ball case
        }
        case PHYLIB_ROLLING_BALL: {
            //generate values based on formulas
            phylib_coord r_ab = phylib_sub((*a)->obj.rolling_ball.pos, (*b)->obj.rolling_ball.pos);
            phylib_coord v_rel = phylib_sub((*a)->obj.rolling_ball.vel, (*b)->obj.rolling_ball.vel);
            phylib_coord n = {r_ab.x / phylib_length(r_ab), r_ab.y / phylib_length(r_ab)};
            double v_rel_n = phylib_dot_product(v_rel, n);

            //store new velocity values
            (*a)->obj.rolling_ball.vel.x -= v_rel_n * n.x;
            (*a)->obj.rolling_ball.vel.y -= v_rel_n * n.y;
            (*b)->obj.rolling_ball.vel.x += v_rel_n * n.x;
            (*b)->obj.rolling_ball.vel.y += v_rel_n * n.y;

            //get speeds using length function
            double speed_a = phylib_length((*a)->obj.rolling_ball.vel);
            double speed_b = phylib_length((*b)->obj.rolling_ball.vel);

            //generate values based on formulas once again
            if (speed_a > PHYLIB_VEL_EPSILON) {
                (*a)->obj.rolling_ball.acc.x = -((*a)->obj.rolling_ball.vel.x / speed_a) * PHYLIB_DRAG;
                (*a)->obj.rolling_ball.acc.y = -((*a)->obj.rolling_ball.vel.y / speed_a) * PHYLIB_DRAG;
            }

            if (speed_b > PHYLIB_VEL_EPSILON) {
                (*b)->obj.rolling_ball.acc.x = -((*b)->obj.rolling_ball.vel.x / speed_b) * PHYLIB_DRAG;
                (*b)->obj.rolling_ball.acc.y = -((*b)->obj.rolling_ball.vel.y / speed_b) * PHYLIB_DRAG;
            }
            break;
            //end of switch
        }
    }
}

unsigned char phylib_rolling(phylib_table *t) {
    unsigned char rollingCount = 0;

    //count number of rolling balls through the use of a for loop
    for (int i = 0; i < PHYLIB_MAX_OBJECTS; ++i) {
        if (t->object[i] != NULL && t->object[i]->type == PHYLIB_ROLLING_BALL) {
            ++rollingCount;
        }
    }

    return rollingCount;
}

phylib_table *phylib_segment(phylib_table *table) {
    if (phylib_rolling(table) == 0) {
        return NULL;
    }

    phylib_table *newTable = phylib_copy_table(table);

    //ensure backup for if copytable function fails
    if (newTable == NULL) {
        return NULL;
    }

    for (double i = PHYLIB_SIM_RATE; i < PHYLIB_MAX_TIME; i += PHYLIB_SIM_RATE) {
        newTable->time += PHYLIB_SIM_RATE;

        for (int j = 0; j < PHYLIB_MAX_OBJECTS; j++) {
            if (newTable->object[j] != NULL && newTable->object[j]->type == PHYLIB_ROLLING_BALL) {
                phylib_roll(newTable->object[j], table->object[j], i);

            }
        }
        
        //checks for if distance is less than 0, then we know we have a collision
        for (int j = 0; j < PHYLIB_MAX_OBJECTS; j++) {
            for (int k = 0; k < PHYLIB_MAX_OBJECTS; k++) {
                if (newTable->object[k] == NULL || k == j) {
                    continue;
                }
                if (newTable->object[j] != NULL && newTable->object[j]->type == PHYLIB_ROLLING_BALL) {
                    if (phylib_distance(newTable->object[j], newTable->object[k]) < 0.0) {
                        phylib_bounce(&(newTable->object[j]), &(newTable->object[k]));
                        return newTable;
                    }

                    if (phylib_stopped(newTable->object[j])) {
                        return newTable;
                    }
                }
            }
        }
        
    }

    return newTable;
}

char *phylib_object_string(phylib_object *object)
{
    static char string[80];
    if (object == NULL)
    {
        snprintf(string, 80, "NULL;");
        return string;
    }
    switch (object->type)
    {
    case PHYLIB_STILL_BALL:
        snprintf(string, 80,
                 "STILL_BALL (%d,%6.1lf,%6.1lf)",
                 object->obj.still_ball.number,
                 object->obj.still_ball.pos.x,
                 object->obj.still_ball.pos.y);
        break;
    case PHYLIB_ROLLING_BALL:
        snprintf(string, 80,
                 "ROLLING_BALL (%d,%6.1lf,%6.1lf,%6.1lf,%6.1lf,%6.1lf,%6.1lf)",
                 object->obj.rolling_ball.number,
                 object->obj.rolling_ball.pos.x,
                 object->obj.rolling_ball.pos.y,
                 object->obj.rolling_ball.vel.x,
                 object->obj.rolling_ball.vel.y,
                 object->obj.rolling_ball.acc.x,
                 object->obj.rolling_ball.acc.y);
        break;
    case PHYLIB_HOLE:
        snprintf(string, 80,
                 "HOLE (%6.1lf,%6.1lf)",
                 object->obj.hole.pos.x,
                 object->obj.hole.pos.y);
        break;
    case PHYLIB_HCUSHION:
        snprintf(string, 80,
                 "HCUSHION (%6.1lf)",
                 object->obj.hcushion.y);
        break;
    case PHYLIB_VCUSHION:
        snprintf(string, 80,
                 "VCUSHION (%6.1lf)",
                 object->obj.vcushion.x);
        break;
    }
    return string;
}
