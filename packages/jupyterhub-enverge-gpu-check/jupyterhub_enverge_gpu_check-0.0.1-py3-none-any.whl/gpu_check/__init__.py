"""
PyTorch GPU Resource Usage Analyzer

This module provides static analysis capabilities to detect GPU resource usage in PyTorch code.
It analyzes Python code using the Abstract Syntax Tree (AST) to identify operations that consume
GPU resources, including compute cycles, memory, data transfers, and device queries.

Architecture:
- DeviceOperationType: Enum defining categories of GPU operations (compute, memory, query, transfer)
- PyTorchResourceAnalyzer: AST visitor that analyzes code for GPU resource usage
  - Tracks device setup and movement
  - Identifies training contexts and loops
  - Detects multi-GPU operations
  - Categorizes operations by resource type

The analyzer is designed to work with both explicit GPU operations and implicit ones
(e.g., training loops in the Transformers library). It can detect:
- Direct and conditional CUDA device setup
- Model movement to devices
- Training-specific operations
- Multi-GPU distributed operations
- Custom training loops

The module is designed to be used as part of a larger static analysis toolchain
and can be extended with additional operation patterns and training contexts.
"""

import ast
from typing import Set, Dict, List, Optional, Any
from enum import Enum
import logging
from dataclasses import dataclass, field

# Configure logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter('%(levelname)s: %(message)s'))
logger.addHandler(handler)

class DeviceOperationType(Enum):
    """Categories of GPU operations"""
    COMPUTE = "compute"      # Operations that use GPU compute cycles
    MEMORY = "memory"       # Operations that allocate/use VRAM
    QUERY = "query"         # Operations that just check device status
    TRANSFER = "transfer"   # Operations that transfer data between devices

@dataclass
class OperationSets:
    """Sets of operations categorized by type"""
    compute: Set[str] = field(default_factory=set)
    memory: Set[str] = field(default_factory=set)
    transfer: Set[str] = field(default_factory=set)
    query: Set[str] = field(default_factory=set)

    def get_operations(self) -> Dict[DeviceOperationType, Set[str]]:
        """Get operations as a dictionary keyed by operation type"""
        return {
            DeviceOperationType.COMPUTE: self.compute,
            DeviceOperationType.MEMORY: self.memory,
            DeviceOperationType.TRANSFER: self.transfer,
            DeviceOperationType.QUERY: self.query
        }

class PyTorchResourceAnalyzer(ast.NodeVisitor):
    """AST visitor to analyze PyTorch code for device resource usage."""
    
    def __init__(self):
        self.operations = OperationSets()
        self.device_variables: Set[str] = set()
        self.cuda_device_set: bool = False
        self.training_objects: Set[str] = set()
        self.training_setup_complete: bool = False
        self.inside_function: bool = False
        self.has_top_level_resource_usage: bool = False
        self._saved_resource_operations: Optional[Dict[DeviceOperationType, Set[str]]] = None

        # Initialize operation sets
        self._init_operation_sets()

    def _init_operation_sets(self) -> None:
        """Initialize sets of operations by type"""
        # Compute operations
        self.operations.compute = {
            'matmul', 'mm', 'bmm', 'mv', 'bmv',
            'conv1d', 'conv2d', 'conv3d', 'conv_transpose1d', 'conv_transpose2d', 'conv_transpose3d',
            'relu', 'sigmoid', 'tanh', 'softmax', 'softplus', 'gelu', 'selu', 'elu', 'leaky_relu',
            'cross_entropy', 'mse_loss', 'l1_loss', 'bce_loss', 'nll_loss', 'kl_div', 'hinge_embedding_loss',
            'linear', 'embedding', 'lstm', 'gru', 'rnn', 'transformer', 'attention',
            'batch_norm', 'layer_norm', 'instance_norm', 'group_norm',
            'max_pool1d', 'max_pool2d', 'max_pool3d', 'avg_pool1d', 'avg_pool2d', 'avg_pool3d',
            'fft', 'ifft', 'eig', 'svd', 'qr', 'cholesky', 'inverse', 'einsum', 'baddbmm'
        }

        # Memory operations
        self.operations.memory = {
            'zeros', 'ones', 'randn', 'rand', 'randint', 'arange', 'linspace', 'logspace',
            'empty', 'empty_like', 'full', 'full_like',
            'parameters', 'named_parameters', 'state_dict', 'load_state_dict',
            'from_pretrained', 'load', 'save', 'load_state_dict', 'save_state_dict',
            'cuda', 'cpu', 'to', 'detach', 'clone', 'contiguous', 'reshape', 'view',
            'register_buffer', 'buffers', 'named_buffers'
        }

        # Transfer operations
        self.operations.transfer = {
            'to', 'cuda', 'cpu',
            'load', 'from_pretrained', 'load_state_dict',
            'tokenize', 'tokenizer', 'collate', 'collate_fn',
            'Dataset', 'DataLoader', 'Subset', 'ConcatDataset',
            'pin_memory', 'non_blocking', 'async_transfer'
        }

        # Query operations
        self.operations.query = {
            'is_available', 'device_count', 'get_device_name', 'current_device',
            'memory_allocated', 'max_memory_allocated', 'memory_reserved',
            'max_memory_reserved', 'memory_stats', 'memory_summary',
            'get_device_properties', 'get_device_capability',
            'current_stream', 'streams', 'synchronize',
            'profiler', 'profile', 'record_function'
        }

        # Training-related operations
        self.training_classes = {
            'Trainer', 'TrainingArguments', 'DataCollatorWithPadding',
            'TrainerCallback', 'EarlyStoppingCallback', 'LoggingCallback',
            'ModelCheckpoint', 'LearningRateScheduler', 'Optimizer',
            'DistributedDataParallel', 'DataParallel', 'DistributedSampler',
            'distributed', 'all_reduce', 'all_gather', 'broadcast',
            'reduce', 'scatter', 'gather', 'barrier'
        }
        
        self.training_methods = {
            'train', 'evaluate', 'predict', 'save_model', 'load_model',
            'compute_loss', 'training_step', 'validation_step',
            'backward', 'step', 'zero_grad', 'optimize',
            'scheduler_step', 'gradient_clip', 'accumulate_grad_batches'
        }

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        """Track when we enter a function definition"""
        logger.debug(f"AST FunctionDef node: {ast.dump(node, indent=2)}")
        logger.info(f"Entering function: {node.name}")
        
        # Save current state
        self._saved_resource_operations = self.operations.get_operations()
        prev_inside_function = self.inside_function
        prev_has_top_level_resource_usage = self.has_top_level_resource_usage
        
        # Set function state
        self.inside_function = True
        self.has_top_level_resource_usage = False
        
        # Visit function body
        self.generic_visit(node)
        
        # Restore state
        self.inside_function = prev_inside_function
        self.has_top_level_resource_usage = prev_has_top_level_resource_usage
        
        # Restore saved resource operations
        if self._saved_resource_operations is not None:
            logger.info(f"Restoring resource operations in {node.name}")
            self.operations = OperationSets()
            for op_type, ops in self._saved_resource_operations.items():
                setattr(self.operations, op_type.value, ops)
            self._saved_resource_operations = None
            
        logger.info(f"Exiting function: {node.name}")

    def visit_Call(self, node: ast.Call) -> None:
        """Analyze function calls for resource usage"""
        if self.inside_function:
            self.generic_visit(node)
            return

        if isinstance(node.func, ast.Attribute):
            method_name = node.func.attr
            self._handle_method_call(node, method_name)
        elif isinstance(node.func, ast.Name):
            self._handle_function_call(node)
            
        self.generic_visit(node)

    def _handle_method_call(self, node: ast.Call, method_name: str) -> None:
        """Handle method calls for resource analysis"""
        if method_name == 'device' and isinstance(node.func.value, ast.Name) and node.func.value.id == 'torch':
            self._handle_device_setup(node)
        elif method_name == 'to':
            self._handle_model_movement(node)
        elif method_name in self.training_methods:
            self._handle_training_method()
        elif method_name in self.operations.compute:
            self._add_operation(DeviceOperationType.COMPUTE, method_name)
        elif method_name in self.operations.memory:
            self._add_operation(DeviceOperationType.MEMORY, method_name)
        elif method_name in self.operations.transfer:
            self._add_operation(DeviceOperationType.TRANSFER, method_name)
        elif method_name in self.operations.query:
            self._add_operation(DeviceOperationType.QUERY, method_name)

    def _handle_device_setup(self, node: ast.Call) -> None:
        """Handle CUDA device setup"""
        for arg in node.args:
            if isinstance(arg, ast.Constant) and arg.value == 'cuda':
                self._set_cuda_device()
            elif isinstance(arg, ast.IfExp):
                self._handle_conditional_device_setup(arg)

    def _handle_model_movement(self, node: ast.Call) -> None:
        """Handle model movement to device"""
        if len(node.args) > 0:
            if isinstance(node.args[0], ast.Name):
                device_var = node.args[0].id
                if device_var in self.device_variables:
                    self._set_cuda_device()
            elif isinstance(node.args[0], ast.Call):
                self._handle_device_call(node.args[0])

    def _handle_training_method(self) -> None:
        """Handle training method calls"""
        if self.cuda_device_set and self.training_setup_complete:
            self._add_operation(DeviceOperationType.COMPUTE, 'training_forward_backward')
            self._add_operation(DeviceOperationType.MEMORY, 'training_memory')

    def _handle_function_call(self, node: ast.Call) -> None:
        """Handle function calls for resource analysis"""
        if node.func.id in self.training_classes:
            self._handle_training_class(node)
        elif node.func.id in {'DistributedDataParallel', 'DataParallel', 'DistributedSampler'}:
            self._handle_multi_gpu_operation()

    def _handle_training_class(self, node: ast.Call) -> None:
        """Handle training class instantiation"""
        self.training_setup_complete = True
        
        if node.func.id == 'TrainingArguments':
            self._handle_training_arguments(node)
        elif node.func.id == 'Trainer':
            self._handle_trainer(node)

    def _handle_training_arguments(self, node: ast.Call) -> None:
        """Handle TrainingArguments instantiation"""
        for keyword in node.keywords:
            if keyword.arg in ['per_device_train_batch_size', 'per_device_eval_batch_size']:
                self._set_cuda_device()
                break

    def _handle_trainer(self, node: ast.Call) -> None:
        """Handle Trainer instantiation"""
        has_model = False
        for keyword in node.keywords:
            if keyword.arg == 'model':
                has_model = True
            elif keyword.arg in ['train_dataset', 'eval_dataset']:
                if has_model:
                    self._set_cuda_device()
                    break

    def _handle_multi_gpu_operation(self) -> None:
        """Handle multi-GPU operations"""
        self._add_operation(DeviceOperationType.TRANSFER, 'multi_gpu_transfer')
        self._add_operation(DeviceOperationType.COMPUTE, 'multi_gpu_compute')

    def _set_cuda_device(self) -> None:
        """Set CUDA device flag and mark resource usage"""
        self.cuda_device_set = True
        self.has_top_level_resource_usage = True

    def _add_operation(self, op_type: DeviceOperationType, operation: str) -> None:
        """Add operation to appropriate set and mark resource usage"""
        setattr(self.operations, op_type.value, getattr(self.operations, op_type.value) | {operation})
        # Only mark non-query operations as resource usage
        if op_type != DeviceOperationType.QUERY:
            self.has_top_level_resource_usage = True

    def _handle_conditional_device_setup(self, if_exp: ast.IfExp) -> None:
        """Handle conditional CUDA device setup"""
        if (isinstance(if_exp.test, ast.Call) and 
            isinstance(if_exp.test.func, ast.Attribute) and
            if_exp.test.func.attr == 'is_available' and
            isinstance(if_exp.test.func.value, ast.Attribute) and
            if_exp.test.func.value.attr == 'cuda'):
            if isinstance(if_exp.body, ast.Constant) and if_exp.body.value == 'cuda':
                self._set_cuda_device()

    def _handle_device_call(self, node: ast.Call) -> None:
        """Handle device-related function calls"""
        if (isinstance(node.func, ast.Attribute) and 
            node.func.attr == 'device'):
            for arg in node.args:
                if isinstance(arg, ast.IfExp):
                    self._handle_conditional_device_setup(arg)

    def visit_Assign(self, node: ast.Assign) -> None:
        """Track device variable assignments and training object creation"""
        if self.inside_function:
            self.generic_visit(node)
            return

        for target in node.targets:
            if isinstance(target, ast.Name):
                if isinstance(node.value, ast.Call):
                    self._handle_assignment_call(target.id, node.value)
                    
        self.generic_visit(node)

    def _handle_assignment_call(self, target_id: str, call: ast.Call) -> None:
        """Handle assignment of call results"""
        if self._is_device_call(call):
            self.device_variables.add(target_id)
            if isinstance(call.func, ast.Attribute) and call.func.attr == 'device':
                self._handle_device_assignment(call)
        elif isinstance(call.func, ast.Name) and call.func.id in self.training_classes:
            self.training_objects.add(target_id)
            self.training_setup_complete = True

    def _handle_device_assignment(self, call: ast.Call) -> None:
        """Handle device assignment"""
        for arg in call.args:
            if isinstance(arg, ast.Constant) and arg.value == 'cuda':
                self._set_cuda_device()
            elif isinstance(arg, ast.IfExp):
                self._handle_conditional_device_setup(arg)

    def _is_device_call(self, node: ast.Call) -> bool:
        """Check if a call is device-related"""
        if isinstance(node.func, ast.Name):
            return node.func.id in self.operations.transfer
        elif isinstance(node.func, ast.Attribute):
            return node.func.attr in self.operations.transfer
        return False

    def has_resource_usage(self) -> bool:
        """Check if any resource-consuming operations were found outside of function definitions"""
        if self.operations is None:
            logger.warning("Resource operations is None in has_resource_usage")
            return False
        # Only consider compute and memory operations as resource usage
        has_compute = bool(self.operations.compute)
        has_memory = bool(self.operations.memory)
        # Query operations don't count as resource usage
        return (has_compute or has_memory) and self.has_top_level_resource_usage

    def get_resource_operations(self) -> Dict[DeviceOperationType, List[str]]:
        """Get categorized list of detected operations"""
        return {
            op_type: sorted(list(ops))
            for op_type, ops in self.operations.get_operations().items()
        }

    def visit_For(self, node: ast.For) -> None:
        """Detect training loops"""
        if self.cuda_device_set and self.training_objects and not self.inside_function:
            if isinstance(node.target, ast.Name):
                if node.target.id in ['epoch', 'batch', 'step']:
                    self._add_operation(DeviceOperationType.COMPUTE, 'training_forward_backward')
                    self._add_operation(DeviceOperationType.MEMORY, 'training_memory')
        self.generic_visit(node)

    def visit_While(self, node: ast.While) -> None:
        """Detect training loops"""
        if self.cuda_device_set and self.training_objects and not self.inside_function:
            self._add_operation(DeviceOperationType.COMPUTE, 'training_forward_backward')
            self._add_operation(DeviceOperationType.MEMORY, 'training_memory')
        self.generic_visit(node)

def analyze_resource_usage(code: str) -> Dict[str, Any]:
    """
    Analyze PyTorch code for actual device resource usage.
    Returns a dictionary with analysis results.
    """
    try:
        tree = ast.parse(code)
        analyzer = PyTorchResourceAnalyzer()
        analyzer.visit(tree)
        
        return {
            'has_resource_usage': analyzer.has_resource_usage(),
            'operations': analyzer.get_resource_operations(),
            'device_variables': sorted(list(analyzer.device_variables))
        }
    except SyntaxError as e:
        return {
            'error': f'Syntax error: {str(e)}',
            'has_resource_usage': False
        }