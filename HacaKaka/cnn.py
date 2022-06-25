import tensorflow as tf
from cnn_func import input_layer, downsample_block, upsample_block, output_layer


def init_cnn():
    print(f'Tensorflow version {tf.__version__}')
    print(f'GPU is {"ON" if tf.config.list_physical_devices("GPU") else "OFF"}')

    inp_layer = input_layer()

    downsample_stack = [
        downsample_block(64, 4, batch_norm=False),
        downsample_block(128, 4),
        downsample_block(256, 4),
        downsample_block(512, 4),
        downsample_block(512, 4),
        downsample_block(512, 4),
        downsample_block(512, 4),
    ]

    upsample_stack = [
        upsample_block(512, 4, dropout=True),
        upsample_block(512, 4, dropout=True),
        upsample_block(512, 4, dropout=True),
        upsample_block(256, 4),
        upsample_block(128, 4),
        upsample_block(64, 4)
    ]

    out_layer = output_layer(4)

    x = inp_layer

    downsample_skips = []

    for block in downsample_stack:
        x = block(x)
        downsample_skips.append(x)

    downsample_skips = reversed(downsample_skips[:-1])

    for up_block, down_block in zip(upsample_stack, downsample_skips):
        x = up_block(x)
        x = tf.keras.layers.Concatenate()([x, down_block])

    out_layer = out_layer(x)

    unet_like = tf.keras.Model(inputs=inp_layer, outputs=out_layer)
    #tf.keras.utils.plot_model(unet_like, show_shapes=True, dpi=72)
    unet_like.load_weights('network_2/network')
    return unet_like
