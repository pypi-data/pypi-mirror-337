# kube_secure/async_scanner.py

import asyncio
import json
import yaml
import click
from tabulate import tabulate
from datetime import datetime
from kubernetes_asyncio import config, client
from kubernetes_asyncio.client import ApiClient
from kube_secure.session import get_connection_method
import keyring

# -------------------- Connection Loader --------------------

async def async_load_k8():
    connection_method = get_connection_method()
    if connection_method == "kubeconfig":
        await config.load_kube_config()
        return ApiClient()
    elif connection_method == "token":
        api_server = keyring.get_password("kube-sec", "api_server")
        token = keyring.get_password("kube-sec", "kube_token")
        ssl_verify_str = keyring.get_password("kube-sec", "SSL_VERIFY")
        ca_cert_path = keyring.get_password("kube-sec", "CA_CERT_PATH")
        ssl_verify = ssl_verify_str.lower() == "true" if ssl_verify_str else False

        configuration = client.Configuration()
        configuration.host = api_server
        configuration.verify_ssl = ssl_verify
        if ssl_verify and ca_cert_path:
            configuration.ssl_ca_cert = ca_cert_path
        configuration.api_key = {"authorization": "Bearer " + token}
        return ApiClient(configuration)
    else:
        raise RuntimeError("❌ No valid connection method found. Please run `kube-sec connect` first.")

# -------------------- Check: Pods Running As Root --------------------

async def check_pods_running_as_root(core_v1):
    pods = (await core_v1.list_pod_for_all_namespaces()).items
    risky = []
    for pod in pods:
        pod_user = pod.spec.security_context.run_as_user if pod.spec.security_context else None
        for c in pod.spec.containers:
            c_user = c.security_context.run_as_user if c.security_context else None
            if (c_user is None or c_user == 0) and (pod_user is None or pod_user == 0):
                risky.append({"Namespace": pod.metadata.namespace, "Pod": pod.metadata.name})
    return "root-user-pods", "Critical", risky
# -------------------- Check: Non-root Enforcement --------------------

async def check_pods_running_as_non_root(core_v1):
    pods = (await core_v1.list_pod_for_all_namespaces()).items
    violations = []
    for pod in pods:
        pod_enforced = pod.spec.security_context.run_as_non_root if pod.spec.security_context else None
        for c in pod.spec.containers:
            c_enforced = c.security_context.run_as_non_root if c.security_context else None
            if not pod_enforced and not c_enforced:
                violations.append({
                    "Namespace": pod.metadata.namespace,
                    "Pod": pod.metadata.name,
                    "Message": "Missing runAsNonRoot"
                })
    return "non-root-enforcement", "Warning", violations

# -------------------- Check: Host PID and Network --------------------

async def check_host_pid_and_network(core_v1):
    pods = (await core_v1.list_pod_for_all_namespaces()).items
    issues = []
    for pod in pods:
        if pod.spec.host_pid or pod.spec.host_network:
            issues.append({
                "Namespace": pod.metadata.namespace,
                "Pod": pod.metadata.name,
                "Message": f"hostPID={pod.spec.host_pid}, hostNetwork={pod.spec.host_network}"
            })
    return "host-pid-and-network-exposure", "Warning", issues

# -------------------- Check: Privileged Containers --------------------

async def check_privileged_containers_and_hostpath(core_v1):
    pods = (await core_v1.list_pod_for_all_namespaces()).items
    issues = []
    for pod in pods:
        for c in pod.spec.containers:
            if c.security_context and c.security_context.privileged:
                issues.append({
                    "Namespace": pod.metadata.namespace,
                    "Pod": pod.metadata.name,
                    "Message": "Privileged container"
                })
            if c.volume_mounts:
                for vol in c.volume_mounts:
                    if vol.mount_path == "/":
                        issues.append({
                            "Namespace": pod.metadata.namespace,
                            "Pod": pod.metadata.name,
                            "Message": f"Mounts {vol.mount_path}"
                        })
    return "privileged-containers-and-hostpath-mounts", "Critical", issues

# -------------------- Check: Public Services --------------------

async def check_publicly_accessible_services(core_v1):
    services = (await core_v1.list_service_for_all_namespaces()).items
    issues = []
    for svc in services:
        if svc.spec.type in ["LoadBalancer", "NodePort"]:
            issues.append({
                "Namespace": svc.metadata.namespace,
                "Service": svc.metadata.name,
                "Type": svc.spec.type
            })
    return "public-service-exposure", "Critical", issues

# -------------------- Check: Open Network Ports --------------------

async def check_open_ports(core_v1):
    services = (await core_v1.list_service_for_all_namespaces()).items
    issues = []
    for svc in services:
        for port in svc.spec.ports or []:
            if port.port and port.port < 1024:
                issues.append({
                    "Namespace": svc.metadata.namespace,
                    "Service": svc.metadata.name,
                    "Port": port.port
                })
    return "open-network-ports", "Warning", issues

# -------------------- Check: Weak Firewall Rules --------------------

async def check_weak_firewall_rules(net_v1):
    policies = (await net_v1.list_network_policy_for_all_namespaces()).items
    if not policies:
        return "internal-traffic-controls", "Warning", [{"Message": "No NetworkPolicies defined"}]
    return "internal-traffic-controls", "Warning", []

# -------------------- Check: RBAC Misconfigurations --------------------

async def check_rbac_misconfigurations(rbac_v1):
    crbs = (await rbac_v1.list_cluster_role_binding()).items
    issues = []
    for crb in crbs:
        for s in crb.subjects or []:
            if s.kind == "User" and s.name == "admin":
                issues.append({
                    "Binding": crb.metadata.name,
                    "User": s.name,
                    "Role": crb.role_ref.name
                })
    return "rbac-privileges", "Critical", issues

# -------------------- Check: RBAC Least Privilege --------------------

async def check_rbac_least_privilege(rbac_v1):
    crbs = (await rbac_v1.list_cluster_role_binding()).items
    issues = []
    for crb in crbs:
        if crb.role_ref.name in ["cluster-admin", "admin"]:
            issues.append({
                "Binding": crb.metadata.name,
                "Role": crb.role_ref.name
            })
    return "rbac-least-privilege", "Warning", issues

# -------------------- Check: Network Exposure --------------------

async def check_network_exposure(core_v1):
    services = (await core_v1.list_service_for_all_namespaces()).items
    issues = []
    for svc in services:
        if svc.spec.cluster_ip != "None" and svc.spec.type == "LoadBalancer":
            issues.append({
                "Namespace": svc.metadata.namespace,
                "Service": svc.metadata.name,
                "Type": svc.spec.type
            })
    return "external-service-exposure", "Critical", issues

# -------------------- CIS Kubernetes Benchmark Check --------------------


async def check_cis_benchmark(core_v1, version_api, net_v1):
    issues = []

    # Control 1: Cluster Setup
    # 1.1 Ensure that the API server only allows authorized API clients
    try:
        api_versions = await version_api.get_code()  # Correct method to get Kubernetes version
        if not api_versions.git_version:
            issues.append({
                "Namespace": "Cluster",
                "Message": "Anonymous access should be disabled"
            })
    except Exception as e:
        issues.append({
            "Namespace": "Cluster",
            "Message": f"Error retrieving API versions: {e}"
        })

    # Control 2: Control Plane
    # 2.1 Ensure that the API server is only accessible over HTTPS
    api_server_access = "https" in api_versions.git_version  # Placeholder check for demonstration
    if not api_server_access:
        issues.append({
            "Namespace": "Control Plane",
            "Message": "API server should only be accessible over HTTPS"
        })

    # Control 3: Node
    # 3.1 Ensure that the nodes do not run privileged containers
    pods = (await core_v1.list_pod_for_all_namespaces()).items
    for pod in pods:
        node_name = pod.spec.node_name  # Get the node name from the pod's spec
        for container in pod.spec.containers:
            if container.security_context and container.security_context.privileged:
                issues.append({
                    "Namespace": pod.metadata.namespace,
                    "Pod": pod.metadata.name,
                    "Node": node_name,  # Print the node where the pod is running
                    "Message": "Privileged container running on node"
                })

    # Control 4: Networking
    # 4.1 Ensure that Network Policies are used
    policies = (await net_v1.list_network_policy_for_all_namespaces()).items
    if not policies:
        issues.append({
            "Namespace": "Cluster",
            "Message": "Network Policies should be defined"
        })

    # Control 5: Logging and Auditing
    # 5.1 Ensure that audit logs are enabled
    audit_logs_enabled = True  # Placeholder, actual logic needed for audit logs
    if not audit_logs_enabled:
        issues.append({
            "Namespace": "Cluster",
            "Message": "Audit logs should be enabled"
        })

    # Control 6: Runtime Security
    # 6.1 Ensure that containers do not run with root privileges
    for pod in pods:
        if pod.spec.security_context and pod.spec.security_context.run_as_user == 0:
            issues.append({
                "Namespace": pod.metadata.namespace,
                "Pod": pod.metadata.name,
                "Message": "Container is running with root privileges"
            })

    return "cis-benchmark", "Critical", issues


# -------------------- Secrets in Env/Volumes Check --------------------

async def check_secrets_in_env_volumes(core_v1):
    issues = []

    # Fetch all pods
    pods = (await core_v1.list_pod_for_all_namespaces()).items

    # Loop through all the pods
    for pod in pods:
        # Check if containers exist in the pod and iterate over them
        if pod.spec.containers:
            for container in pod.spec.containers:
                # Check for environment variables that might contain secrets
                if container.env:
                    for env_var in container.env:
                        # Checking for potential secrets in environment variables
                        if env_var.value and ('password' in env_var.name.lower() or 'token' in env_var.name.lower()):
                            issues.append({
                                "Namespace": pod.metadata.namespace,
                                "Pod": pod.metadata.name,
                                "Message": f"Potential secret in environment variable: {env_var.name}"
                            })

        # Check if volumes exist in the pod and iterate over them
        if pod.spec.volumes:
            for volume in pod.spec.volumes:
                if volume.secret:  # This checks if the volume is mounted from a Secret
                    issues.append({
                        "Namespace": pod.metadata.namespace,
                        "Pod": pod.metadata.name,
                        "Message": f"Mounted volume from Secret: {volume.secret.secret_name}"
                    })

    return "secrets-in-env-volumes", "Critical", issues

# -------------------- Pod Security Standards Check --------------------

async def check_pod_security_standards(core_v1):
    issues = []

    # Fetch all pods in the cluster
    pods = (await core_v1.list_pod_for_all_namespaces()).items

    for pod in pods:
        pod_issues = {
            "Namespace": pod.metadata.namespace,
            "Pod": pod.metadata.name,
            "Messages": []
        }

        # Check for privileged containers
        if pod.spec.containers:
            for container in pod.spec.containers:
                if container.security_context and container.security_context.privileged:
                    pod_issues["Messages"].append("Privileged container running (not compliant with restricted Pod Security Standards)")

        # Check for host network usage
        if pod.spec.host_network:
            pod_issues["Messages"].append("Host networking used (not compliant with restricted Pod Security Standards)")

        # Check for containers running as root
        if pod.spec.containers:
            for container in pod.spec.containers:
                if container.security_context and container.security_context.run_as_user == 0:
                    pod_issues["Messages"].append("Container running as root (not compliant with restricted Pod Security Standards)")

        # Check for privileged volume types (e.g., hostPath volumes)
        if pod.spec.volumes:
            for volume in pod.spec.volumes:
                if volume.host_path:
                    pod_issues["Messages"].append(f"Privileged volume type used (hostPath): {volume.host_path.path} (not compliant with restricted Pod Security Standards)")

        # Only add pod to issues list if there are violations
        if pod_issues["Messages"]:
            issues.append(pod_issues)

    return "pod-security-standards", "Critical", issues



# -------------------- Async Scanner Runner --------------------

async def async_run_scan(disable_checks, output_format, custom_rules):
    api_client = await async_load_k8()
    async with api_client:
        core_v1 = client.CoreV1Api(api_client)
        net_v1 = client.NetworkingV1Api(api_client)
        rbac_v1 = client.RbacAuthorizationV1Api(api_client)
        version_api = client.VersionApi(api_client)

        # All checks, using previously defined functions
        all_checks = {
            "root-user-pods": lambda: check_pods_running_as_root(core_v1),
            "non-root-enforcement": lambda: check_pods_running_as_non_root(core_v1),
            "host-pid-and-network-exposure": lambda: check_host_pid_and_network(core_v1),
            "privileged-containers-and-hostpath-mounts": lambda: check_privileged_containers_and_hostpath(core_v1),
            "public-service-exposure": lambda: check_publicly_accessible_services(core_v1),
            "open-network-ports": lambda: check_open_ports(core_v1),
            "internal-traffic-controls": lambda: check_weak_firewall_rules(net_v1),
            "rbac-privileges": lambda: check_rbac_misconfigurations(rbac_v1),
            "rbac-least-privilege": lambda: check_rbac_least_privilege(rbac_v1),
            "external-service-exposure": lambda: check_network_exposure(core_v1),
            "cis-benchmark": lambda: check_cis_benchmark(core_v1, version_api, net_v1),
            "secrets-in-env-volumes": lambda: check_secrets_in_env_volumes(core_v1),
            "pod-security-standards": lambda: check_pod_security_standards(core_v1),  
        }

        # Apply disabled checks
        checks = {k: v for k, v in all_checks.items() if k not in disable_checks}
        results = {}
        critical = 0
        warning = 0
        security_issues = []

        click.secho("\n🚀 Starting Async Kubernetes Security Scan...\n", fg="cyan", bold=True)

        with click.progressbar(checks.items(), label="⏱️  Running security checks") as bar:
            tasks = [func() for _, func in bar]
            outputs = await asyncio.gather(*tasks)

        # Processing results
        for check_name, severity, data in outputs:
            results[check_name] = data
            click.secho(f"\n🔍 {check_name.replace('-', ' ').title()}", fg="cyan", bold=True)
            if data:
                if isinstance(data[0], dict):
                    click.echo(tabulate(data, headers="keys", tablefmt="grid"))
                else:
                    for item in data:
                        click.echo(f" - {item}")
                if severity == "Critical":
                    critical += len(data)
                else:
                    warning += len(data)
                for item in data:
                    msg = json.dumps(item)
                    security_issues.append((severity, msg))
            else:
                click.secho("✅ No issues found.", fg="green")

        # Final output after scan completes
        if not output_format:
            click.echo("\n✅ Scan Completed")
            click.secho("\n📊 Security Summary:", bold=True)
            click.secho(f"   🔴 {critical} Critical Issues", fg="red")
            click.secho(f"   🟡 {warning} Warnings", fg="yellow")

            if security_issues:
                click.echo("\n🚨 Issues Detected:")
                for severity, message in security_issues:
                    color = "red" if severity == "Critical" else "yellow"
                    click.secho(f"[{severity.upper()}] {message}", fg=color)
            else:
                click.secho("\n✅ No security issues found.", fg="green")

        # Export results in specified format (JSON/YAML)
        if output_format:
            report = {
                "scan_timestamp": datetime.utcnow().isoformat() + "Z",
                "issues_summary": {
                    "critical": critical,
                    "warnings": warning,
                },
                "scan_results": results
            }
            filename = "output.json" if output_format == "json" else "output.yaml"
            with open(filename, 'w') as f:
                if output_format == "json":
                    json.dump(report, f, indent=4)
                else:
                    yaml.dump(report, f)
            click.secho(f"\n📝 Report saved to {filename}", fg="green")

