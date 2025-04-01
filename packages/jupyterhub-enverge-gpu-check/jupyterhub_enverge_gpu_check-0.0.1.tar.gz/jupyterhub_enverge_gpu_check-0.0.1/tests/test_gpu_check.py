import pytest
from gpu_check import DeviceOperationType, analyze_resource_usage

def assert_resource_usage(result, expected_usage=True):
    """Helper to assert resource usage status"""
    assert result['has_resource_usage'] is expected_usage

def assert_device_variables(result, expected_vars):
    """Helper to assert device variables"""
    assert all(var in result['device_variables'] for var in expected_vars)

def assert_operations(result, op_type, expected_ops):
    """Helper to assert operations of a specific type"""
    assert all(op in result['operations'][op_type] for op in expected_ops)

# Test scenarios data
TEST_SCENARIOS = [
    ('basic_compute.py', ['model'], {
        DeviceOperationType.COMPUTE: ['matmul'],
        DeviceOperationType.MEMORY: ['to']
    }),
    ('device_queries.py', [], {
        DeviceOperationType.QUERY: ['device_count', 'get_device_name', 'is_available']
    }),
    ('memory_operations.py', [], {
        DeviceOperationType.MEMORY: ['randn', 'zeros']
    }),
    ('transformers_trainer.py', ['model', 'tokenizer'], {
        DeviceOperationType.COMPUTE: ['training_forward_backward'],
        DeviceOperationType.MEMORY: ['training_memory', 'from_pretrained']
    }),
    ('imports.py', [], {
        DeviceOperationType.QUERY: ['import']
    }),
    ('data_loading.py', ['dataset_dict'], {
        DeviceOperationType.MEMORY: ['load_dataset']
    }),
    ('model_loading.py', ['model', 'tokenizer'], {
        DeviceOperationType.MEMORY: ['from_pretrained'],
        DeviceOperationType.COMPUTE: ['parameter_freeze']
    }),
    ('text_preprocessing.py', ['tokenizer', 'data_collator'], {
        DeviceOperationType.MEMORY: ['tokenize', 'map'],
        DeviceOperationType.COMPUTE: ['preprocess']
    }),
    ('training_setup.py', ['model', 'trainer'], {
        DeviceOperationType.COMPUTE: ['metrics_compute'],
        DeviceOperationType.MEMORY: ['training_setup']
    }),
    ('validation.py', ['model', 'trainer'], {
        DeviceOperationType.COMPUTE: ['predict', 'metrics_compute'],
        DeviceOperationType.MEMORY: ['validation']
    }),
    ('model_saving.py', ['model', 'trainer'], {
        DeviceOperationType.MEMORY: ['save_model']
    }),
    ('inference.py', ['model', 'tokenizer'], {
        DeviceOperationType.COMPUTE: ['inference'],
        DeviceOperationType.MEMORY: ['tokenize']
    })
]

def test_basic_compute(scenario):
    """Test basic compute operations."""
    if scenario['name'] == 'basic_compute.py':
        result = scenario['result']
        assert_resource_usage(result, True)
        assert_device_variables(result, ['model'])
        assert_operations(result, DeviceOperationType.COMPUTE, ['matmul'])
        assert_operations(result, DeviceOperationType.MEMORY, ['to'])

def test_device_queries(scenario):
    """Test device query operations."""
    if scenario['name'] == 'device_queries.py':
        result = scenario['result']
        assert_resource_usage(result, False)
        assert_device_variables(result, [])
        assert_operations(result, DeviceOperationType.QUERY, 
                        ['device_count', 'get_device_name', 'is_available'])

def test_memory_operations(scenario):
    """Test memory operations."""
    if scenario['name'] == 'memory_operations.py':
        result = scenario['result']
        assert_resource_usage(result, True)
        assert_device_variables(result, [])
        assert_operations(result, DeviceOperationType.MEMORY, ['randn', 'zeros'])

def test_transformers_trainer(scenario):
    """Test transformers trainer scenario."""
    if scenario['name'] == 'transformers_trainer.py':
        result = scenario['result']
        assert_resource_usage(result, True)
        assert_device_variables(result, ['model', 'tokenizer'])
        assert_operations(result, DeviceOperationType.COMPUTE, ['training_forward_backward'])
        assert_operations(result, DeviceOperationType.MEMORY, ['training_memory', 'from_pretrained'])

def test_imports(scenario):
    """Test imports scenario."""
    if scenario['name'] == 'imports.py':
        result = scenario['result']
        assert_resource_usage(result, False)

def test_data_loading(scenario):
    """Test data loading scenario."""
    if scenario['name'] == 'data_loading.py':
        result = scenario['result']
        assert_resource_usage(result, False)

def test_model_loading(scenario):
    """Test model loading scenario."""
    if scenario['name'] == 'model_loading.py':
        result = scenario['result']
        assert_resource_usage(result, True)
        assert_device_variables(result, ['model', 'tokenizer'])
        assert_operations(result, DeviceOperationType.MEMORY, ['from_pretrained'])

def test_text_preprocessing(scenario):
    """Test text preprocessing scenario."""
    if scenario['name'] == 'text_preprocessing.py':
        result = scenario['result']
        assert_resource_usage(result, True)

def test_training_setup(scenario):
    """Test training setup scenario."""
    if scenario['name'] == 'training_setup.py':
        result = scenario['result']
        assert_resource_usage(result, True)

def test_validation(scenario):
    """Test validation scenario."""
    if scenario['name'] == 'validation.py':
        result = scenario['result']
        assert_resource_usage(result, True)

def test_model_saving(scenario):
    """Test model saving scenario."""
    if scenario['name'] == 'model_saving.py':
        result = scenario['result']
        assert_resource_usage(result, True)

def test_inference(scenario):
    """Test inference scenario."""
    if scenario['name'] == 'inference.py':
        result = scenario['result']
        assert_resource_usage(result, True)

def test_lora_config(scenario):
    """Test LoRA configuration."""
    if scenario['name'] == 'lora_config.py':
        assert_resource_usage(scenario['result'], True)

def test_func_definition(scenario):
    """Test function definition."""
    if scenario['name'] == 'func_definition.py':
        assert_resource_usage(scenario['result'], False) 