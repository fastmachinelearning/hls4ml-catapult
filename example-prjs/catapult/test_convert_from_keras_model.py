# Classical jet-tagging model as in the hls4ml tutorial

# Local library
def print_dict(d, indent=0):
    align=20
    for key, value in d.items():
        print('  ' * indent + str(key), end='')
        if isinstance(value, dict):
            print()
            print_dict(value, indent+1)
        else:
            print(':' + ' ' * (20 - len(key) - 2 * indent) + str(value))


# Disable some TensorFlow warnings
import os
os.environ['TF_XLA_FLAGS'] = '--tf_xla_enable_xla_devices'
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'


# Load quantized model from file(s)
from qkeras.utils import _add_supported_quantized_objects
from tensorflow.keras.models import model_from_json

print('INFO: -----------------------------------')
print('INFO: Load model')
co = {}
_add_supported_quantized_objects(co)

with open('keras/qkeras_3layer.json', 'r') as f:
    jsons = f.read()
model = model_from_json(jsons, custom_objects=co)
model.load_weights('keras/qkeras_3layer_weights.h5')
print('INFO: -----------------------------------')


# Ready for hls4ml translation
import hls4ml

print("-----------------------------------")
print('INFO: Generate hls4ml configuration')
config = hls4ml.utils.config_from_keras_model(model, granularity='model')
print("-----------------------------------")
print('INFO: Show configuration')
print_dict(config)


# Vivado backend
print("-----------------------------------")
print('INFO: Generate hls4ml model (Vivado backend)')
hls_model = hls4ml.converters.convert_from_keras_model(model,
                                                       hls_config=config,
                                                       backend='Vivado',
                                                       output_dir='hls4ml_catapult_prj',
                                                       part='xcu250-figd2104-2L-e')
print("-----------------------------------")
print('INFO: Compile hls4ml model (Vivado backend)')
hls_model.compile()
print("-----------------------------------")


# Catapult backend
print("-----------------------------------")
print('INFO: Generate hls4ml model (Catapult backend)')
hls_model = hls4ml.converters.convert_from_keras_model(model,
                                                       hls_config=config,
                                                       backend='Catapult',
                                                       output_dir='hls4ml_catapult_prj',
                                                       part='xcu250-figd2104-2L-e')
print("-----------------------------------")
print('INFO: Compile hls4ml model (Catapult backend)')
hls_model.compile()
print("-----------------------------------")
