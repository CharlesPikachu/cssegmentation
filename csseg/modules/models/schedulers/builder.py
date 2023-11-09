'''
Function:
    Implementation of SchedulerBuilder and BuildScheduler
Author:
    Zhenchao Jin
'''
import copy
from .poly import PolyScheduler
from ...utils import BaseModuleBuilder


'''SchedulerBuilder'''
class SchedulerBuilder(BaseModuleBuilder):
    REGISTERED_MODULES = {
        'PolyScheduler': PolyScheduler,
    }
    '''build'''
    def build(self, optimizer, scheduler_cfg):
        scheduler_cfg = copy.deepcopy(scheduler_cfg)
        scheduler_type = scheduler_cfg.pop('type')
        scheduler_cfg.pop('optimizer_cfg')
        scheduler = self.REGISTERED_MODULES[scheduler_type](optimizer=optimizer, **scheduler_cfg)
        return scheduler


'''BuildScheduler'''
BuildScheduler = SchedulerBuilder().build