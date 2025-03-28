import tensorflow as tf
import keras
from keras import layers



@keras.saving.register_keras_serializable()
class PolynomialDense(layers.Layer):
    def __init__(self, units, activation, extra_args={}, degree=2, epsilon=1e-4, **kwargs):
        super().__init__(**kwargs)
        self.units = units
        self.activation = activation
        self.extra_args = extra_args
        self.degree = degree
        self.epsilon = epsilon

        self.p_proj = layers.Dense(
            units=self.units, activation=self.activation,
            **self.extra_args
        )
        self.normalize_01 = layers.LayerNormalization(axis=-1, epsilon=self.epsilon)
        self.normalize_02 = layers.LayerNormalization(axis=-1, epsilon=self.epsilon)

    def build(self, input_shape):
        p_shape = list(input_shape[:-1]) + [self.degree * input_shape[-1]]
        new_shape = list(input_shape[:-1]) + [self.units]
        self.p_proj.build(p_shape)
        self.normalize_01.build(input_shape)
        self.normalize_02.build(new_shape)

    def p_features(self, x):
        self.features = [x]
        for degree in range(2, self.degree + 1):
            self.features.append(tf.pow(x, degree + 1))
        return tf.concat(self.features, axis=-1)

    def compute_output_shape(self, input_shape):
        return input_shape[:-1] + (self.units,)

    def call(self, inputs):
        x = self.normalize_01(inputs)
        x = self.p_features(x)
        x = self.p_proj(x)
        return self.normalize_02(x)

    def get_config(self):
        config = super().get_config()
        config.update({
            "units": self.units,
            "activation": self.activation,
            "extra_args": self.extra_args,
            "degree": self.degree,
            "epsilon": self.epsilon,
        })
        return config
     
    
@keras.saving.register_keras_serializable()
class GMPLPBlock(layers.Layer):
    def __init__(self, units, activation, drop_rate, extra_args={}, degree=2, epsilon=1e-4, **kwargs):
        self.units = units
        self.activation = activation
        self.drop_rate = drop_rate
        self.extra_args = extra_args
        self.degree = degree
        self.epsilon = epsilon
        super().__init__(**kwargs)

    def build(self, input_shape):
        self.p_dense_01 = PolynomialDense(
            units=2 * self.units,
            activation=self.activation,
            extra_args=self.extra_args,
            degree=self.degree,
            epsilon=self.epsilon
        )
        self.p_dense_02 = PolynomialDense(
            units=self.units,
            activation="linear",
            extra_args=self.extra_args,
            degree=self.degree,
            epsilon=self.epsilon
        )
        self.spatial_proj = layers.Dense(
            units=input_shape[-2],
            activation="linear",
            bias_initializer="ones"
        )
        self.normalize = layers.LayerNormalization(
            axis=-1,
            epsilon=self.epsilon
        )
        self.dropout = layers.Dropout(self.drop_rate)

        if self.units != input_shape[1]:
            self.proj = layers.Dense(
                units=self.units,
                activation="linear",
                **self.extra_args
            )
        else:
            self.proj = None

        new_shape = list(input_shape[:-1]) + [self.units] 
        spatial_shape = (new_shape[0], new_shape[-1], new_shape[1])
        self.p_dense_01.build(new_shape)
        self.p_dense_02.build(new_shape)
        self.spatial_proj.build(spatial_shape)
        self.normalize.build(new_shape)
        self.dropout.build(new_shape)
        if self.units != input_shape[1]:
            self.proj.build(input_shape)

    def spatial_gating_unit(self, x):
        u, g = keras.ops.split(x, indices_or_sections=2, axis=-1)
        g = keras.ops.transpose(g, axes=(0, 2, 1))
        g = self.spatial_proj(g)
        g = keras.ops.transpose(g, axes=(0, 2, 1))
        return u * g

    def call(self, inputs):
        if self.proj is not None:
            inputs = self.proj(inputs)
        x = self.p_dense_01(inputs)
        x = self.dropout(x)
        x_spatial = self.spatial_gating_unit(x)
        x = self.p_dense_02(x_spatial)
        return self.normalize(inputs + x)

    def compute_output_shape(self, input_shape):
        return input_shape[:-1] + (self.units,)

    def get_config(self):
        config = super().get_config()
        config.update({
            "units": self.units,
            "activation": self.activation,
            "drop_rate": self.drop_rate,
            "extra_args": self.extra_args,
            "degree": self.degree,
            "epsilon": self.epsilon,
        })
        return config