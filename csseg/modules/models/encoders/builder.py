'''
Function:
    Implementation of BuildEncoder
Author:
    Zhenchao Jin
'''
import copy
from .resnet import ResNet
from .resnetcaf import ResNetCAF
from .resnetilt import ResNetILT
from .resnetmib import ResNetMIB
from .resnetucd import ResNetUCD
from .resnetrcil import ResNetRCIL
from .resnetplop import ResNetPLOP
from .resnetreminder import ResNetREMINDER


'''BuildEncoder'''
def BuildEncoder(encoder_cfg):
    encoder_cfg = copy.deepcopy(encoder_cfg)
    # supported encoders
    supported_encoders = {
        'ResNet': ResNet, 'ResNetILT': ResNetILT, 'ResNetMIB': ResNetMIB, 'ResNetPLOP': ResNetPLOP,
        'ResNetUCD': ResNetUCD, 'ResNetRCIL': ResNetRCIL, 'ResNetREMINDER': ResNetREMINDER,
    }
    # parse
    encoder_type = encoder_cfg.pop('type')
    encoder = supported_encoders[encoder_type](**encoder_cfg)
    # return
    return encoder