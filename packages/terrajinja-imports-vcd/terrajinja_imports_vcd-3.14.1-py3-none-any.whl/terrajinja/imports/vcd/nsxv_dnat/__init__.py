'''
# `vcd_nsxv_dnat`

Refer to the Terraform Registry for docs: [`vcd_nsxv_dnat`](https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxv_dnat).
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


class NsxvDnat(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="vcd.nsxvDnat.NsxvDnat",
):
    '''Represents a {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxv_dnat vcd_nsxv_dnat}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        edge_gateway: builtins.str,
        network_name: builtins.str,
        network_type: builtins.str,
        original_address: builtins.str,
        description: typing.Optional[builtins.str] = None,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        icmp_type: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        logging_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        org: typing.Optional[builtins.str] = None,
        original_port: typing.Optional[builtins.str] = None,
        protocol: typing.Optional[builtins.str] = None,
        rule_tag: typing.Optional[jsii.Number] = None,
        rule_type: typing.Optional[builtins.str] = None,
        translated_address: typing.Optional[builtins.str] = None,
        translated_port: typing.Optional[builtins.str] = None,
        vdc: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxv_dnat vcd_nsxv_dnat} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param edge_gateway: Edge gateway name in which NAT Rule is located. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxv_dnat#edge_gateway NsxvDnat#edge_gateway}
        :param network_name: Org or external network name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxv_dnat#network_name NsxvDnat#network_name}
        :param network_type: Network type. One of 'ext', 'org'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxv_dnat#network_type NsxvDnat#network_type}
        :param original_address: Original address or address range. This is the the destination address for DNAT rules. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxv_dnat#original_address NsxvDnat#original_address}
        :param description: NAT rule description. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxv_dnat#description NsxvDnat#description}
        :param enabled: Whether the rule should be enabled. Default 'true'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxv_dnat#enabled NsxvDnat#enabled}
        :param icmp_type: ICMP type. Only supported when protocol is ICMP. One of ``any``, ``address-mask-request``, ``address-mask-reply``, ``destination-unreachable``, ``echo-request``, ``echo-reply``, ``parameter-problem``, ``redirect``, ``router-advertisement``, ``router-solicitation``, ``source-quench``, ``time-exceeded``, ``timestamp-request``, ``timestamp-reply``. Default ``any`` Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxv_dnat#icmp_type NsxvDnat#icmp_type}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxv_dnat#id NsxvDnat#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param logging_enabled: Whether logging should be enabled for this rule. Default 'false'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxv_dnat#logging_enabled NsxvDnat#logging_enabled}
        :param org: The name of organization to use, optional if defined at provider level. Useful when connected as sysadmin working across different organizations Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxv_dnat#org NsxvDnat#org}
        :param original_port: Original port. This is the destination port for DNAT rules. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxv_dnat#original_port NsxvDnat#original_port}
        :param protocol: Protocol. Such as 'tcp', 'udp', 'icmp', 'any'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxv_dnat#protocol NsxvDnat#protocol}
        :param rule_tag: Optional. Allows to set custom rule tag. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxv_dnat#rule_tag NsxvDnat#rule_tag}
        :param rule_type: Read only. Possible values 'user', 'internal_high'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxv_dnat#rule_type NsxvDnat#rule_type}
        :param translated_address: Translated address or address range. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxv_dnat#translated_address NsxvDnat#translated_address}
        :param translated_port: Translated port. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxv_dnat#translated_port NsxvDnat#translated_port}
        :param vdc: The name of VDC to use, optional if defined at provider level. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxv_dnat#vdc NsxvDnat#vdc}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1637e406cd0ea2fdf85b8dc6420e60b1360c4dcd4aec69b8dcac469b2aa78f25)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = NsxvDnatConfig(
            edge_gateway=edge_gateway,
            network_name=network_name,
            network_type=network_type,
            original_address=original_address,
            description=description,
            enabled=enabled,
            icmp_type=icmp_type,
            id=id,
            logging_enabled=logging_enabled,
            org=org,
            original_port=original_port,
            protocol=protocol,
            rule_tag=rule_tag,
            rule_type=rule_type,
            translated_address=translated_address,
            translated_port=translated_port,
            vdc=vdc,
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
        '''Generates CDKTF code for importing a NsxvDnat resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the NsxvDnat to import.
        :param import_from_id: The id of the existing NsxvDnat that should be imported. Refer to the {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxv_dnat#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the NsxvDnat to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__baf1ef04a8cb2f6c193fc9b49d3787750af47af90e1210e0f373db39327d60bd)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetEnabled")
    def reset_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnabled", []))

    @jsii.member(jsii_name="resetIcmpType")
    def reset_icmp_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIcmpType", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetLoggingEnabled")
    def reset_logging_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLoggingEnabled", []))

    @jsii.member(jsii_name="resetOrg")
    def reset_org(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOrg", []))

    @jsii.member(jsii_name="resetOriginalPort")
    def reset_original_port(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOriginalPort", []))

    @jsii.member(jsii_name="resetProtocol")
    def reset_protocol(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProtocol", []))

    @jsii.member(jsii_name="resetRuleTag")
    def reset_rule_tag(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRuleTag", []))

    @jsii.member(jsii_name="resetRuleType")
    def reset_rule_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRuleType", []))

    @jsii.member(jsii_name="resetTranslatedAddress")
    def reset_translated_address(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTranslatedAddress", []))

    @jsii.member(jsii_name="resetTranslatedPort")
    def reset_translated_port(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTranslatedPort", []))

    @jsii.member(jsii_name="resetVdc")
    def reset_vdc(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVdc", []))

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
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="edgeGatewayInput")
    def edge_gateway_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "edgeGatewayInput"))

    @builtins.property
    @jsii.member(jsii_name="enabledInput")
    def enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enabledInput"))

    @builtins.property
    @jsii.member(jsii_name="icmpTypeInput")
    def icmp_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "icmpTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="loggingEnabledInput")
    def logging_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "loggingEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="networkNameInput")
    def network_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "networkNameInput"))

    @builtins.property
    @jsii.member(jsii_name="networkTypeInput")
    def network_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "networkTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="orgInput")
    def org_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "orgInput"))

    @builtins.property
    @jsii.member(jsii_name="originalAddressInput")
    def original_address_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "originalAddressInput"))

    @builtins.property
    @jsii.member(jsii_name="originalPortInput")
    def original_port_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "originalPortInput"))

    @builtins.property
    @jsii.member(jsii_name="protocolInput")
    def protocol_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "protocolInput"))

    @builtins.property
    @jsii.member(jsii_name="ruleTagInput")
    def rule_tag_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "ruleTagInput"))

    @builtins.property
    @jsii.member(jsii_name="ruleTypeInput")
    def rule_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "ruleTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="translatedAddressInput")
    def translated_address_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "translatedAddressInput"))

    @builtins.property
    @jsii.member(jsii_name="translatedPortInput")
    def translated_port_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "translatedPortInput"))

    @builtins.property
    @jsii.member(jsii_name="vdcInput")
    def vdc_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "vdcInput"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8a3c9df4b237b75958ba6b2c53c96e79a5193a12076a461a0a3f30932f1818c3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value)

    @builtins.property
    @jsii.member(jsii_name="edgeGateway")
    def edge_gateway(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "edgeGateway"))

    @edge_gateway.setter
    def edge_gateway(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b8fb97fbb159e1ba6c3bdabfaeeaeef510333d7feeabff461770948b4347047e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "edgeGateway", value)

    @builtins.property
    @jsii.member(jsii_name="enabled")
    def enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enabled"))

    @enabled.setter
    def enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__30536d8e5987a62f3fc1b59a8fdb2d055bc651d22b40b56a56d0a0a20d605be2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value)

    @builtins.property
    @jsii.member(jsii_name="icmpType")
    def icmp_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "icmpType"))

    @icmp_type.setter
    def icmp_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__58e538cf79bb6a3380b9e872649d78a1d33b98c46c3d8ad0c0c55cde558a08ba)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "icmpType", value)

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1203dfce8ae94164f927cc57dc7c71314c895c562819b741a4db912d0c3f2097)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="loggingEnabled")
    def logging_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "loggingEnabled"))

    @logging_enabled.setter
    def logging_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d6d2d37ae7e0a946129172b68e82f6cd760510a0370f5d5fd078ca8601383363)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "loggingEnabled", value)

    @builtins.property
    @jsii.member(jsii_name="networkName")
    def network_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "networkName"))

    @network_name.setter
    def network_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__985ea9793b811708e7851233f2aed21166737ab9f0909d5d7d5130c97e8f0761)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "networkName", value)

    @builtins.property
    @jsii.member(jsii_name="networkType")
    def network_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "networkType"))

    @network_type.setter
    def network_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5a73a27b5623ba22cc79b748c520766cd4a5552ce18d00b3e308e33fa7ef680a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "networkType", value)

    @builtins.property
    @jsii.member(jsii_name="org")
    def org(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "org"))

    @org.setter
    def org(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fa7b99c1d38484b66240ba96894d74290a81dfc7c97514d30d92c7fbcd075b77)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "org", value)

    @builtins.property
    @jsii.member(jsii_name="originalAddress")
    def original_address(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "originalAddress"))

    @original_address.setter
    def original_address(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4eec35a7f44d9b28b7298ce13f9127b99c5270d62b005d7e4a903b3d25d45b39)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "originalAddress", value)

    @builtins.property
    @jsii.member(jsii_name="originalPort")
    def original_port(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "originalPort"))

    @original_port.setter
    def original_port(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6e6a7cc37010b9450f65f97218eaea5369d230d0b57c07f69bef37c2af737535)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "originalPort", value)

    @builtins.property
    @jsii.member(jsii_name="protocol")
    def protocol(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "protocol"))

    @protocol.setter
    def protocol(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cf77d81f45b0fcc6c8f357368494bf962a065410b6d2ab7be75d8fd9323f4462)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "protocol", value)

    @builtins.property
    @jsii.member(jsii_name="ruleTag")
    def rule_tag(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "ruleTag"))

    @rule_tag.setter
    def rule_tag(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b2ff750ad221de0b11f65660bcff18c113475ff3d443818586f5d803ba59794a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ruleTag", value)

    @builtins.property
    @jsii.member(jsii_name="ruleType")
    def rule_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ruleType"))

    @rule_type.setter
    def rule_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__975873fc0b99b09f6bf7aa8c573063168b736b94827bf9d85da7aafdbcfed4b4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ruleType", value)

    @builtins.property
    @jsii.member(jsii_name="translatedAddress")
    def translated_address(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "translatedAddress"))

    @translated_address.setter
    def translated_address(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1a29a230868c83e09866e58d643b3abaf0eec1efb7a09fb57be35cda35e89935)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "translatedAddress", value)

    @builtins.property
    @jsii.member(jsii_name="translatedPort")
    def translated_port(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "translatedPort"))

    @translated_port.setter
    def translated_port(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f9c1361f2797033a441c8b0885f694b93320866702b687f9339fef4a2b3f68a0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "translatedPort", value)

    @builtins.property
    @jsii.member(jsii_name="vdc")
    def vdc(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "vdc"))

    @vdc.setter
    def vdc(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3aebca3308c178a54c59ca222b455229ac7bed18145ee5ba585b0fbe673ab18d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vdc", value)


@jsii.data_type(
    jsii_type="vcd.nsxvDnat.NsxvDnatConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "edge_gateway": "edgeGateway",
        "network_name": "networkName",
        "network_type": "networkType",
        "original_address": "originalAddress",
        "description": "description",
        "enabled": "enabled",
        "icmp_type": "icmpType",
        "id": "id",
        "logging_enabled": "loggingEnabled",
        "org": "org",
        "original_port": "originalPort",
        "protocol": "protocol",
        "rule_tag": "ruleTag",
        "rule_type": "ruleType",
        "translated_address": "translatedAddress",
        "translated_port": "translatedPort",
        "vdc": "vdc",
    },
)
class NsxvDnatConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        edge_gateway: builtins.str,
        network_name: builtins.str,
        network_type: builtins.str,
        original_address: builtins.str,
        description: typing.Optional[builtins.str] = None,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        icmp_type: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        logging_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        org: typing.Optional[builtins.str] = None,
        original_port: typing.Optional[builtins.str] = None,
        protocol: typing.Optional[builtins.str] = None,
        rule_tag: typing.Optional[jsii.Number] = None,
        rule_type: typing.Optional[builtins.str] = None,
        translated_address: typing.Optional[builtins.str] = None,
        translated_port: typing.Optional[builtins.str] = None,
        vdc: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param edge_gateway: Edge gateway name in which NAT Rule is located. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxv_dnat#edge_gateway NsxvDnat#edge_gateway}
        :param network_name: Org or external network name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxv_dnat#network_name NsxvDnat#network_name}
        :param network_type: Network type. One of 'ext', 'org'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxv_dnat#network_type NsxvDnat#network_type}
        :param original_address: Original address or address range. This is the the destination address for DNAT rules. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxv_dnat#original_address NsxvDnat#original_address}
        :param description: NAT rule description. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxv_dnat#description NsxvDnat#description}
        :param enabled: Whether the rule should be enabled. Default 'true'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxv_dnat#enabled NsxvDnat#enabled}
        :param icmp_type: ICMP type. Only supported when protocol is ICMP. One of ``any``, ``address-mask-request``, ``address-mask-reply``, ``destination-unreachable``, ``echo-request``, ``echo-reply``, ``parameter-problem``, ``redirect``, ``router-advertisement``, ``router-solicitation``, ``source-quench``, ``time-exceeded``, ``timestamp-request``, ``timestamp-reply``. Default ``any`` Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxv_dnat#icmp_type NsxvDnat#icmp_type}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxv_dnat#id NsxvDnat#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param logging_enabled: Whether logging should be enabled for this rule. Default 'false'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxv_dnat#logging_enabled NsxvDnat#logging_enabled}
        :param org: The name of organization to use, optional if defined at provider level. Useful when connected as sysadmin working across different organizations Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxv_dnat#org NsxvDnat#org}
        :param original_port: Original port. This is the destination port for DNAT rules. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxv_dnat#original_port NsxvDnat#original_port}
        :param protocol: Protocol. Such as 'tcp', 'udp', 'icmp', 'any'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxv_dnat#protocol NsxvDnat#protocol}
        :param rule_tag: Optional. Allows to set custom rule tag. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxv_dnat#rule_tag NsxvDnat#rule_tag}
        :param rule_type: Read only. Possible values 'user', 'internal_high'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxv_dnat#rule_type NsxvDnat#rule_type}
        :param translated_address: Translated address or address range. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxv_dnat#translated_address NsxvDnat#translated_address}
        :param translated_port: Translated port. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxv_dnat#translated_port NsxvDnat#translated_port}
        :param vdc: The name of VDC to use, optional if defined at provider level. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxv_dnat#vdc NsxvDnat#vdc}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f178b0a27b9e26c7650c89546fab77d1209a3dc055719c582cdebbd487a53483)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument edge_gateway", value=edge_gateway, expected_type=type_hints["edge_gateway"])
            check_type(argname="argument network_name", value=network_name, expected_type=type_hints["network_name"])
            check_type(argname="argument network_type", value=network_type, expected_type=type_hints["network_type"])
            check_type(argname="argument original_address", value=original_address, expected_type=type_hints["original_address"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument icmp_type", value=icmp_type, expected_type=type_hints["icmp_type"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument logging_enabled", value=logging_enabled, expected_type=type_hints["logging_enabled"])
            check_type(argname="argument org", value=org, expected_type=type_hints["org"])
            check_type(argname="argument original_port", value=original_port, expected_type=type_hints["original_port"])
            check_type(argname="argument protocol", value=protocol, expected_type=type_hints["protocol"])
            check_type(argname="argument rule_tag", value=rule_tag, expected_type=type_hints["rule_tag"])
            check_type(argname="argument rule_type", value=rule_type, expected_type=type_hints["rule_type"])
            check_type(argname="argument translated_address", value=translated_address, expected_type=type_hints["translated_address"])
            check_type(argname="argument translated_port", value=translated_port, expected_type=type_hints["translated_port"])
            check_type(argname="argument vdc", value=vdc, expected_type=type_hints["vdc"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "edge_gateway": edge_gateway,
            "network_name": network_name,
            "network_type": network_type,
            "original_address": original_address,
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
        if description is not None:
            self._values["description"] = description
        if enabled is not None:
            self._values["enabled"] = enabled
        if icmp_type is not None:
            self._values["icmp_type"] = icmp_type
        if id is not None:
            self._values["id"] = id
        if logging_enabled is not None:
            self._values["logging_enabled"] = logging_enabled
        if org is not None:
            self._values["org"] = org
        if original_port is not None:
            self._values["original_port"] = original_port
        if protocol is not None:
            self._values["protocol"] = protocol
        if rule_tag is not None:
            self._values["rule_tag"] = rule_tag
        if rule_type is not None:
            self._values["rule_type"] = rule_type
        if translated_address is not None:
            self._values["translated_address"] = translated_address
        if translated_port is not None:
            self._values["translated_port"] = translated_port
        if vdc is not None:
            self._values["vdc"] = vdc

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
    def edge_gateway(self) -> builtins.str:
        '''Edge gateway name in which NAT Rule is located.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxv_dnat#edge_gateway NsxvDnat#edge_gateway}
        '''
        result = self._values.get("edge_gateway")
        assert result is not None, "Required property 'edge_gateway' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def network_name(self) -> builtins.str:
        '''Org or external network name.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxv_dnat#network_name NsxvDnat#network_name}
        '''
        result = self._values.get("network_name")
        assert result is not None, "Required property 'network_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def network_type(self) -> builtins.str:
        '''Network type. One of 'ext', 'org'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxv_dnat#network_type NsxvDnat#network_type}
        '''
        result = self._values.get("network_type")
        assert result is not None, "Required property 'network_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def original_address(self) -> builtins.str:
        '''Original address or address range. This is the the destination address for DNAT rules.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxv_dnat#original_address NsxvDnat#original_address}
        '''
        result = self._values.get("original_address")
        assert result is not None, "Required property 'original_address' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''NAT rule description.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxv_dnat#description NsxvDnat#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether the rule should be enabled. Default 'true'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxv_dnat#enabled NsxvDnat#enabled}
        '''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def icmp_type(self) -> typing.Optional[builtins.str]:
        '''ICMP type.

        Only supported when protocol is ICMP. One of ``any``, ``address-mask-request``, ``address-mask-reply``, ``destination-unreachable``, ``echo-request``, ``echo-reply``, ``parameter-problem``, ``redirect``, ``router-advertisement``, ``router-solicitation``, ``source-quench``, ``time-exceeded``, ``timestamp-request``, ``timestamp-reply``. Default ``any``

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxv_dnat#icmp_type NsxvDnat#icmp_type}
        '''
        result = self._values.get("icmp_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxv_dnat#id NsxvDnat#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def logging_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether logging should be enabled for this rule. Default 'false'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxv_dnat#logging_enabled NsxvDnat#logging_enabled}
        '''
        result = self._values.get("logging_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def org(self) -> typing.Optional[builtins.str]:
        '''The name of organization to use, optional if defined at provider level.

        Useful when connected as sysadmin working across different organizations

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxv_dnat#org NsxvDnat#org}
        '''
        result = self._values.get("org")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def original_port(self) -> typing.Optional[builtins.str]:
        '''Original port. This is the destination port for DNAT rules.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxv_dnat#original_port NsxvDnat#original_port}
        '''
        result = self._values.get("original_port")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def protocol(self) -> typing.Optional[builtins.str]:
        '''Protocol. Such as 'tcp', 'udp', 'icmp', 'any'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxv_dnat#protocol NsxvDnat#protocol}
        '''
        result = self._values.get("protocol")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def rule_tag(self) -> typing.Optional[jsii.Number]:
        '''Optional. Allows to set custom rule tag.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxv_dnat#rule_tag NsxvDnat#rule_tag}
        '''
        result = self._values.get("rule_tag")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def rule_type(self) -> typing.Optional[builtins.str]:
        '''Read only. Possible values 'user', 'internal_high'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxv_dnat#rule_type NsxvDnat#rule_type}
        '''
        result = self._values.get("rule_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def translated_address(self) -> typing.Optional[builtins.str]:
        '''Translated address or address range.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxv_dnat#translated_address NsxvDnat#translated_address}
        '''
        result = self._values.get("translated_address")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def translated_port(self) -> typing.Optional[builtins.str]:
        '''Translated port.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxv_dnat#translated_port NsxvDnat#translated_port}
        '''
        result = self._values.get("translated_port")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def vdc(self) -> typing.Optional[builtins.str]:
        '''The name of VDC to use, optional if defined at provider level.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxv_dnat#vdc NsxvDnat#vdc}
        '''
        result = self._values.get("vdc")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NsxvDnatConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "NsxvDnat",
    "NsxvDnatConfig",
]

publication.publish()

def _typecheckingstub__1637e406cd0ea2fdf85b8dc6420e60b1360c4dcd4aec69b8dcac469b2aa78f25(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    edge_gateway: builtins.str,
    network_name: builtins.str,
    network_type: builtins.str,
    original_address: builtins.str,
    description: typing.Optional[builtins.str] = None,
    enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    icmp_type: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    logging_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    org: typing.Optional[builtins.str] = None,
    original_port: typing.Optional[builtins.str] = None,
    protocol: typing.Optional[builtins.str] = None,
    rule_tag: typing.Optional[jsii.Number] = None,
    rule_type: typing.Optional[builtins.str] = None,
    translated_address: typing.Optional[builtins.str] = None,
    translated_port: typing.Optional[builtins.str] = None,
    vdc: typing.Optional[builtins.str] = None,
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

def _typecheckingstub__baf1ef04a8cb2f6c193fc9b49d3787750af47af90e1210e0f373db39327d60bd(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a3c9df4b237b75958ba6b2c53c96e79a5193a12076a461a0a3f30932f1818c3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b8fb97fbb159e1ba6c3bdabfaeeaeef510333d7feeabff461770948b4347047e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__30536d8e5987a62f3fc1b59a8fdb2d055bc651d22b40b56a56d0a0a20d605be2(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__58e538cf79bb6a3380b9e872649d78a1d33b98c46c3d8ad0c0c55cde558a08ba(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1203dfce8ae94164f927cc57dc7c71314c895c562819b741a4db912d0c3f2097(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d6d2d37ae7e0a946129172b68e82f6cd760510a0370f5d5fd078ca8601383363(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__985ea9793b811708e7851233f2aed21166737ab9f0909d5d7d5130c97e8f0761(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a73a27b5623ba22cc79b748c520766cd4a5552ce18d00b3e308e33fa7ef680a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa7b99c1d38484b66240ba96894d74290a81dfc7c97514d30d92c7fbcd075b77(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4eec35a7f44d9b28b7298ce13f9127b99c5270d62b005d7e4a903b3d25d45b39(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e6a7cc37010b9450f65f97218eaea5369d230d0b57c07f69bef37c2af737535(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf77d81f45b0fcc6c8f357368494bf962a065410b6d2ab7be75d8fd9323f4462(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b2ff750ad221de0b11f65660bcff18c113475ff3d443818586f5d803ba59794a(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__975873fc0b99b09f6bf7aa8c573063168b736b94827bf9d85da7aafdbcfed4b4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a29a230868c83e09866e58d643b3abaf0eec1efb7a09fb57be35cda35e89935(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f9c1361f2797033a441c8b0885f694b93320866702b687f9339fef4a2b3f68a0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3aebca3308c178a54c59ca222b455229ac7bed18145ee5ba585b0fbe673ab18d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f178b0a27b9e26c7650c89546fab77d1209a3dc055719c582cdebbd487a53483(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    edge_gateway: builtins.str,
    network_name: builtins.str,
    network_type: builtins.str,
    original_address: builtins.str,
    description: typing.Optional[builtins.str] = None,
    enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    icmp_type: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    logging_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    org: typing.Optional[builtins.str] = None,
    original_port: typing.Optional[builtins.str] = None,
    protocol: typing.Optional[builtins.str] = None,
    rule_tag: typing.Optional[jsii.Number] = None,
    rule_type: typing.Optional[builtins.str] = None,
    translated_address: typing.Optional[builtins.str] = None,
    translated_port: typing.Optional[builtins.str] = None,
    vdc: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
