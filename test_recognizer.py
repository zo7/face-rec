'''
Tests the face recognition module with data from yalefaces.

'''

from facerec import ImageIO
from facerec.FaceRecognizer import FaceRecognizer


if __name__ == '__main__':
    '''
    Perform leave-one-out cross-validation on yalefaces dataset.
    '''

    print 'Loading images from yalefaces...'

    instances = ImageIO.loadYalefacesImages('data/yalefaces/')

    modes = list()
    for instance in instances:
        if instance[2] not in modes:
            modes.append(instance[2])

    # Number of correct classifications overall
    correct_count = 0

    # Number of correct classifications per mode
    total_mode = dict()
    correct_mode = dict()

    for mode in modes:
        total_mode[mode] = 0.0
        correct_mode[mode] = 0.0

    print '\nPer-case results:\n'

    for i in range(0, len(instances)):

        # Take first instance from the list
        test_instance = instances.pop(0)

        label, features, mode = test_instance

        # Train with all other instances
        face_recognizer = FaceRecognizer()
        face_recognizer.train(instances)

        # Make a prediction with removed instance
        predicted_label = face_recognizer.classify(features)

        # Increment tallies
        if predicted_label == label:
            correct_count += 1.0
            correct_mode[mode] += 1.0
        total_mode[mode] += 1.0

        print '[Case {:03d}] Predicted {:2d} as {:2d} ({:^11})'.format(
                i, label, predicted_label, mode)

        # Put instance back on the end of the list
        instances.append(test_instance)

    print '\n---- ---- Results ---- ----\n'
    print 'Overall accuracy: {:.2f} ({:3d}/{:3d})'.format(
            correct_count/len(instances), int(correct_count), len(instances))
    print '\nPer mode:'
    for mode in modes:
        print '\t{:>11} accuracy: {:.2f} ({:2d}/{:2d})'.format(
                mode, correct_mode[mode]/total_mode[mode],
                int(correct_mode[mode]), int(total_mode[mode]))


