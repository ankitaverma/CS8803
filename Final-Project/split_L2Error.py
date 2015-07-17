author = 'ppatel'

def split(in_data):
    split80 = in_data[0:int(len(in_data)*0.8):1]
    split20 = in_data[int(len(in_data)*0.8):len(in_data):1]
    return split80, split20

def L2Error(actual_data, pred_data):
    predFrames = pred_data[0:60:1]
    actualFrames= actual_data[0:60:1]
    predX = []
    predY = []
    actualX = []
    actualY = []
    error = 0
    for i in range(len(predFrames)):
            predX.append(predFrames[i][0])
            predY.append(predFrames[i][1])
            actualX.append(actualFrames[i][0])
            actualY.append(actualFrames[i][1])
            error = error + (actualX[i] - predX[i])**2 + (actualY[i] - predY[i])**2
            error = sqrt(error)
    return predFrames, actualFrames, error



input_file = 'test01.txt'
input_array = get_input(input_file)

split80, split20 = split(input_array)
predFrames, actualFrames, error = L2Error(input_array, input_array)

print split80
print split20
print predFrames
print actualFrames
print error
