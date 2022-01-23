import time
import os
import sys

import numpy as np
import pandas as pd

from sklearn import metrics

from sklearn.preprocessing import label_binarize


#libraries
import tensorflow.compat.v1 as tf
tf.disable_v2_behavior()


def learn_rep(Tr_X, Tr_Y, Te_X, Te_Y, Out_Dir):
    ## input
    X_ = tf.compat.v1.placeholder(tf.float32, shape=[None, Tr_X.shape[1], 1, 1])
    Y_ = tf.compat.v1.placeholder(tf.float32, shape=[None, CLASS])

    ## conv1: convolution 1*5, subsampling 1*2
    W_conv1 = tf.Variable(tf.random.truncated_normal([1, 3, 1, 64], stddev=0.1))
    b_conv1 = tf.Variable(tf.constant(0.1, shape=[64]))
    h_conv1 = tf.nn.conv2d(input=X_, filters=W_conv1, strides=[1, 1, 1, 1], padding='SAME') + b_conv1
    h_relu1 = tf.nn.relu(h_conv1)
    h_norm1 = tf.nn.lrn(h_relu1, 2, bias=1.0, alpha=2e-05, beta=0.75)
    h_pool1 = tf.nn.max_pool2d(input=h_norm1, ksize=[1, 2, 1, 1], strides=[1, 1, 1, 1], padding='SAME')

    ## conv2: convolution 1*5, subsampling 1*2
    W_conv2 = tf.Variable(tf.random.truncated_normal([1, 3, 64, 128], stddev=0.1))
    b_conv2 = tf.Variable(tf.constant(0.1, shape=[128]))
    h_conv2 = tf.nn.conv2d(input=h_pool1, filters=W_conv2, strides=[1, 1, 1, 1], padding='SAME') + b_conv2
    h_relu2 = tf.nn.relu(h_conv2)
    h_norm2 = tf.nn.lrn(h_relu2, 2, bias=1.0, alpha=2e-05, beta=0.75)
    h_pool2 = tf.nn.max_pool2d(input=h_norm2, ksize=[1, 2, 1, 1], strides=[1, 1, 1, 1], padding='SAME')

    ## conv3: convolution 1*3, subsampling 1*2
    W_conv3 = tf.Variable(tf.random.truncated_normal([1, 5, 128, 32], stddev=0.1))
    b_conv3 = tf.Variable(tf.constant(0.1, shape=[32]))
    h_conv3 = tf.nn.conv2d(input=h_pool2, filters=W_conv3, strides=[1, 1, 1, 1], padding='SAME') + b_conv3
    h_relu3 = tf.nn.relu(h_conv3)
    h_norm3 = tf.nn.lrn(h_relu3, 2, bias=1.0, alpha=2e-05, beta=0.75)
    h_pool3 = tf.nn.max_pool2d(input=h_norm3, ksize=[1, 2, 1, 1], strides=[1, 1, 1, 1], padding='SAME')

    ## reshape
    shape_n = int(np.prod(h_pool3.get_shape()[1:]))
    h_pool3_reshape = tf.reshape(h_pool3, [-1, shape_n])

    ## fc4: fully connected, dropout
    W_fc4 = tf.Variable(tf.random.truncated_normal([shape_n, 128], stddev=0.1))
    b_fc4 = tf.Variable(tf.constant(0.1, shape=[128]))
    h_fc4 = tf.matmul(h_pool3_reshape, W_fc4) + b_fc4
    keep_prob = tf.compat.v1.placeholder(tf.float32)
    h_fc4_drop = tf.nn.dropout(h_fc4, rate=1 - (keep_prob))

    ## fc5: readout layer
    W_fc4 = tf.Variable(tf.random.truncated_normal([128, CLASS], stddev=0.1))
    b_fc4 = tf.Variable(tf.constant(0.1, shape=[CLASS]))
    y_conv = tf.compat.v1.nn.xw_plus_b(h_fc4_drop, W_fc4, b_fc4)

    ## loss
    cross_entropy = tf.reduce_mean(input_tensor=tf.nn.softmax_cross_entropy_with_logits(labels=tf.stop_gradient(Y_), logits=y_conv))
    train_step = tf.compat.v1.train.AdamOptimizer(1e-4).minimize(cross_entropy)

    ## add ops to collection for transfer
    tf.compat.v1.add_to_collection("X_", X_)
    tf.compat.v1.add_to_collection("Y_", Y_)
    tf.compat.v1.add_to_collection("h_pool3_reshape", h_pool3_reshape)
    tf.compat.v1.add_to_collection("y_conv", y_conv)
    tf.compat.v1.add_to_collection("train_step", train_step)
    tf.compat.v1.add_to_collection("keep_prob", keep_prob)

    start_time = time.time()
    print('#################  start learning  ####################')
    sample_size = Tr_X.shape[0]
    test_results = []
    with tf.compat.v1.Session(config=tf.compat.v1.ConfigProto(intra_op_parallelism_threads=THREAD_NUM)) as sess:
        sess.run(tf.compat.v1.global_variables_initializer())
        sess.run(tf.compat.v1.local_variables_initializer())
        for e in range(EPOCH_NUM):
            ran = get_batch(sample_size, e)
            train_step.run(session=sess, feed_dict={X_: Tr_X[ran].reshape(Tr_X[ran].shape + (1, 1)), Y_: Tr_Y[ran],
                                                    keep_prob: DROPOUT_PROB})
            if e % 100 == 0 or e == EPOCH_NUM - 1:
                
                tr_label_p, tr_score_p = sess.run([tf.argmax(input=y_conv, axis=1), tf.nn.softmax(y_conv)[:, 1]],
                                                  feed_dict={X_: Tr_X.reshape(Tr_X.shape + (1, 1)), Y_: Tr_Y,
                                                             keep_prob: DROPOUT_PROB})
                tr_label = np.argmax(Tr_Y, 1)
            
                tr_acc = metrics.accuracy_score(tr_label, tr_label_p)

                tr_auc = metrics.roc_auc_score(label_binarize(tr_label, classes=[0,1,2]),label_binarize(tr_label_p, classes=[0,1,2]), average='macro', multi_class='ovo')

                #tr_auc = metrics.roc_curve(tr_label, tr_score_p)
                
                
                #tr_auc = metrics.roc_auc_score(np.array(list(tr_label)), np.array(list(tr_score_p)), average ='macro', multi_class='ovo')                                                                  
                print('epoch %d, training accuracy: %f, AUC: %f' % (e, tr_acc, tr_auc))

                te_label_p, te_score_p = sess.run([tf.argmax(input=y_conv, axis=1), tf.nn.softmax(y_conv)[:, 1]],
                                                  feed_dict={X_: Te_X.reshape(Te_X.shape + (1, 1)), Y_: Te_Y,
                                                             keep_prob: DROPOUT_PROB})
                te_label = np.argmax(Te_Y, 1)
                te_acc = metrics.accuracy_score(te_label, te_label_p)
                te_auc = metrics.roc_auc_score(label_binarize(te_label, classes=[0,1,2]),label_binarize(te_label_p, classes=[0,1,2]), average ='macro', multi_class='ovo')

                print('epoch %d, testing accuracy: %f, AUC: %f \n' % (e, te_acc, te_auc))
                test_results.append([te_acc, te_auc])

        saver = tf.compat.v1.train.Saver()
        saver.save(sess, os.path.join(Out_Dir, 'CNN.ckpt'))

    print('#################  end learning  ####################')
    print("time spent: %s seconds\n" % (time.time() - start_time))

    print('store testing results')
    test_res = np.array(test_results)
    auc_order_index = np.argsort(-test_res[:, 1], axis=0)
    local_test_res = test_res[auc_order_index][0:TOP_K]
    np.save(os.path.join(Out_Dir, 'local_test_res'), local_test_res)


def get_batch(size, e):
    if size % BATCH_SIZE == 0:
        m = size / BATCH_SIZE
        bottom, top = int(e % m * BATCH_SIZE), int(e % m * BATCH_SIZE + BATCH_SIZE)
    else:
        m = size / BATCH_SIZE + 1
        bottom = int(e % m * BATCH_SIZE)
        if bottom + BATCH_SIZE > size:
            top = int(size)
        else:
            top = int(bottom + BATCH_SIZE)
    return range(bottom, top)


def run_cnn():
    data_dir = os.path.join(DIR, EXP_DATA)

    D = np.load(f"{data_dir}/D.npy")
    #D = pd.read_csv(f"{data_dir}/D.csv")
    #D = D.values
    D = D[np.isnan(D).sum(axis=1) <= 1]
    D = np.nan_to_num(D)
    np.random.shuffle(D)
    """
    Y = np.zeros([D.shape[0], CLASS])
    for i, l in enumerate(D[:, 40]):
        print(i, l)
        Y[i, int(l)] = 1.0
    """
    Y = D[:, 40]
    Y = label_binarize(Y, classes=[0,1,2])

    test_size = int(D.shape[0] * TEST_PERCENTAGE)
    print('\n\n domain: %s ' % EXP_DATA)
    print('columns: %d, training samples: %d, testing samples: %d \n\n' % (
        D.shape[1] - 1, D.shape[0] - test_size, test_size))

    
    Te_D_X, Te_D_Y = D[0:test_size, 1:], Y[0:test_size]
    Tr_D_X, Tr_D_Y = D[test_size:, 1:], Y[test_size:]
    learn_rep(Tr_X=Tr_D_X, Tr_Y=Tr_D_Y, Te_X=Te_D_X, Te_Y=Te_D_Y, Out_Dir=data_dir)

    np.save(os.path.join(data_dir, 'Tr_D_X'), Tr_D_X)
    np.save(os.path.join(data_dir, 'Tr_D_Y'), Tr_D_Y)
    np.save(os.path.join(data_dir, 'Te_D_X'), Te_D_X)
    np.save(os.path.join(data_dir, 'Te_D_Y'), Te_D_Y)


CLASS = 3
TOP_K = 7
TEST_PERCENTAGE = 0.3
DROPOUT_PROB = 0.8


## run a domain for debug in IDE 
EPOCH_NUM = 1000
THREAD_NUM = 1
BATCH_SIZE = 100
DIR = '/home/juandiri/TFM/Project/Sample'
EXP_DATA = 'Hungary'
run_cnn()


'''
## run batches of domains in command line
EPOCH_NUM, BATCH_SIZE, THREAD_NUM = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
DIR, EXP_DATA = sys.argv[4], sys.argv[5]
run_cnn()
'''