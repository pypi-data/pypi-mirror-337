'''
# `vcd_nsxt_alb_virtual_service_http_sec_rules`

Refer to the Terraform Registry for docs: [`vcd_nsxt_alb_virtual_service_http_sec_rules`](https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_sec_rules).
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


class NsxtAlbVirtualServiceHttpSecRules(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="vcd.nsxtAlbVirtualServiceHttpSecRules.NsxtAlbVirtualServiceHttpSecRules",
):
    '''Represents a {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_sec_rules vcd_nsxt_alb_virtual_service_http_sec_rules}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        rule: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["NsxtAlbVirtualServiceHttpSecRulesRule", typing.Dict[builtins.str, typing.Any]]]],
        virtual_service_id: builtins.str,
        id: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_sec_rules vcd_nsxt_alb_virtual_service_http_sec_rules} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param rule: rule block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_sec_rules#rule NsxtAlbVirtualServiceHttpSecRules#rule}
        :param virtual_service_id: NSX-T ALB Virtual Service ID. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_sec_rules#virtual_service_id NsxtAlbVirtualServiceHttpSecRules#virtual_service_id}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_sec_rules#id NsxtAlbVirtualServiceHttpSecRules#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e433070dd674840a6424cb2c3d548953a77d5c316679b3c3bbabb662bc02a1ac)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = NsxtAlbVirtualServiceHttpSecRulesConfig(
            rule=rule,
            virtual_service_id=virtual_service_id,
            id=id,
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
        '''Generates CDKTF code for importing a NsxtAlbVirtualServiceHttpSecRules resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the NsxtAlbVirtualServiceHttpSecRules to import.
        :param import_from_id: The id of the existing NsxtAlbVirtualServiceHttpSecRules that should be imported. Refer to the {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_sec_rules#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the NsxtAlbVirtualServiceHttpSecRules to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__99c5663f786ca3db0ce74cf4cb77b85bbb0e00dff6aa0d21029be692d127cfb5)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putRule")
    def put_rule(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["NsxtAlbVirtualServiceHttpSecRulesRule", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b207dd4c6c927a53b678c29a87452700a84e17a08d7149ad5e2cb73757e955ea)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putRule", [value]))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

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
    @jsii.member(jsii_name="rule")
    def rule(self) -> "NsxtAlbVirtualServiceHttpSecRulesRuleList":
        return typing.cast("NsxtAlbVirtualServiceHttpSecRulesRuleList", jsii.get(self, "rule"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="ruleInput")
    def rule_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["NsxtAlbVirtualServiceHttpSecRulesRule"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["NsxtAlbVirtualServiceHttpSecRulesRule"]]], jsii.get(self, "ruleInput"))

    @builtins.property
    @jsii.member(jsii_name="virtualServiceIdInput")
    def virtual_service_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "virtualServiceIdInput"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__163e75597676e4d315cb9bbd184383577fc91a8bb2cd0cf4a7809c42b31068f5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="virtualServiceId")
    def virtual_service_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "virtualServiceId"))

    @virtual_service_id.setter
    def virtual_service_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__403ac3e0de8c03b8d9b2f316c0a5389cb951fe566300a5835816ce7163594617)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "virtualServiceId", value)


@jsii.data_type(
    jsii_type="vcd.nsxtAlbVirtualServiceHttpSecRules.NsxtAlbVirtualServiceHttpSecRulesConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "rule": "rule",
        "virtual_service_id": "virtualServiceId",
        "id": "id",
    },
)
class NsxtAlbVirtualServiceHttpSecRulesConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        rule: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["NsxtAlbVirtualServiceHttpSecRulesRule", typing.Dict[builtins.str, typing.Any]]]],
        virtual_service_id: builtins.str,
        id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param rule: rule block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_sec_rules#rule NsxtAlbVirtualServiceHttpSecRules#rule}
        :param virtual_service_id: NSX-T ALB Virtual Service ID. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_sec_rules#virtual_service_id NsxtAlbVirtualServiceHttpSecRules#virtual_service_id}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_sec_rules#id NsxtAlbVirtualServiceHttpSecRules#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__abedb7a7921a9e596af236f3030be95d874509d79c826f5d925dbb13c6c6958b)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument rule", value=rule, expected_type=type_hints["rule"])
            check_type(argname="argument virtual_service_id", value=virtual_service_id, expected_type=type_hints["virtual_service_id"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "rule": rule,
            "virtual_service_id": virtual_service_id,
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
        if id is not None:
            self._values["id"] = id

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
    def rule(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["NsxtAlbVirtualServiceHttpSecRulesRule"]]:
        '''rule block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_sec_rules#rule NsxtAlbVirtualServiceHttpSecRules#rule}
        '''
        result = self._values.get("rule")
        assert result is not None, "Required property 'rule' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["NsxtAlbVirtualServiceHttpSecRulesRule"]], result)

    @builtins.property
    def virtual_service_id(self) -> builtins.str:
        '''NSX-T ALB Virtual Service ID.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_sec_rules#virtual_service_id NsxtAlbVirtualServiceHttpSecRules#virtual_service_id}
        '''
        result = self._values.get("virtual_service_id")
        assert result is not None, "Required property 'virtual_service_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_sec_rules#id NsxtAlbVirtualServiceHttpSecRules#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NsxtAlbVirtualServiceHttpSecRulesConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="vcd.nsxtAlbVirtualServiceHttpSecRules.NsxtAlbVirtualServiceHttpSecRulesRule",
    jsii_struct_bases=[],
    name_mapping={
        "actions": "actions",
        "match_criteria": "matchCriteria",
        "name": "name",
        "active": "active",
        "logging": "logging",
    },
)
class NsxtAlbVirtualServiceHttpSecRulesRule:
    def __init__(
        self,
        *,
        actions: typing.Union["NsxtAlbVirtualServiceHttpSecRulesRuleActions", typing.Dict[builtins.str, typing.Any]],
        match_criteria: typing.Union["NsxtAlbVirtualServiceHttpSecRulesRuleMatchCriteria", typing.Dict[builtins.str, typing.Any]],
        name: builtins.str,
        active: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        logging: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param actions: actions block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_sec_rules#actions NsxtAlbVirtualServiceHttpSecRules#actions}
        :param match_criteria: match_criteria block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_sec_rules#match_criteria NsxtAlbVirtualServiceHttpSecRules#match_criteria}
        :param name: Name of the rule. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_sec_rules#name NsxtAlbVirtualServiceHttpSecRules#name}
        :param active: Defines is the rule is active or not. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_sec_rules#active NsxtAlbVirtualServiceHttpSecRules#active}
        :param logging: Defines whether to enable logging with headers on rule match or not. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_sec_rules#logging NsxtAlbVirtualServiceHttpSecRules#logging}
        '''
        if isinstance(actions, dict):
            actions = NsxtAlbVirtualServiceHttpSecRulesRuleActions(**actions)
        if isinstance(match_criteria, dict):
            match_criteria = NsxtAlbVirtualServiceHttpSecRulesRuleMatchCriteria(**match_criteria)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__857059954153d35c565dd858dc7f1434108953ab597c60219d45000c0c6daec4)
            check_type(argname="argument actions", value=actions, expected_type=type_hints["actions"])
            check_type(argname="argument match_criteria", value=match_criteria, expected_type=type_hints["match_criteria"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument active", value=active, expected_type=type_hints["active"])
            check_type(argname="argument logging", value=logging, expected_type=type_hints["logging"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "actions": actions,
            "match_criteria": match_criteria,
            "name": name,
        }
        if active is not None:
            self._values["active"] = active
        if logging is not None:
            self._values["logging"] = logging

    @builtins.property
    def actions(self) -> "NsxtAlbVirtualServiceHttpSecRulesRuleActions":
        '''actions block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_sec_rules#actions NsxtAlbVirtualServiceHttpSecRules#actions}
        '''
        result = self._values.get("actions")
        assert result is not None, "Required property 'actions' is missing"
        return typing.cast("NsxtAlbVirtualServiceHttpSecRulesRuleActions", result)

    @builtins.property
    def match_criteria(self) -> "NsxtAlbVirtualServiceHttpSecRulesRuleMatchCriteria":
        '''match_criteria block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_sec_rules#match_criteria NsxtAlbVirtualServiceHttpSecRules#match_criteria}
        '''
        result = self._values.get("match_criteria")
        assert result is not None, "Required property 'match_criteria' is missing"
        return typing.cast("NsxtAlbVirtualServiceHttpSecRulesRuleMatchCriteria", result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Name of the rule.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_sec_rules#name NsxtAlbVirtualServiceHttpSecRules#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def active(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Defines is the rule is active or not.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_sec_rules#active NsxtAlbVirtualServiceHttpSecRules#active}
        '''
        result = self._values.get("active")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def logging(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Defines whether to enable logging with headers on rule match or not.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_sec_rules#logging NsxtAlbVirtualServiceHttpSecRules#logging}
        '''
        result = self._values.get("logging")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NsxtAlbVirtualServiceHttpSecRulesRule(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="vcd.nsxtAlbVirtualServiceHttpSecRules.NsxtAlbVirtualServiceHttpSecRulesRuleActions",
    jsii_struct_bases=[],
    name_mapping={
        "connections": "connections",
        "rate_limit": "rateLimit",
        "redirect_to_https": "redirectToHttps",
        "send_response": "sendResponse",
    },
)
class NsxtAlbVirtualServiceHttpSecRulesRuleActions:
    def __init__(
        self,
        *,
        connections: typing.Optional[builtins.str] = None,
        rate_limit: typing.Optional[typing.Union["NsxtAlbVirtualServiceHttpSecRulesRuleActionsRateLimit", typing.Dict[builtins.str, typing.Any]]] = None,
        redirect_to_https: typing.Optional[builtins.str] = None,
        send_response: typing.Optional[typing.Union["NsxtAlbVirtualServiceHttpSecRulesRuleActionsSendResponse", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connections: ALLOW or CLOSE connections. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_sec_rules#connections NsxtAlbVirtualServiceHttpSecRules#connections}
        :param rate_limit: rate_limit block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_sec_rules#rate_limit NsxtAlbVirtualServiceHttpSecRules#rate_limit}
        :param redirect_to_https: Port number that should be redirected to HTTPS. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_sec_rules#redirect_to_https NsxtAlbVirtualServiceHttpSecRules#redirect_to_https}
        :param send_response: send_response block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_sec_rules#send_response NsxtAlbVirtualServiceHttpSecRules#send_response}
        '''
        if isinstance(rate_limit, dict):
            rate_limit = NsxtAlbVirtualServiceHttpSecRulesRuleActionsRateLimit(**rate_limit)
        if isinstance(send_response, dict):
            send_response = NsxtAlbVirtualServiceHttpSecRulesRuleActionsSendResponse(**send_response)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b6c76c40428a483f5512880a85acc24267d43e72b7997a50589fe99d716228cb)
            check_type(argname="argument connections", value=connections, expected_type=type_hints["connections"])
            check_type(argname="argument rate_limit", value=rate_limit, expected_type=type_hints["rate_limit"])
            check_type(argname="argument redirect_to_https", value=redirect_to_https, expected_type=type_hints["redirect_to_https"])
            check_type(argname="argument send_response", value=send_response, expected_type=type_hints["send_response"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if connections is not None:
            self._values["connections"] = connections
        if rate_limit is not None:
            self._values["rate_limit"] = rate_limit
        if redirect_to_https is not None:
            self._values["redirect_to_https"] = redirect_to_https
        if send_response is not None:
            self._values["send_response"] = send_response

    @builtins.property
    def connections(self) -> typing.Optional[builtins.str]:
        '''ALLOW or CLOSE connections.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_sec_rules#connections NsxtAlbVirtualServiceHttpSecRules#connections}
        '''
        result = self._values.get("connections")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def rate_limit(
        self,
    ) -> typing.Optional["NsxtAlbVirtualServiceHttpSecRulesRuleActionsRateLimit"]:
        '''rate_limit block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_sec_rules#rate_limit NsxtAlbVirtualServiceHttpSecRules#rate_limit}
        '''
        result = self._values.get("rate_limit")
        return typing.cast(typing.Optional["NsxtAlbVirtualServiceHttpSecRulesRuleActionsRateLimit"], result)

    @builtins.property
    def redirect_to_https(self) -> typing.Optional[builtins.str]:
        '''Port number that should be redirected to HTTPS.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_sec_rules#redirect_to_https NsxtAlbVirtualServiceHttpSecRules#redirect_to_https}
        '''
        result = self._values.get("redirect_to_https")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def send_response(
        self,
    ) -> typing.Optional["NsxtAlbVirtualServiceHttpSecRulesRuleActionsSendResponse"]:
        '''send_response block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_sec_rules#send_response NsxtAlbVirtualServiceHttpSecRules#send_response}
        '''
        result = self._values.get("send_response")
        return typing.cast(typing.Optional["NsxtAlbVirtualServiceHttpSecRulesRuleActionsSendResponse"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NsxtAlbVirtualServiceHttpSecRulesRuleActions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class NsxtAlbVirtualServiceHttpSecRulesRuleActionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="vcd.nsxtAlbVirtualServiceHttpSecRules.NsxtAlbVirtualServiceHttpSecRulesRuleActionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7f684252c5625e52e85dc95b6ac474561fa181e13c99fa020becf4a3bb4438f6)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putRateLimit")
    def put_rate_limit(
        self,
        *,
        count: builtins.str,
        period: builtins.str,
        action_close_connection: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        action_local_response: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["NsxtAlbVirtualServiceHttpSecRulesRuleActionsRateLimitActionLocalResponse", typing.Dict[builtins.str, typing.Any]]]]] = None,
        action_redirect: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["NsxtAlbVirtualServiceHttpSecRulesRuleActionsRateLimitActionRedirect", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param count: Maximum number of connections, requests or packets permitted each period. The count must be between 1 and 1000000000. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_sec_rules#count NsxtAlbVirtualServiceHttpSecRules#count}
        :param period: Time value in seconds to enforce rate count. The period must be between 1 and 1000000000. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_sec_rules#period NsxtAlbVirtualServiceHttpSecRules#period}
        :param action_close_connection: Set to true if the connection should be closed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_sec_rules#action_close_connection NsxtAlbVirtualServiceHttpSecRules#action_close_connection}
        :param action_local_response: action_local_response block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_sec_rules#action_local_response NsxtAlbVirtualServiceHttpSecRules#action_local_response}
        :param action_redirect: action_redirect block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_sec_rules#action_redirect NsxtAlbVirtualServiceHttpSecRules#action_redirect}
        '''
        value = NsxtAlbVirtualServiceHttpSecRulesRuleActionsRateLimit(
            count=count,
            period=period,
            action_close_connection=action_close_connection,
            action_local_response=action_local_response,
            action_redirect=action_redirect,
        )

        return typing.cast(None, jsii.invoke(self, "putRateLimit", [value]))

    @jsii.member(jsii_name="putSendResponse")
    def put_send_response(
        self,
        *,
        status_code: builtins.str,
        content: typing.Optional[builtins.str] = None,
        content_type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param status_code: HTTP Status code to send. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_sec_rules#status_code NsxtAlbVirtualServiceHttpSecRules#status_code}
        :param content: Base64 encoded content. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_sec_rules#content NsxtAlbVirtualServiceHttpSecRules#content}
        :param content_type: MIME type for the content. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_sec_rules#content_type NsxtAlbVirtualServiceHttpSecRules#content_type}
        '''
        value = NsxtAlbVirtualServiceHttpSecRulesRuleActionsSendResponse(
            status_code=status_code, content=content, content_type=content_type
        )

        return typing.cast(None, jsii.invoke(self, "putSendResponse", [value]))

    @jsii.member(jsii_name="resetConnections")
    def reset_connections(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetConnections", []))

    @jsii.member(jsii_name="resetRateLimit")
    def reset_rate_limit(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRateLimit", []))

    @jsii.member(jsii_name="resetRedirectToHttps")
    def reset_redirect_to_https(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRedirectToHttps", []))

    @jsii.member(jsii_name="resetSendResponse")
    def reset_send_response(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSendResponse", []))

    @builtins.property
    @jsii.member(jsii_name="rateLimit")
    def rate_limit(
        self,
    ) -> "NsxtAlbVirtualServiceHttpSecRulesRuleActionsRateLimitOutputReference":
        return typing.cast("NsxtAlbVirtualServiceHttpSecRulesRuleActionsRateLimitOutputReference", jsii.get(self, "rateLimit"))

    @builtins.property
    @jsii.member(jsii_name="sendResponse")
    def send_response(
        self,
    ) -> "NsxtAlbVirtualServiceHttpSecRulesRuleActionsSendResponseOutputReference":
        return typing.cast("NsxtAlbVirtualServiceHttpSecRulesRuleActionsSendResponseOutputReference", jsii.get(self, "sendResponse"))

    @builtins.property
    @jsii.member(jsii_name="connectionsInput")
    def connections_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "connectionsInput"))

    @builtins.property
    @jsii.member(jsii_name="rateLimitInput")
    def rate_limit_input(
        self,
    ) -> typing.Optional["NsxtAlbVirtualServiceHttpSecRulesRuleActionsRateLimit"]:
        return typing.cast(typing.Optional["NsxtAlbVirtualServiceHttpSecRulesRuleActionsRateLimit"], jsii.get(self, "rateLimitInput"))

    @builtins.property
    @jsii.member(jsii_name="redirectToHttpsInput")
    def redirect_to_https_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "redirectToHttpsInput"))

    @builtins.property
    @jsii.member(jsii_name="sendResponseInput")
    def send_response_input(
        self,
    ) -> typing.Optional["NsxtAlbVirtualServiceHttpSecRulesRuleActionsSendResponse"]:
        return typing.cast(typing.Optional["NsxtAlbVirtualServiceHttpSecRulesRuleActionsSendResponse"], jsii.get(self, "sendResponseInput"))

    @builtins.property
    @jsii.member(jsii_name="connections")
    def connections(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "connections"))

    @connections.setter
    def connections(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c18673681910559da99fbd0eb894141715b2e619a84497d21e167e4f2172998d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "connections", value)

    @builtins.property
    @jsii.member(jsii_name="redirectToHttps")
    def redirect_to_https(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "redirectToHttps"))

    @redirect_to_https.setter
    def redirect_to_https(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__75c8f7c4e6fdbb9801a01d9d5f670a0ad582fd6c4e7244abd525c07c65769888)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "redirectToHttps", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[NsxtAlbVirtualServiceHttpSecRulesRuleActions]:
        return typing.cast(typing.Optional[NsxtAlbVirtualServiceHttpSecRulesRuleActions], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[NsxtAlbVirtualServiceHttpSecRulesRuleActions],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2566ce9ccf41388c4a8cd59d8d3e15ae1ecbe7b6116b536f198c07e7ae566b99)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="vcd.nsxtAlbVirtualServiceHttpSecRules.NsxtAlbVirtualServiceHttpSecRulesRuleActionsRateLimit",
    jsii_struct_bases=[],
    name_mapping={
        "count": "count",
        "period": "period",
        "action_close_connection": "actionCloseConnection",
        "action_local_response": "actionLocalResponse",
        "action_redirect": "actionRedirect",
    },
)
class NsxtAlbVirtualServiceHttpSecRulesRuleActionsRateLimit:
    def __init__(
        self,
        *,
        count: builtins.str,
        period: builtins.str,
        action_close_connection: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        action_local_response: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["NsxtAlbVirtualServiceHttpSecRulesRuleActionsRateLimitActionLocalResponse", typing.Dict[builtins.str, typing.Any]]]]] = None,
        action_redirect: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["NsxtAlbVirtualServiceHttpSecRulesRuleActionsRateLimitActionRedirect", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param count: Maximum number of connections, requests or packets permitted each period. The count must be between 1 and 1000000000. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_sec_rules#count NsxtAlbVirtualServiceHttpSecRules#count}
        :param period: Time value in seconds to enforce rate count. The period must be between 1 and 1000000000. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_sec_rules#period NsxtAlbVirtualServiceHttpSecRules#period}
        :param action_close_connection: Set to true if the connection should be closed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_sec_rules#action_close_connection NsxtAlbVirtualServiceHttpSecRules#action_close_connection}
        :param action_local_response: action_local_response block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_sec_rules#action_local_response NsxtAlbVirtualServiceHttpSecRules#action_local_response}
        :param action_redirect: action_redirect block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_sec_rules#action_redirect NsxtAlbVirtualServiceHttpSecRules#action_redirect}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__869cdf4bc1012cf96ca03dc23532de8740bc0e6a68ca17905fed720e1901a5e1)
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument period", value=period, expected_type=type_hints["period"])
            check_type(argname="argument action_close_connection", value=action_close_connection, expected_type=type_hints["action_close_connection"])
            check_type(argname="argument action_local_response", value=action_local_response, expected_type=type_hints["action_local_response"])
            check_type(argname="argument action_redirect", value=action_redirect, expected_type=type_hints["action_redirect"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "count": count,
            "period": period,
        }
        if action_close_connection is not None:
            self._values["action_close_connection"] = action_close_connection
        if action_local_response is not None:
            self._values["action_local_response"] = action_local_response
        if action_redirect is not None:
            self._values["action_redirect"] = action_redirect

    @builtins.property
    def count(self) -> builtins.str:
        '''Maximum number of connections, requests or packets permitted each period. The count must be between 1 and 1000000000.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_sec_rules#count NsxtAlbVirtualServiceHttpSecRules#count}
        '''
        result = self._values.get("count")
        assert result is not None, "Required property 'count' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def period(self) -> builtins.str:
        '''Time value in seconds to enforce rate count. The period must be between 1 and 1000000000.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_sec_rules#period NsxtAlbVirtualServiceHttpSecRules#period}
        '''
        result = self._values.get("period")
        assert result is not None, "Required property 'period' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def action_close_connection(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Set to true if the connection should be closed.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_sec_rules#action_close_connection NsxtAlbVirtualServiceHttpSecRules#action_close_connection}
        '''
        result = self._values.get("action_close_connection")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def action_local_response(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["NsxtAlbVirtualServiceHttpSecRulesRuleActionsRateLimitActionLocalResponse"]]]:
        '''action_local_response block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_sec_rules#action_local_response NsxtAlbVirtualServiceHttpSecRules#action_local_response}
        '''
        result = self._values.get("action_local_response")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["NsxtAlbVirtualServiceHttpSecRulesRuleActionsRateLimitActionLocalResponse"]]], result)

    @builtins.property
    def action_redirect(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["NsxtAlbVirtualServiceHttpSecRulesRuleActionsRateLimitActionRedirect"]]]:
        '''action_redirect block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_sec_rules#action_redirect NsxtAlbVirtualServiceHttpSecRules#action_redirect}
        '''
        result = self._values.get("action_redirect")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["NsxtAlbVirtualServiceHttpSecRulesRuleActionsRateLimitActionRedirect"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NsxtAlbVirtualServiceHttpSecRulesRuleActionsRateLimit(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="vcd.nsxtAlbVirtualServiceHttpSecRules.NsxtAlbVirtualServiceHttpSecRulesRuleActionsRateLimitActionLocalResponse",
    jsii_struct_bases=[],
    name_mapping={
        "status_code": "statusCode",
        "content": "content",
        "content_type": "contentType",
    },
)
class NsxtAlbVirtualServiceHttpSecRulesRuleActionsRateLimitActionLocalResponse:
    def __init__(
        self,
        *,
        status_code: builtins.str,
        content: typing.Optional[builtins.str] = None,
        content_type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param status_code: HTTP Status code to send. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_sec_rules#status_code NsxtAlbVirtualServiceHttpSecRules#status_code}
        :param content: Base64 encoded content. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_sec_rules#content NsxtAlbVirtualServiceHttpSecRules#content}
        :param content_type: MIME type for the content. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_sec_rules#content_type NsxtAlbVirtualServiceHttpSecRules#content_type}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__09412c347251f5090cc4e3ec9099d34458017a72988dc0e55c495537021f5a31)
            check_type(argname="argument status_code", value=status_code, expected_type=type_hints["status_code"])
            check_type(argname="argument content", value=content, expected_type=type_hints["content"])
            check_type(argname="argument content_type", value=content_type, expected_type=type_hints["content_type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "status_code": status_code,
        }
        if content is not None:
            self._values["content"] = content
        if content_type is not None:
            self._values["content_type"] = content_type

    @builtins.property
    def status_code(self) -> builtins.str:
        '''HTTP Status code to send.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_sec_rules#status_code NsxtAlbVirtualServiceHttpSecRules#status_code}
        '''
        result = self._values.get("status_code")
        assert result is not None, "Required property 'status_code' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def content(self) -> typing.Optional[builtins.str]:
        '''Base64 encoded content.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_sec_rules#content NsxtAlbVirtualServiceHttpSecRules#content}
        '''
        result = self._values.get("content")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def content_type(self) -> typing.Optional[builtins.str]:
        '''MIME type for the content.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_sec_rules#content_type NsxtAlbVirtualServiceHttpSecRules#content_type}
        '''
        result = self._values.get("content_type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NsxtAlbVirtualServiceHttpSecRulesRuleActionsRateLimitActionLocalResponse(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class NsxtAlbVirtualServiceHttpSecRulesRuleActionsRateLimitActionLocalResponseList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="vcd.nsxtAlbVirtualServiceHttpSecRules.NsxtAlbVirtualServiceHttpSecRulesRuleActionsRateLimitActionLocalResponseList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a4210014dd66a73bfdd96c4fec3d5798199619569c91b5f10de278ef042769c0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "NsxtAlbVirtualServiceHttpSecRulesRuleActionsRateLimitActionLocalResponseOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__53b54749c1b120d286337c2649df8d4a5ae52f786a41cb08f510e295692bc4b4)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("NsxtAlbVirtualServiceHttpSecRulesRuleActionsRateLimitActionLocalResponseOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f11d5ef0f76bcfec6c27a9cffc0eee7ce82dd1540e45c1a43ecc6adb9acd2424)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5cc9f9c677c6835a2f9d35001527266b6e0e9d40775a6668fd1b952a66fc669e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__334f08c4568467256a110530c543fad899836b355d076d871d5047348e4858d0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NsxtAlbVirtualServiceHttpSecRulesRuleActionsRateLimitActionLocalResponse]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NsxtAlbVirtualServiceHttpSecRulesRuleActionsRateLimitActionLocalResponse]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NsxtAlbVirtualServiceHttpSecRulesRuleActionsRateLimitActionLocalResponse]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__88d5903d64f939fab3dfe69d1e382c2b843800e3fe60680ab6859a27548a7586)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class NsxtAlbVirtualServiceHttpSecRulesRuleActionsRateLimitActionLocalResponseOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="vcd.nsxtAlbVirtualServiceHttpSecRules.NsxtAlbVirtualServiceHttpSecRulesRuleActionsRateLimitActionLocalResponseOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__847284bcf5d506e72ce7fd81ad62f72d5b0ea091ad45fd8d1c2dddc56413956d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetContent")
    def reset_content(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetContent", []))

    @jsii.member(jsii_name="resetContentType")
    def reset_content_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetContentType", []))

    @builtins.property
    @jsii.member(jsii_name="contentInput")
    def content_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "contentInput"))

    @builtins.property
    @jsii.member(jsii_name="contentTypeInput")
    def content_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "contentTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="statusCodeInput")
    def status_code_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "statusCodeInput"))

    @builtins.property
    @jsii.member(jsii_name="content")
    def content(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "content"))

    @content.setter
    def content(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__20701755e81a83e2dea95da81cb0d5ca7e76d338a591c26735bdd351c59905ae)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "content", value)

    @builtins.property
    @jsii.member(jsii_name="contentType")
    def content_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "contentType"))

    @content_type.setter
    def content_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9c41fcd31f62934287bb14436ba48b9aeb3c7bd31aefe55d8a189d9ce158373d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "contentType", value)

    @builtins.property
    @jsii.member(jsii_name="statusCode")
    def status_code(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "statusCode"))

    @status_code.setter
    def status_code(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__61d23d3d499bfc969caec8f3a51f2eb08417ca3de758c9dbc0ca4a216366e5d2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "statusCode", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NsxtAlbVirtualServiceHttpSecRulesRuleActionsRateLimitActionLocalResponse]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NsxtAlbVirtualServiceHttpSecRulesRuleActionsRateLimitActionLocalResponse]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NsxtAlbVirtualServiceHttpSecRulesRuleActionsRateLimitActionLocalResponse]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__12a74034d026ae7dc313939da45417f5d4ebd5bb37f791d99dc96f796f230500)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="vcd.nsxtAlbVirtualServiceHttpSecRules.NsxtAlbVirtualServiceHttpSecRulesRuleActionsRateLimitActionRedirect",
    jsii_struct_bases=[],
    name_mapping={
        "port": "port",
        "protocol": "protocol",
        "status_code": "statusCode",
        "host": "host",
        "keep_query": "keepQuery",
        "path": "path",
    },
)
class NsxtAlbVirtualServiceHttpSecRulesRuleActionsRateLimitActionRedirect:
    def __init__(
        self,
        *,
        port: builtins.str,
        protocol: builtins.str,
        status_code: jsii.Number,
        host: typing.Optional[builtins.str] = None,
        keep_query: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        path: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param port: Port to which redirect the request. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_sec_rules#port NsxtAlbVirtualServiceHttpSecRules#port}
        :param protocol: HTTP or HTTPS protocol. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_sec_rules#protocol NsxtAlbVirtualServiceHttpSecRules#protocol}
        :param status_code: One of the redirect status codes - 301, 302, 307. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_sec_rules#status_code NsxtAlbVirtualServiceHttpSecRules#status_code}
        :param host: Host to which redirect the request. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_sec_rules#host NsxtAlbVirtualServiceHttpSecRules#host}
        :param keep_query: Should the query part be preserved. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_sec_rules#keep_query NsxtAlbVirtualServiceHttpSecRules#keep_query}
        :param path: Path to which redirect the request. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_sec_rules#path NsxtAlbVirtualServiceHttpSecRules#path}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fd0a7f7590953eca19a05e80d5039f579fef62c96731a65f0a64aff41e507863)
            check_type(argname="argument port", value=port, expected_type=type_hints["port"])
            check_type(argname="argument protocol", value=protocol, expected_type=type_hints["protocol"])
            check_type(argname="argument status_code", value=status_code, expected_type=type_hints["status_code"])
            check_type(argname="argument host", value=host, expected_type=type_hints["host"])
            check_type(argname="argument keep_query", value=keep_query, expected_type=type_hints["keep_query"])
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "port": port,
            "protocol": protocol,
            "status_code": status_code,
        }
        if host is not None:
            self._values["host"] = host
        if keep_query is not None:
            self._values["keep_query"] = keep_query
        if path is not None:
            self._values["path"] = path

    @builtins.property
    def port(self) -> builtins.str:
        '''Port to which redirect the request.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_sec_rules#port NsxtAlbVirtualServiceHttpSecRules#port}
        '''
        result = self._values.get("port")
        assert result is not None, "Required property 'port' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def protocol(self) -> builtins.str:
        '''HTTP or HTTPS protocol.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_sec_rules#protocol NsxtAlbVirtualServiceHttpSecRules#protocol}
        '''
        result = self._values.get("protocol")
        assert result is not None, "Required property 'protocol' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def status_code(self) -> jsii.Number:
        '''One of the redirect status codes - 301, 302, 307.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_sec_rules#status_code NsxtAlbVirtualServiceHttpSecRules#status_code}
        '''
        result = self._values.get("status_code")
        assert result is not None, "Required property 'status_code' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def host(self) -> typing.Optional[builtins.str]:
        '''Host to which redirect the request.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_sec_rules#host NsxtAlbVirtualServiceHttpSecRules#host}
        '''
        result = self._values.get("host")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def keep_query(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Should the query part be preserved.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_sec_rules#keep_query NsxtAlbVirtualServiceHttpSecRules#keep_query}
        '''
        result = self._values.get("keep_query")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def path(self) -> typing.Optional[builtins.str]:
        '''Path to which redirect the request.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_sec_rules#path NsxtAlbVirtualServiceHttpSecRules#path}
        '''
        result = self._values.get("path")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NsxtAlbVirtualServiceHttpSecRulesRuleActionsRateLimitActionRedirect(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class NsxtAlbVirtualServiceHttpSecRulesRuleActionsRateLimitActionRedirectList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="vcd.nsxtAlbVirtualServiceHttpSecRules.NsxtAlbVirtualServiceHttpSecRulesRuleActionsRateLimitActionRedirectList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ba11fdc95570937518c5e56bfc610209ac0a35fd7e1c31dc2f6fa4ebc9d73a91)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "NsxtAlbVirtualServiceHttpSecRulesRuleActionsRateLimitActionRedirectOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c028d6daec46c1cbf3aed566b77203d7c94470d05870bde5ec6ae4806a8e7024)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("NsxtAlbVirtualServiceHttpSecRulesRuleActionsRateLimitActionRedirectOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7adf91d885156830a9136b681a63f64c7a0edaa849d96f41a2850b76b0c6f098)
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
            type_hints = typing.get_type_hints(_typecheckingstub__77faa585f1bac54be540096ff3e7b3d2d89c0a1a56296a183f08f4f0744249cb)
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
            type_hints = typing.get_type_hints(_typecheckingstub__13e20531a8fd2f8b96f8cec502a1ebd6e0d3746223b25d6a795b0e7cb3f60398)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NsxtAlbVirtualServiceHttpSecRulesRuleActionsRateLimitActionRedirect]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NsxtAlbVirtualServiceHttpSecRulesRuleActionsRateLimitActionRedirect]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NsxtAlbVirtualServiceHttpSecRulesRuleActionsRateLimitActionRedirect]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__75a5c046edc8b044ba5b6a07d8b9c67d113dae86c1e7c42644989f130dd167f3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class NsxtAlbVirtualServiceHttpSecRulesRuleActionsRateLimitActionRedirectOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="vcd.nsxtAlbVirtualServiceHttpSecRules.NsxtAlbVirtualServiceHttpSecRulesRuleActionsRateLimitActionRedirectOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f5f717eaf39761c9d3bf0401939298fd4d4a734da8554b79d6dbec8950de918c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetHost")
    def reset_host(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHost", []))

    @jsii.member(jsii_name="resetKeepQuery")
    def reset_keep_query(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKeepQuery", []))

    @jsii.member(jsii_name="resetPath")
    def reset_path(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPath", []))

    @builtins.property
    @jsii.member(jsii_name="hostInput")
    def host_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "hostInput"))

    @builtins.property
    @jsii.member(jsii_name="keepQueryInput")
    def keep_query_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "keepQueryInput"))

    @builtins.property
    @jsii.member(jsii_name="pathInput")
    def path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "pathInput"))

    @builtins.property
    @jsii.member(jsii_name="portInput")
    def port_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "portInput"))

    @builtins.property
    @jsii.member(jsii_name="protocolInput")
    def protocol_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "protocolInput"))

    @builtins.property
    @jsii.member(jsii_name="statusCodeInput")
    def status_code_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "statusCodeInput"))

    @builtins.property
    @jsii.member(jsii_name="host")
    def host(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "host"))

    @host.setter
    def host(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b1957c16464262ead3e67b88d557defe1036dbb8e5a6e9be7d8973bf91c1c800)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "host", value)

    @builtins.property
    @jsii.member(jsii_name="keepQuery")
    def keep_query(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "keepQuery"))

    @keep_query.setter
    def keep_query(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f8f16ee00febee8932b0d0d3f0e40b316ea78c1ca3c41d8a0ed6f0ab17f83ffd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "keepQuery", value)

    @builtins.property
    @jsii.member(jsii_name="path")
    def path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "path"))

    @path.setter
    def path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__29137db88bdddf598b37459bde2ee9a30ae900f71cbd46ee735d3c578d50c099)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "path", value)

    @builtins.property
    @jsii.member(jsii_name="port")
    def port(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "port"))

    @port.setter
    def port(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__94d169d69c39fc6e8fc6d53bef3f2fc9a67a053699700abe821ed5e1eb5b1bd5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "port", value)

    @builtins.property
    @jsii.member(jsii_name="protocol")
    def protocol(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "protocol"))

    @protocol.setter
    def protocol(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6dc0bf2cb7bb15ab5abbddd85e89ae6355c15d9690c25c18e73235625023fdbb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "protocol", value)

    @builtins.property
    @jsii.member(jsii_name="statusCode")
    def status_code(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "statusCode"))

    @status_code.setter
    def status_code(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__23e22e8f1b850b12f800c3d99ea8ed19ef80575aae9834e79b52e48c86383b61)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "statusCode", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NsxtAlbVirtualServiceHttpSecRulesRuleActionsRateLimitActionRedirect]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NsxtAlbVirtualServiceHttpSecRulesRuleActionsRateLimitActionRedirect]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NsxtAlbVirtualServiceHttpSecRulesRuleActionsRateLimitActionRedirect]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2231a71f8901ef9b07dac4beab4496c04e4faf3ab06cc5fee98553a60dd34bbb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class NsxtAlbVirtualServiceHttpSecRulesRuleActionsRateLimitOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="vcd.nsxtAlbVirtualServiceHttpSecRules.NsxtAlbVirtualServiceHttpSecRulesRuleActionsRateLimitOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fe98732cf95eac03a011f38a3c76ca9fe372ab8ad5742b1523295e1f42ddd21f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putActionLocalResponse")
    def put_action_local_response(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[NsxtAlbVirtualServiceHttpSecRulesRuleActionsRateLimitActionLocalResponse, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c03f2024a028ca369c0bbb7eeb573bec66e86fbc538af7f23e3d844ad8f61b6b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putActionLocalResponse", [value]))

    @jsii.member(jsii_name="putActionRedirect")
    def put_action_redirect(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[NsxtAlbVirtualServiceHttpSecRulesRuleActionsRateLimitActionRedirect, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2c22f85c63ffc6bfd3d99809b57cbc7536fd8dd18b1e08b710d6320f7046168f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putActionRedirect", [value]))

    @jsii.member(jsii_name="resetActionCloseConnection")
    def reset_action_close_connection(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetActionCloseConnection", []))

    @jsii.member(jsii_name="resetActionLocalResponse")
    def reset_action_local_response(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetActionLocalResponse", []))

    @jsii.member(jsii_name="resetActionRedirect")
    def reset_action_redirect(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetActionRedirect", []))

    @builtins.property
    @jsii.member(jsii_name="actionLocalResponse")
    def action_local_response(
        self,
    ) -> NsxtAlbVirtualServiceHttpSecRulesRuleActionsRateLimitActionLocalResponseList:
        return typing.cast(NsxtAlbVirtualServiceHttpSecRulesRuleActionsRateLimitActionLocalResponseList, jsii.get(self, "actionLocalResponse"))

    @builtins.property
    @jsii.member(jsii_name="actionRedirect")
    def action_redirect(
        self,
    ) -> NsxtAlbVirtualServiceHttpSecRulesRuleActionsRateLimitActionRedirectList:
        return typing.cast(NsxtAlbVirtualServiceHttpSecRulesRuleActionsRateLimitActionRedirectList, jsii.get(self, "actionRedirect"))

    @builtins.property
    @jsii.member(jsii_name="actionCloseConnectionInput")
    def action_close_connection_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "actionCloseConnectionInput"))

    @builtins.property
    @jsii.member(jsii_name="actionLocalResponseInput")
    def action_local_response_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NsxtAlbVirtualServiceHttpSecRulesRuleActionsRateLimitActionLocalResponse]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NsxtAlbVirtualServiceHttpSecRulesRuleActionsRateLimitActionLocalResponse]]], jsii.get(self, "actionLocalResponseInput"))

    @builtins.property
    @jsii.member(jsii_name="actionRedirectInput")
    def action_redirect_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NsxtAlbVirtualServiceHttpSecRulesRuleActionsRateLimitActionRedirect]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NsxtAlbVirtualServiceHttpSecRulesRuleActionsRateLimitActionRedirect]]], jsii.get(self, "actionRedirectInput"))

    @builtins.property
    @jsii.member(jsii_name="countInput")
    def count_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "countInput"))

    @builtins.property
    @jsii.member(jsii_name="periodInput")
    def period_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "periodInput"))

    @builtins.property
    @jsii.member(jsii_name="actionCloseConnection")
    def action_close_connection(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "actionCloseConnection"))

    @action_close_connection.setter
    def action_close_connection(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c0de60ced93281d54adae7c1696b581605d1c69321fa75f90b1e9e7a4bce4cff)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "actionCloseConnection", value)

    @builtins.property
    @jsii.member(jsii_name="count")
    def count(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "count"))

    @count.setter
    def count(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__49088cbb08054b914819edc1453255f6e2767adbcc205e3406d22f02a7442c68)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "count", value)

    @builtins.property
    @jsii.member(jsii_name="period")
    def period(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "period"))

    @period.setter
    def period(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2894b077fb32c6c3a4de7e42cc7820842274c8542ee1783eb6d8d85f57b01550)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "period", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[NsxtAlbVirtualServiceHttpSecRulesRuleActionsRateLimit]:
        return typing.cast(typing.Optional[NsxtAlbVirtualServiceHttpSecRulesRuleActionsRateLimit], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[NsxtAlbVirtualServiceHttpSecRulesRuleActionsRateLimit],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2dfc07a07e4ee3441f96296ff1e721346d43175da37c438c9ca44b197bf80038)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="vcd.nsxtAlbVirtualServiceHttpSecRules.NsxtAlbVirtualServiceHttpSecRulesRuleActionsSendResponse",
    jsii_struct_bases=[],
    name_mapping={
        "status_code": "statusCode",
        "content": "content",
        "content_type": "contentType",
    },
)
class NsxtAlbVirtualServiceHttpSecRulesRuleActionsSendResponse:
    def __init__(
        self,
        *,
        status_code: builtins.str,
        content: typing.Optional[builtins.str] = None,
        content_type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param status_code: HTTP Status code to send. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_sec_rules#status_code NsxtAlbVirtualServiceHttpSecRules#status_code}
        :param content: Base64 encoded content. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_sec_rules#content NsxtAlbVirtualServiceHttpSecRules#content}
        :param content_type: MIME type for the content. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_sec_rules#content_type NsxtAlbVirtualServiceHttpSecRules#content_type}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f98af7ea098ba2196e33e9e5da21f213dd351f89415b450ff20edda806970129)
            check_type(argname="argument status_code", value=status_code, expected_type=type_hints["status_code"])
            check_type(argname="argument content", value=content, expected_type=type_hints["content"])
            check_type(argname="argument content_type", value=content_type, expected_type=type_hints["content_type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "status_code": status_code,
        }
        if content is not None:
            self._values["content"] = content
        if content_type is not None:
            self._values["content_type"] = content_type

    @builtins.property
    def status_code(self) -> builtins.str:
        '''HTTP Status code to send.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_sec_rules#status_code NsxtAlbVirtualServiceHttpSecRules#status_code}
        '''
        result = self._values.get("status_code")
        assert result is not None, "Required property 'status_code' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def content(self) -> typing.Optional[builtins.str]:
        '''Base64 encoded content.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_sec_rules#content NsxtAlbVirtualServiceHttpSecRules#content}
        '''
        result = self._values.get("content")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def content_type(self) -> typing.Optional[builtins.str]:
        '''MIME type for the content.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_sec_rules#content_type NsxtAlbVirtualServiceHttpSecRules#content_type}
        '''
        result = self._values.get("content_type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NsxtAlbVirtualServiceHttpSecRulesRuleActionsSendResponse(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class NsxtAlbVirtualServiceHttpSecRulesRuleActionsSendResponseOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="vcd.nsxtAlbVirtualServiceHttpSecRules.NsxtAlbVirtualServiceHttpSecRulesRuleActionsSendResponseOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__661fb632b172ff8a0802bb389531964145a399d8312ae883e382167604da263c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetContent")
    def reset_content(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetContent", []))

    @jsii.member(jsii_name="resetContentType")
    def reset_content_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetContentType", []))

    @builtins.property
    @jsii.member(jsii_name="contentInput")
    def content_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "contentInput"))

    @builtins.property
    @jsii.member(jsii_name="contentTypeInput")
    def content_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "contentTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="statusCodeInput")
    def status_code_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "statusCodeInput"))

    @builtins.property
    @jsii.member(jsii_name="content")
    def content(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "content"))

    @content.setter
    def content(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__75a9256aff44e852f0254e06194e9a910adc00b3d8b03d1b1a6ede7fb2b2a9b2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "content", value)

    @builtins.property
    @jsii.member(jsii_name="contentType")
    def content_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "contentType"))

    @content_type.setter
    def content_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__42f01a72f1aca2fd7c0c34676cb31409e6aba4123842f703028f2d23493b8664)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "contentType", value)

    @builtins.property
    @jsii.member(jsii_name="statusCode")
    def status_code(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "statusCode"))

    @status_code.setter
    def status_code(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fc993087c504e9cbd703506c614b2adecaf378e1f70307c71ea7431e9039834e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "statusCode", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[NsxtAlbVirtualServiceHttpSecRulesRuleActionsSendResponse]:
        return typing.cast(typing.Optional[NsxtAlbVirtualServiceHttpSecRulesRuleActionsSendResponse], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[NsxtAlbVirtualServiceHttpSecRulesRuleActionsSendResponse],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__97010067091520996c67de898f7817a88b194bec0dd39b3fb3367ae5beda17f6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class NsxtAlbVirtualServiceHttpSecRulesRuleList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="vcd.nsxtAlbVirtualServiceHttpSecRules.NsxtAlbVirtualServiceHttpSecRulesRuleList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7177924571197631a3b72835f6044b0fb46dc65704bf9d613bab583f8684ba8a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "NsxtAlbVirtualServiceHttpSecRulesRuleOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__53dfec606d249f6879293f1aa72730bc4696ef4922f142b5a3d93f68550e6df5)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("NsxtAlbVirtualServiceHttpSecRulesRuleOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0647d6e97b7cb9c35fac47f556f90b5e1538981f31a9d0c11ed25714f6f1b256)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2ea9f9b3a18f52c9616db1f2ba12573b5e08884761a2b11eb56395504942d800)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e7c3046ffe82b8419f36c8c00065e4a264586bb598933e106b97e0df031b1641)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NsxtAlbVirtualServiceHttpSecRulesRule]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NsxtAlbVirtualServiceHttpSecRulesRule]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NsxtAlbVirtualServiceHttpSecRulesRule]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4e62cd90fcb6424c8739e11490f44e8d13cb93fd86fc27220cd36b1469abe323)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="vcd.nsxtAlbVirtualServiceHttpSecRules.NsxtAlbVirtualServiceHttpSecRulesRuleMatchCriteria",
    jsii_struct_bases=[],
    name_mapping={
        "client_ip_address": "clientIpAddress",
        "cookie": "cookie",
        "http_methods": "httpMethods",
        "path": "path",
        "protocol_type": "protocolType",
        "query": "query",
        "request_headers": "requestHeaders",
        "service_ports": "servicePorts",
    },
)
class NsxtAlbVirtualServiceHttpSecRulesRuleMatchCriteria:
    def __init__(
        self,
        *,
        client_ip_address: typing.Optional[typing.Union["NsxtAlbVirtualServiceHttpSecRulesRuleMatchCriteriaClientIpAddress", typing.Dict[builtins.str, typing.Any]]] = None,
        cookie: typing.Optional[typing.Union["NsxtAlbVirtualServiceHttpSecRulesRuleMatchCriteriaCookie", typing.Dict[builtins.str, typing.Any]]] = None,
        http_methods: typing.Optional[typing.Union["NsxtAlbVirtualServiceHttpSecRulesRuleMatchCriteriaHttpMethods", typing.Dict[builtins.str, typing.Any]]] = None,
        path: typing.Optional[typing.Union["NsxtAlbVirtualServiceHttpSecRulesRuleMatchCriteriaPath", typing.Dict[builtins.str, typing.Any]]] = None,
        protocol_type: typing.Optional[builtins.str] = None,
        query: typing.Optional[typing.Sequence[builtins.str]] = None,
        request_headers: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["NsxtAlbVirtualServiceHttpSecRulesRuleMatchCriteriaRequestHeaders", typing.Dict[builtins.str, typing.Any]]]]] = None,
        service_ports: typing.Optional[typing.Union["NsxtAlbVirtualServiceHttpSecRulesRuleMatchCriteriaServicePorts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param client_ip_address: client_ip_address block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_sec_rules#client_ip_address NsxtAlbVirtualServiceHttpSecRules#client_ip_address}
        :param cookie: cookie block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_sec_rules#cookie NsxtAlbVirtualServiceHttpSecRules#cookie}
        :param http_methods: http_methods block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_sec_rules#http_methods NsxtAlbVirtualServiceHttpSecRules#http_methods}
        :param path: path block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_sec_rules#path NsxtAlbVirtualServiceHttpSecRules#path}
        :param protocol_type: Protocol to match - 'HTTP' or 'HTTPS'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_sec_rules#protocol_type NsxtAlbVirtualServiceHttpSecRules#protocol_type}
        :param query: HTTP request query strings to match. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_sec_rules#query NsxtAlbVirtualServiceHttpSecRules#query}
        :param request_headers: request_headers block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_sec_rules#request_headers NsxtAlbVirtualServiceHttpSecRules#request_headers}
        :param service_ports: service_ports block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_sec_rules#service_ports NsxtAlbVirtualServiceHttpSecRules#service_ports}
        '''
        if isinstance(client_ip_address, dict):
            client_ip_address = NsxtAlbVirtualServiceHttpSecRulesRuleMatchCriteriaClientIpAddress(**client_ip_address)
        if isinstance(cookie, dict):
            cookie = NsxtAlbVirtualServiceHttpSecRulesRuleMatchCriteriaCookie(**cookie)
        if isinstance(http_methods, dict):
            http_methods = NsxtAlbVirtualServiceHttpSecRulesRuleMatchCriteriaHttpMethods(**http_methods)
        if isinstance(path, dict):
            path = NsxtAlbVirtualServiceHttpSecRulesRuleMatchCriteriaPath(**path)
        if isinstance(service_ports, dict):
            service_ports = NsxtAlbVirtualServiceHttpSecRulesRuleMatchCriteriaServicePorts(**service_ports)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1fe1075398b0f4eb48e2fea0328e28e92ad6ee6229055c798bce5fcca7efb252)
            check_type(argname="argument client_ip_address", value=client_ip_address, expected_type=type_hints["client_ip_address"])
            check_type(argname="argument cookie", value=cookie, expected_type=type_hints["cookie"])
            check_type(argname="argument http_methods", value=http_methods, expected_type=type_hints["http_methods"])
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
            check_type(argname="argument protocol_type", value=protocol_type, expected_type=type_hints["protocol_type"])
            check_type(argname="argument query", value=query, expected_type=type_hints["query"])
            check_type(argname="argument request_headers", value=request_headers, expected_type=type_hints["request_headers"])
            check_type(argname="argument service_ports", value=service_ports, expected_type=type_hints["service_ports"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if client_ip_address is not None:
            self._values["client_ip_address"] = client_ip_address
        if cookie is not None:
            self._values["cookie"] = cookie
        if http_methods is not None:
            self._values["http_methods"] = http_methods
        if path is not None:
            self._values["path"] = path
        if protocol_type is not None:
            self._values["protocol_type"] = protocol_type
        if query is not None:
            self._values["query"] = query
        if request_headers is not None:
            self._values["request_headers"] = request_headers
        if service_ports is not None:
            self._values["service_ports"] = service_ports

    @builtins.property
    def client_ip_address(
        self,
    ) -> typing.Optional["NsxtAlbVirtualServiceHttpSecRulesRuleMatchCriteriaClientIpAddress"]:
        '''client_ip_address block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_sec_rules#client_ip_address NsxtAlbVirtualServiceHttpSecRules#client_ip_address}
        '''
        result = self._values.get("client_ip_address")
        return typing.cast(typing.Optional["NsxtAlbVirtualServiceHttpSecRulesRuleMatchCriteriaClientIpAddress"], result)

    @builtins.property
    def cookie(
        self,
    ) -> typing.Optional["NsxtAlbVirtualServiceHttpSecRulesRuleMatchCriteriaCookie"]:
        '''cookie block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_sec_rules#cookie NsxtAlbVirtualServiceHttpSecRules#cookie}
        '''
        result = self._values.get("cookie")
        return typing.cast(typing.Optional["NsxtAlbVirtualServiceHttpSecRulesRuleMatchCriteriaCookie"], result)

    @builtins.property
    def http_methods(
        self,
    ) -> typing.Optional["NsxtAlbVirtualServiceHttpSecRulesRuleMatchCriteriaHttpMethods"]:
        '''http_methods block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_sec_rules#http_methods NsxtAlbVirtualServiceHttpSecRules#http_methods}
        '''
        result = self._values.get("http_methods")
        return typing.cast(typing.Optional["NsxtAlbVirtualServiceHttpSecRulesRuleMatchCriteriaHttpMethods"], result)

    @builtins.property
    def path(
        self,
    ) -> typing.Optional["NsxtAlbVirtualServiceHttpSecRulesRuleMatchCriteriaPath"]:
        '''path block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_sec_rules#path NsxtAlbVirtualServiceHttpSecRules#path}
        '''
        result = self._values.get("path")
        return typing.cast(typing.Optional["NsxtAlbVirtualServiceHttpSecRulesRuleMatchCriteriaPath"], result)

    @builtins.property
    def protocol_type(self) -> typing.Optional[builtins.str]:
        '''Protocol to match - 'HTTP' or 'HTTPS'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_sec_rules#protocol_type NsxtAlbVirtualServiceHttpSecRules#protocol_type}
        '''
        result = self._values.get("protocol_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def query(self) -> typing.Optional[typing.List[builtins.str]]:
        '''HTTP request query strings to match.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_sec_rules#query NsxtAlbVirtualServiceHttpSecRules#query}
        '''
        result = self._values.get("query")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def request_headers(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["NsxtAlbVirtualServiceHttpSecRulesRuleMatchCriteriaRequestHeaders"]]]:
        '''request_headers block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_sec_rules#request_headers NsxtAlbVirtualServiceHttpSecRules#request_headers}
        '''
        result = self._values.get("request_headers")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["NsxtAlbVirtualServiceHttpSecRulesRuleMatchCriteriaRequestHeaders"]]], result)

    @builtins.property
    def service_ports(
        self,
    ) -> typing.Optional["NsxtAlbVirtualServiceHttpSecRulesRuleMatchCriteriaServicePorts"]:
        '''service_ports block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_sec_rules#service_ports NsxtAlbVirtualServiceHttpSecRules#service_ports}
        '''
        result = self._values.get("service_ports")
        return typing.cast(typing.Optional["NsxtAlbVirtualServiceHttpSecRulesRuleMatchCriteriaServicePorts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NsxtAlbVirtualServiceHttpSecRulesRuleMatchCriteria(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="vcd.nsxtAlbVirtualServiceHttpSecRules.NsxtAlbVirtualServiceHttpSecRulesRuleMatchCriteriaClientIpAddress",
    jsii_struct_bases=[],
    name_mapping={"criteria": "criteria", "ip_addresses": "ipAddresses"},
)
class NsxtAlbVirtualServiceHttpSecRulesRuleMatchCriteriaClientIpAddress:
    def __init__(
        self,
        *,
        criteria: builtins.str,
        ip_addresses: typing.Sequence[builtins.str],
    ) -> None:
        '''
        :param criteria: Criteria to use for IP address matching the HTTP request. Options - IS_IN, IS_NOT_IN. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_sec_rules#criteria NsxtAlbVirtualServiceHttpSecRules#criteria}
        :param ip_addresses: A set of IP addresses. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_sec_rules#ip_addresses NsxtAlbVirtualServiceHttpSecRules#ip_addresses}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bf73a05b89d6e6e16b9a533205d53eff6bb060ce76f0e3ce8913e5a43c68142d)
            check_type(argname="argument criteria", value=criteria, expected_type=type_hints["criteria"])
            check_type(argname="argument ip_addresses", value=ip_addresses, expected_type=type_hints["ip_addresses"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "criteria": criteria,
            "ip_addresses": ip_addresses,
        }

    @builtins.property
    def criteria(self) -> builtins.str:
        '''Criteria to use for IP address matching the HTTP request. Options - IS_IN, IS_NOT_IN.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_sec_rules#criteria NsxtAlbVirtualServiceHttpSecRules#criteria}
        '''
        result = self._values.get("criteria")
        assert result is not None, "Required property 'criteria' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def ip_addresses(self) -> typing.List[builtins.str]:
        '''A set of IP addresses.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_sec_rules#ip_addresses NsxtAlbVirtualServiceHttpSecRules#ip_addresses}
        '''
        result = self._values.get("ip_addresses")
        assert result is not None, "Required property 'ip_addresses' is missing"
        return typing.cast(typing.List[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NsxtAlbVirtualServiceHttpSecRulesRuleMatchCriteriaClientIpAddress(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class NsxtAlbVirtualServiceHttpSecRulesRuleMatchCriteriaClientIpAddressOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="vcd.nsxtAlbVirtualServiceHttpSecRules.NsxtAlbVirtualServiceHttpSecRulesRuleMatchCriteriaClientIpAddressOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__cefc4e71d6a1ffc777e6f1a8b3c8813c560f27849e0b0fa9385eec807efac432)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="criteriaInput")
    def criteria_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "criteriaInput"))

    @builtins.property
    @jsii.member(jsii_name="ipAddressesInput")
    def ip_addresses_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "ipAddressesInput"))

    @builtins.property
    @jsii.member(jsii_name="criteria")
    def criteria(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "criteria"))

    @criteria.setter
    def criteria(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__130ddc47465ea2915f43635443e74870a41515137a8ca80305aaf955c1633f93)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "criteria", value)

    @builtins.property
    @jsii.member(jsii_name="ipAddresses")
    def ip_addresses(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "ipAddresses"))

    @ip_addresses.setter
    def ip_addresses(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b75ec3df4936b825fd130ad7d961ee14cb4a8eee5339606c54334621907a880a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ipAddresses", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[NsxtAlbVirtualServiceHttpSecRulesRuleMatchCriteriaClientIpAddress]:
        return typing.cast(typing.Optional[NsxtAlbVirtualServiceHttpSecRulesRuleMatchCriteriaClientIpAddress], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[NsxtAlbVirtualServiceHttpSecRulesRuleMatchCriteriaClientIpAddress],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__34a6a83a997c989f4f27dd8afd17f97e2cc13a1af354222941accab01579173a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="vcd.nsxtAlbVirtualServiceHttpSecRules.NsxtAlbVirtualServiceHttpSecRulesRuleMatchCriteriaCookie",
    jsii_struct_bases=[],
    name_mapping={"criteria": "criteria", "name": "name", "value": "value"},
)
class NsxtAlbVirtualServiceHttpSecRulesRuleMatchCriteriaCookie:
    def __init__(
        self,
        *,
        criteria: builtins.str,
        name: builtins.str,
        value: builtins.str,
    ) -> None:
        '''
        :param criteria: Criteria to use for matching cookies in the HTTP request. Options - EXISTS, DOES_NOT_EXIST, BEGINS_WITH, DOES_NOT_BEGIN_WITH, CONTAINS, DOES_NOT_CONTAIN, ENDS_WITH, DOES_NOT_END_WITH, EQUALS, DOES_NOT_EQUAL Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_sec_rules#criteria NsxtAlbVirtualServiceHttpSecRules#criteria}
        :param name: Name of the HTTP cookie whose value is to be matched. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_sec_rules#name NsxtAlbVirtualServiceHttpSecRules#name}
        :param value: String values to match for an HTTP cookie. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_sec_rules#value NsxtAlbVirtualServiceHttpSecRules#value}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f6e47ede8048cab1058fe7b34c31ed7c6d9cccf6e70bfde127662eedebbcf7bf)
            check_type(argname="argument criteria", value=criteria, expected_type=type_hints["criteria"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "criteria": criteria,
            "name": name,
            "value": value,
        }

    @builtins.property
    def criteria(self) -> builtins.str:
        '''Criteria to use for matching cookies in the HTTP request.

        Options - EXISTS, DOES_NOT_EXIST, BEGINS_WITH, DOES_NOT_BEGIN_WITH, CONTAINS, DOES_NOT_CONTAIN, ENDS_WITH, DOES_NOT_END_WITH, EQUALS, DOES_NOT_EQUAL

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_sec_rules#criteria NsxtAlbVirtualServiceHttpSecRules#criteria}
        '''
        result = self._values.get("criteria")
        assert result is not None, "Required property 'criteria' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Name of the HTTP cookie whose value is to be matched.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_sec_rules#name NsxtAlbVirtualServiceHttpSecRules#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> builtins.str:
        '''String values to match for an HTTP cookie.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_sec_rules#value NsxtAlbVirtualServiceHttpSecRules#value}
        '''
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NsxtAlbVirtualServiceHttpSecRulesRuleMatchCriteriaCookie(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class NsxtAlbVirtualServiceHttpSecRulesRuleMatchCriteriaCookieOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="vcd.nsxtAlbVirtualServiceHttpSecRules.NsxtAlbVirtualServiceHttpSecRulesRuleMatchCriteriaCookieOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__957f13c81535567b8fb05224acfde7742f9c07fe3453331b9bfbe37311bda465)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="criteriaInput")
    def criteria_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "criteriaInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="valueInput")
    def value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "valueInput"))

    @builtins.property
    @jsii.member(jsii_name="criteria")
    def criteria(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "criteria"))

    @criteria.setter
    def criteria(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__459d454f4f42e0d4d1a537240126da3d6aced60201d30ae285ceb7e2f6079ae2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "criteria", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__296338832ddba8d009175fc38f9133daf90e90fda855e349be1cf3d9339d4773)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ec07d725972f223b3e63c96f373151bbad7accd1e95a79482b6d67f680021362)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[NsxtAlbVirtualServiceHttpSecRulesRuleMatchCriteriaCookie]:
        return typing.cast(typing.Optional[NsxtAlbVirtualServiceHttpSecRulesRuleMatchCriteriaCookie], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[NsxtAlbVirtualServiceHttpSecRulesRuleMatchCriteriaCookie],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__194ef5338a5658261ebd4d44b4671c758466e8f5b1d6dd83be6a699157e2a3bb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="vcd.nsxtAlbVirtualServiceHttpSecRules.NsxtAlbVirtualServiceHttpSecRulesRuleMatchCriteriaHttpMethods",
    jsii_struct_bases=[],
    name_mapping={"criteria": "criteria", "methods": "methods"},
)
class NsxtAlbVirtualServiceHttpSecRulesRuleMatchCriteriaHttpMethods:
    def __init__(
        self,
        *,
        criteria: builtins.str,
        methods: typing.Sequence[builtins.str],
    ) -> None:
        '''
        :param criteria: Criteria to use for IP address matching the HTTP request. Options - IS_IN, IS_NOT_IN. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_sec_rules#criteria NsxtAlbVirtualServiceHttpSecRules#criteria}
        :param methods: HTTP methods to match. Options - GET, PUT, POST, DELETE, HEAD, OPTIONS, TRACE, CONNECT, PATCH, PROPFIND, PROPPATCH, MKCOL, COPY, MOVE, LOCK, UNLOCK Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_sec_rules#methods NsxtAlbVirtualServiceHttpSecRules#methods}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5983182719a288ec886ea3c65e33c56e3425d58aefdf11d5c7b0fc1a183def1e)
            check_type(argname="argument criteria", value=criteria, expected_type=type_hints["criteria"])
            check_type(argname="argument methods", value=methods, expected_type=type_hints["methods"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "criteria": criteria,
            "methods": methods,
        }

    @builtins.property
    def criteria(self) -> builtins.str:
        '''Criteria to use for IP address matching the HTTP request. Options - IS_IN, IS_NOT_IN.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_sec_rules#criteria NsxtAlbVirtualServiceHttpSecRules#criteria}
        '''
        result = self._values.get("criteria")
        assert result is not None, "Required property 'criteria' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def methods(self) -> typing.List[builtins.str]:
        '''HTTP methods to match.

        Options - GET, PUT, POST, DELETE, HEAD, OPTIONS, TRACE, CONNECT, PATCH, PROPFIND, PROPPATCH, MKCOL, COPY, MOVE, LOCK, UNLOCK

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_sec_rules#methods NsxtAlbVirtualServiceHttpSecRules#methods}
        '''
        result = self._values.get("methods")
        assert result is not None, "Required property 'methods' is missing"
        return typing.cast(typing.List[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NsxtAlbVirtualServiceHttpSecRulesRuleMatchCriteriaHttpMethods(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class NsxtAlbVirtualServiceHttpSecRulesRuleMatchCriteriaHttpMethodsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="vcd.nsxtAlbVirtualServiceHttpSecRules.NsxtAlbVirtualServiceHttpSecRulesRuleMatchCriteriaHttpMethodsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5d1bac08e245e92e3d0524a04d0cec1ca35855458d8bf7ec90fd92f42b1a7d68)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="criteriaInput")
    def criteria_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "criteriaInput"))

    @builtins.property
    @jsii.member(jsii_name="methodsInput")
    def methods_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "methodsInput"))

    @builtins.property
    @jsii.member(jsii_name="criteria")
    def criteria(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "criteria"))

    @criteria.setter
    def criteria(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__78128ae1e50f28d1e298de8b7175e3a6d744b00f4023fec6239f8915d8aec216)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "criteria", value)

    @builtins.property
    @jsii.member(jsii_name="methods")
    def methods(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "methods"))

    @methods.setter
    def methods(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__80f65c853ef62487f226fa6ebbdb1360f598ff6b3baaf23403b01db2977cfb2f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "methods", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[NsxtAlbVirtualServiceHttpSecRulesRuleMatchCriteriaHttpMethods]:
        return typing.cast(typing.Optional[NsxtAlbVirtualServiceHttpSecRulesRuleMatchCriteriaHttpMethods], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[NsxtAlbVirtualServiceHttpSecRulesRuleMatchCriteriaHttpMethods],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b04b8313366e9376e40c254a3a4c574d6eb658708709f638b769e637cd6cfc51)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class NsxtAlbVirtualServiceHttpSecRulesRuleMatchCriteriaOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="vcd.nsxtAlbVirtualServiceHttpSecRules.NsxtAlbVirtualServiceHttpSecRulesRuleMatchCriteriaOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__85b7cb1d15732249d521111cd419bd41a4f9d94a846b654033706fcb220b8253)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putClientIpAddress")
    def put_client_ip_address(
        self,
        *,
        criteria: builtins.str,
        ip_addresses: typing.Sequence[builtins.str],
    ) -> None:
        '''
        :param criteria: Criteria to use for IP address matching the HTTP request. Options - IS_IN, IS_NOT_IN. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_sec_rules#criteria NsxtAlbVirtualServiceHttpSecRules#criteria}
        :param ip_addresses: A set of IP addresses. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_sec_rules#ip_addresses NsxtAlbVirtualServiceHttpSecRules#ip_addresses}
        '''
        value = NsxtAlbVirtualServiceHttpSecRulesRuleMatchCriteriaClientIpAddress(
            criteria=criteria, ip_addresses=ip_addresses
        )

        return typing.cast(None, jsii.invoke(self, "putClientIpAddress", [value]))

    @jsii.member(jsii_name="putCookie")
    def put_cookie(
        self,
        *,
        criteria: builtins.str,
        name: builtins.str,
        value: builtins.str,
    ) -> None:
        '''
        :param criteria: Criteria to use for matching cookies in the HTTP request. Options - EXISTS, DOES_NOT_EXIST, BEGINS_WITH, DOES_NOT_BEGIN_WITH, CONTAINS, DOES_NOT_CONTAIN, ENDS_WITH, DOES_NOT_END_WITH, EQUALS, DOES_NOT_EQUAL Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_sec_rules#criteria NsxtAlbVirtualServiceHttpSecRules#criteria}
        :param name: Name of the HTTP cookie whose value is to be matched. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_sec_rules#name NsxtAlbVirtualServiceHttpSecRules#name}
        :param value: String values to match for an HTTP cookie. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_sec_rules#value NsxtAlbVirtualServiceHttpSecRules#value}
        '''
        value_ = NsxtAlbVirtualServiceHttpSecRulesRuleMatchCriteriaCookie(
            criteria=criteria, name=name, value=value
        )

        return typing.cast(None, jsii.invoke(self, "putCookie", [value_]))

    @jsii.member(jsii_name="putHttpMethods")
    def put_http_methods(
        self,
        *,
        criteria: builtins.str,
        methods: typing.Sequence[builtins.str],
    ) -> None:
        '''
        :param criteria: Criteria to use for IP address matching the HTTP request. Options - IS_IN, IS_NOT_IN. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_sec_rules#criteria NsxtAlbVirtualServiceHttpSecRules#criteria}
        :param methods: HTTP methods to match. Options - GET, PUT, POST, DELETE, HEAD, OPTIONS, TRACE, CONNECT, PATCH, PROPFIND, PROPPATCH, MKCOL, COPY, MOVE, LOCK, UNLOCK Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_sec_rules#methods NsxtAlbVirtualServiceHttpSecRules#methods}
        '''
        value = NsxtAlbVirtualServiceHttpSecRulesRuleMatchCriteriaHttpMethods(
            criteria=criteria, methods=methods
        )

        return typing.cast(None, jsii.invoke(self, "putHttpMethods", [value]))

    @jsii.member(jsii_name="putPath")
    def put_path(
        self,
        *,
        criteria: builtins.str,
        paths: typing.Sequence[builtins.str],
    ) -> None:
        '''
        :param criteria: Criteria to use for matching the path in the HTTP request URI. Options - BEGINS_WITH, DOES_NOT_BEGIN_WITH, CONTAINS, DOES_NOT_CONTAIN, ENDS_WITH, DOES_NOT_END_WITH, EQUALS, DOES_NOT_EQUAL, REGEX_MATCH, REGEX_DOES_NOT_MATCH Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_sec_rules#criteria NsxtAlbVirtualServiceHttpSecRules#criteria}
        :param paths: String values to match the path. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_sec_rules#paths NsxtAlbVirtualServiceHttpSecRules#paths}
        '''
        value = NsxtAlbVirtualServiceHttpSecRulesRuleMatchCriteriaPath(
            criteria=criteria, paths=paths
        )

        return typing.cast(None, jsii.invoke(self, "putPath", [value]))

    @jsii.member(jsii_name="putRequestHeaders")
    def put_request_headers(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["NsxtAlbVirtualServiceHttpSecRulesRuleMatchCriteriaRequestHeaders", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__290c87068a95cdec9121283831dc43bcdaed73a22b66824bdd6180d6e818a49e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putRequestHeaders", [value]))

    @jsii.member(jsii_name="putServicePorts")
    def put_service_ports(
        self,
        *,
        criteria: builtins.str,
        ports: typing.Sequence[jsii.Number],
    ) -> None:
        '''
        :param criteria: Criteria to use for IP address matching the HTTP request. Options - IS_IN, IS_NOT_IN. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_sec_rules#criteria NsxtAlbVirtualServiceHttpSecRules#criteria}
        :param ports: A set of TCP ports. Allowed values are 1-65535. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_sec_rules#ports NsxtAlbVirtualServiceHttpSecRules#ports}
        '''
        value = NsxtAlbVirtualServiceHttpSecRulesRuleMatchCriteriaServicePorts(
            criteria=criteria, ports=ports
        )

        return typing.cast(None, jsii.invoke(self, "putServicePorts", [value]))

    @jsii.member(jsii_name="resetClientIpAddress")
    def reset_client_ip_address(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetClientIpAddress", []))

    @jsii.member(jsii_name="resetCookie")
    def reset_cookie(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCookie", []))

    @jsii.member(jsii_name="resetHttpMethods")
    def reset_http_methods(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHttpMethods", []))

    @jsii.member(jsii_name="resetPath")
    def reset_path(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPath", []))

    @jsii.member(jsii_name="resetProtocolType")
    def reset_protocol_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProtocolType", []))

    @jsii.member(jsii_name="resetQuery")
    def reset_query(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetQuery", []))

    @jsii.member(jsii_name="resetRequestHeaders")
    def reset_request_headers(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRequestHeaders", []))

    @jsii.member(jsii_name="resetServicePorts")
    def reset_service_ports(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetServicePorts", []))

    @builtins.property
    @jsii.member(jsii_name="clientIpAddress")
    def client_ip_address(
        self,
    ) -> NsxtAlbVirtualServiceHttpSecRulesRuleMatchCriteriaClientIpAddressOutputReference:
        return typing.cast(NsxtAlbVirtualServiceHttpSecRulesRuleMatchCriteriaClientIpAddressOutputReference, jsii.get(self, "clientIpAddress"))

    @builtins.property
    @jsii.member(jsii_name="cookie")
    def cookie(
        self,
    ) -> NsxtAlbVirtualServiceHttpSecRulesRuleMatchCriteriaCookieOutputReference:
        return typing.cast(NsxtAlbVirtualServiceHttpSecRulesRuleMatchCriteriaCookieOutputReference, jsii.get(self, "cookie"))

    @builtins.property
    @jsii.member(jsii_name="httpMethods")
    def http_methods(
        self,
    ) -> NsxtAlbVirtualServiceHttpSecRulesRuleMatchCriteriaHttpMethodsOutputReference:
        return typing.cast(NsxtAlbVirtualServiceHttpSecRulesRuleMatchCriteriaHttpMethodsOutputReference, jsii.get(self, "httpMethods"))

    @builtins.property
    @jsii.member(jsii_name="path")
    def path(
        self,
    ) -> "NsxtAlbVirtualServiceHttpSecRulesRuleMatchCriteriaPathOutputReference":
        return typing.cast("NsxtAlbVirtualServiceHttpSecRulesRuleMatchCriteriaPathOutputReference", jsii.get(self, "path"))

    @builtins.property
    @jsii.member(jsii_name="requestHeaders")
    def request_headers(
        self,
    ) -> "NsxtAlbVirtualServiceHttpSecRulesRuleMatchCriteriaRequestHeadersList":
        return typing.cast("NsxtAlbVirtualServiceHttpSecRulesRuleMatchCriteriaRequestHeadersList", jsii.get(self, "requestHeaders"))

    @builtins.property
    @jsii.member(jsii_name="servicePorts")
    def service_ports(
        self,
    ) -> "NsxtAlbVirtualServiceHttpSecRulesRuleMatchCriteriaServicePortsOutputReference":
        return typing.cast("NsxtAlbVirtualServiceHttpSecRulesRuleMatchCriteriaServicePortsOutputReference", jsii.get(self, "servicePorts"))

    @builtins.property
    @jsii.member(jsii_name="clientIpAddressInput")
    def client_ip_address_input(
        self,
    ) -> typing.Optional[NsxtAlbVirtualServiceHttpSecRulesRuleMatchCriteriaClientIpAddress]:
        return typing.cast(typing.Optional[NsxtAlbVirtualServiceHttpSecRulesRuleMatchCriteriaClientIpAddress], jsii.get(self, "clientIpAddressInput"))

    @builtins.property
    @jsii.member(jsii_name="cookieInput")
    def cookie_input(
        self,
    ) -> typing.Optional[NsxtAlbVirtualServiceHttpSecRulesRuleMatchCriteriaCookie]:
        return typing.cast(typing.Optional[NsxtAlbVirtualServiceHttpSecRulesRuleMatchCriteriaCookie], jsii.get(self, "cookieInput"))

    @builtins.property
    @jsii.member(jsii_name="httpMethodsInput")
    def http_methods_input(
        self,
    ) -> typing.Optional[NsxtAlbVirtualServiceHttpSecRulesRuleMatchCriteriaHttpMethods]:
        return typing.cast(typing.Optional[NsxtAlbVirtualServiceHttpSecRulesRuleMatchCriteriaHttpMethods], jsii.get(self, "httpMethodsInput"))

    @builtins.property
    @jsii.member(jsii_name="pathInput")
    def path_input(
        self,
    ) -> typing.Optional["NsxtAlbVirtualServiceHttpSecRulesRuleMatchCriteriaPath"]:
        return typing.cast(typing.Optional["NsxtAlbVirtualServiceHttpSecRulesRuleMatchCriteriaPath"], jsii.get(self, "pathInput"))

    @builtins.property
    @jsii.member(jsii_name="protocolTypeInput")
    def protocol_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "protocolTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="queryInput")
    def query_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "queryInput"))

    @builtins.property
    @jsii.member(jsii_name="requestHeadersInput")
    def request_headers_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["NsxtAlbVirtualServiceHttpSecRulesRuleMatchCriteriaRequestHeaders"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["NsxtAlbVirtualServiceHttpSecRulesRuleMatchCriteriaRequestHeaders"]]], jsii.get(self, "requestHeadersInput"))

    @builtins.property
    @jsii.member(jsii_name="servicePortsInput")
    def service_ports_input(
        self,
    ) -> typing.Optional["NsxtAlbVirtualServiceHttpSecRulesRuleMatchCriteriaServicePorts"]:
        return typing.cast(typing.Optional["NsxtAlbVirtualServiceHttpSecRulesRuleMatchCriteriaServicePorts"], jsii.get(self, "servicePortsInput"))

    @builtins.property
    @jsii.member(jsii_name="protocolType")
    def protocol_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "protocolType"))

    @protocol_type.setter
    def protocol_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3505529fb166856ad94db7ade2efcd1f296dafa4388986272782e9a55d68188c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "protocolType", value)

    @builtins.property
    @jsii.member(jsii_name="query")
    def query(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "query"))

    @query.setter
    def query(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4e672df2cbd8d40d40199a88a8b838ccc9e75882c7755c29e84c0ebe2da837c3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "query", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[NsxtAlbVirtualServiceHttpSecRulesRuleMatchCriteria]:
        return typing.cast(typing.Optional[NsxtAlbVirtualServiceHttpSecRulesRuleMatchCriteria], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[NsxtAlbVirtualServiceHttpSecRulesRuleMatchCriteria],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4b98a945acc6fdcb9b634ce47eb5bd7ceaa713e4e7a89f7199fb25b12ad659de)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="vcd.nsxtAlbVirtualServiceHttpSecRules.NsxtAlbVirtualServiceHttpSecRulesRuleMatchCriteriaPath",
    jsii_struct_bases=[],
    name_mapping={"criteria": "criteria", "paths": "paths"},
)
class NsxtAlbVirtualServiceHttpSecRulesRuleMatchCriteriaPath:
    def __init__(
        self,
        *,
        criteria: builtins.str,
        paths: typing.Sequence[builtins.str],
    ) -> None:
        '''
        :param criteria: Criteria to use for matching the path in the HTTP request URI. Options - BEGINS_WITH, DOES_NOT_BEGIN_WITH, CONTAINS, DOES_NOT_CONTAIN, ENDS_WITH, DOES_NOT_END_WITH, EQUALS, DOES_NOT_EQUAL, REGEX_MATCH, REGEX_DOES_NOT_MATCH Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_sec_rules#criteria NsxtAlbVirtualServiceHttpSecRules#criteria}
        :param paths: String values to match the path. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_sec_rules#paths NsxtAlbVirtualServiceHttpSecRules#paths}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__423fcee3379b4fbef7c09c20b1af216aa20a8b51834d284a3a1e1027ab60973f)
            check_type(argname="argument criteria", value=criteria, expected_type=type_hints["criteria"])
            check_type(argname="argument paths", value=paths, expected_type=type_hints["paths"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "criteria": criteria,
            "paths": paths,
        }

    @builtins.property
    def criteria(self) -> builtins.str:
        '''Criteria to use for matching the path in the HTTP request URI.

        Options - BEGINS_WITH, DOES_NOT_BEGIN_WITH, CONTAINS, DOES_NOT_CONTAIN, ENDS_WITH, DOES_NOT_END_WITH, EQUALS, DOES_NOT_EQUAL, REGEX_MATCH, REGEX_DOES_NOT_MATCH

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_sec_rules#criteria NsxtAlbVirtualServiceHttpSecRules#criteria}
        '''
        result = self._values.get("criteria")
        assert result is not None, "Required property 'criteria' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def paths(self) -> typing.List[builtins.str]:
        '''String values to match the path.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_sec_rules#paths NsxtAlbVirtualServiceHttpSecRules#paths}
        '''
        result = self._values.get("paths")
        assert result is not None, "Required property 'paths' is missing"
        return typing.cast(typing.List[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NsxtAlbVirtualServiceHttpSecRulesRuleMatchCriteriaPath(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class NsxtAlbVirtualServiceHttpSecRulesRuleMatchCriteriaPathOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="vcd.nsxtAlbVirtualServiceHttpSecRules.NsxtAlbVirtualServiceHttpSecRulesRuleMatchCriteriaPathOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6eaeec695da8c9eb340c59dd5ade0a231df6e48409173478dd6e37b45d3c636f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="criteriaInput")
    def criteria_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "criteriaInput"))

    @builtins.property
    @jsii.member(jsii_name="pathsInput")
    def paths_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "pathsInput"))

    @builtins.property
    @jsii.member(jsii_name="criteria")
    def criteria(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "criteria"))

    @criteria.setter
    def criteria(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eaed05ad49ba6e08c2a90c73d3b6e3193fae8e2c9d929068d78763fb6ce39dca)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "criteria", value)

    @builtins.property
    @jsii.member(jsii_name="paths")
    def paths(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "paths"))

    @paths.setter
    def paths(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9790c3f8393b43cc6c0711b958f397119ca4800f380b8e1a91a6f37a6c6fb390)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "paths", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[NsxtAlbVirtualServiceHttpSecRulesRuleMatchCriteriaPath]:
        return typing.cast(typing.Optional[NsxtAlbVirtualServiceHttpSecRulesRuleMatchCriteriaPath], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[NsxtAlbVirtualServiceHttpSecRulesRuleMatchCriteriaPath],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ed2b8e04762c8fc86017e4410cdf8e852c6206c230b114ab482f9f6f492ce7e2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="vcd.nsxtAlbVirtualServiceHttpSecRules.NsxtAlbVirtualServiceHttpSecRulesRuleMatchCriteriaRequestHeaders",
    jsii_struct_bases=[],
    name_mapping={"criteria": "criteria", "name": "name", "values": "values"},
)
class NsxtAlbVirtualServiceHttpSecRulesRuleMatchCriteriaRequestHeaders:
    def __init__(
        self,
        *,
        criteria: builtins.str,
        name: builtins.str,
        values: typing.Sequence[builtins.str],
    ) -> None:
        '''
        :param criteria: Criteria to use for matching headers and cookies in the HTTP request amd response. Options - EXISTS, DOES_NOT_EXIST, BEGINS_WITH, DOES_NOT_BEGIN_WITH, CONTAINS, DOES_NOT_CONTAIN, ENDS_WITH, DOES_NOT_END_WITH, EQUALS, DOES_NOT_EQUAL Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_sec_rules#criteria NsxtAlbVirtualServiceHttpSecRules#criteria}
        :param name: Name of the HTTP header whose value is to be matched. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_sec_rules#name NsxtAlbVirtualServiceHttpSecRules#name}
        :param values: String values to match for an HTTP header. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_sec_rules#values NsxtAlbVirtualServiceHttpSecRules#values}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__602fd539a236f08aa721ad684d3d218c375c2d02085298bd5c527ea239547a69)
            check_type(argname="argument criteria", value=criteria, expected_type=type_hints["criteria"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument values", value=values, expected_type=type_hints["values"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "criteria": criteria,
            "name": name,
            "values": values,
        }

    @builtins.property
    def criteria(self) -> builtins.str:
        '''Criteria to use for matching headers and cookies in the HTTP request amd response.

        Options - EXISTS, DOES_NOT_EXIST, BEGINS_WITH, DOES_NOT_BEGIN_WITH, CONTAINS, DOES_NOT_CONTAIN, ENDS_WITH, DOES_NOT_END_WITH, EQUALS, DOES_NOT_EQUAL

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_sec_rules#criteria NsxtAlbVirtualServiceHttpSecRules#criteria}
        '''
        result = self._values.get("criteria")
        assert result is not None, "Required property 'criteria' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Name of the HTTP header whose value is to be matched.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_sec_rules#name NsxtAlbVirtualServiceHttpSecRules#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def values(self) -> typing.List[builtins.str]:
        '''String values to match for an HTTP header.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_sec_rules#values NsxtAlbVirtualServiceHttpSecRules#values}
        '''
        result = self._values.get("values")
        assert result is not None, "Required property 'values' is missing"
        return typing.cast(typing.List[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NsxtAlbVirtualServiceHttpSecRulesRuleMatchCriteriaRequestHeaders(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class NsxtAlbVirtualServiceHttpSecRulesRuleMatchCriteriaRequestHeadersList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="vcd.nsxtAlbVirtualServiceHttpSecRules.NsxtAlbVirtualServiceHttpSecRulesRuleMatchCriteriaRequestHeadersList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7a7ade3d36ca469c8be1d7e7ac33cae288b018948e57a01874fd60c6b736d547)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "NsxtAlbVirtualServiceHttpSecRulesRuleMatchCriteriaRequestHeadersOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__13cfa0bb94a23f87805b9147732b8f1bdec9933c67a6e9e22d625bf763a21501)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("NsxtAlbVirtualServiceHttpSecRulesRuleMatchCriteriaRequestHeadersOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__704160d123e0ed04ef405a4b97832b48fdfceca203ef68e5d6e202b586e11b81)
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
            type_hints = typing.get_type_hints(_typecheckingstub__705f0857f6228ac89698c563505bf515456a6a725a751403d514ff59f48faf3e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__79702c5583ea5dc47506bb93dfed88e7bcb636ccdce2b78d1076ea1bd600e22b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NsxtAlbVirtualServiceHttpSecRulesRuleMatchCriteriaRequestHeaders]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NsxtAlbVirtualServiceHttpSecRulesRuleMatchCriteriaRequestHeaders]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NsxtAlbVirtualServiceHttpSecRulesRuleMatchCriteriaRequestHeaders]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3715f0e6152bc7ea42cac9c7c8ea3ddb1d146964a1cf4e3ce75f3696cad273a4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class NsxtAlbVirtualServiceHttpSecRulesRuleMatchCriteriaRequestHeadersOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="vcd.nsxtAlbVirtualServiceHttpSecRules.NsxtAlbVirtualServiceHttpSecRulesRuleMatchCriteriaRequestHeadersOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8e6e7cec12a6cb05771eadf4036d0c5a7ae079d490ed913a9d446efbf07c4b1a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="criteriaInput")
    def criteria_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "criteriaInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="valuesInput")
    def values_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "valuesInput"))

    @builtins.property
    @jsii.member(jsii_name="criteria")
    def criteria(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "criteria"))

    @criteria.setter
    def criteria(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__830c59f21dfc9ac1754daa66c9cb3cd92831d0149d61c6778064697b3a72ea6a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "criteria", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aa9011069daa5691f9d2b208351ffb8487e3991f780340686a10dbc2fa9d3456)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="values")
    def values(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "values"))

    @values.setter
    def values(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d1742d6ea8498fd1e2763282ce12df5491ab4d03d544946e5dc919416ffc3715)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "values", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NsxtAlbVirtualServiceHttpSecRulesRuleMatchCriteriaRequestHeaders]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NsxtAlbVirtualServiceHttpSecRulesRuleMatchCriteriaRequestHeaders]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NsxtAlbVirtualServiceHttpSecRulesRuleMatchCriteriaRequestHeaders]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2cfa39c375ad6b619c1dcaf14641e4898e4990f6c3d9ebdd994ffd92fe01d8c9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="vcd.nsxtAlbVirtualServiceHttpSecRules.NsxtAlbVirtualServiceHttpSecRulesRuleMatchCriteriaServicePorts",
    jsii_struct_bases=[],
    name_mapping={"criteria": "criteria", "ports": "ports"},
)
class NsxtAlbVirtualServiceHttpSecRulesRuleMatchCriteriaServicePorts:
    def __init__(
        self,
        *,
        criteria: builtins.str,
        ports: typing.Sequence[jsii.Number],
    ) -> None:
        '''
        :param criteria: Criteria to use for IP address matching the HTTP request. Options - IS_IN, IS_NOT_IN. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_sec_rules#criteria NsxtAlbVirtualServiceHttpSecRules#criteria}
        :param ports: A set of TCP ports. Allowed values are 1-65535. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_sec_rules#ports NsxtAlbVirtualServiceHttpSecRules#ports}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8ad7df28a696e124ce7ae649da565f0e58d1611acdc5afc233f90db168b7c019)
            check_type(argname="argument criteria", value=criteria, expected_type=type_hints["criteria"])
            check_type(argname="argument ports", value=ports, expected_type=type_hints["ports"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "criteria": criteria,
            "ports": ports,
        }

    @builtins.property
    def criteria(self) -> builtins.str:
        '''Criteria to use for IP address matching the HTTP request. Options - IS_IN, IS_NOT_IN.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_sec_rules#criteria NsxtAlbVirtualServiceHttpSecRules#criteria}
        '''
        result = self._values.get("criteria")
        assert result is not None, "Required property 'criteria' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def ports(self) -> typing.List[jsii.Number]:
        '''A set of TCP ports. Allowed values are 1-65535.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_sec_rules#ports NsxtAlbVirtualServiceHttpSecRules#ports}
        '''
        result = self._values.get("ports")
        assert result is not None, "Required property 'ports' is missing"
        return typing.cast(typing.List[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NsxtAlbVirtualServiceHttpSecRulesRuleMatchCriteriaServicePorts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class NsxtAlbVirtualServiceHttpSecRulesRuleMatchCriteriaServicePortsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="vcd.nsxtAlbVirtualServiceHttpSecRules.NsxtAlbVirtualServiceHttpSecRulesRuleMatchCriteriaServicePortsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__cc303f12dc09aec0e6b03a20ffbcdf3783a8888d879023b2483b43cb3b3217cb)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="criteriaInput")
    def criteria_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "criteriaInput"))

    @builtins.property
    @jsii.member(jsii_name="portsInput")
    def ports_input(self) -> typing.Optional[typing.List[jsii.Number]]:
        return typing.cast(typing.Optional[typing.List[jsii.Number]], jsii.get(self, "portsInput"))

    @builtins.property
    @jsii.member(jsii_name="criteria")
    def criteria(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "criteria"))

    @criteria.setter
    def criteria(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6158a7dc40185f15a8be2c3e54a8bdb547479b8f1f1217fae49414f34d1b9a34)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "criteria", value)

    @builtins.property
    @jsii.member(jsii_name="ports")
    def ports(self) -> typing.List[jsii.Number]:
        return typing.cast(typing.List[jsii.Number], jsii.get(self, "ports"))

    @ports.setter
    def ports(self, value: typing.List[jsii.Number]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__666cbb5811c200287677c536496850290999f8921ff9274a77ecd31c4b848969)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ports", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[NsxtAlbVirtualServiceHttpSecRulesRuleMatchCriteriaServicePorts]:
        return typing.cast(typing.Optional[NsxtAlbVirtualServiceHttpSecRulesRuleMatchCriteriaServicePorts], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[NsxtAlbVirtualServiceHttpSecRulesRuleMatchCriteriaServicePorts],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__54f2200ecac396c11e823166094f6a8a1538161bf92546e00922d413a2a75e18)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class NsxtAlbVirtualServiceHttpSecRulesRuleOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="vcd.nsxtAlbVirtualServiceHttpSecRules.NsxtAlbVirtualServiceHttpSecRulesRuleOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1909d67109a9322403c2afffe937ec281ec56853a17a3e6aebd1a4ef5eadca11)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putActions")
    def put_actions(
        self,
        *,
        connections: typing.Optional[builtins.str] = None,
        rate_limit: typing.Optional[typing.Union[NsxtAlbVirtualServiceHttpSecRulesRuleActionsRateLimit, typing.Dict[builtins.str, typing.Any]]] = None,
        redirect_to_https: typing.Optional[builtins.str] = None,
        send_response: typing.Optional[typing.Union[NsxtAlbVirtualServiceHttpSecRulesRuleActionsSendResponse, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connections: ALLOW or CLOSE connections. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_sec_rules#connections NsxtAlbVirtualServiceHttpSecRules#connections}
        :param rate_limit: rate_limit block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_sec_rules#rate_limit NsxtAlbVirtualServiceHttpSecRules#rate_limit}
        :param redirect_to_https: Port number that should be redirected to HTTPS. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_sec_rules#redirect_to_https NsxtAlbVirtualServiceHttpSecRules#redirect_to_https}
        :param send_response: send_response block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_sec_rules#send_response NsxtAlbVirtualServiceHttpSecRules#send_response}
        '''
        value = NsxtAlbVirtualServiceHttpSecRulesRuleActions(
            connections=connections,
            rate_limit=rate_limit,
            redirect_to_https=redirect_to_https,
            send_response=send_response,
        )

        return typing.cast(None, jsii.invoke(self, "putActions", [value]))

    @jsii.member(jsii_name="putMatchCriteria")
    def put_match_criteria(
        self,
        *,
        client_ip_address: typing.Optional[typing.Union[NsxtAlbVirtualServiceHttpSecRulesRuleMatchCriteriaClientIpAddress, typing.Dict[builtins.str, typing.Any]]] = None,
        cookie: typing.Optional[typing.Union[NsxtAlbVirtualServiceHttpSecRulesRuleMatchCriteriaCookie, typing.Dict[builtins.str, typing.Any]]] = None,
        http_methods: typing.Optional[typing.Union[NsxtAlbVirtualServiceHttpSecRulesRuleMatchCriteriaHttpMethods, typing.Dict[builtins.str, typing.Any]]] = None,
        path: typing.Optional[typing.Union[NsxtAlbVirtualServiceHttpSecRulesRuleMatchCriteriaPath, typing.Dict[builtins.str, typing.Any]]] = None,
        protocol_type: typing.Optional[builtins.str] = None,
        query: typing.Optional[typing.Sequence[builtins.str]] = None,
        request_headers: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[NsxtAlbVirtualServiceHttpSecRulesRuleMatchCriteriaRequestHeaders, typing.Dict[builtins.str, typing.Any]]]]] = None,
        service_ports: typing.Optional[typing.Union[NsxtAlbVirtualServiceHttpSecRulesRuleMatchCriteriaServicePorts, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param client_ip_address: client_ip_address block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_sec_rules#client_ip_address NsxtAlbVirtualServiceHttpSecRules#client_ip_address}
        :param cookie: cookie block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_sec_rules#cookie NsxtAlbVirtualServiceHttpSecRules#cookie}
        :param http_methods: http_methods block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_sec_rules#http_methods NsxtAlbVirtualServiceHttpSecRules#http_methods}
        :param path: path block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_sec_rules#path NsxtAlbVirtualServiceHttpSecRules#path}
        :param protocol_type: Protocol to match - 'HTTP' or 'HTTPS'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_sec_rules#protocol_type NsxtAlbVirtualServiceHttpSecRules#protocol_type}
        :param query: HTTP request query strings to match. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_sec_rules#query NsxtAlbVirtualServiceHttpSecRules#query}
        :param request_headers: request_headers block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_sec_rules#request_headers NsxtAlbVirtualServiceHttpSecRules#request_headers}
        :param service_ports: service_ports block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_sec_rules#service_ports NsxtAlbVirtualServiceHttpSecRules#service_ports}
        '''
        value = NsxtAlbVirtualServiceHttpSecRulesRuleMatchCriteria(
            client_ip_address=client_ip_address,
            cookie=cookie,
            http_methods=http_methods,
            path=path,
            protocol_type=protocol_type,
            query=query,
            request_headers=request_headers,
            service_ports=service_ports,
        )

        return typing.cast(None, jsii.invoke(self, "putMatchCriteria", [value]))

    @jsii.member(jsii_name="resetActive")
    def reset_active(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetActive", []))

    @jsii.member(jsii_name="resetLogging")
    def reset_logging(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLogging", []))

    @builtins.property
    @jsii.member(jsii_name="actions")
    def actions(self) -> NsxtAlbVirtualServiceHttpSecRulesRuleActionsOutputReference:
        return typing.cast(NsxtAlbVirtualServiceHttpSecRulesRuleActionsOutputReference, jsii.get(self, "actions"))

    @builtins.property
    @jsii.member(jsii_name="matchCriteria")
    def match_criteria(
        self,
    ) -> NsxtAlbVirtualServiceHttpSecRulesRuleMatchCriteriaOutputReference:
        return typing.cast(NsxtAlbVirtualServiceHttpSecRulesRuleMatchCriteriaOutputReference, jsii.get(self, "matchCriteria"))

    @builtins.property
    @jsii.member(jsii_name="actionsInput")
    def actions_input(
        self,
    ) -> typing.Optional[NsxtAlbVirtualServiceHttpSecRulesRuleActions]:
        return typing.cast(typing.Optional[NsxtAlbVirtualServiceHttpSecRulesRuleActions], jsii.get(self, "actionsInput"))

    @builtins.property
    @jsii.member(jsii_name="activeInput")
    def active_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "activeInput"))

    @builtins.property
    @jsii.member(jsii_name="loggingInput")
    def logging_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "loggingInput"))

    @builtins.property
    @jsii.member(jsii_name="matchCriteriaInput")
    def match_criteria_input(
        self,
    ) -> typing.Optional[NsxtAlbVirtualServiceHttpSecRulesRuleMatchCriteria]:
        return typing.cast(typing.Optional[NsxtAlbVirtualServiceHttpSecRulesRuleMatchCriteria], jsii.get(self, "matchCriteriaInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="active")
    def active(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "active"))

    @active.setter
    def active(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1400a25a1cd9af1b046fe35baa2bc6bacbb3c7ad005151a87c49834737e01b21)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "active", value)

    @builtins.property
    @jsii.member(jsii_name="logging")
    def logging(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "logging"))

    @logging.setter
    def logging(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2065a4ed43a3393f03b031ef081eede105de00cc1ecf4843105e64cee19f23eb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "logging", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ed5acee29f555a76947123f1368543360c9fc8a26ed162a950f2ea763b04246e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NsxtAlbVirtualServiceHttpSecRulesRule]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NsxtAlbVirtualServiceHttpSecRulesRule]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NsxtAlbVirtualServiceHttpSecRulesRule]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6ed8b73df405cc1642d9cedb0ff01bcd7d20489a0803561d2abe384a59da1edc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


__all__ = [
    "NsxtAlbVirtualServiceHttpSecRules",
    "NsxtAlbVirtualServiceHttpSecRulesConfig",
    "NsxtAlbVirtualServiceHttpSecRulesRule",
    "NsxtAlbVirtualServiceHttpSecRulesRuleActions",
    "NsxtAlbVirtualServiceHttpSecRulesRuleActionsOutputReference",
    "NsxtAlbVirtualServiceHttpSecRulesRuleActionsRateLimit",
    "NsxtAlbVirtualServiceHttpSecRulesRuleActionsRateLimitActionLocalResponse",
    "NsxtAlbVirtualServiceHttpSecRulesRuleActionsRateLimitActionLocalResponseList",
    "NsxtAlbVirtualServiceHttpSecRulesRuleActionsRateLimitActionLocalResponseOutputReference",
    "NsxtAlbVirtualServiceHttpSecRulesRuleActionsRateLimitActionRedirect",
    "NsxtAlbVirtualServiceHttpSecRulesRuleActionsRateLimitActionRedirectList",
    "NsxtAlbVirtualServiceHttpSecRulesRuleActionsRateLimitActionRedirectOutputReference",
    "NsxtAlbVirtualServiceHttpSecRulesRuleActionsRateLimitOutputReference",
    "NsxtAlbVirtualServiceHttpSecRulesRuleActionsSendResponse",
    "NsxtAlbVirtualServiceHttpSecRulesRuleActionsSendResponseOutputReference",
    "NsxtAlbVirtualServiceHttpSecRulesRuleList",
    "NsxtAlbVirtualServiceHttpSecRulesRuleMatchCriteria",
    "NsxtAlbVirtualServiceHttpSecRulesRuleMatchCriteriaClientIpAddress",
    "NsxtAlbVirtualServiceHttpSecRulesRuleMatchCriteriaClientIpAddressOutputReference",
    "NsxtAlbVirtualServiceHttpSecRulesRuleMatchCriteriaCookie",
    "NsxtAlbVirtualServiceHttpSecRulesRuleMatchCriteriaCookieOutputReference",
    "NsxtAlbVirtualServiceHttpSecRulesRuleMatchCriteriaHttpMethods",
    "NsxtAlbVirtualServiceHttpSecRulesRuleMatchCriteriaHttpMethodsOutputReference",
    "NsxtAlbVirtualServiceHttpSecRulesRuleMatchCriteriaOutputReference",
    "NsxtAlbVirtualServiceHttpSecRulesRuleMatchCriteriaPath",
    "NsxtAlbVirtualServiceHttpSecRulesRuleMatchCriteriaPathOutputReference",
    "NsxtAlbVirtualServiceHttpSecRulesRuleMatchCriteriaRequestHeaders",
    "NsxtAlbVirtualServiceHttpSecRulesRuleMatchCriteriaRequestHeadersList",
    "NsxtAlbVirtualServiceHttpSecRulesRuleMatchCriteriaRequestHeadersOutputReference",
    "NsxtAlbVirtualServiceHttpSecRulesRuleMatchCriteriaServicePorts",
    "NsxtAlbVirtualServiceHttpSecRulesRuleMatchCriteriaServicePortsOutputReference",
    "NsxtAlbVirtualServiceHttpSecRulesRuleOutputReference",
]

publication.publish()

def _typecheckingstub__e433070dd674840a6424cb2c3d548953a77d5c316679b3c3bbabb662bc02a1ac(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    rule: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[NsxtAlbVirtualServiceHttpSecRulesRule, typing.Dict[builtins.str, typing.Any]]]],
    virtual_service_id: builtins.str,
    id: typing.Optional[builtins.str] = None,
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

def _typecheckingstub__99c5663f786ca3db0ce74cf4cb77b85bbb0e00dff6aa0d21029be692d127cfb5(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b207dd4c6c927a53b678c29a87452700a84e17a08d7149ad5e2cb73757e955ea(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[NsxtAlbVirtualServiceHttpSecRulesRule, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__163e75597676e4d315cb9bbd184383577fc91a8bb2cd0cf4a7809c42b31068f5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__403ac3e0de8c03b8d9b2f316c0a5389cb951fe566300a5835816ce7163594617(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__abedb7a7921a9e596af236f3030be95d874509d79c826f5d925dbb13c6c6958b(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    rule: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[NsxtAlbVirtualServiceHttpSecRulesRule, typing.Dict[builtins.str, typing.Any]]]],
    virtual_service_id: builtins.str,
    id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__857059954153d35c565dd858dc7f1434108953ab597c60219d45000c0c6daec4(
    *,
    actions: typing.Union[NsxtAlbVirtualServiceHttpSecRulesRuleActions, typing.Dict[builtins.str, typing.Any]],
    match_criteria: typing.Union[NsxtAlbVirtualServiceHttpSecRulesRuleMatchCriteria, typing.Dict[builtins.str, typing.Any]],
    name: builtins.str,
    active: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    logging: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b6c76c40428a483f5512880a85acc24267d43e72b7997a50589fe99d716228cb(
    *,
    connections: typing.Optional[builtins.str] = None,
    rate_limit: typing.Optional[typing.Union[NsxtAlbVirtualServiceHttpSecRulesRuleActionsRateLimit, typing.Dict[builtins.str, typing.Any]]] = None,
    redirect_to_https: typing.Optional[builtins.str] = None,
    send_response: typing.Optional[typing.Union[NsxtAlbVirtualServiceHttpSecRulesRuleActionsSendResponse, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f684252c5625e52e85dc95b6ac474561fa181e13c99fa020becf4a3bb4438f6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c18673681910559da99fbd0eb894141715b2e619a84497d21e167e4f2172998d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__75c8f7c4e6fdbb9801a01d9d5f670a0ad582fd6c4e7244abd525c07c65769888(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2566ce9ccf41388c4a8cd59d8d3e15ae1ecbe7b6116b536f198c07e7ae566b99(
    value: typing.Optional[NsxtAlbVirtualServiceHttpSecRulesRuleActions],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__869cdf4bc1012cf96ca03dc23532de8740bc0e6a68ca17905fed720e1901a5e1(
    *,
    count: builtins.str,
    period: builtins.str,
    action_close_connection: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    action_local_response: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[NsxtAlbVirtualServiceHttpSecRulesRuleActionsRateLimitActionLocalResponse, typing.Dict[builtins.str, typing.Any]]]]] = None,
    action_redirect: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[NsxtAlbVirtualServiceHttpSecRulesRuleActionsRateLimitActionRedirect, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__09412c347251f5090cc4e3ec9099d34458017a72988dc0e55c495537021f5a31(
    *,
    status_code: builtins.str,
    content: typing.Optional[builtins.str] = None,
    content_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a4210014dd66a73bfdd96c4fec3d5798199619569c91b5f10de278ef042769c0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__53b54749c1b120d286337c2649df8d4a5ae52f786a41cb08f510e295692bc4b4(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f11d5ef0f76bcfec6c27a9cffc0eee7ce82dd1540e45c1a43ecc6adb9acd2424(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5cc9f9c677c6835a2f9d35001527266b6e0e9d40775a6668fd1b952a66fc669e(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__334f08c4568467256a110530c543fad899836b355d076d871d5047348e4858d0(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__88d5903d64f939fab3dfe69d1e382c2b843800e3fe60680ab6859a27548a7586(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NsxtAlbVirtualServiceHttpSecRulesRuleActionsRateLimitActionLocalResponse]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__847284bcf5d506e72ce7fd81ad62f72d5b0ea091ad45fd8d1c2dddc56413956d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__20701755e81a83e2dea95da81cb0d5ca7e76d338a591c26735bdd351c59905ae(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c41fcd31f62934287bb14436ba48b9aeb3c7bd31aefe55d8a189d9ce158373d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__61d23d3d499bfc969caec8f3a51f2eb08417ca3de758c9dbc0ca4a216366e5d2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__12a74034d026ae7dc313939da45417f5d4ebd5bb37f791d99dc96f796f230500(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NsxtAlbVirtualServiceHttpSecRulesRuleActionsRateLimitActionLocalResponse]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fd0a7f7590953eca19a05e80d5039f579fef62c96731a65f0a64aff41e507863(
    *,
    port: builtins.str,
    protocol: builtins.str,
    status_code: jsii.Number,
    host: typing.Optional[builtins.str] = None,
    keep_query: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    path: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba11fdc95570937518c5e56bfc610209ac0a35fd7e1c31dc2f6fa4ebc9d73a91(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c028d6daec46c1cbf3aed566b77203d7c94470d05870bde5ec6ae4806a8e7024(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7adf91d885156830a9136b681a63f64c7a0edaa849d96f41a2850b76b0c6f098(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__77faa585f1bac54be540096ff3e7b3d2d89c0a1a56296a183f08f4f0744249cb(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__13e20531a8fd2f8b96f8cec502a1ebd6e0d3746223b25d6a795b0e7cb3f60398(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__75a5c046edc8b044ba5b6a07d8b9c67d113dae86c1e7c42644989f130dd167f3(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NsxtAlbVirtualServiceHttpSecRulesRuleActionsRateLimitActionRedirect]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f5f717eaf39761c9d3bf0401939298fd4d4a734da8554b79d6dbec8950de918c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b1957c16464262ead3e67b88d557defe1036dbb8e5a6e9be7d8973bf91c1c800(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f8f16ee00febee8932b0d0d3f0e40b316ea78c1ca3c41d8a0ed6f0ab17f83ffd(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__29137db88bdddf598b37459bde2ee9a30ae900f71cbd46ee735d3c578d50c099(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__94d169d69c39fc6e8fc6d53bef3f2fc9a67a053699700abe821ed5e1eb5b1bd5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6dc0bf2cb7bb15ab5abbddd85e89ae6355c15d9690c25c18e73235625023fdbb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__23e22e8f1b850b12f800c3d99ea8ed19ef80575aae9834e79b52e48c86383b61(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2231a71f8901ef9b07dac4beab4496c04e4faf3ab06cc5fee98553a60dd34bbb(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NsxtAlbVirtualServiceHttpSecRulesRuleActionsRateLimitActionRedirect]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe98732cf95eac03a011f38a3c76ca9fe372ab8ad5742b1523295e1f42ddd21f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c03f2024a028ca369c0bbb7eeb573bec66e86fbc538af7f23e3d844ad8f61b6b(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[NsxtAlbVirtualServiceHttpSecRulesRuleActionsRateLimitActionLocalResponse, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c22f85c63ffc6bfd3d99809b57cbc7536fd8dd18b1e08b710d6320f7046168f(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[NsxtAlbVirtualServiceHttpSecRulesRuleActionsRateLimitActionRedirect, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c0de60ced93281d54adae7c1696b581605d1c69321fa75f90b1e9e7a4bce4cff(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__49088cbb08054b914819edc1453255f6e2767adbcc205e3406d22f02a7442c68(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2894b077fb32c6c3a4de7e42cc7820842274c8542ee1783eb6d8d85f57b01550(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2dfc07a07e4ee3441f96296ff1e721346d43175da37c438c9ca44b197bf80038(
    value: typing.Optional[NsxtAlbVirtualServiceHttpSecRulesRuleActionsRateLimit],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f98af7ea098ba2196e33e9e5da21f213dd351f89415b450ff20edda806970129(
    *,
    status_code: builtins.str,
    content: typing.Optional[builtins.str] = None,
    content_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__661fb632b172ff8a0802bb389531964145a399d8312ae883e382167604da263c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__75a9256aff44e852f0254e06194e9a910adc00b3d8b03d1b1a6ede7fb2b2a9b2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__42f01a72f1aca2fd7c0c34676cb31409e6aba4123842f703028f2d23493b8664(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc993087c504e9cbd703506c614b2adecaf378e1f70307c71ea7431e9039834e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__97010067091520996c67de898f7817a88b194bec0dd39b3fb3367ae5beda17f6(
    value: typing.Optional[NsxtAlbVirtualServiceHttpSecRulesRuleActionsSendResponse],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7177924571197631a3b72835f6044b0fb46dc65704bf9d613bab583f8684ba8a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__53dfec606d249f6879293f1aa72730bc4696ef4922f142b5a3d93f68550e6df5(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0647d6e97b7cb9c35fac47f556f90b5e1538981f31a9d0c11ed25714f6f1b256(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ea9f9b3a18f52c9616db1f2ba12573b5e08884761a2b11eb56395504942d800(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e7c3046ffe82b8419f36c8c00065e4a264586bb598933e106b97e0df031b1641(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e62cd90fcb6424c8739e11490f44e8d13cb93fd86fc27220cd36b1469abe323(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NsxtAlbVirtualServiceHttpSecRulesRule]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1fe1075398b0f4eb48e2fea0328e28e92ad6ee6229055c798bce5fcca7efb252(
    *,
    client_ip_address: typing.Optional[typing.Union[NsxtAlbVirtualServiceHttpSecRulesRuleMatchCriteriaClientIpAddress, typing.Dict[builtins.str, typing.Any]]] = None,
    cookie: typing.Optional[typing.Union[NsxtAlbVirtualServiceHttpSecRulesRuleMatchCriteriaCookie, typing.Dict[builtins.str, typing.Any]]] = None,
    http_methods: typing.Optional[typing.Union[NsxtAlbVirtualServiceHttpSecRulesRuleMatchCriteriaHttpMethods, typing.Dict[builtins.str, typing.Any]]] = None,
    path: typing.Optional[typing.Union[NsxtAlbVirtualServiceHttpSecRulesRuleMatchCriteriaPath, typing.Dict[builtins.str, typing.Any]]] = None,
    protocol_type: typing.Optional[builtins.str] = None,
    query: typing.Optional[typing.Sequence[builtins.str]] = None,
    request_headers: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[NsxtAlbVirtualServiceHttpSecRulesRuleMatchCriteriaRequestHeaders, typing.Dict[builtins.str, typing.Any]]]]] = None,
    service_ports: typing.Optional[typing.Union[NsxtAlbVirtualServiceHttpSecRulesRuleMatchCriteriaServicePorts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf73a05b89d6e6e16b9a533205d53eff6bb060ce76f0e3ce8913e5a43c68142d(
    *,
    criteria: builtins.str,
    ip_addresses: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cefc4e71d6a1ffc777e6f1a8b3c8813c560f27849e0b0fa9385eec807efac432(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__130ddc47465ea2915f43635443e74870a41515137a8ca80305aaf955c1633f93(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b75ec3df4936b825fd130ad7d961ee14cb4a8eee5339606c54334621907a880a(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__34a6a83a997c989f4f27dd8afd17f97e2cc13a1af354222941accab01579173a(
    value: typing.Optional[NsxtAlbVirtualServiceHttpSecRulesRuleMatchCriteriaClientIpAddress],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f6e47ede8048cab1058fe7b34c31ed7c6d9cccf6e70bfde127662eedebbcf7bf(
    *,
    criteria: builtins.str,
    name: builtins.str,
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__957f13c81535567b8fb05224acfde7742f9c07fe3453331b9bfbe37311bda465(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__459d454f4f42e0d4d1a537240126da3d6aced60201d30ae285ceb7e2f6079ae2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__296338832ddba8d009175fc38f9133daf90e90fda855e349be1cf3d9339d4773(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec07d725972f223b3e63c96f373151bbad7accd1e95a79482b6d67f680021362(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__194ef5338a5658261ebd4d44b4671c758466e8f5b1d6dd83be6a699157e2a3bb(
    value: typing.Optional[NsxtAlbVirtualServiceHttpSecRulesRuleMatchCriteriaCookie],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5983182719a288ec886ea3c65e33c56e3425d58aefdf11d5c7b0fc1a183def1e(
    *,
    criteria: builtins.str,
    methods: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5d1bac08e245e92e3d0524a04d0cec1ca35855458d8bf7ec90fd92f42b1a7d68(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__78128ae1e50f28d1e298de8b7175e3a6d744b00f4023fec6239f8915d8aec216(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__80f65c853ef62487f226fa6ebbdb1360f598ff6b3baaf23403b01db2977cfb2f(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b04b8313366e9376e40c254a3a4c574d6eb658708709f638b769e637cd6cfc51(
    value: typing.Optional[NsxtAlbVirtualServiceHttpSecRulesRuleMatchCriteriaHttpMethods],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__85b7cb1d15732249d521111cd419bd41a4f9d94a846b654033706fcb220b8253(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__290c87068a95cdec9121283831dc43bcdaed73a22b66824bdd6180d6e818a49e(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[NsxtAlbVirtualServiceHttpSecRulesRuleMatchCriteriaRequestHeaders, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3505529fb166856ad94db7ade2efcd1f296dafa4388986272782e9a55d68188c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e672df2cbd8d40d40199a88a8b838ccc9e75882c7755c29e84c0ebe2da837c3(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b98a945acc6fdcb9b634ce47eb5bd7ceaa713e4e7a89f7199fb25b12ad659de(
    value: typing.Optional[NsxtAlbVirtualServiceHttpSecRulesRuleMatchCriteria],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__423fcee3379b4fbef7c09c20b1af216aa20a8b51834d284a3a1e1027ab60973f(
    *,
    criteria: builtins.str,
    paths: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6eaeec695da8c9eb340c59dd5ade0a231df6e48409173478dd6e37b45d3c636f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eaed05ad49ba6e08c2a90c73d3b6e3193fae8e2c9d929068d78763fb6ce39dca(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9790c3f8393b43cc6c0711b958f397119ca4800f380b8e1a91a6f37a6c6fb390(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed2b8e04762c8fc86017e4410cdf8e852c6206c230b114ab482f9f6f492ce7e2(
    value: typing.Optional[NsxtAlbVirtualServiceHttpSecRulesRuleMatchCriteriaPath],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__602fd539a236f08aa721ad684d3d218c375c2d02085298bd5c527ea239547a69(
    *,
    criteria: builtins.str,
    name: builtins.str,
    values: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7a7ade3d36ca469c8be1d7e7ac33cae288b018948e57a01874fd60c6b736d547(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__13cfa0bb94a23f87805b9147732b8f1bdec9933c67a6e9e22d625bf763a21501(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__704160d123e0ed04ef405a4b97832b48fdfceca203ef68e5d6e202b586e11b81(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__705f0857f6228ac89698c563505bf515456a6a725a751403d514ff59f48faf3e(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__79702c5583ea5dc47506bb93dfed88e7bcb636ccdce2b78d1076ea1bd600e22b(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3715f0e6152bc7ea42cac9c7c8ea3ddb1d146964a1cf4e3ce75f3696cad273a4(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NsxtAlbVirtualServiceHttpSecRulesRuleMatchCriteriaRequestHeaders]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e6e7cec12a6cb05771eadf4036d0c5a7ae079d490ed913a9d446efbf07c4b1a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__830c59f21dfc9ac1754daa66c9cb3cd92831d0149d61c6778064697b3a72ea6a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa9011069daa5691f9d2b208351ffb8487e3991f780340686a10dbc2fa9d3456(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d1742d6ea8498fd1e2763282ce12df5491ab4d03d544946e5dc919416ffc3715(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2cfa39c375ad6b619c1dcaf14641e4898e4990f6c3d9ebdd994ffd92fe01d8c9(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NsxtAlbVirtualServiceHttpSecRulesRuleMatchCriteriaRequestHeaders]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ad7df28a696e124ce7ae649da565f0e58d1611acdc5afc233f90db168b7c019(
    *,
    criteria: builtins.str,
    ports: typing.Sequence[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc303f12dc09aec0e6b03a20ffbcdf3783a8888d879023b2483b43cb3b3217cb(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6158a7dc40185f15a8be2c3e54a8bdb547479b8f1f1217fae49414f34d1b9a34(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__666cbb5811c200287677c536496850290999f8921ff9274a77ecd31c4b848969(
    value: typing.List[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__54f2200ecac396c11e823166094f6a8a1538161bf92546e00922d413a2a75e18(
    value: typing.Optional[NsxtAlbVirtualServiceHttpSecRulesRuleMatchCriteriaServicePorts],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1909d67109a9322403c2afffe937ec281ec56853a17a3e6aebd1a4ef5eadca11(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1400a25a1cd9af1b046fe35baa2bc6bacbb3c7ad005151a87c49834737e01b21(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2065a4ed43a3393f03b031ef081eede105de00cc1ecf4843105e64cee19f23eb(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed5acee29f555a76947123f1368543360c9fc8a26ed162a950f2ea763b04246e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ed8b73df405cc1642d9cedb0ff01bcd7d20489a0803561d2abe384a59da1edc(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NsxtAlbVirtualServiceHttpSecRulesRule]],
) -> None:
    """Type checking stubs"""
    pass
