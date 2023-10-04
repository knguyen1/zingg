import unittest
import sys

from zingg import *
from zingg.client import *
from zingg.pipes import *

import subprocess
from py4j.java_gateway import JavaGateway
from py4j.protocol import Py4JNetworkError
from time import sleep
from multiprocessing import Process
from py4j.java_gateway import JavaGateway, GatewayParameters

# PY4J_JAVA_PATH='.:../thirdParty/lib//py4j0.10.9.jar:$ZINGG_HOME/common/client/target/zingg-common-client-0.4.0-SNAPSHOT.jar'
PY4J_JAVA_PATH='.:../thirdParty/lib//py4j0.10.9.jar:../assembly/target/zingg-0.4.0-SNAPSHOT.jar:/opt/spark-3.2.4-bin-hadoop3.2/jars/jackson-databind-2.12.3.jar:/opt/spark-3.2.4-bin-hadoop3.2/jars/jackson-core-2.12.3.jar:/opt/spark-3.2.4-bin-hadoop3.2/jars/jackson-annotations-2.12.3.jar'

def compileGatewayEntry():
    subprocess.call([
        "javac", "-cp", PY4J_JAVA_PATH, "-source", "1.8", "-target", "1.8",
        "TestPy4JGateway.java"])
    
def startGatewayEntry():
    subprocess.call([
        "java", "-Xmx512m", "-cp", PY4J_JAVA_PATH,
        "TestPy4JGateway"])
    
def start_example_app_process():
    # XXX DO NOT FORGET TO KILL THE PROCESS IF THE TEST DOES NOT SUCCEED
    p = Process(target=startGatewayEntry)
    p.start()
    sleep(2)
    return p

def check_connection(gateway_parameters=None):
    test_gateway = JavaGateway(gateway_parameters=gateway_parameters)
    try:
        # Call a dummy method just to make sure we can connect to the JVM
        test_gateway.jvm.System.currentTimeMillis()
    except Py4JNetworkError:
        # We could not connect. Let"s wait a long time.
        # If it fails after that, there is a bug with our code!
        sleep(2)
    finally:
        test_gateway.close()

def safe_shutdown(instance):
    if hasattr(instance, 'gateway'):
        try:
            instance.gateway.shutdown()
        except Exception:
            print("exception")
        


class MyJavaIntegrationTest(unittest.TestCase):
    def setUp(self):
        compileGatewayEntry()
        self.p = start_example_app_process()
        self.gateway = JavaGateway(
            gateway_parameters=GatewayParameters(auto_convert=True))
        # self.arguments = self.gateway.jvm.zingg.common.client.Arguments()
        self.arguments = Arguments()
        # self.pipes = Pipe("path_to_data.csv", "CsvPipe")

    def tearDown(self):
        safe_shutdown(self)
        self.p.join()
        sleep(2)
   
    
    def test_jvm_access(self):
        print("Accessing the JVM...")
        try:
            current_time = self.gateway.jvm.System.currentTimeMillis()
            print("Current time from JVM:", current_time)
            x = self.gateway.jvm.zingg.common.client.Arguments()
            # print(x)
            y  = self.gateway.jvm.zingg.common.client.pipe.Pipe()
            print(y)
        except Py4JNetworkError:
            print("Failed to access the JVM.")
    
    def test_setArgsAndGetArgs(self):
        expected_args = {
            "zinggDir": "/tmp/zingg",
            "numPartitions": 10,
            "labelDataSampleSize": 0.01,
            "modelId": "1",
            "jobId": 1,
            "collectMetrics": True,
            # "showConcise": False,
            # "stopWordsCutoff": 0.1,
            "blockSize": 100
        }

        self.arguments.setArgs(expected_args)
        java_args = self.arguments.getArgs()

        self.assertEqual(java_args, expected_args)

    
    def test_setDataAndGetArgs(self):
        pipe1 = Pipe("path_to_data1.csv", "CsvPipe")
        pipe2 = Pipe("path_to_data2.csv", "CsvPipe")

        self.arguments.setData(pipe1, pipe2)

        java_args = self.arguments.getArgs()
        java_pipes = java_args.getData()

        self.assertEqual(len(java_pipes), 2)

        for python_pipe, java_pipe in zip([pipe1, pipe2], java_pipes):
            self.assertEqual(python_pipe.getName(), java_pipe.getName())
            self.assertEqual(python_pipe.getFormat(), java_pipe.getFormat())

    
    def test_setFieldDefinition(self):
        field_def_list = [
            FieldDefinition("field1", "type1"),
            FieldDefinition("field2", "type2"),
        ]

        self.arguments.setFieldDefinition(field_def_list)

        java_args = self.arguments.getArgs()
        # print(java_args)

        java_field_defs = java_args.getFieldDefinition()
        print(java_field_defs)
        print(field_def_list)

        self.assertEqual(len(java_field_defs), len(field_def_list))
        # self.assertEqual(java_field_defs, field_def_list)
        # self.assertEqual(java_args["zinggDir"], expected_args["zinggDir"])
        # self.assertEqual(java_args["numPartitions"], expected_args["numPartitions"])
        
        for java_field_def, expected_field_def in zip(java_field_defs, field_def_list):
            self.assertEqual(java_field_def.getFieldName(), expected_field_def.getFieldName())
            self.assertEqual(java_field_def.getDataType(), expected_field_def.getDataType())

# class TestArguments(unittest.TestCase):
#     def setUp(self):
#         self.arguments = Arguments()

#     def test_setArgsAndGetArgs(self):
#         expected_args = {
#             "zinggDir": "/tmp/zingg",
#             "numPartitions": 10,
#             "labelDataSampleSize": 0.01,
#             "modelId": "1",
#             "jobId": 1,
#             "collectMetrics": True,
#             "showConcise": False,
#             "stopWordsCutoff": 0.1,
#             "blockSize": 100
#         }
#         self.arguments.setArgs(expected_args)
#         java_args = self.arguments.getArgs()
#         self.assertEqual(java_args, expected_args)


if __name__ == '__main__':
    unittest.main(argv=sys.argv[:1])
