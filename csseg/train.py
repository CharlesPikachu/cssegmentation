'''
Function:
    Implementation of Trainer
Author:
    Zhenchao Jin
'''
import torch
import warnings
import argparse
import torch.distributed as dist
from configs import BuildConfig
from modules import BuildRunner, BuildDataset
warnings.filterwarnings('ignore')


'''parsecmdargs'''
def parsecmdargs():
    parser = argparse.ArgumentParser(description='CSSegmentation: An Open Source Continual Semantic Segmentation Toolbox Based on PyTorch.')
    parser.add_argument('--local_rank', dest='local_rank', help='node rank for distributed training.', default=0, type=int)
    parser.add_argument('--nproc_per_node', dest='nproc_per_node', help='number of processes per node.', default=2, type=int)
    parser.add_argument('--cfgfilepath', dest='cfgfilepath', help='config file path you want to load.', type=str, required=True)
    cmd_args = parser.parse_args()
    return cmd_args


'''Trainer'''
class Trainer():
    def __init__(self, cmd_args):
        self.cmd_args = cmd_args
        self.cfg = BuildConfig(cmd_args.cfgfilepath)[0]
    '''start'''
    def start(self):
        cmd_args, runner_cfg = self.cmd_args, self.cfg.RUNNER_CFG
        dist.init_process_group(backend=runner_cfg['PARALLEL_CFG']['backend'], init_method=runner_cfg['PARALLEL_CFG']['init_method'])
        torch.cuda.set_device(cmd_args.local_rank)
        for task_id in range(runner_cfg['num_tasks']):
            runner_cfg['task_id'] = task_id
            runner_client = BuildRunner(cmd_args=cmd_args, runner_cfg=runner_cfg)
            runner_client.start()


'''main'''
if __name__ == '__main__':
    cmd_args = parsecmdargs()
    trainer_client = Trainer(cmd_args=cmd_args)
    trainer_client.start()