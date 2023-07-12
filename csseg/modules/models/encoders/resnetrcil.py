'''
Function:
    Implementation of ResNetRCIL
Author:
    Zhenchao Jin
'''
import re
import torch
import torch.nn as nn
import torch.nn.functional as F
from .bricks import BuildNormalization
from .resnet import ResNet, BasicBlock, Bottleneck


'''BasicBlockRCIL'''
class BasicBlockRCIL(BasicBlock):
    expansion = 1
    def __init__(self, inplanes, planes, stride=1, dilation=1, downsample=None, norm_cfg=None, act_cfg=None, shortcut_norm_cfg=None, shortcut_act_cfg=None):
        super(BasicBlockRCIL, self).__init__(
            inplanes=inplanes, planes=planes, stride=stride, dilation=dilation, downsample=downsample, 
            norm_cfg=norm_cfg, act_cfg=act_cfg, shortcut_norm_cfg=shortcut_norm_cfg, shortcut_act_cfg=shortcut_act_cfg,
        )
        self.conv2_branch2 = nn.Conv2d(planes, planes, kernel_size=3, stride=1, padding=1, bias=False)
        self.bn2_branch2 = BuildNormalization(placeholder=planes, norm_cfg=shortcut_norm_cfg)
    '''forward'''
    def forward(self, x):
        if isinstance(x, tuple): x = x[0]
        identity = x
        out = self.conv1(x)
        out = self.bn1(out)
        out = F.leaky_relu(out, 0.01)
        out_branch1 = self.conv2(out)
        out_branch1 = self.bn2(out_branch1)
        out_branch2 = self.conv2_branch2(out)
        out_branch2 = self.bn2_branch2(out_branch2)
        r = torch.rand(1, out_branch1.shape[1], 1, 1, dtype=torch.float32)
        if not self.training: r[:, :, :, :] = 1.0
        weight_branch1, weight_branch2 = torch.zeros_like(r), torch.zeros_like(r)
        weight_branch1[r < 0.33] = 2.
        weight_branch1[(r < 0.66) & (r >= 0.33)] = 0.
        weight_branch1[r >= 0.66] = 1.
        weight_branch2[r < 0.33] = 0.
        weight_branch2[(r < 0.66) & (r >= 0.33)] = 2.
        weight_branch2[r >= 0.66] = 1.
        out = out_branch1 * weight_branch1.type_as(out_branch1) * 0.5 + out_branch2 * weight_branch2.type_as(out_branch2) * 0.5
        out = F.leaky_relu(out, 0.01)
        if self.downsample is not None: identity = self.downsample(x)
        out = out + identity
        distillation = out
        out = self.shortcut_relu(out)
        return out, distillation


'''BottleneckRCIL'''
class BottleneckRCIL(Bottleneck):
    expansion = 4
    def __init__(self, inplanes, planes, stride=1, dilation=1, downsample=None, norm_cfg=None, act_cfg=None, shortcut_norm_cfg=None, shortcut_act_cfg=None):
        super(BottleneckRCIL, self).__init__(
            inplanes=inplanes, planes=planes, stride=stride, dilation=dilation, downsample=downsample, 
            norm_cfg=norm_cfg, act_cfg=act_cfg, shortcut_norm_cfg=shortcut_norm_cfg, shortcut_act_cfg=shortcut_act_cfg,
        )
        self.conv2_branch2 = nn.Conv2d(planes, planes, kernel_size=3, stride=stride, padding=dilation, dilation=dilation, bias=False)
        self.bn2_branch2 = BuildNormalization(placeholder=planes, norm_cfg=norm_cfg)
    '''forward'''
    def forward(self, x):
        if isinstance(x, tuple): x = x[0]
        identity = x
        out = self.conv1(x)
        out = self.bn1(out)
        out = F.leaky_relu(out, 0.01)
        out_branch1 = self.conv2(out)
        out_branch1 = self.bn2(out_branch1)
        out_branch2 = self.conv2_branch2(out)
        out_branch2 = self.bn2_branch2(out_branch2)
        r = torch.rand(1, out_branch1.shape[1], 1, 1, dtype=torch.float32)
        if not self.training: r[:, :, :, :] = 1.0
        weight_branch1, weight_branch2 = torch.zeros_like(r), torch.zeros_like(r)
        weight_branch1[r < 0.33] = 2.
        weight_branch1[(r < 0.66) & (r >= 0.33)] = 0.
        weight_branch1[r >= 0.66] = 1.
        weight_branch2[r < 0.33] = 0.
        weight_branch2[(r < 0.66) & (r >= 0.33)] = 2.
        weight_branch2[r >= 0.66] = 1.
        out = out_branch1 * weight_branch1.type_as(out_branch1) * 0.5 + out_branch2 * weight_branch2.type_as(out_branch2) * 0.5
        out = F.leaky_relu(out, 0.01)
        out = self.conv3(out)
        out = self.bn3(out)
        if self.downsample is not None: identity = self.downsample(x)
        out = out + identity
        distillation = out
        out = self.shortcut_relu(out)
        return out, distillation


'''ResNetRCIL'''
class ResNetRCIL(ResNet):
    def __init__(self, in_channels=3, base_channels=64, stem_channels=64, depth=101, outstride=16, contract_dilation=False, deep_stem=False, 
                 out_indices=(0, 1, 2, 3), use_avg_for_downsample=False, norm_cfg={'type': 'InPlaceABNSync', 'activation': 'leaky_relu', 'activation_param': 0.01}, 
                 act_cfg=None,  pretrained=True, pretrained_model_path=None, user_defined_block=None, use_inplaceabn_style=True):
        if user_defined_block is None:
            user_defined_block = BasicBlockRCIL if depth in [18, 34] else BottleneckRCIL
        super(ResNetRCIL, self).__init__(
            in_channels=in_channels, base_channels=base_channels, stem_channels=stem_channels, depth=depth, outstride=outstride, 
            contract_dilation=contract_dilation, deep_stem=deep_stem, out_indices=out_indices, use_avg_for_downsample=use_avg_for_downsample, 
            norm_cfg=norm_cfg, act_cfg=act_cfg, pretrained=pretrained, pretrained_model_path=pretrained_model_path, user_defined_block=user_defined_block,
            use_inplaceabn_style=use_inplaceabn_style,
        )
    '''forward'''
    def forward(self, x):
        outs, distillation_feats = [], []
        if self.deep_stem:
            x = self.stem(x)
        else:
            x = self.conv1(x)
            x = self.bn1(x)
            x = self.relu(x)
        x = self.maxpool(x)
        x1, distillation1 = self.layer1(x)
        x2, distillation2 = self.layer2(x1)
        x3, distillation3 = self.layer3(x2)
        x4, distillation4 = self.layer4(x3)
        for i, feats in enumerate([(x1, distillation1), (x2, distillation2), (x3, distillation3), (x4, distillation4)]):
            if i in self.out_indices: 
                outs.append(feats[0])
                distillation_feats.append(feats[1])
        return tuple(outs), tuple(distillation_feats)
    '''convert in-place abn official checkpoints'''
    def convertabnckpt(self, state_dict):
        for key in list(state_dict.keys()):
            state_dict[key[7:]] = state_dict.pop(key)
        converted_state_dict = dict()
        for key in list(state_dict.keys()):
            if 'mod1' in key:
                converted_state_dict[key[5:]] = state_dict.pop(key)
            else:
                converted_key = key.replace('convs.', '')
                for idx in range(2, 6):
                    converted_key = converted_key.replace(f'mod{idx}', f'layer{idx-1}')
                idx = re.findall(r'\.block(.*?)\.', converted_key)
                if len(idx) > 0:
                    idx = int(idx[0])
                    converted_key = converted_key.replace(f'block{idx}', f'{idx-1}')
                for idx in range(1, 5):
                    oldkeys_to_keys = {
                        f'layer{idx}.0.proj_conv.weight': f'layer{idx}.0.downsample.0.weight', 
                        f'layer{idx}.0.proj_bn.weight': f'layer{idx}.0.downsample.1.weight', 
                        f'layer{idx}.0.proj_bn.bias': f'layer{idx}.0.downsample.1.bias', 
                        f'layer{idx}.0.proj_bn.running_mean': f'layer{idx}.0.downsample.1.running_mean', 
                        f'layer{idx}.0.proj_bn.running_var': f'layer{idx}.0.downsample.1.running_var',
                    }
                    if converted_key in oldkeys_to_keys:
                        converted_key = oldkeys_to_keys[converted_key]
                        break
                assert converted_key not in converted_state_dict
                converted_state_dict[converted_key] = state_dict.pop(key)
        for key in list(converted_state_dict.keys()):
            if 'conv2' in key or 'bn2' in key:
                converted_state_dict[key.replace('conv2', 'conv2_branch2').replace('bn2', 'bn2_branch2')] = converted_state_dict[key]
        return converted_state_dict