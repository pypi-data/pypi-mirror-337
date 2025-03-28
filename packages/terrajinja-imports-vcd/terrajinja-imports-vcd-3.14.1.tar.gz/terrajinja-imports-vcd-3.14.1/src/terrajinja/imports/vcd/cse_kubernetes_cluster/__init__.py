'''
# `vcd_cse_kubernetes_cluster`

Refer to the Terraform Registry for docs: [`vcd_cse_kubernetes_cluster`](https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/cse_kubernetes_cluster).
'''
import abc
import builtins
import datetime
import enum
import typing

import jsii
import publication
import typing_extensions

from typeguard import check_type

from .._jsii import *

import cdktf as _cdktf_9a9027ec
import constructs as _constructs_77d1e7e8


class CseKubernetesCluster(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="vcd.cseKubernetesCluster.CseKubernetesCluster",
):
    '''Represents a {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/cse_kubernetes_cluster vcd_cse_kubernetes_cluster}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        control_plane: typing.Union["CseKubernetesClusterControlPlane", typing.Dict[builtins.str, typing.Any]],
        cse_version: builtins.str,
        kubernetes_template_id: builtins.str,
        name: builtins.str,
        network_id: builtins.str,
        vdc_id: builtins.str,
        worker_pool: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CseKubernetesClusterWorkerPool", typing.Dict[builtins.str, typing.Any]]]],
        api_token_file: typing.Optional[builtins.str] = None,
        auto_repair_on_errors: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        default_storage_class: typing.Optional[typing.Union["CseKubernetesClusterDefaultStorageClass", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        node_health_check: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        operations_timeout_minutes: typing.Optional[jsii.Number] = None,
        org: typing.Optional[builtins.str] = None,
        owner: typing.Optional[builtins.str] = None,
        pods_cidr: typing.Optional[builtins.str] = None,
        runtime: typing.Optional[builtins.str] = None,
        services_cidr: typing.Optional[builtins.str] = None,
        ssh_public_key: typing.Optional[builtins.str] = None,
        virtual_ip_subnet: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/cse_kubernetes_cluster vcd_cse_kubernetes_cluster} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param control_plane: control_plane block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/cse_kubernetes_cluster#control_plane CseKubernetesCluster#control_plane}
        :param cse_version: The CSE version to use. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/cse_kubernetes_cluster#cse_version CseKubernetesCluster#cse_version}
        :param kubernetes_template_id: The ID of the vApp Template that corresponds to a Kubernetes template OVA. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/cse_kubernetes_cluster#kubernetes_template_id CseKubernetesCluster#kubernetes_template_id}
        :param name: The name of the Kubernetes cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/cse_kubernetes_cluster#name CseKubernetesCluster#name}
        :param network_id: The ID of the network that the Kubernetes cluster will use. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/cse_kubernetes_cluster#network_id CseKubernetesCluster#network_id}
        :param vdc_id: The ID of the VDC that hosts the Kubernetes cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/cse_kubernetes_cluster#vdc_id CseKubernetesCluster#vdc_id}
        :param worker_pool: worker_pool block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/cse_kubernetes_cluster#worker_pool CseKubernetesCluster#worker_pool}
        :param api_token_file: A file generated by 'vcd_api_token' resource, that stores the API token used to create and manage the cluster, owned by the user specified in 'owner'. Be careful about this file, as it contains sensitive information Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/cse_kubernetes_cluster#api_token_file CseKubernetesCluster#api_token_file}
        :param auto_repair_on_errors: If errors occur before the Kubernetes cluster becomes available, and this argument is 'true', CSE Server will automatically attempt to repair the cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/cse_kubernetes_cluster#auto_repair_on_errors CseKubernetesCluster#auto_repair_on_errors}
        :param default_storage_class: default_storage_class block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/cse_kubernetes_cluster#default_storage_class CseKubernetesCluster#default_storage_class}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/cse_kubernetes_cluster#id CseKubernetesCluster#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param node_health_check: After the Kubernetes cluster becomes available, nodes that become unhealthy will be remediated according to unhealthy node conditions and remediation rules. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/cse_kubernetes_cluster#node_health_check CseKubernetesCluster#node_health_check}
        :param operations_timeout_minutes: The time, in minutes, to wait for the cluster operations to be successfully completed. For example, during cluster creation, it should be in ``provisioned``state before the timeout is reached, otherwise the operation will return an error. For cluster deletion, this timeoutspecifies the time to wait until the cluster is completely deleted. Setting this argument to ``0`` means to wait indefinitely Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/cse_kubernetes_cluster#operations_timeout_minutes CseKubernetesCluster#operations_timeout_minutes}
        :param org: The name of organization that will own this Kubernetes cluster, optional if defined at provider level. Useful when connected as sysadmin working across different organizations Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/cse_kubernetes_cluster#org CseKubernetesCluster#org}
        :param owner: The user that creates the cluster and owns the API token specified in 'api_token'. It must have the 'Kubernetes Cluster Author' role. If not specified, it assumes it's the user from the provider configuration Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/cse_kubernetes_cluster#owner CseKubernetesCluster#owner}
        :param pods_cidr: CIDR that the Kubernetes pods will use. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/cse_kubernetes_cluster#pods_cidr CseKubernetesCluster#pods_cidr}
        :param runtime: The Kubernetes runtime for the cluster. Only 'tkg' (Tanzu Kubernetes Grid) is supported. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/cse_kubernetes_cluster#runtime CseKubernetesCluster#runtime}
        :param services_cidr: CIDR that the Kubernetes services will use. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/cse_kubernetes_cluster#services_cidr CseKubernetesCluster#services_cidr}
        :param ssh_public_key: The SSH public key used to login into the cluster nodes. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/cse_kubernetes_cluster#ssh_public_key CseKubernetesCluster#ssh_public_key}
        :param virtual_ip_subnet: Virtual IP subnet for the cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/cse_kubernetes_cluster#virtual_ip_subnet CseKubernetesCluster#virtual_ip_subnet}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__55e1692321c5899968b29eb1cc339e805a493fcffc91ab86eb1256d4420f0cd1)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = CseKubernetesClusterConfig(
            control_plane=control_plane,
            cse_version=cse_version,
            kubernetes_template_id=kubernetes_template_id,
            name=name,
            network_id=network_id,
            vdc_id=vdc_id,
            worker_pool=worker_pool,
            api_token_file=api_token_file,
            auto_repair_on_errors=auto_repair_on_errors,
            default_storage_class=default_storage_class,
            id=id,
            node_health_check=node_health_check,
            operations_timeout_minutes=operations_timeout_minutes,
            org=org,
            owner=owner,
            pods_cidr=pods_cidr,
            runtime=runtime,
            services_cidr=services_cidr,
            ssh_public_key=ssh_public_key,
            virtual_ip_subnet=virtual_ip_subnet,
            connection=connection,
            count=count,
            depends_on=depends_on,
            for_each=for_each,
            lifecycle=lifecycle,
            provider=provider,
            provisioners=provisioners,
        )

        jsii.create(self.__class__, self, [scope, id_, config])

    @jsii.member(jsii_name="generateConfigForImport")
    @builtins.classmethod
    def generate_config_for_import(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        import_to_id: builtins.str,
        import_from_id: builtins.str,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    ) -> _cdktf_9a9027ec.ImportableResource:
        '''Generates CDKTF code for importing a CseKubernetesCluster resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the CseKubernetesCluster to import.
        :param import_from_id: The id of the existing CseKubernetesCluster that should be imported. Refer to the {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/cse_kubernetes_cluster#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the CseKubernetesCluster to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__79ba73201799f5608a7407387514c08f6991a99ab4e52d9b65cdef875b4e5577)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putControlPlane")
    def put_control_plane(
        self,
        *,
        disk_size_gi: typing.Optional[jsii.Number] = None,
        ip: typing.Optional[builtins.str] = None,
        machine_count: typing.Optional[jsii.Number] = None,
        placement_policy_id: typing.Optional[builtins.str] = None,
        sizing_policy_id: typing.Optional[builtins.str] = None,
        storage_profile_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param disk_size_gi: Disk size, in Gibibytes (Gi), for the control plane nodes. Must be at least 20. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/cse_kubernetes_cluster#disk_size_gi CseKubernetesCluster#disk_size_gi}
        :param ip: IP for the control plane. It will be automatically assigned during cluster creation if left empty. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/cse_kubernetes_cluster#ip CseKubernetesCluster#ip}
        :param machine_count: The number of nodes that the control plane has. Must be an odd number and higher than 0. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/cse_kubernetes_cluster#machine_count CseKubernetesCluster#machine_count}
        :param placement_policy_id: VM Placement policy for the control plane nodes. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/cse_kubernetes_cluster#placement_policy_id CseKubernetesCluster#placement_policy_id}
        :param sizing_policy_id: VM Sizing policy for the control plane nodes. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/cse_kubernetes_cluster#sizing_policy_id CseKubernetesCluster#sizing_policy_id}
        :param storage_profile_id: Storage profile for the control plane nodes. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/cse_kubernetes_cluster#storage_profile_id CseKubernetesCluster#storage_profile_id}
        '''
        value = CseKubernetesClusterControlPlane(
            disk_size_gi=disk_size_gi,
            ip=ip,
            machine_count=machine_count,
            placement_policy_id=placement_policy_id,
            sizing_policy_id=sizing_policy_id,
            storage_profile_id=storage_profile_id,
        )

        return typing.cast(None, jsii.invoke(self, "putControlPlane", [value]))

    @jsii.member(jsii_name="putDefaultStorageClass")
    def put_default_storage_class(
        self,
        *,
        filesystem: builtins.str,
        name: builtins.str,
        reclaim_policy: builtins.str,
        storage_profile_id: builtins.str,
    ) -> None:
        '''
        :param filesystem: Filesystem of the storage class, can be either 'ext4' or 'xfs'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/cse_kubernetes_cluster#filesystem CseKubernetesCluster#filesystem}
        :param name: Name to give to this storage class. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/cse_kubernetes_cluster#name CseKubernetesCluster#name}
        :param reclaim_policy: Reclaim policy. Possible values are: ``delete`` deletes the volume when the ``PersistentVolumeClaim`` is deleted; ``retain`` does not delete, and the volume can be manually reclaimed Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/cse_kubernetes_cluster#reclaim_policy CseKubernetesCluster#reclaim_policy}
        :param storage_profile_id: ID of the storage profile to use for the storage class. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/cse_kubernetes_cluster#storage_profile_id CseKubernetesCluster#storage_profile_id}
        '''
        value = CseKubernetesClusterDefaultStorageClass(
            filesystem=filesystem,
            name=name,
            reclaim_policy=reclaim_policy,
            storage_profile_id=storage_profile_id,
        )

        return typing.cast(None, jsii.invoke(self, "putDefaultStorageClass", [value]))

    @jsii.member(jsii_name="putWorkerPool")
    def put_worker_pool(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CseKubernetesClusterWorkerPool", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__43cfe502eec2afb37dba6f2abfca88980727ba8c37797d04b1cefebdd24c35d7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putWorkerPool", [value]))

    @jsii.member(jsii_name="resetApiTokenFile")
    def reset_api_token_file(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetApiTokenFile", []))

    @jsii.member(jsii_name="resetAutoRepairOnErrors")
    def reset_auto_repair_on_errors(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAutoRepairOnErrors", []))

    @jsii.member(jsii_name="resetDefaultStorageClass")
    def reset_default_storage_class(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDefaultStorageClass", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetNodeHealthCheck")
    def reset_node_health_check(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNodeHealthCheck", []))

    @jsii.member(jsii_name="resetOperationsTimeoutMinutes")
    def reset_operations_timeout_minutes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOperationsTimeoutMinutes", []))

    @jsii.member(jsii_name="resetOrg")
    def reset_org(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOrg", []))

    @jsii.member(jsii_name="resetOwner")
    def reset_owner(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOwner", []))

    @jsii.member(jsii_name="resetPodsCidr")
    def reset_pods_cidr(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPodsCidr", []))

    @jsii.member(jsii_name="resetRuntime")
    def reset_runtime(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRuntime", []))

    @jsii.member(jsii_name="resetServicesCidr")
    def reset_services_cidr(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetServicesCidr", []))

    @jsii.member(jsii_name="resetSshPublicKey")
    def reset_ssh_public_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSshPublicKey", []))

    @jsii.member(jsii_name="resetVirtualIpSubnet")
    def reset_virtual_ip_subnet(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVirtualIpSubnet", []))

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))

    @jsii.member(jsii_name="synthesizeHclAttributes")
    def _synthesize_hcl_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeHclAttributes", []))

    @jsii.python.classproperty
    @jsii.member(jsii_name="tfResourceType")
    def TF_RESOURCE_TYPE(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "tfResourceType"))

    @builtins.property
    @jsii.member(jsii_name="capvcdVersion")
    def capvcd_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "capvcdVersion"))

    @builtins.property
    @jsii.member(jsii_name="clusterResourceSetBindings")
    def cluster_resource_set_bindings(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "clusterResourceSetBindings"))

    @builtins.property
    @jsii.member(jsii_name="controlPlane")
    def control_plane(self) -> "CseKubernetesClusterControlPlaneOutputReference":
        return typing.cast("CseKubernetesClusterControlPlaneOutputReference", jsii.get(self, "controlPlane"))

    @builtins.property
    @jsii.member(jsii_name="cpiVersion")
    def cpi_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "cpiVersion"))

    @builtins.property
    @jsii.member(jsii_name="csiVersion")
    def csi_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "csiVersion"))

    @builtins.property
    @jsii.member(jsii_name="defaultStorageClass")
    def default_storage_class(
        self,
    ) -> "CseKubernetesClusterDefaultStorageClassOutputReference":
        return typing.cast("CseKubernetesClusterDefaultStorageClassOutputReference", jsii.get(self, "defaultStorageClass"))

    @builtins.property
    @jsii.member(jsii_name="events")
    def events(self) -> "CseKubernetesClusterEventsList":
        return typing.cast("CseKubernetesClusterEventsList", jsii.get(self, "events"))

    @builtins.property
    @jsii.member(jsii_name="kubeconfig")
    def kubeconfig(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "kubeconfig"))

    @builtins.property
    @jsii.member(jsii_name="kubernetesVersion")
    def kubernetes_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "kubernetesVersion"))

    @builtins.property
    @jsii.member(jsii_name="state")
    def state(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "state"))

    @builtins.property
    @jsii.member(jsii_name="supportedUpgrades")
    def supported_upgrades(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "supportedUpgrades"))

    @builtins.property
    @jsii.member(jsii_name="tkgProductVersion")
    def tkg_product_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tkgProductVersion"))

    @builtins.property
    @jsii.member(jsii_name="workerPool")
    def worker_pool(self) -> "CseKubernetesClusterWorkerPoolList":
        return typing.cast("CseKubernetesClusterWorkerPoolList", jsii.get(self, "workerPool"))

    @builtins.property
    @jsii.member(jsii_name="apiTokenFileInput")
    def api_token_file_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "apiTokenFileInput"))

    @builtins.property
    @jsii.member(jsii_name="autoRepairOnErrorsInput")
    def auto_repair_on_errors_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "autoRepairOnErrorsInput"))

    @builtins.property
    @jsii.member(jsii_name="controlPlaneInput")
    def control_plane_input(
        self,
    ) -> typing.Optional["CseKubernetesClusterControlPlane"]:
        return typing.cast(typing.Optional["CseKubernetesClusterControlPlane"], jsii.get(self, "controlPlaneInput"))

    @builtins.property
    @jsii.member(jsii_name="cseVersionInput")
    def cse_version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "cseVersionInput"))

    @builtins.property
    @jsii.member(jsii_name="defaultStorageClassInput")
    def default_storage_class_input(
        self,
    ) -> typing.Optional["CseKubernetesClusterDefaultStorageClass"]:
        return typing.cast(typing.Optional["CseKubernetesClusterDefaultStorageClass"], jsii.get(self, "defaultStorageClassInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="kubernetesTemplateIdInput")
    def kubernetes_template_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "kubernetesTemplateIdInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="networkIdInput")
    def network_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "networkIdInput"))

    @builtins.property
    @jsii.member(jsii_name="nodeHealthCheckInput")
    def node_health_check_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "nodeHealthCheckInput"))

    @builtins.property
    @jsii.member(jsii_name="operationsTimeoutMinutesInput")
    def operations_timeout_minutes_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "operationsTimeoutMinutesInput"))

    @builtins.property
    @jsii.member(jsii_name="orgInput")
    def org_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "orgInput"))

    @builtins.property
    @jsii.member(jsii_name="ownerInput")
    def owner_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "ownerInput"))

    @builtins.property
    @jsii.member(jsii_name="podsCidrInput")
    def pods_cidr_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "podsCidrInput"))

    @builtins.property
    @jsii.member(jsii_name="runtimeInput")
    def runtime_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "runtimeInput"))

    @builtins.property
    @jsii.member(jsii_name="servicesCidrInput")
    def services_cidr_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "servicesCidrInput"))

    @builtins.property
    @jsii.member(jsii_name="sshPublicKeyInput")
    def ssh_public_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sshPublicKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="vdcIdInput")
    def vdc_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "vdcIdInput"))

    @builtins.property
    @jsii.member(jsii_name="virtualIpSubnetInput")
    def virtual_ip_subnet_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "virtualIpSubnetInput"))

    @builtins.property
    @jsii.member(jsii_name="workerPoolInput")
    def worker_pool_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CseKubernetesClusterWorkerPool"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CseKubernetesClusterWorkerPool"]]], jsii.get(self, "workerPoolInput"))

    @builtins.property
    @jsii.member(jsii_name="apiTokenFile")
    def api_token_file(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "apiTokenFile"))

    @api_token_file.setter
    def api_token_file(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__db1b36416feed5b56f8fa80c8fbca4cea63c16cdbf9b0091bc8e49f38bfae616)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "apiTokenFile", value)

    @builtins.property
    @jsii.member(jsii_name="autoRepairOnErrors")
    def auto_repair_on_errors(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "autoRepairOnErrors"))

    @auto_repair_on_errors.setter
    def auto_repair_on_errors(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__10e906c86f300b4bbfa4b91c1024b9b277ae0924f9231f930896ca6d2434ecdf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "autoRepairOnErrors", value)

    @builtins.property
    @jsii.member(jsii_name="cseVersion")
    def cse_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "cseVersion"))

    @cse_version.setter
    def cse_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1fafe0ca37b1fa236faa3b6d4562985989dab2d74b7f45f7a1c6b6cceab7ba39)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cseVersion", value)

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__25d443ff5c50b95358912cf924a233e4749e5fb693534e610e1ed15b35381eb3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="kubernetesTemplateId")
    def kubernetes_template_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "kubernetesTemplateId"))

    @kubernetes_template_id.setter
    def kubernetes_template_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__af115396d6a5e5ef01e6e894602027b259ef12597afa8feecfd13f39989cb01c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kubernetesTemplateId", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2a516c0d4406c7e11ab8266015b7bb935c91b3595cbc8c7cdb878723c76027d4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="networkId")
    def network_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "networkId"))

    @network_id.setter
    def network_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8c594808e37763efd43c50fc81ae49bcbd1d5a4442c249a488123f43df97c199)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "networkId", value)

    @builtins.property
    @jsii.member(jsii_name="nodeHealthCheck")
    def node_health_check(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "nodeHealthCheck"))

    @node_health_check.setter
    def node_health_check(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4c00daaf89718772f31084b13e1e5c3b57f9529b6f97ba3b19bf93ab87788ed5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "nodeHealthCheck", value)

    @builtins.property
    @jsii.member(jsii_name="operationsTimeoutMinutes")
    def operations_timeout_minutes(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "operationsTimeoutMinutes"))

    @operations_timeout_minutes.setter
    def operations_timeout_minutes(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ba33b0fe9c152396d4e7f50c1b8fc4ec5f2fe9fefd408846e2a7b956b2bb58f9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "operationsTimeoutMinutes", value)

    @builtins.property
    @jsii.member(jsii_name="org")
    def org(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "org"))

    @org.setter
    def org(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__57f5375c38a30ed217d39883528e582497f0717c3a936edf4d42e8119c99a691)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "org", value)

    @builtins.property
    @jsii.member(jsii_name="owner")
    def owner(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "owner"))

    @owner.setter
    def owner(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9c1691f7385f4a5d88afda3a4c696480b9d845ab8d90dd475a180e83cfb21bb5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "owner", value)

    @builtins.property
    @jsii.member(jsii_name="podsCidr")
    def pods_cidr(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "podsCidr"))

    @pods_cidr.setter
    def pods_cidr(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b8bec526992ecc68f3beff0acb1b7c454ba1b814a600c857f5e58acb3b90d71d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "podsCidr", value)

    @builtins.property
    @jsii.member(jsii_name="runtime")
    def runtime(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "runtime"))

    @runtime.setter
    def runtime(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1ce077644be209dd90794ac776b830e407905b611843de586b21244b1eeaa127)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "runtime", value)

    @builtins.property
    @jsii.member(jsii_name="servicesCidr")
    def services_cidr(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "servicesCidr"))

    @services_cidr.setter
    def services_cidr(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6bfbb5a24ccdc93affe27818f8d9255c929bb95a9346a188716c78145ec2c75b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "servicesCidr", value)

    @builtins.property
    @jsii.member(jsii_name="sshPublicKey")
    def ssh_public_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sshPublicKey"))

    @ssh_public_key.setter
    def ssh_public_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__166456eea3d7de565a0b9838732d29e765c8abbae6a8673c2004996757ae1a85)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sshPublicKey", value)

    @builtins.property
    @jsii.member(jsii_name="vdcId")
    def vdc_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "vdcId"))

    @vdc_id.setter
    def vdc_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b1e8841170b5a7950c5a272bb7b64b73f105063cec8061bc12b0b5205fc4ed41)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vdcId", value)

    @builtins.property
    @jsii.member(jsii_name="virtualIpSubnet")
    def virtual_ip_subnet(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "virtualIpSubnet"))

    @virtual_ip_subnet.setter
    def virtual_ip_subnet(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b84fe2e1ebc57f345eb78c996d90ee736f4478b4e412ffc2fd52c44bf161eee7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "virtualIpSubnet", value)


@jsii.data_type(
    jsii_type="vcd.cseKubernetesCluster.CseKubernetesClusterConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "control_plane": "controlPlane",
        "cse_version": "cseVersion",
        "kubernetes_template_id": "kubernetesTemplateId",
        "name": "name",
        "network_id": "networkId",
        "vdc_id": "vdcId",
        "worker_pool": "workerPool",
        "api_token_file": "apiTokenFile",
        "auto_repair_on_errors": "autoRepairOnErrors",
        "default_storage_class": "defaultStorageClass",
        "id": "id",
        "node_health_check": "nodeHealthCheck",
        "operations_timeout_minutes": "operationsTimeoutMinutes",
        "org": "org",
        "owner": "owner",
        "pods_cidr": "podsCidr",
        "runtime": "runtime",
        "services_cidr": "servicesCidr",
        "ssh_public_key": "sshPublicKey",
        "virtual_ip_subnet": "virtualIpSubnet",
    },
)
class CseKubernetesClusterConfig(_cdktf_9a9027ec.TerraformMetaArguments):
    def __init__(
        self,
        *,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
        control_plane: typing.Union["CseKubernetesClusterControlPlane", typing.Dict[builtins.str, typing.Any]],
        cse_version: builtins.str,
        kubernetes_template_id: builtins.str,
        name: builtins.str,
        network_id: builtins.str,
        vdc_id: builtins.str,
        worker_pool: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CseKubernetesClusterWorkerPool", typing.Dict[builtins.str, typing.Any]]]],
        api_token_file: typing.Optional[builtins.str] = None,
        auto_repair_on_errors: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        default_storage_class: typing.Optional[typing.Union["CseKubernetesClusterDefaultStorageClass", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        node_health_check: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        operations_timeout_minutes: typing.Optional[jsii.Number] = None,
        org: typing.Optional[builtins.str] = None,
        owner: typing.Optional[builtins.str] = None,
        pods_cidr: typing.Optional[builtins.str] = None,
        runtime: typing.Optional[builtins.str] = None,
        services_cidr: typing.Optional[builtins.str] = None,
        ssh_public_key: typing.Optional[builtins.str] = None,
        virtual_ip_subnet: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param control_plane: control_plane block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/cse_kubernetes_cluster#control_plane CseKubernetesCluster#control_plane}
        :param cse_version: The CSE version to use. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/cse_kubernetes_cluster#cse_version CseKubernetesCluster#cse_version}
        :param kubernetes_template_id: The ID of the vApp Template that corresponds to a Kubernetes template OVA. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/cse_kubernetes_cluster#kubernetes_template_id CseKubernetesCluster#kubernetes_template_id}
        :param name: The name of the Kubernetes cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/cse_kubernetes_cluster#name CseKubernetesCluster#name}
        :param network_id: The ID of the network that the Kubernetes cluster will use. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/cse_kubernetes_cluster#network_id CseKubernetesCluster#network_id}
        :param vdc_id: The ID of the VDC that hosts the Kubernetes cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/cse_kubernetes_cluster#vdc_id CseKubernetesCluster#vdc_id}
        :param worker_pool: worker_pool block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/cse_kubernetes_cluster#worker_pool CseKubernetesCluster#worker_pool}
        :param api_token_file: A file generated by 'vcd_api_token' resource, that stores the API token used to create and manage the cluster, owned by the user specified in 'owner'. Be careful about this file, as it contains sensitive information Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/cse_kubernetes_cluster#api_token_file CseKubernetesCluster#api_token_file}
        :param auto_repair_on_errors: If errors occur before the Kubernetes cluster becomes available, and this argument is 'true', CSE Server will automatically attempt to repair the cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/cse_kubernetes_cluster#auto_repair_on_errors CseKubernetesCluster#auto_repair_on_errors}
        :param default_storage_class: default_storage_class block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/cse_kubernetes_cluster#default_storage_class CseKubernetesCluster#default_storage_class}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/cse_kubernetes_cluster#id CseKubernetesCluster#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param node_health_check: After the Kubernetes cluster becomes available, nodes that become unhealthy will be remediated according to unhealthy node conditions and remediation rules. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/cse_kubernetes_cluster#node_health_check CseKubernetesCluster#node_health_check}
        :param operations_timeout_minutes: The time, in minutes, to wait for the cluster operations to be successfully completed. For example, during cluster creation, it should be in ``provisioned``state before the timeout is reached, otherwise the operation will return an error. For cluster deletion, this timeoutspecifies the time to wait until the cluster is completely deleted. Setting this argument to ``0`` means to wait indefinitely Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/cse_kubernetes_cluster#operations_timeout_minutes CseKubernetesCluster#operations_timeout_minutes}
        :param org: The name of organization that will own this Kubernetes cluster, optional if defined at provider level. Useful when connected as sysadmin working across different organizations Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/cse_kubernetes_cluster#org CseKubernetesCluster#org}
        :param owner: The user that creates the cluster and owns the API token specified in 'api_token'. It must have the 'Kubernetes Cluster Author' role. If not specified, it assumes it's the user from the provider configuration Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/cse_kubernetes_cluster#owner CseKubernetesCluster#owner}
        :param pods_cidr: CIDR that the Kubernetes pods will use. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/cse_kubernetes_cluster#pods_cidr CseKubernetesCluster#pods_cidr}
        :param runtime: The Kubernetes runtime for the cluster. Only 'tkg' (Tanzu Kubernetes Grid) is supported. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/cse_kubernetes_cluster#runtime CseKubernetesCluster#runtime}
        :param services_cidr: CIDR that the Kubernetes services will use. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/cse_kubernetes_cluster#services_cidr CseKubernetesCluster#services_cidr}
        :param ssh_public_key: The SSH public key used to login into the cluster nodes. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/cse_kubernetes_cluster#ssh_public_key CseKubernetesCluster#ssh_public_key}
        :param virtual_ip_subnet: Virtual IP subnet for the cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/cse_kubernetes_cluster#virtual_ip_subnet CseKubernetesCluster#virtual_ip_subnet}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(control_plane, dict):
            control_plane = CseKubernetesClusterControlPlane(**control_plane)
        if isinstance(default_storage_class, dict):
            default_storage_class = CseKubernetesClusterDefaultStorageClass(**default_storage_class)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f5d169aee4929b4339ae2cfea84c0d9235ac048b8d2cd2dd952a6d495ab05232)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument control_plane", value=control_plane, expected_type=type_hints["control_plane"])
            check_type(argname="argument cse_version", value=cse_version, expected_type=type_hints["cse_version"])
            check_type(argname="argument kubernetes_template_id", value=kubernetes_template_id, expected_type=type_hints["kubernetes_template_id"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument network_id", value=network_id, expected_type=type_hints["network_id"])
            check_type(argname="argument vdc_id", value=vdc_id, expected_type=type_hints["vdc_id"])
            check_type(argname="argument worker_pool", value=worker_pool, expected_type=type_hints["worker_pool"])
            check_type(argname="argument api_token_file", value=api_token_file, expected_type=type_hints["api_token_file"])
            check_type(argname="argument auto_repair_on_errors", value=auto_repair_on_errors, expected_type=type_hints["auto_repair_on_errors"])
            check_type(argname="argument default_storage_class", value=default_storage_class, expected_type=type_hints["default_storage_class"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument node_health_check", value=node_health_check, expected_type=type_hints["node_health_check"])
            check_type(argname="argument operations_timeout_minutes", value=operations_timeout_minutes, expected_type=type_hints["operations_timeout_minutes"])
            check_type(argname="argument org", value=org, expected_type=type_hints["org"])
            check_type(argname="argument owner", value=owner, expected_type=type_hints["owner"])
            check_type(argname="argument pods_cidr", value=pods_cidr, expected_type=type_hints["pods_cidr"])
            check_type(argname="argument runtime", value=runtime, expected_type=type_hints["runtime"])
            check_type(argname="argument services_cidr", value=services_cidr, expected_type=type_hints["services_cidr"])
            check_type(argname="argument ssh_public_key", value=ssh_public_key, expected_type=type_hints["ssh_public_key"])
            check_type(argname="argument virtual_ip_subnet", value=virtual_ip_subnet, expected_type=type_hints["virtual_ip_subnet"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "control_plane": control_plane,
            "cse_version": cse_version,
            "kubernetes_template_id": kubernetes_template_id,
            "name": name,
            "network_id": network_id,
            "vdc_id": vdc_id,
            "worker_pool": worker_pool,
        }
        if connection is not None:
            self._values["connection"] = connection
        if count is not None:
            self._values["count"] = count
        if depends_on is not None:
            self._values["depends_on"] = depends_on
        if for_each is not None:
            self._values["for_each"] = for_each
        if lifecycle is not None:
            self._values["lifecycle"] = lifecycle
        if provider is not None:
            self._values["provider"] = provider
        if provisioners is not None:
            self._values["provisioners"] = provisioners
        if api_token_file is not None:
            self._values["api_token_file"] = api_token_file
        if auto_repair_on_errors is not None:
            self._values["auto_repair_on_errors"] = auto_repair_on_errors
        if default_storage_class is not None:
            self._values["default_storage_class"] = default_storage_class
        if id is not None:
            self._values["id"] = id
        if node_health_check is not None:
            self._values["node_health_check"] = node_health_check
        if operations_timeout_minutes is not None:
            self._values["operations_timeout_minutes"] = operations_timeout_minutes
        if org is not None:
            self._values["org"] = org
        if owner is not None:
            self._values["owner"] = owner
        if pods_cidr is not None:
            self._values["pods_cidr"] = pods_cidr
        if runtime is not None:
            self._values["runtime"] = runtime
        if services_cidr is not None:
            self._values["services_cidr"] = services_cidr
        if ssh_public_key is not None:
            self._values["ssh_public_key"] = ssh_public_key
        if virtual_ip_subnet is not None:
            self._values["virtual_ip_subnet"] = virtual_ip_subnet

    @builtins.property
    def connection(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, _cdktf_9a9027ec.WinrmProvisionerConnection]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("connection")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, _cdktf_9a9027ec.WinrmProvisionerConnection]], result)

    @builtins.property
    def count(
        self,
    ) -> typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("count")
        return typing.cast(typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]], result)

    @builtins.property
    def depends_on(
        self,
    ) -> typing.Optional[typing.List[_cdktf_9a9027ec.ITerraformDependable]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("depends_on")
        return typing.cast(typing.Optional[typing.List[_cdktf_9a9027ec.ITerraformDependable]], result)

    @builtins.property
    def for_each(self) -> typing.Optional[_cdktf_9a9027ec.ITerraformIterator]:
        '''
        :stability: experimental
        '''
        result = self._values.get("for_each")
        return typing.cast(typing.Optional[_cdktf_9a9027ec.ITerraformIterator], result)

    @builtins.property
    def lifecycle(self) -> typing.Optional[_cdktf_9a9027ec.TerraformResourceLifecycle]:
        '''
        :stability: experimental
        '''
        result = self._values.get("lifecycle")
        return typing.cast(typing.Optional[_cdktf_9a9027ec.TerraformResourceLifecycle], result)

    @builtins.property
    def provider(self) -> typing.Optional[_cdktf_9a9027ec.TerraformProvider]:
        '''
        :stability: experimental
        '''
        result = self._values.get("provider")
        return typing.cast(typing.Optional[_cdktf_9a9027ec.TerraformProvider], result)

    @builtins.property
    def provisioners(
        self,
    ) -> typing.Optional[typing.List[typing.Union[_cdktf_9a9027ec.FileProvisioner, _cdktf_9a9027ec.LocalExecProvisioner, _cdktf_9a9027ec.RemoteExecProvisioner]]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("provisioners")
        return typing.cast(typing.Optional[typing.List[typing.Union[_cdktf_9a9027ec.FileProvisioner, _cdktf_9a9027ec.LocalExecProvisioner, _cdktf_9a9027ec.RemoteExecProvisioner]]], result)

    @builtins.property
    def control_plane(self) -> "CseKubernetesClusterControlPlane":
        '''control_plane block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/cse_kubernetes_cluster#control_plane CseKubernetesCluster#control_plane}
        '''
        result = self._values.get("control_plane")
        assert result is not None, "Required property 'control_plane' is missing"
        return typing.cast("CseKubernetesClusterControlPlane", result)

    @builtins.property
    def cse_version(self) -> builtins.str:
        '''The CSE version to use.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/cse_kubernetes_cluster#cse_version CseKubernetesCluster#cse_version}
        '''
        result = self._values.get("cse_version")
        assert result is not None, "Required property 'cse_version' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def kubernetes_template_id(self) -> builtins.str:
        '''The ID of the vApp Template that corresponds to a Kubernetes template OVA.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/cse_kubernetes_cluster#kubernetes_template_id CseKubernetesCluster#kubernetes_template_id}
        '''
        result = self._values.get("kubernetes_template_id")
        assert result is not None, "Required property 'kubernetes_template_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''The name of the Kubernetes cluster.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/cse_kubernetes_cluster#name CseKubernetesCluster#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def network_id(self) -> builtins.str:
        '''The ID of the network that the Kubernetes cluster will use.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/cse_kubernetes_cluster#network_id CseKubernetesCluster#network_id}
        '''
        result = self._values.get("network_id")
        assert result is not None, "Required property 'network_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def vdc_id(self) -> builtins.str:
        '''The ID of the VDC that hosts the Kubernetes cluster.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/cse_kubernetes_cluster#vdc_id CseKubernetesCluster#vdc_id}
        '''
        result = self._values.get("vdc_id")
        assert result is not None, "Required property 'vdc_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def worker_pool(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CseKubernetesClusterWorkerPool"]]:
        '''worker_pool block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/cse_kubernetes_cluster#worker_pool CseKubernetesCluster#worker_pool}
        '''
        result = self._values.get("worker_pool")
        assert result is not None, "Required property 'worker_pool' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CseKubernetesClusterWorkerPool"]], result)

    @builtins.property
    def api_token_file(self) -> typing.Optional[builtins.str]:
        '''A file generated by 'vcd_api_token' resource, that stores the API token used to create and manage the cluster, owned by the user specified in 'owner'.

        Be careful about this file, as it contains sensitive information

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/cse_kubernetes_cluster#api_token_file CseKubernetesCluster#api_token_file}
        '''
        result = self._values.get("api_token_file")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def auto_repair_on_errors(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If errors occur before the Kubernetes cluster becomes available, and this argument is 'true', CSE Server will automatically attempt to repair the cluster.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/cse_kubernetes_cluster#auto_repair_on_errors CseKubernetesCluster#auto_repair_on_errors}
        '''
        result = self._values.get("auto_repair_on_errors")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def default_storage_class(
        self,
    ) -> typing.Optional["CseKubernetesClusterDefaultStorageClass"]:
        '''default_storage_class block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/cse_kubernetes_cluster#default_storage_class CseKubernetesCluster#default_storage_class}
        '''
        result = self._values.get("default_storage_class")
        return typing.cast(typing.Optional["CseKubernetesClusterDefaultStorageClass"], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/cse_kubernetes_cluster#id CseKubernetesCluster#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def node_health_check(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''After the Kubernetes cluster becomes available, nodes that become unhealthy will be remediated according to unhealthy node conditions and remediation rules.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/cse_kubernetes_cluster#node_health_check CseKubernetesCluster#node_health_check}
        '''
        result = self._values.get("node_health_check")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def operations_timeout_minutes(self) -> typing.Optional[jsii.Number]:
        '''The time, in minutes, to wait for the cluster operations to be successfully completed.

        For example, during cluster creation, it should be in ``provisioned``state before the timeout is reached, otherwise the operation will return an error. For cluster deletion, this timeoutspecifies the time to wait until the cluster is completely deleted. Setting this argument to ``0`` means to wait indefinitely

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/cse_kubernetes_cluster#operations_timeout_minutes CseKubernetesCluster#operations_timeout_minutes}
        '''
        result = self._values.get("operations_timeout_minutes")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def org(self) -> typing.Optional[builtins.str]:
        '''The name of organization that will own this Kubernetes cluster, optional if defined at provider level.

        Useful when connected as sysadmin working across different organizations

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/cse_kubernetes_cluster#org CseKubernetesCluster#org}
        '''
        result = self._values.get("org")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def owner(self) -> typing.Optional[builtins.str]:
        '''The user that creates the cluster and owns the API token specified in 'api_token'.

        It must have the 'Kubernetes Cluster Author' role. If not specified, it assumes it's the user from the provider configuration

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/cse_kubernetes_cluster#owner CseKubernetesCluster#owner}
        '''
        result = self._values.get("owner")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def pods_cidr(self) -> typing.Optional[builtins.str]:
        '''CIDR that the Kubernetes pods will use.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/cse_kubernetes_cluster#pods_cidr CseKubernetesCluster#pods_cidr}
        '''
        result = self._values.get("pods_cidr")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def runtime(self) -> typing.Optional[builtins.str]:
        '''The Kubernetes runtime for the cluster. Only 'tkg' (Tanzu Kubernetes Grid) is supported.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/cse_kubernetes_cluster#runtime CseKubernetesCluster#runtime}
        '''
        result = self._values.get("runtime")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def services_cidr(self) -> typing.Optional[builtins.str]:
        '''CIDR that the Kubernetes services will use.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/cse_kubernetes_cluster#services_cidr CseKubernetesCluster#services_cidr}
        '''
        result = self._values.get("services_cidr")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ssh_public_key(self) -> typing.Optional[builtins.str]:
        '''The SSH public key used to login into the cluster nodes.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/cse_kubernetes_cluster#ssh_public_key CseKubernetesCluster#ssh_public_key}
        '''
        result = self._values.get("ssh_public_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def virtual_ip_subnet(self) -> typing.Optional[builtins.str]:
        '''Virtual IP subnet for the cluster.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/cse_kubernetes_cluster#virtual_ip_subnet CseKubernetesCluster#virtual_ip_subnet}
        '''
        result = self._values.get("virtual_ip_subnet")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CseKubernetesClusterConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="vcd.cseKubernetesCluster.CseKubernetesClusterControlPlane",
    jsii_struct_bases=[],
    name_mapping={
        "disk_size_gi": "diskSizeGi",
        "ip": "ip",
        "machine_count": "machineCount",
        "placement_policy_id": "placementPolicyId",
        "sizing_policy_id": "sizingPolicyId",
        "storage_profile_id": "storageProfileId",
    },
)
class CseKubernetesClusterControlPlane:
    def __init__(
        self,
        *,
        disk_size_gi: typing.Optional[jsii.Number] = None,
        ip: typing.Optional[builtins.str] = None,
        machine_count: typing.Optional[jsii.Number] = None,
        placement_policy_id: typing.Optional[builtins.str] = None,
        sizing_policy_id: typing.Optional[builtins.str] = None,
        storage_profile_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param disk_size_gi: Disk size, in Gibibytes (Gi), for the control plane nodes. Must be at least 20. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/cse_kubernetes_cluster#disk_size_gi CseKubernetesCluster#disk_size_gi}
        :param ip: IP for the control plane. It will be automatically assigned during cluster creation if left empty. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/cse_kubernetes_cluster#ip CseKubernetesCluster#ip}
        :param machine_count: The number of nodes that the control plane has. Must be an odd number and higher than 0. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/cse_kubernetes_cluster#machine_count CseKubernetesCluster#machine_count}
        :param placement_policy_id: VM Placement policy for the control plane nodes. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/cse_kubernetes_cluster#placement_policy_id CseKubernetesCluster#placement_policy_id}
        :param sizing_policy_id: VM Sizing policy for the control plane nodes. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/cse_kubernetes_cluster#sizing_policy_id CseKubernetesCluster#sizing_policy_id}
        :param storage_profile_id: Storage profile for the control plane nodes. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/cse_kubernetes_cluster#storage_profile_id CseKubernetesCluster#storage_profile_id}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4d42168cbe752d0b26f7ed61093c165624a4a41c8765c1b19e46a41daba76cfd)
            check_type(argname="argument disk_size_gi", value=disk_size_gi, expected_type=type_hints["disk_size_gi"])
            check_type(argname="argument ip", value=ip, expected_type=type_hints["ip"])
            check_type(argname="argument machine_count", value=machine_count, expected_type=type_hints["machine_count"])
            check_type(argname="argument placement_policy_id", value=placement_policy_id, expected_type=type_hints["placement_policy_id"])
            check_type(argname="argument sizing_policy_id", value=sizing_policy_id, expected_type=type_hints["sizing_policy_id"])
            check_type(argname="argument storage_profile_id", value=storage_profile_id, expected_type=type_hints["storage_profile_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if disk_size_gi is not None:
            self._values["disk_size_gi"] = disk_size_gi
        if ip is not None:
            self._values["ip"] = ip
        if machine_count is not None:
            self._values["machine_count"] = machine_count
        if placement_policy_id is not None:
            self._values["placement_policy_id"] = placement_policy_id
        if sizing_policy_id is not None:
            self._values["sizing_policy_id"] = sizing_policy_id
        if storage_profile_id is not None:
            self._values["storage_profile_id"] = storage_profile_id

    @builtins.property
    def disk_size_gi(self) -> typing.Optional[jsii.Number]:
        '''Disk size, in Gibibytes (Gi), for the control plane nodes. Must be at least 20.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/cse_kubernetes_cluster#disk_size_gi CseKubernetesCluster#disk_size_gi}
        '''
        result = self._values.get("disk_size_gi")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def ip(self) -> typing.Optional[builtins.str]:
        '''IP for the control plane. It will be automatically assigned during cluster creation if left empty.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/cse_kubernetes_cluster#ip CseKubernetesCluster#ip}
        '''
        result = self._values.get("ip")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def machine_count(self) -> typing.Optional[jsii.Number]:
        '''The number of nodes that the control plane has. Must be an odd number and higher than 0.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/cse_kubernetes_cluster#machine_count CseKubernetesCluster#machine_count}
        '''
        result = self._values.get("machine_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def placement_policy_id(self) -> typing.Optional[builtins.str]:
        '''VM Placement policy for the control plane nodes.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/cse_kubernetes_cluster#placement_policy_id CseKubernetesCluster#placement_policy_id}
        '''
        result = self._values.get("placement_policy_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sizing_policy_id(self) -> typing.Optional[builtins.str]:
        '''VM Sizing policy for the control plane nodes.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/cse_kubernetes_cluster#sizing_policy_id CseKubernetesCluster#sizing_policy_id}
        '''
        result = self._values.get("sizing_policy_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def storage_profile_id(self) -> typing.Optional[builtins.str]:
        '''Storage profile for the control plane nodes.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/cse_kubernetes_cluster#storage_profile_id CseKubernetesCluster#storage_profile_id}
        '''
        result = self._values.get("storage_profile_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CseKubernetesClusterControlPlane(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CseKubernetesClusterControlPlaneOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="vcd.cseKubernetesCluster.CseKubernetesClusterControlPlaneOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c7b56ae53a69b8d9b3c563ca59bb1b49353b03492e1134fc0fb11ebb257ca042)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetDiskSizeGi")
    def reset_disk_size_gi(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDiskSizeGi", []))

    @jsii.member(jsii_name="resetIp")
    def reset_ip(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIp", []))

    @jsii.member(jsii_name="resetMachineCount")
    def reset_machine_count(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMachineCount", []))

    @jsii.member(jsii_name="resetPlacementPolicyId")
    def reset_placement_policy_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPlacementPolicyId", []))

    @jsii.member(jsii_name="resetSizingPolicyId")
    def reset_sizing_policy_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSizingPolicyId", []))

    @jsii.member(jsii_name="resetStorageProfileId")
    def reset_storage_profile_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStorageProfileId", []))

    @builtins.property
    @jsii.member(jsii_name="diskSizeGiInput")
    def disk_size_gi_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "diskSizeGiInput"))

    @builtins.property
    @jsii.member(jsii_name="ipInput")
    def ip_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "ipInput"))

    @builtins.property
    @jsii.member(jsii_name="machineCountInput")
    def machine_count_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "machineCountInput"))

    @builtins.property
    @jsii.member(jsii_name="placementPolicyIdInput")
    def placement_policy_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "placementPolicyIdInput"))

    @builtins.property
    @jsii.member(jsii_name="sizingPolicyIdInput")
    def sizing_policy_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sizingPolicyIdInput"))

    @builtins.property
    @jsii.member(jsii_name="storageProfileIdInput")
    def storage_profile_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "storageProfileIdInput"))

    @builtins.property
    @jsii.member(jsii_name="diskSizeGi")
    def disk_size_gi(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "diskSizeGi"))

    @disk_size_gi.setter
    def disk_size_gi(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4517ff5408dd86f12ce03e709d015e5252254f283ba01245abf5088d36b63ff1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "diskSizeGi", value)

    @builtins.property
    @jsii.member(jsii_name="ip")
    def ip(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ip"))

    @ip.setter
    def ip(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__635cdc6e4f0180439f5fcd8be4f59ab643dfdacac2e781ca14dcac592eb30bb7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ip", value)

    @builtins.property
    @jsii.member(jsii_name="machineCount")
    def machine_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "machineCount"))

    @machine_count.setter
    def machine_count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__204f98649bf7057e4c8037051e92475c5002251f1cd71d0b4f43ba8090b6eaea)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "machineCount", value)

    @builtins.property
    @jsii.member(jsii_name="placementPolicyId")
    def placement_policy_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "placementPolicyId"))

    @placement_policy_id.setter
    def placement_policy_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__17076281a02e5d16aec51dc35cbd72349bfa2ff4d276b24ccf311f92f4da844a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "placementPolicyId", value)

    @builtins.property
    @jsii.member(jsii_name="sizingPolicyId")
    def sizing_policy_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sizingPolicyId"))

    @sizing_policy_id.setter
    def sizing_policy_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c4ba3ae489cf74818277d49a428d48ddc2fb2bca10c5082b2e55c19acb56b268)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sizingPolicyId", value)

    @builtins.property
    @jsii.member(jsii_name="storageProfileId")
    def storage_profile_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "storageProfileId"))

    @storage_profile_id.setter
    def storage_profile_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__292c3c89d0ccf60e1a7bf6fc9b902b1e0a2233202abcc774da9dbdf97a8c7496)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "storageProfileId", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[CseKubernetesClusterControlPlane]:
        return typing.cast(typing.Optional[CseKubernetesClusterControlPlane], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CseKubernetesClusterControlPlane],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__01dad8bd4bb75f8396201a0e1d90b65d4115675cf7a7adf89b80c0b9c0d92013)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="vcd.cseKubernetesCluster.CseKubernetesClusterDefaultStorageClass",
    jsii_struct_bases=[],
    name_mapping={
        "filesystem": "filesystem",
        "name": "name",
        "reclaim_policy": "reclaimPolicy",
        "storage_profile_id": "storageProfileId",
    },
)
class CseKubernetesClusterDefaultStorageClass:
    def __init__(
        self,
        *,
        filesystem: builtins.str,
        name: builtins.str,
        reclaim_policy: builtins.str,
        storage_profile_id: builtins.str,
    ) -> None:
        '''
        :param filesystem: Filesystem of the storage class, can be either 'ext4' or 'xfs'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/cse_kubernetes_cluster#filesystem CseKubernetesCluster#filesystem}
        :param name: Name to give to this storage class. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/cse_kubernetes_cluster#name CseKubernetesCluster#name}
        :param reclaim_policy: Reclaim policy. Possible values are: ``delete`` deletes the volume when the ``PersistentVolumeClaim`` is deleted; ``retain`` does not delete, and the volume can be manually reclaimed Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/cse_kubernetes_cluster#reclaim_policy CseKubernetesCluster#reclaim_policy}
        :param storage_profile_id: ID of the storage profile to use for the storage class. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/cse_kubernetes_cluster#storage_profile_id CseKubernetesCluster#storage_profile_id}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9f9a2d6e5a721e38d6bf80ba3c1dbce0c93dd0fbfc9709960ec791e9051983e5)
            check_type(argname="argument filesystem", value=filesystem, expected_type=type_hints["filesystem"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument reclaim_policy", value=reclaim_policy, expected_type=type_hints["reclaim_policy"])
            check_type(argname="argument storage_profile_id", value=storage_profile_id, expected_type=type_hints["storage_profile_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "filesystem": filesystem,
            "name": name,
            "reclaim_policy": reclaim_policy,
            "storage_profile_id": storage_profile_id,
        }

    @builtins.property
    def filesystem(self) -> builtins.str:
        '''Filesystem of the storage class, can be either 'ext4' or 'xfs'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/cse_kubernetes_cluster#filesystem CseKubernetesCluster#filesystem}
        '''
        result = self._values.get("filesystem")
        assert result is not None, "Required property 'filesystem' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Name to give to this storage class.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/cse_kubernetes_cluster#name CseKubernetesCluster#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def reclaim_policy(self) -> builtins.str:
        '''Reclaim policy.

        Possible values are: ``delete`` deletes the volume when the ``PersistentVolumeClaim`` is deleted; ``retain`` does not delete, and the volume can be manually reclaimed

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/cse_kubernetes_cluster#reclaim_policy CseKubernetesCluster#reclaim_policy}
        '''
        result = self._values.get("reclaim_policy")
        assert result is not None, "Required property 'reclaim_policy' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def storage_profile_id(self) -> builtins.str:
        '''ID of the storage profile to use for the storage class.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/cse_kubernetes_cluster#storage_profile_id CseKubernetesCluster#storage_profile_id}
        '''
        result = self._values.get("storage_profile_id")
        assert result is not None, "Required property 'storage_profile_id' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CseKubernetesClusterDefaultStorageClass(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CseKubernetesClusterDefaultStorageClassOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="vcd.cseKubernetesCluster.CseKubernetesClusterDefaultStorageClassOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2e9af5a27e3ee16c7045bbb1716ce52277dca01ad42ec4f32f667df9e12f6c35)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="filesystemInput")
    def filesystem_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "filesystemInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="reclaimPolicyInput")
    def reclaim_policy_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "reclaimPolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="storageProfileIdInput")
    def storage_profile_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "storageProfileIdInput"))

    @builtins.property
    @jsii.member(jsii_name="filesystem")
    def filesystem(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "filesystem"))

    @filesystem.setter
    def filesystem(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__04700d38c1cc54fac2764f7970c01a8d0ec05d0b998af6624fb0d5c4961bda4b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "filesystem", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c1e814c4583b646cb4c91577e99d0e929ed4b967b1cc5f064a77f2fff636d4ce)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="reclaimPolicy")
    def reclaim_policy(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "reclaimPolicy"))

    @reclaim_policy.setter
    def reclaim_policy(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f699574e9c05ac240775c52de6b8fed67d8707c66bdd3e5094ca041ae8f979c8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "reclaimPolicy", value)

    @builtins.property
    @jsii.member(jsii_name="storageProfileId")
    def storage_profile_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "storageProfileId"))

    @storage_profile_id.setter
    def storage_profile_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c77d51d9f33d2d5ae19609d58552bf7ace97b55833de1788fac83c42105860cb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "storageProfileId", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[CseKubernetesClusterDefaultStorageClass]:
        return typing.cast(typing.Optional[CseKubernetesClusterDefaultStorageClass], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CseKubernetesClusterDefaultStorageClass],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__123a2a4681b66184505cf9016cf611860caa43107586448abf7720d063c1a156)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="vcd.cseKubernetesCluster.CseKubernetesClusterEvents",
    jsii_struct_bases=[],
    name_mapping={},
)
class CseKubernetesClusterEvents:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CseKubernetesClusterEvents(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CseKubernetesClusterEventsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="vcd.cseKubernetesCluster.CseKubernetesClusterEventsList",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        wraps_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param wraps_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6941a1a27723b36660d2ac9ffaa75425de3901ef8d4eec3fc7ddef4520b06f14)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "CseKubernetesClusterEventsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7103c429911597bd30cbb829ad06240cf7e17ff6aa4847ac83afd89eb79cd921)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("CseKubernetesClusterEventsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__96290521f85892f70e151c28af2dae9f2987e3d0525c42cd3e0ae0f359454381)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformAttribute", value)

    @builtins.property
    @jsii.member(jsii_name="terraformResource")
    def _terraform_resource(self) -> _cdktf_9a9027ec.IInterpolatingParent:
        '''The parent resource.'''
        return typing.cast(_cdktf_9a9027ec.IInterpolatingParent, jsii.get(self, "terraformResource"))

    @_terraform_resource.setter
    def _terraform_resource(self, value: _cdktf_9a9027ec.IInterpolatingParent) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4b760a2f4d447cd52491d4940c50ed96316ca5606721fb5bca01169c32228e7a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformResource", value)

    @builtins.property
    @jsii.member(jsii_name="wrapsSet")
    def _wraps_set(self) -> builtins.bool:
        '''whether the list is wrapping a set (will add tolist() to be able to access an item via an index).'''
        return typing.cast(builtins.bool, jsii.get(self, "wrapsSet"))

    @_wraps_set.setter
    def _wraps_set(self, value: builtins.bool) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c31360e21b89854a3793ced6ba932513d5b30697211f6bf545fe4ca054670dda)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)


class CseKubernetesClusterEventsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="vcd.cseKubernetesCluster.CseKubernetesClusterEventsOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        complex_object_index: jsii.Number,
        complex_object_is_from_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param complex_object_index: the index of this item in the list.
        :param complex_object_is_from_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d4c7ba975ede1d33cf3c7527576926d6b1af21d8683a2e8e554b6b22f9f4a6a0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="details")
    def details(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "details"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="occurredAt")
    def occurred_at(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "occurredAt"))

    @builtins.property
    @jsii.member(jsii_name="resourceId")
    def resource_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "resourceId"))

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[CseKubernetesClusterEvents]:
        return typing.cast(typing.Optional[CseKubernetesClusterEvents], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CseKubernetesClusterEvents],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6f66779b10037d19a3cb8e03aa0f5de95cc6f22b10288a2b5f7344b2f1125e14)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="vcd.cseKubernetesCluster.CseKubernetesClusterWorkerPool",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "autoscaler_max_replicas": "autoscalerMaxReplicas",
        "autoscaler_min_replicas": "autoscalerMinReplicas",
        "disk_size_gi": "diskSizeGi",
        "machine_count": "machineCount",
        "placement_policy_id": "placementPolicyId",
        "sizing_policy_id": "sizingPolicyId",
        "storage_profile_id": "storageProfileId",
        "vgpu_policy_id": "vgpuPolicyId",
    },
)
class CseKubernetesClusterWorkerPool:
    def __init__(
        self,
        *,
        name: builtins.str,
        autoscaler_max_replicas: typing.Optional[jsii.Number] = None,
        autoscaler_min_replicas: typing.Optional[jsii.Number] = None,
        disk_size_gi: typing.Optional[jsii.Number] = None,
        machine_count: typing.Optional[jsii.Number] = None,
        placement_policy_id: typing.Optional[builtins.str] = None,
        sizing_policy_id: typing.Optional[builtins.str] = None,
        storage_profile_id: typing.Optional[builtins.str] = None,
        vgpu_policy_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param name: The name of this worker pool. Must be unique. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/cse_kubernetes_cluster#name CseKubernetesCluster#name}
        :param autoscaler_max_replicas: Maximum replicas for the autoscaling capabilities of this worker pool. Requires 'autoscaler_min_replicas'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/cse_kubernetes_cluster#autoscaler_max_replicas CseKubernetesCluster#autoscaler_max_replicas}
        :param autoscaler_min_replicas: Minimum replicas for the autoscaling capabilities of this worker pool. Requires 'autoscaler_max_replicas'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/cse_kubernetes_cluster#autoscaler_min_replicas CseKubernetesCluster#autoscaler_min_replicas}
        :param disk_size_gi: Disk size, in Gibibytes (Gi), for this worker pool. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/cse_kubernetes_cluster#disk_size_gi CseKubernetesCluster#disk_size_gi}
        :param machine_count: The number of nodes that this worker pool has. Must be higher than or equal to 0. Ignored if 'autoscaler_max_replicas' and 'autoscaler_min_replicas' are set Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/cse_kubernetes_cluster#machine_count CseKubernetesCluster#machine_count}
        :param placement_policy_id: VM Placement policy for this worker pool. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/cse_kubernetes_cluster#placement_policy_id CseKubernetesCluster#placement_policy_id}
        :param sizing_policy_id: VM Sizing policy for this worker pool. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/cse_kubernetes_cluster#sizing_policy_id CseKubernetesCluster#sizing_policy_id}
        :param storage_profile_id: Storage profile for this worker pool. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/cse_kubernetes_cluster#storage_profile_id CseKubernetesCluster#storage_profile_id}
        :param vgpu_policy_id: vGPU policy for this worker pool. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/cse_kubernetes_cluster#vgpu_policy_id CseKubernetesCluster#vgpu_policy_id}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__16e1ac2555b0eca0cd8e2b804396dd4bdc24eecd38ff8f76e64077385a3909aa)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument autoscaler_max_replicas", value=autoscaler_max_replicas, expected_type=type_hints["autoscaler_max_replicas"])
            check_type(argname="argument autoscaler_min_replicas", value=autoscaler_min_replicas, expected_type=type_hints["autoscaler_min_replicas"])
            check_type(argname="argument disk_size_gi", value=disk_size_gi, expected_type=type_hints["disk_size_gi"])
            check_type(argname="argument machine_count", value=machine_count, expected_type=type_hints["machine_count"])
            check_type(argname="argument placement_policy_id", value=placement_policy_id, expected_type=type_hints["placement_policy_id"])
            check_type(argname="argument sizing_policy_id", value=sizing_policy_id, expected_type=type_hints["sizing_policy_id"])
            check_type(argname="argument storage_profile_id", value=storage_profile_id, expected_type=type_hints["storage_profile_id"])
            check_type(argname="argument vgpu_policy_id", value=vgpu_policy_id, expected_type=type_hints["vgpu_policy_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }
        if autoscaler_max_replicas is not None:
            self._values["autoscaler_max_replicas"] = autoscaler_max_replicas
        if autoscaler_min_replicas is not None:
            self._values["autoscaler_min_replicas"] = autoscaler_min_replicas
        if disk_size_gi is not None:
            self._values["disk_size_gi"] = disk_size_gi
        if machine_count is not None:
            self._values["machine_count"] = machine_count
        if placement_policy_id is not None:
            self._values["placement_policy_id"] = placement_policy_id
        if sizing_policy_id is not None:
            self._values["sizing_policy_id"] = sizing_policy_id
        if storage_profile_id is not None:
            self._values["storage_profile_id"] = storage_profile_id
        if vgpu_policy_id is not None:
            self._values["vgpu_policy_id"] = vgpu_policy_id

    @builtins.property
    def name(self) -> builtins.str:
        '''The name of this worker pool. Must be unique.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/cse_kubernetes_cluster#name CseKubernetesCluster#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def autoscaler_max_replicas(self) -> typing.Optional[jsii.Number]:
        '''Maximum replicas for the autoscaling capabilities of this worker pool. Requires 'autoscaler_min_replicas'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/cse_kubernetes_cluster#autoscaler_max_replicas CseKubernetesCluster#autoscaler_max_replicas}
        '''
        result = self._values.get("autoscaler_max_replicas")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def autoscaler_min_replicas(self) -> typing.Optional[jsii.Number]:
        '''Minimum replicas for the autoscaling capabilities of this worker pool. Requires 'autoscaler_max_replicas'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/cse_kubernetes_cluster#autoscaler_min_replicas CseKubernetesCluster#autoscaler_min_replicas}
        '''
        result = self._values.get("autoscaler_min_replicas")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def disk_size_gi(self) -> typing.Optional[jsii.Number]:
        '''Disk size, in Gibibytes (Gi), for this worker pool.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/cse_kubernetes_cluster#disk_size_gi CseKubernetesCluster#disk_size_gi}
        '''
        result = self._values.get("disk_size_gi")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def machine_count(self) -> typing.Optional[jsii.Number]:
        '''The number of nodes that this worker pool has.

        Must be higher than or equal to 0. Ignored if 'autoscaler_max_replicas' and 'autoscaler_min_replicas' are set

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/cse_kubernetes_cluster#machine_count CseKubernetesCluster#machine_count}
        '''
        result = self._values.get("machine_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def placement_policy_id(self) -> typing.Optional[builtins.str]:
        '''VM Placement policy for this worker pool.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/cse_kubernetes_cluster#placement_policy_id CseKubernetesCluster#placement_policy_id}
        '''
        result = self._values.get("placement_policy_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sizing_policy_id(self) -> typing.Optional[builtins.str]:
        '''VM Sizing policy for this worker pool.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/cse_kubernetes_cluster#sizing_policy_id CseKubernetesCluster#sizing_policy_id}
        '''
        result = self._values.get("sizing_policy_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def storage_profile_id(self) -> typing.Optional[builtins.str]:
        '''Storage profile for this worker pool.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/cse_kubernetes_cluster#storage_profile_id CseKubernetesCluster#storage_profile_id}
        '''
        result = self._values.get("storage_profile_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def vgpu_policy_id(self) -> typing.Optional[builtins.str]:
        '''vGPU policy for this worker pool.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/cse_kubernetes_cluster#vgpu_policy_id CseKubernetesCluster#vgpu_policy_id}
        '''
        result = self._values.get("vgpu_policy_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CseKubernetesClusterWorkerPool(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CseKubernetesClusterWorkerPoolList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="vcd.cseKubernetesCluster.CseKubernetesClusterWorkerPoolList",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        wraps_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param wraps_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4563b02dcf3c9319936988e9a021741ce10552b8726028b22cec927b632bb935)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "CseKubernetesClusterWorkerPoolOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__67c9da043ec9bcb181a4b84cd433b7fef6eb4c2028458d691d5d50713610db37)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("CseKubernetesClusterWorkerPoolOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__88eea2195a46c8cb591a39983eafe5e47b8a0ea1e74dda55a564b365be5ca123)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformAttribute", value)

    @builtins.property
    @jsii.member(jsii_name="terraformResource")
    def _terraform_resource(self) -> _cdktf_9a9027ec.IInterpolatingParent:
        '''The parent resource.'''
        return typing.cast(_cdktf_9a9027ec.IInterpolatingParent, jsii.get(self, "terraformResource"))

    @_terraform_resource.setter
    def _terraform_resource(self, value: _cdktf_9a9027ec.IInterpolatingParent) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__56a2a2985a0d9926d7d84ced4b651bac0a840004b863b12450191892cd7e9926)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformResource", value)

    @builtins.property
    @jsii.member(jsii_name="wrapsSet")
    def _wraps_set(self) -> builtins.bool:
        '''whether the list is wrapping a set (will add tolist() to be able to access an item via an index).'''
        return typing.cast(builtins.bool, jsii.get(self, "wrapsSet"))

    @_wraps_set.setter
    def _wraps_set(self, value: builtins.bool) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__207cd00c81b89ca9e766c59bdb4abe12a087d91f34f7b8591b9d7f5e21bb21eb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CseKubernetesClusterWorkerPool]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CseKubernetesClusterWorkerPool]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CseKubernetesClusterWorkerPool]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0e1c0ef86d8cf3a5dc8dc9e764fde830141bfbacd76f155925856eef4e9434bf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class CseKubernetesClusterWorkerPoolOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="vcd.cseKubernetesCluster.CseKubernetesClusterWorkerPoolOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        complex_object_index: jsii.Number,
        complex_object_is_from_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param complex_object_index: the index of this item in the list.
        :param complex_object_is_from_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__031205af59c81d734b4959aa46b150c12efd76ba6510909e01f49457a83a02ad)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetAutoscalerMaxReplicas")
    def reset_autoscaler_max_replicas(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAutoscalerMaxReplicas", []))

    @jsii.member(jsii_name="resetAutoscalerMinReplicas")
    def reset_autoscaler_min_replicas(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAutoscalerMinReplicas", []))

    @jsii.member(jsii_name="resetDiskSizeGi")
    def reset_disk_size_gi(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDiskSizeGi", []))

    @jsii.member(jsii_name="resetMachineCount")
    def reset_machine_count(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMachineCount", []))

    @jsii.member(jsii_name="resetPlacementPolicyId")
    def reset_placement_policy_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPlacementPolicyId", []))

    @jsii.member(jsii_name="resetSizingPolicyId")
    def reset_sizing_policy_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSizingPolicyId", []))

    @jsii.member(jsii_name="resetStorageProfileId")
    def reset_storage_profile_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStorageProfileId", []))

    @jsii.member(jsii_name="resetVgpuPolicyId")
    def reset_vgpu_policy_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVgpuPolicyId", []))

    @builtins.property
    @jsii.member(jsii_name="autoscalerMaxReplicasInput")
    def autoscaler_max_replicas_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "autoscalerMaxReplicasInput"))

    @builtins.property
    @jsii.member(jsii_name="autoscalerMinReplicasInput")
    def autoscaler_min_replicas_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "autoscalerMinReplicasInput"))

    @builtins.property
    @jsii.member(jsii_name="diskSizeGiInput")
    def disk_size_gi_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "diskSizeGiInput"))

    @builtins.property
    @jsii.member(jsii_name="machineCountInput")
    def machine_count_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "machineCountInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="placementPolicyIdInput")
    def placement_policy_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "placementPolicyIdInput"))

    @builtins.property
    @jsii.member(jsii_name="sizingPolicyIdInput")
    def sizing_policy_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sizingPolicyIdInput"))

    @builtins.property
    @jsii.member(jsii_name="storageProfileIdInput")
    def storage_profile_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "storageProfileIdInput"))

    @builtins.property
    @jsii.member(jsii_name="vgpuPolicyIdInput")
    def vgpu_policy_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "vgpuPolicyIdInput"))

    @builtins.property
    @jsii.member(jsii_name="autoscalerMaxReplicas")
    def autoscaler_max_replicas(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "autoscalerMaxReplicas"))

    @autoscaler_max_replicas.setter
    def autoscaler_max_replicas(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0747eaecf3e92c2ffe35118de2543807219f4b16be6104acdc05d947f01adbde)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "autoscalerMaxReplicas", value)

    @builtins.property
    @jsii.member(jsii_name="autoscalerMinReplicas")
    def autoscaler_min_replicas(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "autoscalerMinReplicas"))

    @autoscaler_min_replicas.setter
    def autoscaler_min_replicas(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f813a638e8d2cfeb99961769683bde712bb25f04cb7b866668e1d93f5d1eb514)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "autoscalerMinReplicas", value)

    @builtins.property
    @jsii.member(jsii_name="diskSizeGi")
    def disk_size_gi(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "diskSizeGi"))

    @disk_size_gi.setter
    def disk_size_gi(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5536faaa2e8dafefffd983aca713521b9fcb5a49f6efca0d8d0f8fc7cd9e8245)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "diskSizeGi", value)

    @builtins.property
    @jsii.member(jsii_name="machineCount")
    def machine_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "machineCount"))

    @machine_count.setter
    def machine_count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f15e2a4b4c7f532f36ea4a24dc704c0a95e35522b02e45d223b731a6a73fdf37)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "machineCount", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b8b2e2d8af0ac56fcc3d0535335efd58eea5004cfa532e29a9899ca97bd6bce9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="placementPolicyId")
    def placement_policy_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "placementPolicyId"))

    @placement_policy_id.setter
    def placement_policy_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3eb7dbdc586766591495bdbf51cbfeeaf694ef8fffd03698b611656a4a53fdff)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "placementPolicyId", value)

    @builtins.property
    @jsii.member(jsii_name="sizingPolicyId")
    def sizing_policy_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sizingPolicyId"))

    @sizing_policy_id.setter
    def sizing_policy_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6f4008b86acb2a2703239bf8c1617a5ce9000debb4119f9aabe95d3224c62bb4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sizingPolicyId", value)

    @builtins.property
    @jsii.member(jsii_name="storageProfileId")
    def storage_profile_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "storageProfileId"))

    @storage_profile_id.setter
    def storage_profile_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cc65054c1e8809d9c9d44920f3f084e0488949f9a11b602b2fddb2f478ccb7a1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "storageProfileId", value)

    @builtins.property
    @jsii.member(jsii_name="vgpuPolicyId")
    def vgpu_policy_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "vgpuPolicyId"))

    @vgpu_policy_id.setter
    def vgpu_policy_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__75ae460149d3da2d19dccabcb65627d70b6b8e77d47d5f0a7b2f7d02f13c171e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vgpuPolicyId", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CseKubernetesClusterWorkerPool]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CseKubernetesClusterWorkerPool]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CseKubernetesClusterWorkerPool]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cc2c7ac75f3262ddf4123369ecec461c0002682288b1dafbf0eb69fb525ad8b3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


__all__ = [
    "CseKubernetesCluster",
    "CseKubernetesClusterConfig",
    "CseKubernetesClusterControlPlane",
    "CseKubernetesClusterControlPlaneOutputReference",
    "CseKubernetesClusterDefaultStorageClass",
    "CseKubernetesClusterDefaultStorageClassOutputReference",
    "CseKubernetesClusterEvents",
    "CseKubernetesClusterEventsList",
    "CseKubernetesClusterEventsOutputReference",
    "CseKubernetesClusterWorkerPool",
    "CseKubernetesClusterWorkerPoolList",
    "CseKubernetesClusterWorkerPoolOutputReference",
]

publication.publish()

def _typecheckingstub__55e1692321c5899968b29eb1cc339e805a493fcffc91ab86eb1256d4420f0cd1(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    control_plane: typing.Union[CseKubernetesClusterControlPlane, typing.Dict[builtins.str, typing.Any]],
    cse_version: builtins.str,
    kubernetes_template_id: builtins.str,
    name: builtins.str,
    network_id: builtins.str,
    vdc_id: builtins.str,
    worker_pool: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CseKubernetesClusterWorkerPool, typing.Dict[builtins.str, typing.Any]]]],
    api_token_file: typing.Optional[builtins.str] = None,
    auto_repair_on_errors: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    default_storage_class: typing.Optional[typing.Union[CseKubernetesClusterDefaultStorageClass, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    node_health_check: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    operations_timeout_minutes: typing.Optional[jsii.Number] = None,
    org: typing.Optional[builtins.str] = None,
    owner: typing.Optional[builtins.str] = None,
    pods_cidr: typing.Optional[builtins.str] = None,
    runtime: typing.Optional[builtins.str] = None,
    services_cidr: typing.Optional[builtins.str] = None,
    ssh_public_key: typing.Optional[builtins.str] = None,
    virtual_ip_subnet: typing.Optional[builtins.str] = None,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__79ba73201799f5608a7407387514c08f6991a99ab4e52d9b65cdef875b4e5577(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__43cfe502eec2afb37dba6f2abfca88980727ba8c37797d04b1cefebdd24c35d7(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CseKubernetesClusterWorkerPool, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db1b36416feed5b56f8fa80c8fbca4cea63c16cdbf9b0091bc8e49f38bfae616(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__10e906c86f300b4bbfa4b91c1024b9b277ae0924f9231f930896ca6d2434ecdf(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1fafe0ca37b1fa236faa3b6d4562985989dab2d74b7f45f7a1c6b6cceab7ba39(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__25d443ff5c50b95358912cf924a233e4749e5fb693534e610e1ed15b35381eb3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af115396d6a5e5ef01e6e894602027b259ef12597afa8feecfd13f39989cb01c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a516c0d4406c7e11ab8266015b7bb935c91b3595cbc8c7cdb878723c76027d4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8c594808e37763efd43c50fc81ae49bcbd1d5a4442c249a488123f43df97c199(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c00daaf89718772f31084b13e1e5c3b57f9529b6f97ba3b19bf93ab87788ed5(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba33b0fe9c152396d4e7f50c1b8fc4ec5f2fe9fefd408846e2a7b956b2bb58f9(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__57f5375c38a30ed217d39883528e582497f0717c3a936edf4d42e8119c99a691(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c1691f7385f4a5d88afda3a4c696480b9d845ab8d90dd475a180e83cfb21bb5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b8bec526992ecc68f3beff0acb1b7c454ba1b814a600c857f5e58acb3b90d71d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ce077644be209dd90794ac776b830e407905b611843de586b21244b1eeaa127(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6bfbb5a24ccdc93affe27818f8d9255c929bb95a9346a188716c78145ec2c75b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__166456eea3d7de565a0b9838732d29e765c8abbae6a8673c2004996757ae1a85(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b1e8841170b5a7950c5a272bb7b64b73f105063cec8061bc12b0b5205fc4ed41(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b84fe2e1ebc57f345eb78c996d90ee736f4478b4e412ffc2fd52c44bf161eee7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f5d169aee4929b4339ae2cfea84c0d9235ac048b8d2cd2dd952a6d495ab05232(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    control_plane: typing.Union[CseKubernetesClusterControlPlane, typing.Dict[builtins.str, typing.Any]],
    cse_version: builtins.str,
    kubernetes_template_id: builtins.str,
    name: builtins.str,
    network_id: builtins.str,
    vdc_id: builtins.str,
    worker_pool: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CseKubernetesClusterWorkerPool, typing.Dict[builtins.str, typing.Any]]]],
    api_token_file: typing.Optional[builtins.str] = None,
    auto_repair_on_errors: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    default_storage_class: typing.Optional[typing.Union[CseKubernetesClusterDefaultStorageClass, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    node_health_check: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    operations_timeout_minutes: typing.Optional[jsii.Number] = None,
    org: typing.Optional[builtins.str] = None,
    owner: typing.Optional[builtins.str] = None,
    pods_cidr: typing.Optional[builtins.str] = None,
    runtime: typing.Optional[builtins.str] = None,
    services_cidr: typing.Optional[builtins.str] = None,
    ssh_public_key: typing.Optional[builtins.str] = None,
    virtual_ip_subnet: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4d42168cbe752d0b26f7ed61093c165624a4a41c8765c1b19e46a41daba76cfd(
    *,
    disk_size_gi: typing.Optional[jsii.Number] = None,
    ip: typing.Optional[builtins.str] = None,
    machine_count: typing.Optional[jsii.Number] = None,
    placement_policy_id: typing.Optional[builtins.str] = None,
    sizing_policy_id: typing.Optional[builtins.str] = None,
    storage_profile_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c7b56ae53a69b8d9b3c563ca59bb1b49353b03492e1134fc0fb11ebb257ca042(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4517ff5408dd86f12ce03e709d015e5252254f283ba01245abf5088d36b63ff1(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__635cdc6e4f0180439f5fcd8be4f59ab643dfdacac2e781ca14dcac592eb30bb7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__204f98649bf7057e4c8037051e92475c5002251f1cd71d0b4f43ba8090b6eaea(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__17076281a02e5d16aec51dc35cbd72349bfa2ff4d276b24ccf311f92f4da844a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c4ba3ae489cf74818277d49a428d48ddc2fb2bca10c5082b2e55c19acb56b268(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__292c3c89d0ccf60e1a7bf6fc9b902b1e0a2233202abcc774da9dbdf97a8c7496(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__01dad8bd4bb75f8396201a0e1d90b65d4115675cf7a7adf89b80c0b9c0d92013(
    value: typing.Optional[CseKubernetesClusterControlPlane],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f9a2d6e5a721e38d6bf80ba3c1dbce0c93dd0fbfc9709960ec791e9051983e5(
    *,
    filesystem: builtins.str,
    name: builtins.str,
    reclaim_policy: builtins.str,
    storage_profile_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e9af5a27e3ee16c7045bbb1716ce52277dca01ad42ec4f32f667df9e12f6c35(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__04700d38c1cc54fac2764f7970c01a8d0ec05d0b998af6624fb0d5c4961bda4b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c1e814c4583b646cb4c91577e99d0e929ed4b967b1cc5f064a77f2fff636d4ce(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f699574e9c05ac240775c52de6b8fed67d8707c66bdd3e5094ca041ae8f979c8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c77d51d9f33d2d5ae19609d58552bf7ace97b55833de1788fac83c42105860cb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__123a2a4681b66184505cf9016cf611860caa43107586448abf7720d063c1a156(
    value: typing.Optional[CseKubernetesClusterDefaultStorageClass],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6941a1a27723b36660d2ac9ffaa75425de3901ef8d4eec3fc7ddef4520b06f14(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7103c429911597bd30cbb829ad06240cf7e17ff6aa4847ac83afd89eb79cd921(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__96290521f85892f70e151c28af2dae9f2987e3d0525c42cd3e0ae0f359454381(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b760a2f4d447cd52491d4940c50ed96316ca5606721fb5bca01169c32228e7a(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c31360e21b89854a3793ced6ba932513d5b30697211f6bf545fe4ca054670dda(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d4c7ba975ede1d33cf3c7527576926d6b1af21d8683a2e8e554b6b22f9f4a6a0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f66779b10037d19a3cb8e03aa0f5de95cc6f22b10288a2b5f7344b2f1125e14(
    value: typing.Optional[CseKubernetesClusterEvents],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__16e1ac2555b0eca0cd8e2b804396dd4bdc24eecd38ff8f76e64077385a3909aa(
    *,
    name: builtins.str,
    autoscaler_max_replicas: typing.Optional[jsii.Number] = None,
    autoscaler_min_replicas: typing.Optional[jsii.Number] = None,
    disk_size_gi: typing.Optional[jsii.Number] = None,
    machine_count: typing.Optional[jsii.Number] = None,
    placement_policy_id: typing.Optional[builtins.str] = None,
    sizing_policy_id: typing.Optional[builtins.str] = None,
    storage_profile_id: typing.Optional[builtins.str] = None,
    vgpu_policy_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4563b02dcf3c9319936988e9a021741ce10552b8726028b22cec927b632bb935(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__67c9da043ec9bcb181a4b84cd433b7fef6eb4c2028458d691d5d50713610db37(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__88eea2195a46c8cb591a39983eafe5e47b8a0ea1e74dda55a564b365be5ca123(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__56a2a2985a0d9926d7d84ced4b651bac0a840004b863b12450191892cd7e9926(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__207cd00c81b89ca9e766c59bdb4abe12a087d91f34f7b8591b9d7f5e21bb21eb(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0e1c0ef86d8cf3a5dc8dc9e764fde830141bfbacd76f155925856eef4e9434bf(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CseKubernetesClusterWorkerPool]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__031205af59c81d734b4959aa46b150c12efd76ba6510909e01f49457a83a02ad(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0747eaecf3e92c2ffe35118de2543807219f4b16be6104acdc05d947f01adbde(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f813a638e8d2cfeb99961769683bde712bb25f04cb7b866668e1d93f5d1eb514(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5536faaa2e8dafefffd983aca713521b9fcb5a49f6efca0d8d0f8fc7cd9e8245(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f15e2a4b4c7f532f36ea4a24dc704c0a95e35522b02e45d223b731a6a73fdf37(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b8b2e2d8af0ac56fcc3d0535335efd58eea5004cfa532e29a9899ca97bd6bce9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3eb7dbdc586766591495bdbf51cbfeeaf694ef8fffd03698b611656a4a53fdff(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f4008b86acb2a2703239bf8c1617a5ce9000debb4119f9aabe95d3224c62bb4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc65054c1e8809d9c9d44920f3f084e0488949f9a11b602b2fddb2f478ccb7a1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__75ae460149d3da2d19dccabcb65627d70b6b8e77d47d5f0a7b2f7d02f13c171e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc2c7ac75f3262ddf4123369ecec461c0002682288b1dafbf0eb69fb525ad8b3(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CseKubernetesClusterWorkerPool]],
) -> None:
    """Type checking stubs"""
    pass
