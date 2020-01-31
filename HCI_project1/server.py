'''

You can modify the parameters, return values and data structures used in every function if it conflicts with your
coding style or you want to accelerate your code.

You can also import packages you want.

But please do not change the basic structure of this file including the function names. It is not recommended to merge
functions, otherwise it will be hard for TAs to grade your code. However, you can add helper function if necessary.

'''

from flask import Flask, request
from flask import render_template
import time
import json
import math
import matplotlib.pyplot as plt


app = Flask(__name__)

# Centroids of 26 keys
centroids_X = [50, 205, 135, 120, 100, 155, 190, 225, 275, 260, 295, 330, 275, 240, 310, 345, 30, 135, 85, 170, 240, 170, 65, 100, 205, 65]
centroids_Y = [85, 120, 120, 85,  50,  85,  85,  85,  50,  85,  85,  85,  120, 120, 50,  50,  50, 50,  85, 50,  50,  120, 50, 120, 50, 120]

# Pre-process the dictionary and get templates of 10000 words
words, probabilities = [], {}
template_points_X, template_points_Y = [], []
file = open('words_10000.txt')
content = file.read()
file.close()
content = content.split('\n')
for line in content:
    line = line.split('\t')
    words.append(line[0])
    probabilities[line[0]] = float(line[2])
    template_points_X.append([])
    template_points_Y.append([])
    for c in line[0]:
        template_points_X[-1].append(centroids_X[ord(c) - 97])
        template_points_Y[-1].append(centroids_Y[ord(c) - 97])


def generate_sample_points(points_X, points_Y):
    '''Generate 100 sampled points for a gesture.

    In this function, we should convert every gesture or template to a set of 100 points, such that we can compare
    the input gesture and a template computationally.

    :param points_X: A list of X-axis values of a gesture.
    :param points_Y: A list of Y-axis values of a gesture.

    :return:
        sample_points_X: A list of X-axis values of a gesture after sampling, containing 100 elements.
        sample_points_Y: A list of Y-axis values of a gesture after sampling, containing 100 elements.
    '''


    sample_points_X, sample_points_Y = [], []
    # TODO: Start sampling (12 points)

    distance = 0

    for i in range(1,len(points_X)):
        s_x = points_X[i] - points_X[i-1]
        s_y = points_Y[i] - points_Y[i-1]
        s = math.sqrt(math.pow(s_x, 2) + math.pow(s_y, 2))
        distance += s


    distance = distance / 99

    # sample starting and ending point
    sample_points_X.append(float(points_X[0]))
    sample_points_Y.append(float(points_Y[0]))

    sample_point_count = 1
    cur_distance = distance
    # print("distance = ", distance)
    for i in range(1,len(points_X)):
        s_x = points_X[i] - points_X[i-1]
        s_y = points_Y[i] - points_Y[i-1]
        s = math.sqrt(math.pow(s_x, 2) + math.pow(s_y, 2))
        # print("s = ",s)
        while(s  > cur_distance):
            # print(cur_distance)
            if abs(s_x) != 0:
                k = s_y / s_x
                if s_x >= 0:
                    x1 = math.sqrt(math.pow(cur_distance,2) / (math.pow(k,2) + 1)) + points_X[i-1]
                else:
                    x1 = points_X[i-1] - math.sqrt(math.pow(cur_distance,2) / (math.pow(k,2) + 1))

                y1 = points_Y[i-1] + k*(x1 - points_X[i-1])
                sample_points_X.append(float(x1))
                sample_points_Y.append(float(y1))
                # print((s_x,s_y),(x1,y1) , (points_X[i-1], points_Y[i-1]), math.sqrt(math.pow(x1- points_X[i-1], 2) + math.pow(y1 - points_Y[i-1], 2)))
                cur_distance = cur_distance + distance
                sample_point_count = sample_point_count +1
            else:
                x1 = points_X[i-1]
                if s_y > 0:
                    y1 = points_Y[i-1] + cur_distance
                else:
                    y1 = points_Y[i-1] - cur_distance
                sample_points_X.append(x1)
                sample_points_Y.append(y1)
                cur_distance = cur_distance + distance
                sample_point_count = sample_point_count +1

        if(s == cur_distance):
            if len(sample_points_X) == 100 and len(sample_points_Y) == 100: break
            if(sample_points_X.__contains__(float(points_X[i])) and sample_points_Y.__contains__(float(points_Y[i]))):
                continue
            sample_points_X.append(float(points_X[i]))
            sample_points_Y.append(float(points_Y[i]))
            # print(points_X[i], points_Y[i])
            sample_point_count = sample_point_count +1
            cur_distance = cur_distance - s
            continue

        if(s < cur_distance):
            cur_distance = cur_distance - s
            # print((s,cur_distance),(points_X[i],points_Y[i]),(points_X[i-1],points_Y[i-1]))
            continue

    if len(sample_points_X) != 100 and len(sample_points_X) < 100:
        sample_points_X.append(float(points_X[len(points_X)-1]))
    if len(sample_points_Y) != 100 and len(sample_points_Y) < 100:
        sample_points_Y.append(float(points_Y[len(points_Y)-1]))
    # print(sample_points_X)

    while(len(sample_points_X) < 100):
        sample_points_X.append(sample_points_X[0])
        sample_points_Y.append(sample_points_Y[0])

    if len(sample_points_X) > 100:
        for i in range(1, len(sample_points_X)):
            if i < len(sample_points_X) and sample_points_X[i] == sample_points_X[i - 1] and sample_points_Y[i] == sample_points_Y[i - 1]:
                sample_points_X.remove(sample_points_X[i - 1])
                sample_points_Y.remove(sample_points_Y[i - 1])

    return sample_points_X, sample_points_Y


# Pre-sample every template
template_sample_points_X, template_sample_points_Y = [], []
for i in range(10000):
    X, Y = generate_sample_points(template_points_X[i], template_points_Y[i])
    # if(len(X) != 100 or len(Y) != 100): continue

    template_sample_points_X.append(X)
    template_sample_points_Y.append(Y)
    # if(len(X) != 100 or len(Y) != 100):
    #     print(len(X),len(Y))
    #     print(words[i], template_points_X[i],template_points_Y[i])
    # print(len(template_sample_points_X[i]), len(template_sample_points_Y[i]))
    # print(words[i], template_sample_points_X[i] , template_sample_points_Y[i])



# show the test case
# X, Y = template_sample_points_X[len(template_sample_points_X)-1], template_sample_points_Y[len(template_sample_points_Y)-1]
# # for x,y in zip(X,Y):
# #     print((x,y))
# fig = plt.figure()
# plt.scatter(X, Y, color='red', marker='+',s= 200)
# plt.scatter(template_points_X[len(template_points_X)-1],template_points_Y[len(template_points_Y)-1])
# # plt.plot(points_X,points_Y)
# plt.gca().set_aspect('equal', adjustable='box')
# # plt.draw()
# plt.show()

def do_pruning(gesture_points_X, gesture_points_Y, template_sample_points_X, template_sample_points_Y):
    '''Do pruning on the dictionary of 10000 words.

    In this function, we use the pruning method described in the paper (or any other method you consider it reasonable)
    to narrow down the number of valid words so that the ambiguity can be avoided to some extent.

    :param gesture_points_X: A list of X-axis values of input gesture points, which has 100 values since we have
        sampled 100 points.
    :param gesture_points_Y: A list of Y-axis values of input gesture points, which has 100 values since we have
        sampled 100 points.
    :param template_sample_points_X: 2D list, containing X-axis values of every template (10000 templates in total).
        Each of the elements is a 1D list and has the length of 100.
    :param template_sample_points_Y: 2D list, containing Y-axis values of every template (10000 templates in total).
        Each of the elements is a 1D list and has the length of 100.

    :return:
        valid_words: A list of valid words after pruning.
        valid_probabilities: The corresponding probabilities of valid_words.
        valid_template_sample_points_X: 2D list, the corresponding X-axis values of valid_words. Each of the elements
            is a 1D list and has the length of 100.
        valid_template_sample_points_Y: 2D list, the corresponding Y-axis values of valid_words. Each of the elements
            is a 1D list and has the length of 100.
    '''
    valid_words, valid_template_sample_points_X, valid_template_sample_points_Y = [], [], []
    # TODO: Set your own pruning threshold
    threshold = 20
    for i in range(len(template_sample_points_X)):
        # print(gesture_points_X)
        # print(gesture_points_Y)
        # print("-------------------")
        # print(len(gesture_points_X))
        # print(len(gesture_points_Y))
        # print(len(template_sample_points_X[i]))
        # print(len(template_sample_points_Y[i]))
        # print(template_sample_points_X)
        # print(template_sample_points_Y)
        start_x = gesture_points_X[0] - template_sample_points_X[i][0]
        start_y = gesture_points_Y[0] - template_sample_points_Y[i][0]
        # quater_front_x = gesture_points_X[25] - template_sample_points_X[i][25]
        # quater_front_y = gesture_points_Y[25] - template_sample_points_Y[i][25]
        # mid_x = gesture_points_X[50] - template_sample_points_X[i][50]
        # mid_y = gesture_points_Y[50] - template_sample_points_Y[i][50]
        # quater_back_x = gesture_points_X[75] - template_sample_points_X[i][75]
        # quater_back_y = gesture_points_Y[75] - template_sample_points_Y[i][75]
        end_x = gesture_points_X[99] - template_sample_points_X[i][99]
        end_y = gesture_points_Y[99] - template_sample_points_Y[i][99]


        distance_start = math.sqrt(math.pow(start_x,2) + math.pow(start_y,2))
        distance_end = math.sqrt(math.pow(end_x,2) + math.pow(end_y,2))
        # distance_mid = math.sqrt(math.pow(mid_x, 2) + math.pow(mid_y, 2))
        # distance_quater_front = math.sqrt(math.pow(quater_front_x, 2) + math.pow(quater_front_y, 2))
        # distance_quater_back = math.sqrt(math.pow(quater_back_x, 2) + math.pow(quater_back_y, 2))
        # and distance_mid < threshold and distance_quater_front < threshold and distance_quater_back < threshold
        if(distance_start + distance_end < threshold):
            # print(words[i])
            # print("gesture x = ", gesture_points_X)
            # print("template x = ", (template_sample_points_X[i]))
            # print("gesture y = ", gesture_points_Y)
            # print("template y = ", (template_sample_points_Y[i]))
            valid_template_sample_points_X.append(template_sample_points_X[i])
            valid_template_sample_points_Y.append(template_sample_points_Y[i])
            valid_words.append(words[i])
    # TODO: Do pruning (12 points)

    return valid_words, valid_template_sample_points_X, valid_template_sample_points_Y


def get_shape_scores(gesture_sample_points_X, gesture_sample_points_Y, valid_template_sample_points_X, valid_template_sample_points_Y):
    '''Get the shape score for every valid word after pruning.

    In this function, we should compare the sampled input gesture (containing 100 points) with every single valid
    template (containing 100 points) and give each of them a shape score.

    :param gesture_sample_points_X: A list of X-axis values of input gesture points, which has 100 values since we
        have sampled 100 points.
    :param gesture_sample_points_Y: A list of Y-axis values of input gesture points, which has 100 values since we
        have sampled 100 points.
    :param valid_template_sample_points_X: 2D list, containing X-axis values of every valid template. Each of the
        elements is a 1D list and has the length of 100.
    :param valid_template_sample_points_Y: 2D list, containing Y-axis values of every valid template. Each of the
        elements is a 1D list and has the length of 100.

    :return:
        A list of shape scores.
    '''
    shape_scores = []
    gesture_sample_points_X1 = [0] * 100
    gesture_sample_points_Y1 = [0] * 100
    valid_template_sample_points_X1 = []
    valid_template_sample_points_Y1 = []
    for i in range(len(valid_template_sample_points_X)):
        valid_template_sample_points_X1.append([0] * 100)
        valid_template_sample_points_Y1.append([0] * 100)
    # TODO: Set your own L
    L = 1
    # TODO: Calculate shape scores (12 points)

    X = gesture_sample_points_X
    Y = gesture_sample_points_Y
    g_max_x = None
    g_min_x = None
    g_max_y = None
    g_min_y = None

    for i in range(100):
        if g_max_x == None or g_max_x < gesture_sample_points_X[i]:
            g_max_x = gesture_sample_points_X[i]
        if g_min_x == None or g_min_x > gesture_sample_points_X[i]:
            g_min_x = gesture_sample_points_X[i]

        if g_max_y == None or g_max_y < gesture_sample_points_Y[i]:
            g_max_y = gesture_sample_points_Y[i]
        if g_min_y == None or g_min_y > gesture_sample_points_Y[i]:
            g_min_y = gesture_sample_points_Y[i]

    g_width = g_max_x - g_min_x
    g_height = g_max_y - g_min_y

    g_s = L / max(g_width, g_height)

    mid_gesture_x = ((g_max_x + g_min_x) /2) * g_s
    mid_gesture_y = ((g_max_y + g_min_y) /2) * g_s

    for i in range(100):
        gesture_sample_points_X1[i] = gesture_sample_points_X[i] * g_s - mid_gesture_x
        gesture_sample_points_Y1[i] = gesture_sample_points_Y[i] * g_s - mid_gesture_y

    for i in range(len(valid_template_sample_points_X)):

        max_x = None
        min_x = None
        max_y = None
        min_y = None

        for j in range(100):
            if max_x == None or max_x < valid_template_sample_points_X[i][j]:
                max_x = valid_template_sample_points_X[i][j]
            if min_x == None or min_x > valid_template_sample_points_X[i][j]:
                min_x = valid_template_sample_points_X[i][j]

            if max_y == None or max_y < valid_template_sample_points_Y[i][j]:
                max_y = valid_template_sample_points_Y[i][j]
            if min_y == None or min_y > valid_template_sample_points_Y[i][j]:
                min_y = valid_template_sample_points_Y[i][j]

        width_template = max_x  - min_x
        height_template = max_y - min_y


        s = L / max(width_template,height_template)

        mid_template_x = ((max_x + min_x) / 2) * s
        mid_template_y = ((max_y + min_y) / 2) * s

        for j in range(100):
            valid_template_sample_points_X1[i][j] = valid_template_sample_points_X[i][j] * s - mid_template_x
            valid_template_sample_points_Y1[i][j] = valid_template_sample_points_Y[i][j] * s - mid_template_y

    for i in range(len(valid_template_sample_points_X)):

        distance = 0
        for j in range(100):
            template_x = valid_template_sample_points_X1[i][j]
            template_y = valid_template_sample_points_Y1[i][j]
            gesture_x = gesture_sample_points_X1[j]
            gesture_y = gesture_sample_points_Y1[j]

            distance = distance + math.sqrt(math.pow(template_x - gesture_x, 2) + math.pow(template_y - gesture_y, 2))
        # print("test")
        # print(valid_template_sample_points_X1[i])
        # print(valid_template_sample_points_Y1[i])
        # print(gesture_sample_points_X1)
        # print(gesture_sample_points_Y1)
        # print(words[i], distance)
        score = distance / 100

        shape_scores.append(score)

    return shape_scores


def get_location_scores(gesture_sample_points_X, gesture_sample_points_Y, valid_template_sample_points_X, valid_template_sample_points_Y):
    '''Get the location score for every valid word after pruning.

    In this function, we should compare the sampled user gesture (containing 100 points) with every single valid
    template (containing 100 points) and give each of them a location score.

    :param gesture_sample_points_X: A list of X-axis values of input gesture points, which has 100 values since we
        have sampled 100 points.
    :param gesture_sample_points_Y: A list of Y-axis values of input gesture points, which has 100 values since we
        have sampled 100 points.
    :param template_sample_points_X: 2D list, containing X-axis values of every valid template. Each of the
        elements is a 1D list and has the length of 100.
    :param template_sample_points_Y: 2D list, containing Y-axis values of every valid template. Each of the
        elements is a 1D list and has the length of 100.

    :return:
        A list of location scores.
    '''
    location_scores = []
    radius = 15



    # TODO: Calculate location scores (12 points)
    alpha = [0] * 100
    for i in range(50,100):
        alpha[i] = (i - 50) * (0.02/49)

    for i in range(49,-1,-1):
        alpha[i] = abs(i - 49) * (0.02/49)

    for i in range(len(valid_template_sample_points_X)):
        score = 0
        lambda1 = 0
        for j in range(100):
            Dtu = 0
            Dut = 0

            for k in range(100):
                template_x = valid_template_sample_points_X[i][k]
                template_y = valid_template_sample_points_Y[i][k]

                min_dis = None
                for l in range(100):
                    gesture_x = gesture_sample_points_X[l]
                    gesture_y = gesture_sample_points_Y[l]

                    # print("**********")
                    # print(template_x,template_y)
                    # print(gesture_x,gesture_y)
                    dis = math.sqrt(math.pow(template_x - gesture_x, 2) + math.pow(template_y - gesture_y, 2))
                    # print(dis)

                    if min_dis == None or min_dis > dis:
                        min_dis = dis
                # print("min_dis = ", min_dis)

                min_dis = min_dis - radius

                Dtu += max(min_dis, 0)

            for k in range(100):
                gesture_x = gesture_sample_points_X[k]
                gesture_y = gesture_sample_points_Y[k]

                min_dis = None
                for l in range(100):

                    template_x = valid_template_sample_points_X[i][l]
                    template_y = valid_template_sample_points_Y[i][l]

                    dis = math.sqrt(math.pow(template_x - gesture_x, 2) + math.pow(template_y - gesture_y, 2))

                    if (min_dis == None or min_dis > dis):
                        min_dis = dis
                min_dis = min_dis - radius

                Dut += max(min_dis, 0)

            if Dut == 0 and Dtu == 0:
                lambda1 = 0
                # location_scores.append(lambda1)
                score = score + lambda1 * alpha[j]

            else:
                # print("----------------")
                gesture_x = gesture_sample_points_X[j]
                gesture_y = gesture_sample_points_Y[j]
                template_x = valid_template_sample_points_X[i][j]
                template_y = valid_template_sample_points_Y[i][j]

                lambda1 = math.sqrt(math.pow(template_x - gesture_x, 2) + math.pow(template_y - gesture_y,2))
                score = score + lambda1 * alpha[j]

        location_scores.append(score)
    return location_scores


def get_integration_scores(shape_scores, location_scores):
    integration_scores = []
    # TODO: Set your own shape weight
    shape_coef = 0.5
    # TODO: Set your own location weight
    location_coef = 0.5
    for i in range(len(shape_scores)):
        integration_scores.append(shape_coef * shape_scores[i] + location_coef * location_scores[i])
    return integration_scores


def get_best_word(valid_words, integration_scores):
    '''Get the best word.

    In this function, you should select top-n words with the highest integration scores and then use their corresponding
    probability (stored in variable "probabilities") as weight. The word with the highest weighted integration score is
    exactly the word we want.

    :param valid_words: A list of valid words.
    :param integration_scores: A list of corresponding integration scores of valid_words.
    :return: The most probable word suggested to the user.
    '''
    best_word = ""
    # TODO: Set your own range.
    n = 3
    # TODO: Get the best word (12 points)
    min = None
    index = 0
    for i in range(len(integration_scores)):
        if(min == None or integration_scores[i] < min):
            min = integration_scores[i]
            index = i

    best_word = valid_words[index]

    for i in range(len(integration_scores)):
        if(integration_scores[i] == min and i != index):
            best_word = best_word + " " +  valid_words[i]


    return best_word


@app.route("/")
def init():
    return render_template('index.html')


@app.route('/shark2', methods=['POST'])
def shark2():

    start_time = time.time()
    data = json.loads(request.get_data())

    gesture_points_X = []
    gesture_points_Y = []
    for i in range(len(data)):
        gesture_points_X.append(data[i]['x'])
        gesture_points_Y.append(data[i]['y'])
    # gesture_points_X = [gesture_points_X] ???????????????????????????here has an issue list of list
    # gesture_points_Y = [gesture_points_Y]
    # print("original = " , gesture_points_X)
    # print("original = " , gesture_points_Y)
    gesture_sample_points_X, gesture_sample_points_Y = generate_sample_points(gesture_points_X, gesture_points_Y)
    # print("gesture = ", (gesture_sample_points_X))
    # print("gesture = ", (gesture_sample_points_Y))
    # print("gesture length= ", len(gesture_sample_points_X))
    # print("gesture length= ", len(gesture_sample_points_Y))
    valid_words, valid_template_sample_points_X, valid_template_sample_points_Y = do_pruning(gesture_sample_points_X, gesture_sample_points_Y, template_sample_points_X, template_sample_points_Y)
    # print("valid_words = ", valid_words)
    # for x,y in valid_template_sample_points_X,valid_template_sample_points_Y:
    #     for i,j in zip(x,y):
    #         print((i,j))
    shape_scores = get_shape_scores(gesture_sample_points_X, gesture_sample_points_Y, valid_template_sample_points_X, valid_template_sample_points_Y)
    # print("shape_score = " , shape_scores)
    location_scores = get_location_scores(gesture_sample_points_X, gesture_sample_points_Y, valid_template_sample_points_X, valid_template_sample_points_Y)
    # print("location_score = ", location_scores)

    integration_scores = get_integration_scores(shape_scores, location_scores)
    # print("final_score = ", integration_scores)

    best_word = get_best_word(valid_words, integration_scores)
    # print("best_word = ", best_word)
    end_time = time.time()

    return '{"best_word":"' + best_word + '", "elapsed_time":"' + str(round((end_time - start_time) * 1000, 5)) + 'ms"}'


if __name__ == "__main__":
    app.run()
