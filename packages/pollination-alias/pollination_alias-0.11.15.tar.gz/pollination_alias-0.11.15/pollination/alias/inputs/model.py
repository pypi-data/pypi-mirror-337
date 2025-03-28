from pollination_dsl.alias import InputAlias
from queenbee.io.common import IOAliasHandler


"""Alias inputs that expect a HBJSON model file as the recipe input."""
hbjson_model_input = [
    # RH GH Alias
    InputAlias.any(
        name='model',
        description='A Honeybee Model to simulate or the path to a HBJSON file '
        'of a Model. This can also be the path to a HBpkl file, though this is only '
        'recommended for cases where the model is extremely large.',
        platform=['grasshopper', 'rhino'],
        handler=[
            IOAliasHandler(
                language='python', module='pollination_handlers.inputs.model',
                function='model_to_json'
            ),
            IOAliasHandler(
                language='csharp', module='Pollination.RhinoHandlers',
                function='HBModelToJSON'
            )
        ]
    ),
    InputAlias.any(
        name='model',
        description='A Honeybee Model to simulate or the path to a HBJSON file '
        'of a Model. This can also be the path to a HBpkl file, though this is only '
        'recommended for cases where the model is extremely large.',
        platform=['revit'],
        handler=[
            IOAliasHandler(
                language='python', module='pollination_handlers.inputs.model',
                function='model_to_json'
            )
        ]
    )
]


"""Alias inputs that expect a HBJSON model with sensor grids."""
hbjson_model_grid_input = [
    # RH GH Alias
    InputAlias.any(
        name='model',
        description='A Honeybee Model to simulate or the path to a HBJSON file '
        'of a Model. This can also be the path to a HBpkl file, though this is only '
        'recommended for cases where the model is extremely large. Note that this '
        'model should have sensor grids assigned to it.',
        platform=['grasshopper'],
        handler=[
            IOAliasHandler(
                language='python', module='pollination_handlers.inputs.model',
                function='model_to_json_grid_check'
            ),
            IOAliasHandler(
                language='csharp', module='Pollination.RhinoHandlers',
                function='HBModelToJSON'
            )
        ]
    ),
    InputAlias.linked(
        name='model',
        description='This input links the model to Rhino model.',
        platform=['rhino'],
        handler=[
            IOAliasHandler(
                language='csharp', module='Pollination.RhinoHandlers',
                function='RhinoHBModelToJSON'
            )
        ]
    ),
    InputAlias.any(
        name='model',
        description='A Honeybee Model to simulate or the path to a HBJSON file '
        'of a Model. This can also be the path to a HBpkl file, though this is only '
        'recommended for cases where the model is extremely large. Note that this '
        'model should have sensor grids assigned to it.',
        platform=['revit'],
        handler=[
            IOAliasHandler(
                language='python', module='pollination_handlers.inputs.model',
                function='model_to_json_grid_check'
            )
        ]
    )
]


"""Alias inputs that expect a HBJSON model with sensor grids and rooms."""
hbjson_model_grid_room_input = [
    # RH GH Alias
    InputAlias.any(
        name='model',
        description='A Honeybee Model to simulate or the path to a HBJSON file '
        'of a Model. Note that this model must contain rooms and have sensor '
        'grids assigned to it.',
        platform=['grasshopper', 'rhino'],
        handler=[
            IOAliasHandler(
                language='python', module='pollination_handlers.inputs.model',
                function='model_to_json_grid_room_check'
            ),
            IOAliasHandler(
                language='csharp', module='Pollination.RhinoHandlers',
                function='HBModelToJSON'
            )
        ]
    ),
    InputAlias.any(
        name='model',
        description='A Honeybee Model to simulate or the path to a HBJSON file '
        'of a Model. Note that this model must contain rooms and have sensor '
        'grids assigned to it.',
        platform=['revit'],
        handler=[
            IOAliasHandler(
                language='python', module='pollination_handlers.inputs.model',
                function='model_to_json_grid_room_check'
            )
        ]
    )
]


"""Alias inputs that expect a HBJSON model with Rooms."""
hbjson_model_room_input = [
    # RH GH Alias
    InputAlias.any(
        name='model',
        description='A Honeybee Model to simulate or the path to a HBJSON file '
        'of a Model. This can also be the path to a HBpkl file, though this is only '
        'recommended for cases where the model is extremely large. Note that this '
        'model should have Rooms assigned to it to be usable with this recipe.',
        platform=['grasshopper', 'rhino'],
        handler=[
            IOAliasHandler(
                language='python', module='pollination_handlers.inputs.model',
                function='model_to_json_room_check'
            ),
            IOAliasHandler(
                language='csharp', module='Pollination.RhinoHandlers',
                function='HBModelToJSON'
            )
        ]
    ),
    InputAlias.any(
        name='model',
        description='A Honeybee Model to simulate or the path to a HBJSON file '
        'of a Model. This can also be the path to a HBpkl file, though this is only '
        'recommended for cases where the model is extremely large. Note that this '
        'model should have Rooms assigned to it to be usable with this recipe.',
        platform=['revit'],
        handler=[
            IOAliasHandler(
                language='python', module='pollination_handlers.inputs.model',
                function='model_to_json_room_check'
            )
        ]
    )
]


"""Alias inputs that expect a HBJSON model with HVAC systems."""
hbjson_model_hvac_input = [
    # RH GH Alias
    InputAlias.any(
        name='model',
        description='A Honeybee Model to simulate or the path to a HBJSON file '
        'of a Model. Note that this model should represent a full building and '
        'have Programs, ConstructionSets, and real HVAC systems (other than Ideal Air) '
        'assigned to it. If the building has hot water loads, the building should also '
        'have a SHW system assigned to it for the results to be meaningful.',
        platform=['grasshopper', 'rhino'],
        handler=[
            IOAliasHandler(
                language='python', module='pollination_handlers.inputs.model',
                function='model_to_json_hvac_check'
            ),
            IOAliasHandler(
                language='csharp', module='Pollination.RhinoHandlers',
                function='HBModelToJSON'
            )
        ]
    ),
    InputAlias.any(
        name='model',
        description='A Honeybee Model to simulate or the path to a HBJSON file '
        'of a Model. Note that this model should represent a full building and '
        'have Programs, ConstructionSets, and real HVAC systems (other than Ideal Air) '
        'assigned to it. If the building has hot water loads, the building should also '
        'have a SHW system assigned to it for the results to be meaningful.',
        platform=['revit'],
        handler=[
            IOAliasHandler(
                language='python', module='pollination_handlers.inputs.model',
                function='model_to_json_hvac_check'
            )
        ]
    )
]


"""Alias inputs that expect a HBJSON model with views."""
hbjson_model_view_input = [
    # RH GH Alias
    InputAlias.any(
        name='model',
        description='A Honeybee Model to simulate or the path to a HBJSON file '
        'of a Model. This can also be the path to a HBpkl file, though this is only '
        'recommended for cases where the model is extremely large. Note that this '
        'model should have views assigned to it.',
        platform=['grasshopper', 'rhino'],
        handler=[
            IOAliasHandler(
                language='python', module='pollination_handlers.inputs.model',
                function='model_to_json_view_check'
            ),
            IOAliasHandler(
                language='csharp', module='Pollination.RhinoHandlers',
                function='HBModelToJSON'
            )
        ]
    ),
    InputAlias.any(
        name='model',
        description='A Honeybee Model to simulate or the path to a HBJSON file '
        'of a Model. This can also be the path to a HBpkl file, though this is only '
        'recommended for cases where the model is extremely large. Note that this '
        'model should have views assigned to it.',
        platform=['revit'],
        handler=[
            IOAliasHandler(
                language='python', module='pollination_handlers.inputs.model',
                function='model_to_json_view_check'
            )
        ]
    )
]

"""Alias inputs that expect a DFJSON model file as the recipe input."""
dfjson_model_input = [
    # grasshopper Alias
    InputAlias.any(
        name='model',
        description='A Dragonfly Model object or the path to a DFJSON file.',
        platform=['grasshopper'],
        handler=[
            IOAliasHandler(
                language='python', module='pollination_handlers.inputs.model',
                function='model_dragonfly_to_json'
            )
        ]
    )
]
