# reference: https://segmentfault.com/a/1190000009820053
# 使用此库需要设置VGG19模型路径，即将NETWORK设置为模型文件的绝对路径 


from functools import reduce
from collections import OrderedDict
import numpy as np
import tensorflow as tf2
import cv2
tf=tf2.compat.v1

tf.disable_v2_behavior()

import vgg19
NETWORK='D:\\ProgrammingWorking\\VScode_Python\\OpenCV_DIP\\Final task\\code\\imagenet-vgg-verydeep-19.mat'

CONTENT_LAYERS = ("relu4_2", "relu5_2")
STYLE_LAYERS = ("relu1_1", "relu2_1", "relu3_1", "relu4_1", "relu5_1")
ALPHA=1
BETA=10

def get_loss_vals(loss_store):
    return OrderedDict((key, val.eval()) for key, val in loss_store.items())

def print_progress(loss_vals):
    for key, val in loss_vals.items():
        print("{:>13s} {:g}".format(key + " loss:", val))

def stylize( content, style, iterations):
    #设置一部分初始参数
    content_weight_blend=1.0
    style_layer_weight_exp=1
    style_blend_weights=1.0

    #风格图
    style=cv2.resize(style,content.shape[0:2],interpolation=cv2.INTER_CUBIC)
    content_shape = (1,) + content.shape
    style_shape = (1,) + style.shape
    content_features = {}
    style_features = {} 
    pooling='avg'


    initial=content
    vgg_weights, vgg_mean_pixel = vgg19.load_net(NETWORK)

    layer_weight = 1.0
    style_layers_weights = {}
    for style_layer in STYLE_LAYERS:
        style_layers_weights[style_layer] = layer_weight
        layer_weight *= style_layer_weight_exp

    layer_weights_sum = 0
    for style_layer in STYLE_LAYERS:
        layer_weights_sum += style_layers_weights[style_layer]
    for style_layer in STYLE_LAYERS:
        style_layers_weights[style_layer] /= layer_weights_sum

    # 计算内容图片的feature map
    g = tf.Graph()
    with g.as_default(), g.device("/cpu:0"), tf.Session() as sess:
        image = tf.placeholder("float", shape=content_shape)
        net = vgg19.net_preloaded(vgg_weights, image, pooling)
        content_pre = np.array([vgg19.preprocess(content, vgg_mean_pixel)])
        for layer in CONTENT_LAYERS:
            content_features[layer] = net[layer].eval(feed_dict={image: content_pre})

    # 计算风格图片的feature map
    g = tf.Graph()
    with g.as_default(), g.device("/cpu:0"), tf.Session() as sess:
        image = tf.placeholder("float", shape=style_shape)
        net = vgg19.net_preloaded(vgg_weights, image, pooling)
        style_pre = np.array([vgg19.preprocess(style, vgg_mean_pixel)])
        for layer in STYLE_LAYERS:
            features = net[layer].eval(feed_dict={image: style_pre})
            features = np.reshape(features, (-1, features.shape[3]))
            gram = np.matmul(features.T, features) / features.size
            style_features[layer] = gram

    initial_content_noise_coeff = 1.0

    with tf.Graph().as_default():
        # 计算经过VGG预处理过后的内容图片的feature map
        initial = np.array([vgg19.preprocess(initial, vgg_mean_pixel)])
        initial = initial.astype("float32")
        initial = (initial) * initial_content_noise_coeff 
        image = tf.Variable(initial)
        net = vgg19.net_preloaded(vgg_weights, image, pooling)

        # 计算content loss
        content_layers_weights = {}
        content_layers_weights["relu4_2"] = content_weight_blend
        content_layers_weights["relu5_2"] = 1.0 - content_weight_blend

        content_loss = 0
        content_losses = []
        for content_layer in CONTENT_LAYERS:
            content_losses.append(
                content_layers_weights[content_layer]*(
                    2*tf.nn.l2_loss(net[content_layer] - content_features[content_layer])
                    / content_features[content_layer].size
                )
            )
        content_loss += reduce(tf.add, content_losses)

        # 计算style loss
        style_loss = 0
        style_losses = []
        for style_layer in STYLE_LAYERS:
            layer = net[style_layer]
            _, height, width, number = map(lambda style: style.value, layer.get_shape())
            size = height * width * number
            feats = tf.reshape(layer, (-1, number))
            gram = tf.matmul(tf.transpose(feats), feats) / size
            style_gram = style_features[style_layer]
            style_losses.append(
                    style_layers_weights[style_layer]
                    * 2
                    * tf.nn.l2_loss(gram - style_gram)
                    / style_gram.size
                )
        style_loss += style_blend_weights * reduce(tf.add, style_losses)

        # total loss
        total_loss = ALPHA*content_loss + BETA*style_loss

        loss_store = OrderedDict(
            [("content", content_loss), ("style", style_loss),  ("total", total_loss)]
        )

        # 优化得出最小损失的输出图片
        train_step = tf.train.AdamOptimizer(1e1, 0.9, 0.999, 1e-8).minimize(total_loss)

        best_loss = float("inf")
        best = None
        with tf.Session() as sess:
            sess.run(tf.global_variables_initializer())

            for i in range(iterations):
                print("Iteration %4d/% 4d" % (i + 1, iterations))
                train_step.run()
                
                if i == iterations - 1 :
                    loss_vals = get_loss_vals(loss_store)
                    print_progress(loss_vals)
                    this_loss = total_loss.eval()
                    if this_loss < best_loss:
                        best_loss = this_loss
                        best = image.eval()

                    img_out = vgg19.unprocess(best.reshape(content_shape[1:]), vgg_mean_pixel)
                    return img_out
                else:
                    loss_vals = None
                    img_out = None



