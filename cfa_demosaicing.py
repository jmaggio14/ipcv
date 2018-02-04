import numpy as np
import cv2
from scipy import signal


def cfaDemosaic(raw,window_size_rb=5,regularization_parameter=.01):
    raw = raw.astype(np.float64)
    red_band = raw[:,:,0]
    green_band = raw[:,:,1]
    blue_band = raw[:,:,2]

    # --------- GREEN COMPONENT ESTIMATION -------------

    # ###### ======== pre-estimations =========== #########
    # Calculating N,S,E,W pre-estimations for the blue band
    preestimations_R = {}
    preestimations_B = {}
    preestimations_B["W"] = np.roll(green_band,-1,1)  + (blue_band - np.roll(blue_band,-2,1)) / 2.0
    preestimations_B["E"] = np.roll(green_band,+1,1)  + (blue_band - np.roll(blue_band,+2,1)) / 2.0
    preestimations_B["N"] = np.roll(green_band,-1,0)  + (blue_band - np.roll(blue_band,-2,0)) / 2.0
    preestimations_B["S"] = np.roll(green_band,+1,1)  + (blue_band - np.roll(blue_band,+2,0)) / 2.0

    # Calculating N,S,E,W pre-estimations for the red band
    preestimations_R["W"] = np.roll(green_band,-1,1)  + (red_band - np.roll(red_band,-2,1)) / 2.0
    preestimations_R["E"] = np.roll(green_band,+1,1)  + (red_band - np.roll(red_band,+2,1)) / 2.0
    preestimations_R["N"] = np.roll(green_band,-1,0)  + (red_band - np.roll(red_band,-2,0)) / 2.0
    preestimations_R["S"] = np.roll(green_band,+1,1)  + (red_band - np.roll(red_band,+2,0)) / 2.0

    # Calculating NW,SW,NE,SE pre-estimations for the blue band
    h8 = np.asarray([-1,4,-11,40,40,-11,4,-1]) / 64.0
    diagonal_rolls = {
                    "NW":[(-4,-3),(-3,-2),(-2,-1),(-1,0),(0,-1),(+1,-2),(+2,-3),(+3,-4)],
                    "NE":[(+3,-4),(+2,-3),(+1,-2),(0,-1),(-1,0),(-2,+1),(-3,+2),(-4,+3)],
                    "SE":[(+4,-3),(+3,-2),(+2,-1),(+1,0),(0,+1),(-1,+2),(-2,+3),(-3,+4)],
                    "SW":[(-3,-4),(-2,-3),(-1,-2),(0,-1),(+1,0),(+2,+1),(+3,+2),(+4,+3)],
                }

    for key,value in diagonal_rolls.items():
        diagnonal_sum = 0
        for shift,multiplier in value,h8:
            diagnonal_sum =  (np.roll(green_band,shift,(0,1)) * multiplier) + diagnonal_sum
        preestimations_R[key] = diagnonal_sum
        preestimations_B[key] = diagnonal_sum

    # Calculating the weighting factors for the pre-estimations
    # gradients indices are
    # --------- CALCULATING GRADIENTS -------------
    epsilon = 1e-6
    gradient_rolls = {
                    "N":{"G":[ [(-2,-1),(+0,-1)],[(-3,+0),(-1,+0)],[(-2,+1),(+0,+1)] ],
                         "R":[ [(-3,-1),(-1,-1)],[(-3,+1),(-1,+1)] ],
                         "B":[ [(-2,+0),(+0,+0)] ] }
                    "S":{"G":[ [(+2,-1),(+0,-1)],[(+3,+0),(+1,+0)],[(+2,+1),(+0,+1)] ],
                         "R":[ [(+3,+1),(+1,-1)],[(+3,+1),(+1,+1)] ],
                         "B":[ [(+2,+0),(+0,+0)] ] }
                    "E":{"G":[ [(-1,+2),(-1,+0)],[(+1,+2),(+1,+0)],[(+0,+3),(+0,+1)] ],
                         "R":[ [(-1,+3),(-1,+1)],[(+1,+3),(+1,+1)] ],
                         "B":[ [(+0,+2),(+0,+0)] ] }
                    "W":{"G":[ [(-1,-2),(-1,+0)],[(+1,-2),(+1,+0)],[(+0,-3),(+0,-1)] ],
                         "R":[ [(-1,-3),(-1,-1)],[(+1,-3),(+1,-1)] ],
                         "B":[ [(+0,-2),(+0,+0)] ] }
                   "NW":{"G":[ [(-2,-1),(-1,+0)],[(-1,+0),(0,+1)],[(-1,-2),(+0,-1)],[(+0,-1),(+1,+0)] ],
                         "R":[ [(-1,-1),(+1,+1)] ],
                         "B":[ [(-2,-2),(+0,+0)] ] }
                   "NE":{"G":[ [(-2,+1),(-1,+0)],[(-1,+0),(+0,-1)],[(-1,+2),(+0,+1)],[(+0,+1),(+1,+0)] ],
                         "R":[ [(-1,+1),(+1,-1)] ],
                         "B":[ [(-2,+2),(+0,+0)] ] }
                   "SW":{"G":[ [(+1,-2),(+0,-1)],[(+0,-1),(-1,+0)],[(+2,-1),(+1,+0)],[(+1,+0),(+0,+1)] ],
                         "R":[ [(-1,+1),(+1,-1)] ],
                         "B":[ [(+2,-2),(+0,+0)] ] }
                   "SE":{"G":[ [(+1,+2),(+0,+1)],[(+0,+1),(-1,+0)],[(+2,+1),(+1,+0)],[(+1,+0),(+0,-1)] ],
                         "R":[ [(+1,+1),(-1,-1)] ],
                         "B":[ [(+2,+2),(+0,+0)] ]}
                         }
    bands = {"G":green_band,"R":red_band,"B":blue_band}
    weights = {}
    for direction,pixel_pairs_by_band in gradient_rolls.items():
        gradient = 0;
        for band,pixel_pairs in pixel_pairs_by_band.items():
            gradient = gradient + np.abs( np.roll(bands[band],pixel_pairs[0],(0,1)) - np.roll(bands[band],pixel_pairs[1],(0,1)) )
        gradient += epsilon
        weights[direction] = 1.0 / gradient

    green_estimation_B = 0
    green_estimation_R = 0
    weight_sum = 0
    for direction in gradient_rolls.keys():
        green_estimation_B = green_estimation + (preestimations_B[direction] * weights[direction])
        green_estimation_R = green_estimation + (preestimations_R[direction] * weights[direction])
        weight_sum = weight_sum + weights[direction]

    green_estimation_R = (green_estimation_R / weight_sum)
    green_estimation_B = (green_estimation_B / weight_sum)

    green_estimation = green_estimation_R + green_estimation_B

    # --------------- Red and Blue component estimation -------------
    # calculating components for both red and blue estimation
    window_coefficient = 1.0 / (window_size_rb **2)
    summation_kernel = np.ones( (window_size_rb,window_size_rb) )
    average_kernel = window_coefficient * np.ones( (window_size_rb,window_size_rb) )
    local_average_G = signal.convolve2d(green_estimation,average_kernel)
    local_average_Gsquared = signal.convolve2d(green_estimation**2,average_kernel)
    local_stddev_G = (1.0 / (window_size_rb**2 - 1) ) * (local_average_Gsquared - (local_average_G**2 * window_coefficient )

    # calculating R
    local_average_R = signal.convolve2d(green_estimation,average_kernel)
    a_numerator_R = (window_coefficient * signal.convolve2d( (green_estimation*red_band),summation_kernel) ) - (local_average_G * local_average_R)
    a_denominator_R = local_stddev_G + regularization_parameter
    a_R = a_numerator_R / a_numerator_R
    b_R = local_average_R - (a_R * local_average_G)

    R_approx = (a_R * green_estimation) + b_R


    # calculating B
    local_average_B = signal.convolve2d(green_estimation,average_kernel)
    a_numerator_B = (window_coefficient * signal.convolve2d( (green_estimation*blue_band),summation_kernel) ) - (local_average_G * local_average_B)
    a_denominator_B = local_stddev_G + regularization_parameter
    a_B = a_numerator_B / a_numerator_B
    b_B = local_average_B - (a_B * local_average_G)

    B_approx = (a_B * green_estimation) + b_B

    # ------------------------- Calculating Residuals ---------------
    calcResidualR = lambda i,j: blue_band - np.roll(B_approx,(i,j),(0,1))
    calcResidualB = lambda i,j: red_band - np.roll(R_approx,(i,j),(0,1))


    residual_B = np.clip((blue_band - B_approx ),0,None) + (calcResidualB(-1,-1) + calcResidualB(-1,+1) + calcResidualB(+1,-1) + calcResidualB(+1,+1)) / 4.0
    residual_R = np.clip((red_band - R_approx),0,None) + (calcResidualR(-1,-1) + calcResidualR(-1,+1) + calcResidualR(+1,-1) + calcResidualR(+1,+1)) / 4.0



    red_estimation = R_approx + residual
    blue_estimation = B_approx + residual








# END
