from .base_parser import BaseParser
from ..utils import _unsqueeze_shape

class UnsqueezeParser(BaseParser):
    """
    Parses the ONNX Unsqueeze node.

    This parser extracts the necessary inputs, outputs and attributes, determines their
    shapes and values, and adds an entry to the parser's node list representing the
    Unsqueeze operation.

    """
    def parse(self, node, parser):
        """
        Parses the Unsqueeze node and updates the parser's internal representation.

        Args:
            node (dict): A dictionary describing the ONNX node. Expected to have the following keys:
            "name", "type", "input", "output", "attributes", "initializers", and "constants".
            parser: The main parser module, which maintains information like
                current_shape, intermediate_tensors_shapes, and the node list.

        Returns:
            None: The method updates the parser in place.

        Side Effects:
            - Updates `parser.intermediate_tensors_shapes` with the output of the node and its shape.
            - Updates `parser.current_shape` with the shape of the output.
            - Appends a new entry to `parser.nodes` describing the Unsqueeze node.
        """
        axes_values = [int(attr.i) for attr in node.attribute if attr.name == "axes"]
        shape_tensor_input = parser.current_shape.copy()
        output_shape = _unsqueeze_shape(parser.current_shape.copy(), axes_values)
        inputs = [{'name': node.input[0], 'shape': shape_tensor_input}]
        outputs = [{'name': node.output[0], 'shape': output_shape}]
        attributes = {'axes' : axes_values}
        parser.intermediate_tensors_shapes[node.output[0]] = output_shape
        parser.current_shape = output_shape.copy()

        parser.nodes.append({
            'name': node.name,
            'type': node.op_type,
            'input': inputs,
            'output': outputs,
            'attributes': attributes,
            'initializers': parser.initializer_values,
            'constants': parser.constant_values
        })

