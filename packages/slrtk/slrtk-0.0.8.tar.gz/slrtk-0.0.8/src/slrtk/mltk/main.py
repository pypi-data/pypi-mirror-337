import docker
import os
import argparse

def parse_and_run(args):
    client = docker.from_env()
    
    # Prepare volume bindings
    volumes = {
        os.path.abspath(args.data): {'bind': '/data', 'mode': 'ro'},
        os.path.abspath(args.meta): {'bind': '/meta', 'mode': 'ro'},
        os.path.abspath(args.save): {'bind': '/saves', 'mode': 'rw'}
    }
    
    # Optional models directory
    if args.models:
        volumes[os.path.abspath(args.models)] = {'bind': '/models/external', 'mode': 'ro'}
    
    # GPU configuration
    device_requests = None
    if args.gpu:
        device_requests = [docker.types.DeviceRequest(count=1, capabilities=[['gpu']])]
    
    # IPC mode for shared memory
    ipc_mode = 'host' if args.host_shm else None
    
    try:
        # Run the container
        container = client.containers.run(
            image='retrain-test',
            name='retrain-runner',
            command=args.branch,  # Pass branch as command
            volumes=volumes,
            device_requests=device_requests,
            ipc_mode=ipc_mode,
            remove=True,  # Equivalent to --rm
            detach=True
        )
        
        # Stream logs
        logs = container.logs(stream=True)
        for log in logs:
            decoded_log = log.decode('utf-8')
            print(decoded_log, end='')
            
            if "OSError" in decoded_log or "Error" in decoded_log:
                print("Error encountered. Exiting...")
                break
                
        print("Done!")
        
    except Exception as e:
        print(f"Error running Docker container: {e}")

parser = argparse.ArgumentParser(prog='mltk', description='Run the Machine Learning Toolkit bundled for SLR.')
parser.add_argument('branch', type=str, choices=["isolated", "fingerspelling", "phrases"], 
                    help='Branch for the ML pipeline you want to run')
parser.add_argument('--gpu', type=bool, default=True, 
                    help='Use the GPU [Strongly recommended]')
parser.add_argument('--host-shm', type=bool, default=True, 
                    help='Use the host\'s ipc (will pass --ipc=host to docker) [Strongly recommended]')
parser.add_argument('--data', type=str, required=True, 
                    help='The directory to be used for the datasets')
parser.add_argument('--meta', type=str, required=True, 
                    help='The directory to be used for metadata input')
parser.add_argument('--models', type=str, 
                    help='The directory to load in additional models')
parser.add_argument('--save', type=str, required=True, 
                    help='The directory to load and save models to')

if __name__ == "__main__":
    args = parser.parse_args()
    run_docker(args)
