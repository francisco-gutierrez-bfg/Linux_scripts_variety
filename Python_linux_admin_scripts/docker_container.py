import argparse
import docker

# This script will build a Docker image from a Dockerfile, both, image and Dockerfile will be specified as arguments.
# Run this script as follows:
# python build_docker_container.py image_name /path/to/Dockerfile

def build_container(image_name, dockerfile_path):
    client = docker.from_env()
    image, build_log = client.images.build(path=dockerfile_path, tag=image_name)
    for log_line in build_log:
        print(log_line)
    print("Docker container built successfully.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Build Docker container from Dockerfile.')
    parser.add_argument('image_name', help='Name for the Docker image')
    parser.add_argument('dockerfile_path', help='Path to the Dockerfile')

    args = parser.parse_args()

    build_container(args.image_name, args.dockerfile_path)
