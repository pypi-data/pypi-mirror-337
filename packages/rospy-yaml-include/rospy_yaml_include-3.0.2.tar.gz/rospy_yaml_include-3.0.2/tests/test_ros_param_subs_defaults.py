#!/usr/bin/env python3
import json
import os
import sys

import pytest
import armw
import yaml

from rospy_yaml_include.yaml_include import (RospyYamlInclude,
                                             extract_arguments,
                                             )


def run(inputs):
    for idx, ip in enumerate(inputs):
        print(f'For Input {idx+1}: "{ip}"')
        results = extract_arguments(ip)
        for r in [x for x in results]:
            print(f'  -> {r}')


class TestRosParamSubsExtractingDefaults(armw.ArmwNode):
    """
    Class containing unit tests for ros_param_substitute include
    with default value inputs
    """
    def __init__(self):
        super(TestRosParamSubsExtractingDefaults, self).__init__()

    def test_extracting_default_args(self):
        """
        Unit test for dynamic relative include
        """
        try:
            self.test_node = armw.ArmwNode()
        except Exception as e:
            print(e)
            pass

        # NOTE: commenting lines MIGHT require restarting roscore
        armw.NODE().set_param("/test", 1)  # comment to raise ValueError
        armw.NODE().set_param("test2", 2)  # comment to test w/ default value "{name}/status"
        armw.NODE().set_param("test3", [3, 3])
        armw.NODE().set_param("test7", [7, 8, 9])  # comment to test w/ default value "[7,7,8,8,9,9]"

        yml = """
            value: !ros_param_substitute ${/test}
            value_default: !ros_param_substitute ${test2; "{name}/status"}
            fields: !ros_param_substitute ${test3;5}
            fields_augmented: !ros_param_substitute ${test3; 5} ${test4; 50}
            fields_default_dict: !ros_param_substitute ${test4; {"test5":5, "test6":6.0,"hello":"world"}}
            fields_default_list: !ros_param_substitute ${test7; [7, 7, 8, 8, 9, 9]}
            """

        cwd = os.getcwd()

        # TODO:
        #  - [ ] better handling of fields_augmented key-value substitutions
        #  - [ ] better handling of fields_default_dict key-value
        #           substitution (yaml.scanner.ScannerError)
        try:
            constructor = RospyYamlInclude(base_directory=cwd)
            params = yaml.load(yml, Loader=constructor.add_constructor())
        except RecursionError as error:
            pytest.fail(f"RecursionError: Maximum recursion limit reached: {error}")
        except yaml.scanner.ScannerError as error:
            pytest.fail(f"ScannerError: {error} (try removing spaces between "
                        f"any mappings [e.g. 'k':v] in the default input)")
        else:
            armw.NODE().log_info(f'Pretty Print:\n{json.dumps(params, indent=4)}')
            armw.NODE().log_info(params)


if __name__ == "__main__":
    # Example extract_arguments() output:
    inputs = [
        "${~status_max_queuesize} ${~status_priority}",
        "${~status_max_queuesize;30} ${~status_priority;50}",
        "${~status_max_queuesize; 30} ${~status_priority}",
        "${~status_max_queuesize} ${~status_priority; 5",
    ]
    run(inputs)

    # Example TestExtractingDefaultArgs
    test = TestRosParamSubsExtractingDefaults()
    test.test_extracting_default_args()
    sys.exit(pytest.main(["--capture=no", __file__]))
