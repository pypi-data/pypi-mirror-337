# Pathfinder is a service
# It takes a pathway and parameters
# the run method runs the posts in the pathway with the given parameters
# the run method returns a result
# the result is a dictionary with the following keys:
# - status: the status of the pathway
# - result: the result of the pathway
# - pathway: the pathway that was run
# - parameters: the parameters that were used to run the pathway    
# Pathfinder use Pouch to store and retrieve pathway and parameters
# Pathfinder use Pouch to store the state of a pathway run    

from .Pit import Pit
from .Agent import Agent
from .Pathway import Pathway,Post
from .Practice import Practice
import time
import json
import os
from opentelemetry import metrics
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import (
    PeriodicExportingMetricReader,
)
from opentelemetry.exporter.otlp.proto.http.metric_exporter import OTLPMetricExporter

# Create metrics directory if it doesn't exist
metrics_dir = "metrics"
if not os.path.exists(metrics_dir):
    os.makedirs(metrics_dir)

# Set up file-based OTLP exporter
class FileMetricExporter(OTLPMetricExporter):
    def __init__(self, file_path):
        super().__init__()
        self.file_path = file_path

    def _export(self, metrics_data):
        # Convert metrics to JSON-serializable format
        metrics_json = []
        for metric in metrics_data.resource_metrics:
            for scope_metrics in metric.scope_metrics:
                for metric_data in scope_metrics.metrics:
                    metric_dict = {
                        "name": metric_data.name,
                        "description": metric_data.description,
                        "unit": metric_data.unit,
                        "timestamp": time.time(),
                        "data_points": []
                    }
                    
                    for point in metric_data.data.data_points:
                        data_point = {
                            "attributes": dict(point.attributes),
                            "time_unix_nano": point.time_unix_nano,
                            "value": point.value if hasattr(point, 'value') else None,
                        }
                        if hasattr(point, 'count'):
                            data_point["count"] = point.count
                        if hasattr(point, 'sum'):
                            data_point["sum"] = point.sum
                        if hasattr(point, 'bucket_counts'):
                            data_point["bucket_counts"] = point.bucket_counts
                        metric_dict["data_points"].append(data_point)
                    
                    metrics_json.append(metric_dict)
        
        # Append metrics to file
        with open(self.file_path, 'a') as f:
            for metric in metrics_json:
                f.write(json.dumps(metric) + '\n')
        
        return None

# Create file exporter
file_exporter = FileMetricExporter(os.path.join(metrics_dir, "pathfinder_metrics.jsonl"))
metric_reader = PeriodicExportingMetricReader(file_exporter, export_interval_millis=5000)
provider = MeterProvider(metric_readers=[metric_reader])
metrics.set_meter_provider(provider)
meter = metrics.get_meter("pathfinder_metrics")

# Create metrics
pathway_duration = meter.create_histogram(
    name="pathway_execution_duration",
    description="Duration of pathway execution",
    unit="s"
)

post_duration = meter.create_histogram(
    name="post_execution_duration",
    description="Duration of post execution",
    unit="s"
)

pathway_counter = meter.create_counter(
    name="pathway_executions",
    description="Number of pathway executions",
)

post_counter = meter.create_counter(
    name="post_executions",
    description="Number of post executions",
)

error_counter = meter.create_counter(
    name="execution_errors",
    description="Number of execution errors",
)

class Pathfinder(Pit):
    def __init__(self, agent: Agent,name="Pathfinder",description="Pathfinder is a service that takes a pathway and parameters and runs the posts in the pathway with the given parameters" ):
        super().__init__(name,description)
        self.agent = agent

        self.AddPractice(Practice("Status", self.Status))
        self.AddPractice(Practice("Run", self.Run))

    def _find_agent_practice(self, practice: str):
        # list active agents
        plaza_name = "MainPlaza"
        agents_info = self.agent.UsePractice(f"{plaza_name}/ListActiveAgents")
        #print(agents_info)

        for agent_info in agents_info:
            # find in each pits of the agent
            for pit_type in agent_info["agent_info"]["components"].keys():
                print(f"pit_type: {pit_type}")
                #print(agent_info["agent_info"]["components"][pit_type])
                for pit in agent_info["agent_info"]["components"][pit_type].keys():
                    print(f"pit: {pit}")
                    if pit in agent_info["agent_info"]["components"][pit_type]:
                        print(f"pit in agent_info: {pit}")
                        print(f"{agent_info['agent_info']['components'][pit_type]}")
                        if "practices" in agent_info["agent_info"]["components"][pit_type][pit]:
                            for remote_practice in agent_info["agent_info"]["components"][pit_type][pit]['practices']:
                                #print(f"practice: {practice}")
                                if remote_practice == practice:
                                    return {"agent_address": agent_info["agent_id"]+'@'+plaza_name, "practice": pit+"/"+practice}
                    else:
                        print(f"pit not in agent_info: {pit}")
        return None
    
    def Status(self):
        return {
            "status": "running",
            "message": "Pathfinder is running"
        }
    
    def run_post(self, post: Post, inputs: dict) -> tuple[dict, dict]:
        # Record post execution metrics
        start_time = time.time()
        try:
            # pathfinder find suitable agent at the runtime
            # it may be recursive and run other pathways or posts
            # variables are inputs and parameters
            # the output of the post is the input of the next post
            agent_info = self._find_agent_practice(post.practice)
            # keep track of variables
            variables = inputs
            print(f"run_post: {post.post_id}, {inputs}")
            print(f"agent_info: {agent_info}")
            if agent_info:
                # send UsePracticeRequest to the agent
                practice_input={}
                for key in post.parameters.keys():
                    v = post.parameters[key]
                    if isinstance(v, str):
                        # replace {key} with inputs[key]
                        # multiple {key} can be in the string
                        for input_key in inputs.keys():
                            print(f"input_key: {input_key}")
                            while True:
                                start_index = v.find('{'+input_key+'}')
                                if start_index == -1:
                                    break
                                end_index = v.find('}', start_index)
                                if end_index == -1:
                                    break
                                v = v[:start_index] + inputs[input_key] + v[end_index+1:]
                                print(f"v: {v}")
                    practice_input[key] = v
                response = self.agent.UsePracticeRemote(agent_info['practice'], agent_info['agent_address'], practice_input)
                # put the output into variables
                # output is the first key of the outputs
                print(f"response: {response}")
                output=list(post.outputs.keys())[0]
                for post_output in post.outputs[output]['field_mapping'].keys():
                    variables[post.outputs[output]['field_mapping'][post_output]] = response['result'][post_output]
                # Record successful post execution
                post_counter.add(1, {"post_id": post.post_id, "status": "success"})
                return response, variables
            else:
                error_counter.add(1, {"post_id": post.post_id, "error": "no_agent_found"})
                raise Exception(f"No agent found for practice {post.practice}")
        except Exception as e:
            error_counter.add(1, {"post_id": post.post_id, "error": str(e)})
            raise
        finally:
            duration = time.time() - start_time
            post_duration.record(duration, {"post_id": post.post_id})

    def Run(self, pathway_dict: dict, **inputs: dict):
        # Record pathway execution metrics
        start_time = time.time()
        try:
            # start from entrance post
            # the output of the last post is the output of the pathway
            pathway = Pathway.FromJson(pathway_dict)
            current_post = pathway.entrance_post
            # variables are inputs and post parameters   
            variables = inputs

            while current_post is not None:
                print(f"current_post: {current_post.post_id}",inputs)
                response, variables = self.run_post(current_post, inputs)
                # next post may be concurrent
                # input of the next post is defined in pathway
                # the output of the current post is the input of the next post
                # the output of the last post is the output of the pathway
                next_post = current_post.next_post
                if current_post.next_post == "exit":
                    break
                else:
                    # Find the next post in the posts list
                    next_post = next((post for post in pathway.posts if post.post_id == current_post.next_post), None)
                    if next_post is None:
                        break
                    current_post = next_post
            # Record successful pathway execution
            pathway_counter.add(1, {"pathway_id": pathway.pathway_id, "status": "success"})
            return variables
        except Exception as e:
            error_counter.add(1, {"pathway_id": pathway.pathway_id, "error": str(e)})
            raise
        finally:
            duration = time.time() - start_time
            pathway_duration.record(duration, {"pathway_id": pathway.pathway_id})

    def FromJson(self, json_data: dict):
        self.pathway = Pathway.FromJson(json_data)
        self.parameters = json_data["parameters"]
        self.agent = json_data["agent"]
        self.pathfinder = Pathfinder(self.agent)
        return self

    def ToJson(self):
        return {
            "pathway": self.pathway.ToJson(),
            "parameters": self.parameters,
            "agent": self.agent.ToJson()
        }
