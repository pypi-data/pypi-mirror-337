# CoreX Storage - S3 Implementation

CoreX Storage - S3 is a comprehensive Python package that provides a complete, production-ready implementation of the CoreX Storage Interface using AWS S3. This package leverages the power of boto3 to perform file operations, manage buckets, and handle event notifications. By adhering to the CoreX standard, your application can remain agnostic to the underlying storage provider. This means you can easily switch between S3, Azure Blob, Local File System, Minio, or other storage backends simply by updating your configuration—no code changes required.

---

## Overview

CoreX Storage - S3 is designed with modularity and flexibility in mind. It implements the CoreX Storage Interface, which defines standard methods for saving, deleting, listing, and searching files, as well as bucket operations and event handling. By using dependency injection and dynamic configuration loading, you can choose the appropriate storage backend at runtime. This decouples your application logic from specific storage implementations, making your system highly adaptable.

---

## Features

- **Seamless AWS S3 Integration:** Uses boto3 to perform all S3 operations reliably.
- **Standard File Operations:** Upload, download, delete, list, and search files within S3 buckets.
- **Bucket Management:** Create, delete, and list S3 buckets.
- **Event Handling:** Supports SQS-based event notifications to process file events such as creation, deletion, or modification.
- **Dynamic Backend Switching:** Configure your storage backend via a YAML configuration file. Easily swap between S3, Azure Blob, Local File System, Minio, etc., without changing your application code.
- **Dependency Injection Friendly:** Your code only depends on the CoreX Storage Interface, not on the specific implementation.

---

## Installation

Install the S3 package via pip:

~~~bash
pip install corex-storage-s3
~~~

This package requires Python 3.6 or later and depends on [boto3](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html) for AWS S3 operations.

---

## Usage Example

Below is an example of how to integrate the CoreX Storage Interface into your application. The example demonstrates how to use the S3 implementation, load it dynamically via configuration, and perform standard file operations.

### Step 1: Define Your YAML Configuration

Create a `corex_config.yaml` file with the following content:

~~~yaml
storage:
  backend: "corex_storage_s3.handler.S3Handler"
  init_args:
    bucket_name: "your-bucket-name"
    region_name: "us-east-1"
    # Optionally, include your SQS queue URL for event notifications:
    sqs_queue_url: "https://sqs.region.amazonaws.com/123456789012/your-queue"
~~~

### Step 2: Load the Storage Backend via the Config Loader

CoreX provides a configuration loader that dynamically loads and instantiates the backend specified in your configuration file.

~~~python
from corex.config_loader import load_storage_backend

# Load the storage backend from the configuration file
storage = load_storage_backend("corex_config.yaml")

# Use the storage interface in your application code
storage.save("local/path/to/file.txt", "remote/path/in/bucket/file.txt")
files = storage.list_files("remote/path/in/bucket/")
print("Files in bucket:", files)
storage.delete("remote/path/in/bucket/file.txt")
~~~

### Step 3: Switching Backends Without Changing Code

Your application only depends on the CoreX Storage Interface. To switch from AWS S3 to another backend (e.g., Azure Blob, Local File System, or Minio), simply update the `backend` and `init_args` in your `corex_config.yaml` file.

#### Example: Switching to Azure Blob Storage

~~~yaml
storage:
  backend: "corex_storage_azure_blob.handler.AzureBlobHandler"
  init_args:
    container_name: "your-container-name"
    connection_string: "DefaultEndpointsProtocol=https;AccountName=youraccount;AccountKey=yourkey;EndpointSuffix=core.windows.net"
~~~

#### Example: Switching to a Local File System

~~~yaml
storage:
  backend: "corex_storage_local.handler.LocalStorageHandler"
  init_args:
    base_path: "/path/to/local/storage"
~~~

#### Example: Switching to Minio

~~~yaml
storage:
  backend: "corex_storage_minio.handler.MinioHandler"
  init_args:
    endpoint: "play.min.io"
    bucket_name: "your-bucket-name"
    access_key: "your-access-key"
    secret_key: "your-secret-key"
~~~

By simply modifying the YAML configuration, you can change the storage backend without any modifications to your application code.

---

## Advanced Usage

### Event Notifications with SQS

If you want to use event notifications, configure the `sqs_queue_url` in your YAML file. Then, register event listeners to handle events such as file creation or deletion.

~~~python
def on_file_created(event, file_path):
    print(f"Event '{event}' received for file: {file_path}")

# Register an event listener for a specific file and event type
storage.add_event_listener("remote/path/in/bucket/file.txt", "create", on_file_created)

# Start watching for events (this will poll the SQS queue for notifications)
storage.watch("remote/path/in/bucket/")
~~~

### Bucket Operations

Manage your buckets directly through the storage interface:

~~~python
# Create a new bucket
storage.create_bucket("new-bucket-name")

# List all available buckets
buckets = storage.list_buckets()
print("Buckets:", buckets)

# Delete a bucket
storage.delete_bucket("new-bucket-name")
~~~

---

## Integration with CoreX Framework

CoreX Storage - S3 is designed to seamlessly integrate into the broader CoreX ecosystem. By implementing the CoreX Storage Interface, it works perfectly with other CoreX modules such as caching, messaging, and configuration management. Use the provided config loader to dynamically assemble your application's backends based on your YAML configuration.

---

## Contributing

We welcome contributions to enhance CoreX Storage - S3. To contribute:

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Write tests and update the documentation as needed.
4. Submit a Pull Request with a detailed description of your changes.

For further guidelines, please refer to our [CONTRIBUTING.md](CONTRIBUTING.md).

---

## License

This project is licensed under the MIT License. See the [LICENSE](../LICENSE) file for details.

---

## Contact & Support

- **Email:** js@intelligent-intern.com
- **GitHub Issues:** [CoreX Issues](https://github.com/intelligent-intern/corex/issues)

---

CoreX Storage - S3 empowers your Python applications with a flexible, modular, and dynamic storage solution. By relying on configuration-driven dependency injection, you can easily adapt to changing requirements and seamlessly switch between storage providers without modifying your core code.
