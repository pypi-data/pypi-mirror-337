'''
# `vcd_nsxt_alb_virtual_service_http_resp_rules`

Refer to the Terraform Registry for docs: [`vcd_nsxt_alb_virtual_service_http_resp_rules`](https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_resp_rules).
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


class NsxtAlbVirtualServiceHttpRespRules(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="vcd.nsxtAlbVirtualServiceHttpRespRules.NsxtAlbVirtualServiceHttpRespRules",
):
    '''Represents a {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_resp_rules vcd_nsxt_alb_virtual_service_http_resp_rules}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        rule: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["NsxtAlbVirtualServiceHttpRespRulesRule", typing.Dict[builtins.str, typing.Any]]]],
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
        '''Create a new {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_resp_rules vcd_nsxt_alb_virtual_service_http_resp_rules} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param rule: rule block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_resp_rules#rule NsxtAlbVirtualServiceHttpRespRules#rule}
        :param virtual_service_id: NSX-T ALB Virtual Service ID. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_resp_rules#virtual_service_id NsxtAlbVirtualServiceHttpRespRules#virtual_service_id}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_resp_rules#id NsxtAlbVirtualServiceHttpRespRules#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1e93eeef6e93221a7712a46a29a6d88b0e4296ae46d1f7af7c5fd7e33d8f0258)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = NsxtAlbVirtualServiceHttpRespRulesConfig(
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
        '''Generates CDKTF code for importing a NsxtAlbVirtualServiceHttpRespRules resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the NsxtAlbVirtualServiceHttpRespRules to import.
        :param import_from_id: The id of the existing NsxtAlbVirtualServiceHttpRespRules that should be imported. Refer to the {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_resp_rules#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the NsxtAlbVirtualServiceHttpRespRules to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__505b44e42f91db7ba016efa2130ff4a05f0471ddb8a5b1a29b55ce777496bc18)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putRule")
    def put_rule(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["NsxtAlbVirtualServiceHttpRespRulesRule", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__369fbc63ad12532e0bbda6e18d254ae47b8c639a077e08cd6c0aec58c8e13b74)
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
    def rule(self) -> "NsxtAlbVirtualServiceHttpRespRulesRuleList":
        return typing.cast("NsxtAlbVirtualServiceHttpRespRulesRuleList", jsii.get(self, "rule"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="ruleInput")
    def rule_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["NsxtAlbVirtualServiceHttpRespRulesRule"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["NsxtAlbVirtualServiceHttpRespRulesRule"]]], jsii.get(self, "ruleInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__801bc3787d22ad161cf6b92a27f0060b256387758ff752f6fddd8c434decbb19)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="virtualServiceId")
    def virtual_service_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "virtualServiceId"))

    @virtual_service_id.setter
    def virtual_service_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8224dcadbbb461308d03f66e5045075ec517ef2ed5a8e7d1f7f67fc7a58007e7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "virtualServiceId", value)


@jsii.data_type(
    jsii_type="vcd.nsxtAlbVirtualServiceHttpRespRules.NsxtAlbVirtualServiceHttpRespRulesConfig",
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
class NsxtAlbVirtualServiceHttpRespRulesConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        rule: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["NsxtAlbVirtualServiceHttpRespRulesRule", typing.Dict[builtins.str, typing.Any]]]],
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
        :param rule: rule block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_resp_rules#rule NsxtAlbVirtualServiceHttpRespRules#rule}
        :param virtual_service_id: NSX-T ALB Virtual Service ID. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_resp_rules#virtual_service_id NsxtAlbVirtualServiceHttpRespRules#virtual_service_id}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_resp_rules#id NsxtAlbVirtualServiceHttpRespRules#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__72a54bd19a903e366ff57d92833ac40b635375ac7c79e118fd24377146fd984b)
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
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["NsxtAlbVirtualServiceHttpRespRulesRule"]]:
        '''rule block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_resp_rules#rule NsxtAlbVirtualServiceHttpRespRules#rule}
        '''
        result = self._values.get("rule")
        assert result is not None, "Required property 'rule' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["NsxtAlbVirtualServiceHttpRespRulesRule"]], result)

    @builtins.property
    def virtual_service_id(self) -> builtins.str:
        '''NSX-T ALB Virtual Service ID.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_resp_rules#virtual_service_id NsxtAlbVirtualServiceHttpRespRules#virtual_service_id}
        '''
        result = self._values.get("virtual_service_id")
        assert result is not None, "Required property 'virtual_service_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_resp_rules#id NsxtAlbVirtualServiceHttpRespRules#id}.

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
        return "NsxtAlbVirtualServiceHttpRespRulesConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="vcd.nsxtAlbVirtualServiceHttpRespRules.NsxtAlbVirtualServiceHttpRespRulesRule",
    jsii_struct_bases=[],
    name_mapping={
        "actions": "actions",
        "match_criteria": "matchCriteria",
        "name": "name",
        "active": "active",
        "logging": "logging",
    },
)
class NsxtAlbVirtualServiceHttpRespRulesRule:
    def __init__(
        self,
        *,
        actions: typing.Union["NsxtAlbVirtualServiceHttpRespRulesRuleActions", typing.Dict[builtins.str, typing.Any]],
        match_criteria: typing.Union["NsxtAlbVirtualServiceHttpRespRulesRuleMatchCriteria", typing.Dict[builtins.str, typing.Any]],
        name: builtins.str,
        active: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        logging: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param actions: actions block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_resp_rules#actions NsxtAlbVirtualServiceHttpRespRules#actions}
        :param match_criteria: match_criteria block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_resp_rules#match_criteria NsxtAlbVirtualServiceHttpRespRules#match_criteria}
        :param name: Name of the rule. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_resp_rules#name NsxtAlbVirtualServiceHttpRespRules#name}
        :param active: Defines if the rule is active or not. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_resp_rules#active NsxtAlbVirtualServiceHttpRespRules#active}
        :param logging: Defines whether to enable logging with headers on rule match or not. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_resp_rules#logging NsxtAlbVirtualServiceHttpRespRules#logging}
        '''
        if isinstance(actions, dict):
            actions = NsxtAlbVirtualServiceHttpRespRulesRuleActions(**actions)
        if isinstance(match_criteria, dict):
            match_criteria = NsxtAlbVirtualServiceHttpRespRulesRuleMatchCriteria(**match_criteria)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0bfe42c3e56e02a383811a27251e50357e965479d025e68c6a26592bf41ca20c)
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
    def actions(self) -> "NsxtAlbVirtualServiceHttpRespRulesRuleActions":
        '''actions block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_resp_rules#actions NsxtAlbVirtualServiceHttpRespRules#actions}
        '''
        result = self._values.get("actions")
        assert result is not None, "Required property 'actions' is missing"
        return typing.cast("NsxtAlbVirtualServiceHttpRespRulesRuleActions", result)

    @builtins.property
    def match_criteria(self) -> "NsxtAlbVirtualServiceHttpRespRulesRuleMatchCriteria":
        '''match_criteria block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_resp_rules#match_criteria NsxtAlbVirtualServiceHttpRespRules#match_criteria}
        '''
        result = self._values.get("match_criteria")
        assert result is not None, "Required property 'match_criteria' is missing"
        return typing.cast("NsxtAlbVirtualServiceHttpRespRulesRuleMatchCriteria", result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Name of the rule.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_resp_rules#name NsxtAlbVirtualServiceHttpRespRules#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def active(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Defines if the rule is active or not.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_resp_rules#active NsxtAlbVirtualServiceHttpRespRules#active}
        '''
        result = self._values.get("active")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def logging(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Defines whether to enable logging with headers on rule match or not.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_resp_rules#logging NsxtAlbVirtualServiceHttpRespRules#logging}
        '''
        result = self._values.get("logging")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NsxtAlbVirtualServiceHttpRespRulesRule(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="vcd.nsxtAlbVirtualServiceHttpRespRules.NsxtAlbVirtualServiceHttpRespRulesRuleActions",
    jsii_struct_bases=[],
    name_mapping={
        "modify_header": "modifyHeader",
        "rewrite_location_header": "rewriteLocationHeader",
    },
)
class NsxtAlbVirtualServiceHttpRespRulesRuleActions:
    def __init__(
        self,
        *,
        modify_header: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["NsxtAlbVirtualServiceHttpRespRulesRuleActionsModifyHeader", typing.Dict[builtins.str, typing.Any]]]]] = None,
        rewrite_location_header: typing.Optional[typing.Union["NsxtAlbVirtualServiceHttpRespRulesRuleActionsRewriteLocationHeader", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param modify_header: modify_header block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_resp_rules#modify_header NsxtAlbVirtualServiceHttpRespRules#modify_header}
        :param rewrite_location_header: rewrite_location_header block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_resp_rules#rewrite_location_header NsxtAlbVirtualServiceHttpRespRules#rewrite_location_header}
        '''
        if isinstance(rewrite_location_header, dict):
            rewrite_location_header = NsxtAlbVirtualServiceHttpRespRulesRuleActionsRewriteLocationHeader(**rewrite_location_header)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3e3a18e1cea62902490b550d53bfe31fe5c4c28859dd524c20cb83c185235a5b)
            check_type(argname="argument modify_header", value=modify_header, expected_type=type_hints["modify_header"])
            check_type(argname="argument rewrite_location_header", value=rewrite_location_header, expected_type=type_hints["rewrite_location_header"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if modify_header is not None:
            self._values["modify_header"] = modify_header
        if rewrite_location_header is not None:
            self._values["rewrite_location_header"] = rewrite_location_header

    @builtins.property
    def modify_header(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["NsxtAlbVirtualServiceHttpRespRulesRuleActionsModifyHeader"]]]:
        '''modify_header block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_resp_rules#modify_header NsxtAlbVirtualServiceHttpRespRules#modify_header}
        '''
        result = self._values.get("modify_header")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["NsxtAlbVirtualServiceHttpRespRulesRuleActionsModifyHeader"]]], result)

    @builtins.property
    def rewrite_location_header(
        self,
    ) -> typing.Optional["NsxtAlbVirtualServiceHttpRespRulesRuleActionsRewriteLocationHeader"]:
        '''rewrite_location_header block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_resp_rules#rewrite_location_header NsxtAlbVirtualServiceHttpRespRules#rewrite_location_header}
        '''
        result = self._values.get("rewrite_location_header")
        return typing.cast(typing.Optional["NsxtAlbVirtualServiceHttpRespRulesRuleActionsRewriteLocationHeader"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NsxtAlbVirtualServiceHttpRespRulesRuleActions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="vcd.nsxtAlbVirtualServiceHttpRespRules.NsxtAlbVirtualServiceHttpRespRulesRuleActionsModifyHeader",
    jsii_struct_bases=[],
    name_mapping={"action": "action", "name": "name", "value": "value"},
)
class NsxtAlbVirtualServiceHttpRespRulesRuleActionsModifyHeader:
    def __init__(
        self,
        *,
        action: builtins.str,
        name: builtins.str,
        value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param action: One of the following HTTP header actions. Options - ADD, REMOVE, REPLACE. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_resp_rules#action NsxtAlbVirtualServiceHttpRespRules#action}
        :param name: HTTP header name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_resp_rules#name NsxtAlbVirtualServiceHttpRespRules#name}
        :param value: HTTP header value. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_resp_rules#value NsxtAlbVirtualServiceHttpRespRules#value}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e1c7d23999d9f256b2761f47d79e043fbdc0d7aa954ff7279ed3bd5f51df9b46)
            check_type(argname="argument action", value=action, expected_type=type_hints["action"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "action": action,
            "name": name,
        }
        if value is not None:
            self._values["value"] = value

    @builtins.property
    def action(self) -> builtins.str:
        '''One of the following HTTP header actions. Options - ADD, REMOVE, REPLACE.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_resp_rules#action NsxtAlbVirtualServiceHttpRespRules#action}
        '''
        result = self._values.get("action")
        assert result is not None, "Required property 'action' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''HTTP header name.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_resp_rules#name NsxtAlbVirtualServiceHttpRespRules#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> typing.Optional[builtins.str]:
        '''HTTP header value.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_resp_rules#value NsxtAlbVirtualServiceHttpRespRules#value}
        '''
        result = self._values.get("value")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NsxtAlbVirtualServiceHttpRespRulesRuleActionsModifyHeader(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class NsxtAlbVirtualServiceHttpRespRulesRuleActionsModifyHeaderList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="vcd.nsxtAlbVirtualServiceHttpRespRules.NsxtAlbVirtualServiceHttpRespRulesRuleActionsModifyHeaderList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__418e133dad57c7d861c96988e341403cd749e33b0864028eb5048cba1a3b463d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "NsxtAlbVirtualServiceHttpRespRulesRuleActionsModifyHeaderOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__24421a291e443551e591ec28bbdced4635752f100fc0d09659155f26c66a6182)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("NsxtAlbVirtualServiceHttpRespRulesRuleActionsModifyHeaderOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__44583dfb97a1601a3252487de7e30442450902c642427b42edbf3d76e763cc28)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5ed11c3c1baea1a8cdd2c2451df720515042355f0cff9db99e7e0614e1c9d644)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5fde7890512ba78efc3fa4379c6f65496d02b54b290f1bfba9ae7f6f5005f67d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NsxtAlbVirtualServiceHttpRespRulesRuleActionsModifyHeader]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NsxtAlbVirtualServiceHttpRespRulesRuleActionsModifyHeader]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NsxtAlbVirtualServiceHttpRespRulesRuleActionsModifyHeader]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1d69325acee440b9c20cd1201a7083042db50b85bbc3d9e5c4b9e5153688a765)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class NsxtAlbVirtualServiceHttpRespRulesRuleActionsModifyHeaderOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="vcd.nsxtAlbVirtualServiceHttpRespRules.NsxtAlbVirtualServiceHttpRespRulesRuleActionsModifyHeaderOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2ad67dca77b4006fe8d7ef36b2fde003518ba6110269c900b15c6fa43e997b36)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetValue")
    def reset_value(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetValue", []))

    @builtins.property
    @jsii.member(jsii_name="actionInput")
    def action_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "actionInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="valueInput")
    def value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "valueInput"))

    @builtins.property
    @jsii.member(jsii_name="action")
    def action(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "action"))

    @action.setter
    def action(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8f515157e000d3743d0d883f7cee0d9f60fa5758a62b1dab5e45f6757bf2dd71)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "action", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9289fb046fc3a2a5cce7a17ef9637a6cbad189f4f4fa0346fedd9d044d4bee28)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a9a1baa2f3fba7ee8ab83600423b9e3c4ecf6329f79b9fe43ad8e70c9d625092)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NsxtAlbVirtualServiceHttpRespRulesRuleActionsModifyHeader]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NsxtAlbVirtualServiceHttpRespRulesRuleActionsModifyHeader]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NsxtAlbVirtualServiceHttpRespRulesRuleActionsModifyHeader]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f06289aecb7bb9e6cccee5a2de4f43223dacbe7150aca3af49697dcc2422f7dc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class NsxtAlbVirtualServiceHttpRespRulesRuleActionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="vcd.nsxtAlbVirtualServiceHttpRespRules.NsxtAlbVirtualServiceHttpRespRulesRuleActionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a89bab0028f21fcf4d527d3da9fb0dea8b74b8bb7ef4806015c456e196c0307b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putModifyHeader")
    def put_modify_header(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[NsxtAlbVirtualServiceHttpRespRulesRuleActionsModifyHeader, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d2789cf2a4b6b305b9629b94066da8946672c8893ce1c8da04440080723efe25)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putModifyHeader", [value]))

    @jsii.member(jsii_name="putRewriteLocationHeader")
    def put_rewrite_location_header(
        self,
        *,
        port: builtins.str,
        protocol: builtins.str,
        host: typing.Optional[builtins.str] = None,
        keep_query: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        path: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param port: Port to which redirect the request. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_resp_rules#port NsxtAlbVirtualServiceHttpRespRules#port}
        :param protocol: HTTP or HTTPS protocol. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_resp_rules#protocol NsxtAlbVirtualServiceHttpRespRules#protocol}
        :param host: Host to which redirect the request. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_resp_rules#host NsxtAlbVirtualServiceHttpRespRules#host}
        :param keep_query: Should the query part be preserved. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_resp_rules#keep_query NsxtAlbVirtualServiceHttpRespRules#keep_query}
        :param path: Path to which redirect the request. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_resp_rules#path NsxtAlbVirtualServiceHttpRespRules#path}
        '''
        value = NsxtAlbVirtualServiceHttpRespRulesRuleActionsRewriteLocationHeader(
            port=port, protocol=protocol, host=host, keep_query=keep_query, path=path
        )

        return typing.cast(None, jsii.invoke(self, "putRewriteLocationHeader", [value]))

    @jsii.member(jsii_name="resetModifyHeader")
    def reset_modify_header(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetModifyHeader", []))

    @jsii.member(jsii_name="resetRewriteLocationHeader")
    def reset_rewrite_location_header(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRewriteLocationHeader", []))

    @builtins.property
    @jsii.member(jsii_name="modifyHeader")
    def modify_header(
        self,
    ) -> NsxtAlbVirtualServiceHttpRespRulesRuleActionsModifyHeaderList:
        return typing.cast(NsxtAlbVirtualServiceHttpRespRulesRuleActionsModifyHeaderList, jsii.get(self, "modifyHeader"))

    @builtins.property
    @jsii.member(jsii_name="rewriteLocationHeader")
    def rewrite_location_header(
        self,
    ) -> "NsxtAlbVirtualServiceHttpRespRulesRuleActionsRewriteLocationHeaderOutputReference":
        return typing.cast("NsxtAlbVirtualServiceHttpRespRulesRuleActionsRewriteLocationHeaderOutputReference", jsii.get(self, "rewriteLocationHeader"))

    @builtins.property
    @jsii.member(jsii_name="modifyHeaderInput")
    def modify_header_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NsxtAlbVirtualServiceHttpRespRulesRuleActionsModifyHeader]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NsxtAlbVirtualServiceHttpRespRulesRuleActionsModifyHeader]]], jsii.get(self, "modifyHeaderInput"))

    @builtins.property
    @jsii.member(jsii_name="rewriteLocationHeaderInput")
    def rewrite_location_header_input(
        self,
    ) -> typing.Optional["NsxtAlbVirtualServiceHttpRespRulesRuleActionsRewriteLocationHeader"]:
        return typing.cast(typing.Optional["NsxtAlbVirtualServiceHttpRespRulesRuleActionsRewriteLocationHeader"], jsii.get(self, "rewriteLocationHeaderInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[NsxtAlbVirtualServiceHttpRespRulesRuleActions]:
        return typing.cast(typing.Optional[NsxtAlbVirtualServiceHttpRespRulesRuleActions], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[NsxtAlbVirtualServiceHttpRespRulesRuleActions],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__488c78fcd667efb9d73bd731c01ef27e086ba07b5d8006b12f52ce1dc4e8c2f4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="vcd.nsxtAlbVirtualServiceHttpRespRules.NsxtAlbVirtualServiceHttpRespRulesRuleActionsRewriteLocationHeader",
    jsii_struct_bases=[],
    name_mapping={
        "port": "port",
        "protocol": "protocol",
        "host": "host",
        "keep_query": "keepQuery",
        "path": "path",
    },
)
class NsxtAlbVirtualServiceHttpRespRulesRuleActionsRewriteLocationHeader:
    def __init__(
        self,
        *,
        port: builtins.str,
        protocol: builtins.str,
        host: typing.Optional[builtins.str] = None,
        keep_query: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        path: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param port: Port to which redirect the request. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_resp_rules#port NsxtAlbVirtualServiceHttpRespRules#port}
        :param protocol: HTTP or HTTPS protocol. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_resp_rules#protocol NsxtAlbVirtualServiceHttpRespRules#protocol}
        :param host: Host to which redirect the request. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_resp_rules#host NsxtAlbVirtualServiceHttpRespRules#host}
        :param keep_query: Should the query part be preserved. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_resp_rules#keep_query NsxtAlbVirtualServiceHttpRespRules#keep_query}
        :param path: Path to which redirect the request. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_resp_rules#path NsxtAlbVirtualServiceHttpRespRules#path}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__74456f32d0cb74d158b582574af125fcca2bdbf2b5088b8e9e9e15c18e8b8a26)
            check_type(argname="argument port", value=port, expected_type=type_hints["port"])
            check_type(argname="argument protocol", value=protocol, expected_type=type_hints["protocol"])
            check_type(argname="argument host", value=host, expected_type=type_hints["host"])
            check_type(argname="argument keep_query", value=keep_query, expected_type=type_hints["keep_query"])
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "port": port,
            "protocol": protocol,
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_resp_rules#port NsxtAlbVirtualServiceHttpRespRules#port}
        '''
        result = self._values.get("port")
        assert result is not None, "Required property 'port' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def protocol(self) -> builtins.str:
        '''HTTP or HTTPS protocol.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_resp_rules#protocol NsxtAlbVirtualServiceHttpRespRules#protocol}
        '''
        result = self._values.get("protocol")
        assert result is not None, "Required property 'protocol' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def host(self) -> typing.Optional[builtins.str]:
        '''Host to which redirect the request.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_resp_rules#host NsxtAlbVirtualServiceHttpRespRules#host}
        '''
        result = self._values.get("host")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def keep_query(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Should the query part be preserved.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_resp_rules#keep_query NsxtAlbVirtualServiceHttpRespRules#keep_query}
        '''
        result = self._values.get("keep_query")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def path(self) -> typing.Optional[builtins.str]:
        '''Path to which redirect the request.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_resp_rules#path NsxtAlbVirtualServiceHttpRespRules#path}
        '''
        result = self._values.get("path")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NsxtAlbVirtualServiceHttpRespRulesRuleActionsRewriteLocationHeader(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class NsxtAlbVirtualServiceHttpRespRulesRuleActionsRewriteLocationHeaderOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="vcd.nsxtAlbVirtualServiceHttpRespRules.NsxtAlbVirtualServiceHttpRespRulesRuleActionsRewriteLocationHeaderOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ecb87e122a1070f12110ce6ecf9a4da0b11b93fcc9f4f929373498c3bf462f33)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

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
    @jsii.member(jsii_name="host")
    def host(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "host"))

    @host.setter
    def host(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__18d3b51901c48e4c062700dc7ccf4d0c3ff7a66e616f39aabf31311668f007e9)
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
            type_hints = typing.get_type_hints(_typecheckingstub__126120cb9fab731357e3aa4762f7d7dba8bd1c14cdb2719c02f1b7ba88ae3017)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "keepQuery", value)

    @builtins.property
    @jsii.member(jsii_name="path")
    def path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "path"))

    @path.setter
    def path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__668af1f155ca400b0840ca1250346553181bae7ed517b42e4cf6d82b3f40f010)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "path", value)

    @builtins.property
    @jsii.member(jsii_name="port")
    def port(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "port"))

    @port.setter
    def port(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__de229e1e1235d261062dd6c8aa76d5891a5151b708557db5c7405f4907267611)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "port", value)

    @builtins.property
    @jsii.member(jsii_name="protocol")
    def protocol(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "protocol"))

    @protocol.setter
    def protocol(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2e4354f39a706b55584562b33fcdc7af945dad42f14a09b1878dcec8a1564193)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "protocol", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[NsxtAlbVirtualServiceHttpRespRulesRuleActionsRewriteLocationHeader]:
        return typing.cast(typing.Optional[NsxtAlbVirtualServiceHttpRespRulesRuleActionsRewriteLocationHeader], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[NsxtAlbVirtualServiceHttpRespRulesRuleActionsRewriteLocationHeader],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2f9f00bd79b5497f809a9f99988d654c40ff6e4eb31a352be53a39a0dd616b2d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class NsxtAlbVirtualServiceHttpRespRulesRuleList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="vcd.nsxtAlbVirtualServiceHttpRespRules.NsxtAlbVirtualServiceHttpRespRulesRuleList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__10cef74aecc6fd3236efe882d130c18816fbbbd1d5c7171270aeaf39e13a1b3b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "NsxtAlbVirtualServiceHttpRespRulesRuleOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b575cd57bf8dace6da2a53f2f6ebed0ea8136457aae76148dc592eb89be9a5b8)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("NsxtAlbVirtualServiceHttpRespRulesRuleOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dc2f156044a92288296f6b8c29c8278d8e30efa568c0f69bf73aaa79e0490b6a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__801aef5770551fd0095036181b49fb1f13ddc6ae313fb731382450801e56f3a4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b1899298cfe45d3f3e3f171bfa937bf482d922f755ad83532b1d9cbcb5b92175)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NsxtAlbVirtualServiceHttpRespRulesRule]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NsxtAlbVirtualServiceHttpRespRulesRule]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NsxtAlbVirtualServiceHttpRespRulesRule]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__15cda5f6bed6bbf972cda09c5f35431984976640dfb84d63ba5d057e435bb3dd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="vcd.nsxtAlbVirtualServiceHttpRespRules.NsxtAlbVirtualServiceHttpRespRulesRuleMatchCriteria",
    jsii_struct_bases=[],
    name_mapping={
        "client_ip_address": "clientIpAddress",
        "cookie": "cookie",
        "http_methods": "httpMethods",
        "location_header": "locationHeader",
        "path": "path",
        "protocol_type": "protocolType",
        "query": "query",
        "request_headers": "requestHeaders",
        "response_headers": "responseHeaders",
        "service_ports": "servicePorts",
        "status_code": "statusCode",
    },
)
class NsxtAlbVirtualServiceHttpRespRulesRuleMatchCriteria:
    def __init__(
        self,
        *,
        client_ip_address: typing.Optional[typing.Union["NsxtAlbVirtualServiceHttpRespRulesRuleMatchCriteriaClientIpAddress", typing.Dict[builtins.str, typing.Any]]] = None,
        cookie: typing.Optional[typing.Union["NsxtAlbVirtualServiceHttpRespRulesRuleMatchCriteriaCookie", typing.Dict[builtins.str, typing.Any]]] = None,
        http_methods: typing.Optional[typing.Union["NsxtAlbVirtualServiceHttpRespRulesRuleMatchCriteriaHttpMethods", typing.Dict[builtins.str, typing.Any]]] = None,
        location_header: typing.Optional[typing.Union["NsxtAlbVirtualServiceHttpRespRulesRuleMatchCriteriaLocationHeader", typing.Dict[builtins.str, typing.Any]]] = None,
        path: typing.Optional[typing.Union["NsxtAlbVirtualServiceHttpRespRulesRuleMatchCriteriaPath", typing.Dict[builtins.str, typing.Any]]] = None,
        protocol_type: typing.Optional[builtins.str] = None,
        query: typing.Optional[typing.Sequence[builtins.str]] = None,
        request_headers: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["NsxtAlbVirtualServiceHttpRespRulesRuleMatchCriteriaRequestHeaders", typing.Dict[builtins.str, typing.Any]]]]] = None,
        response_headers: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["NsxtAlbVirtualServiceHttpRespRulesRuleMatchCriteriaResponseHeaders", typing.Dict[builtins.str, typing.Any]]]]] = None,
        service_ports: typing.Optional[typing.Union["NsxtAlbVirtualServiceHttpRespRulesRuleMatchCriteriaServicePorts", typing.Dict[builtins.str, typing.Any]]] = None,
        status_code: typing.Optional[typing.Union["NsxtAlbVirtualServiceHttpRespRulesRuleMatchCriteriaStatusCode", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param client_ip_address: client_ip_address block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_resp_rules#client_ip_address NsxtAlbVirtualServiceHttpRespRules#client_ip_address}
        :param cookie: cookie block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_resp_rules#cookie NsxtAlbVirtualServiceHttpRespRules#cookie}
        :param http_methods: http_methods block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_resp_rules#http_methods NsxtAlbVirtualServiceHttpRespRules#http_methods}
        :param location_header: location_header block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_resp_rules#location_header NsxtAlbVirtualServiceHttpRespRules#location_header}
        :param path: path block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_resp_rules#path NsxtAlbVirtualServiceHttpRespRules#path}
        :param protocol_type: Protocol to match - 'HTTP' or 'HTTPS'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_resp_rules#protocol_type NsxtAlbVirtualServiceHttpRespRules#protocol_type}
        :param query: HTTP request query strings to match. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_resp_rules#query NsxtAlbVirtualServiceHttpRespRules#query}
        :param request_headers: request_headers block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_resp_rules#request_headers NsxtAlbVirtualServiceHttpRespRules#request_headers}
        :param response_headers: response_headers block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_resp_rules#response_headers NsxtAlbVirtualServiceHttpRespRules#response_headers}
        :param service_ports: service_ports block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_resp_rules#service_ports NsxtAlbVirtualServiceHttpRespRules#service_ports}
        :param status_code: status_code block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_resp_rules#status_code NsxtAlbVirtualServiceHttpRespRules#status_code}
        '''
        if isinstance(client_ip_address, dict):
            client_ip_address = NsxtAlbVirtualServiceHttpRespRulesRuleMatchCriteriaClientIpAddress(**client_ip_address)
        if isinstance(cookie, dict):
            cookie = NsxtAlbVirtualServiceHttpRespRulesRuleMatchCriteriaCookie(**cookie)
        if isinstance(http_methods, dict):
            http_methods = NsxtAlbVirtualServiceHttpRespRulesRuleMatchCriteriaHttpMethods(**http_methods)
        if isinstance(location_header, dict):
            location_header = NsxtAlbVirtualServiceHttpRespRulesRuleMatchCriteriaLocationHeader(**location_header)
        if isinstance(path, dict):
            path = NsxtAlbVirtualServiceHttpRespRulesRuleMatchCriteriaPath(**path)
        if isinstance(service_ports, dict):
            service_ports = NsxtAlbVirtualServiceHttpRespRulesRuleMatchCriteriaServicePorts(**service_ports)
        if isinstance(status_code, dict):
            status_code = NsxtAlbVirtualServiceHttpRespRulesRuleMatchCriteriaStatusCode(**status_code)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cfd79fb675b980a21f40544248ddef82d3da488eb3c8cfc0f42836b7309461de)
            check_type(argname="argument client_ip_address", value=client_ip_address, expected_type=type_hints["client_ip_address"])
            check_type(argname="argument cookie", value=cookie, expected_type=type_hints["cookie"])
            check_type(argname="argument http_methods", value=http_methods, expected_type=type_hints["http_methods"])
            check_type(argname="argument location_header", value=location_header, expected_type=type_hints["location_header"])
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
            check_type(argname="argument protocol_type", value=protocol_type, expected_type=type_hints["protocol_type"])
            check_type(argname="argument query", value=query, expected_type=type_hints["query"])
            check_type(argname="argument request_headers", value=request_headers, expected_type=type_hints["request_headers"])
            check_type(argname="argument response_headers", value=response_headers, expected_type=type_hints["response_headers"])
            check_type(argname="argument service_ports", value=service_ports, expected_type=type_hints["service_ports"])
            check_type(argname="argument status_code", value=status_code, expected_type=type_hints["status_code"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if client_ip_address is not None:
            self._values["client_ip_address"] = client_ip_address
        if cookie is not None:
            self._values["cookie"] = cookie
        if http_methods is not None:
            self._values["http_methods"] = http_methods
        if location_header is not None:
            self._values["location_header"] = location_header
        if path is not None:
            self._values["path"] = path
        if protocol_type is not None:
            self._values["protocol_type"] = protocol_type
        if query is not None:
            self._values["query"] = query
        if request_headers is not None:
            self._values["request_headers"] = request_headers
        if response_headers is not None:
            self._values["response_headers"] = response_headers
        if service_ports is not None:
            self._values["service_ports"] = service_ports
        if status_code is not None:
            self._values["status_code"] = status_code

    @builtins.property
    def client_ip_address(
        self,
    ) -> typing.Optional["NsxtAlbVirtualServiceHttpRespRulesRuleMatchCriteriaClientIpAddress"]:
        '''client_ip_address block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_resp_rules#client_ip_address NsxtAlbVirtualServiceHttpRespRules#client_ip_address}
        '''
        result = self._values.get("client_ip_address")
        return typing.cast(typing.Optional["NsxtAlbVirtualServiceHttpRespRulesRuleMatchCriteriaClientIpAddress"], result)

    @builtins.property
    def cookie(
        self,
    ) -> typing.Optional["NsxtAlbVirtualServiceHttpRespRulesRuleMatchCriteriaCookie"]:
        '''cookie block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_resp_rules#cookie NsxtAlbVirtualServiceHttpRespRules#cookie}
        '''
        result = self._values.get("cookie")
        return typing.cast(typing.Optional["NsxtAlbVirtualServiceHttpRespRulesRuleMatchCriteriaCookie"], result)

    @builtins.property
    def http_methods(
        self,
    ) -> typing.Optional["NsxtAlbVirtualServiceHttpRespRulesRuleMatchCriteriaHttpMethods"]:
        '''http_methods block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_resp_rules#http_methods NsxtAlbVirtualServiceHttpRespRules#http_methods}
        '''
        result = self._values.get("http_methods")
        return typing.cast(typing.Optional["NsxtAlbVirtualServiceHttpRespRulesRuleMatchCriteriaHttpMethods"], result)

    @builtins.property
    def location_header(
        self,
    ) -> typing.Optional["NsxtAlbVirtualServiceHttpRespRulesRuleMatchCriteriaLocationHeader"]:
        '''location_header block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_resp_rules#location_header NsxtAlbVirtualServiceHttpRespRules#location_header}
        '''
        result = self._values.get("location_header")
        return typing.cast(typing.Optional["NsxtAlbVirtualServiceHttpRespRulesRuleMatchCriteriaLocationHeader"], result)

    @builtins.property
    def path(
        self,
    ) -> typing.Optional["NsxtAlbVirtualServiceHttpRespRulesRuleMatchCriteriaPath"]:
        '''path block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_resp_rules#path NsxtAlbVirtualServiceHttpRespRules#path}
        '''
        result = self._values.get("path")
        return typing.cast(typing.Optional["NsxtAlbVirtualServiceHttpRespRulesRuleMatchCriteriaPath"], result)

    @builtins.property
    def protocol_type(self) -> typing.Optional[builtins.str]:
        '''Protocol to match - 'HTTP' or 'HTTPS'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_resp_rules#protocol_type NsxtAlbVirtualServiceHttpRespRules#protocol_type}
        '''
        result = self._values.get("protocol_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def query(self) -> typing.Optional[typing.List[builtins.str]]:
        '''HTTP request query strings to match.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_resp_rules#query NsxtAlbVirtualServiceHttpRespRules#query}
        '''
        result = self._values.get("query")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def request_headers(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["NsxtAlbVirtualServiceHttpRespRulesRuleMatchCriteriaRequestHeaders"]]]:
        '''request_headers block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_resp_rules#request_headers NsxtAlbVirtualServiceHttpRespRules#request_headers}
        '''
        result = self._values.get("request_headers")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["NsxtAlbVirtualServiceHttpRespRulesRuleMatchCriteriaRequestHeaders"]]], result)

    @builtins.property
    def response_headers(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["NsxtAlbVirtualServiceHttpRespRulesRuleMatchCriteriaResponseHeaders"]]]:
        '''response_headers block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_resp_rules#response_headers NsxtAlbVirtualServiceHttpRespRules#response_headers}
        '''
        result = self._values.get("response_headers")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["NsxtAlbVirtualServiceHttpRespRulesRuleMatchCriteriaResponseHeaders"]]], result)

    @builtins.property
    def service_ports(
        self,
    ) -> typing.Optional["NsxtAlbVirtualServiceHttpRespRulesRuleMatchCriteriaServicePorts"]:
        '''service_ports block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_resp_rules#service_ports NsxtAlbVirtualServiceHttpRespRules#service_ports}
        '''
        result = self._values.get("service_ports")
        return typing.cast(typing.Optional["NsxtAlbVirtualServiceHttpRespRulesRuleMatchCriteriaServicePorts"], result)

    @builtins.property
    def status_code(
        self,
    ) -> typing.Optional["NsxtAlbVirtualServiceHttpRespRulesRuleMatchCriteriaStatusCode"]:
        '''status_code block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_resp_rules#status_code NsxtAlbVirtualServiceHttpRespRules#status_code}
        '''
        result = self._values.get("status_code")
        return typing.cast(typing.Optional["NsxtAlbVirtualServiceHttpRespRulesRuleMatchCriteriaStatusCode"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NsxtAlbVirtualServiceHttpRespRulesRuleMatchCriteria(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="vcd.nsxtAlbVirtualServiceHttpRespRules.NsxtAlbVirtualServiceHttpRespRulesRuleMatchCriteriaClientIpAddress",
    jsii_struct_bases=[],
    name_mapping={"criteria": "criteria", "ip_addresses": "ipAddresses"},
)
class NsxtAlbVirtualServiceHttpRespRulesRuleMatchCriteriaClientIpAddress:
    def __init__(
        self,
        *,
        criteria: builtins.str,
        ip_addresses: typing.Sequence[builtins.str],
    ) -> None:
        '''
        :param criteria: Criteria to use for IP address matching the HTTP request. Options - IS_IN, IS_NOT_IN. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_resp_rules#criteria NsxtAlbVirtualServiceHttpRespRules#criteria}
        :param ip_addresses: A set of IP addresses. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_resp_rules#ip_addresses NsxtAlbVirtualServiceHttpRespRules#ip_addresses}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b79df52a155703debf15261c9e302b20666a14e801e73262cd10a06d6b2551e9)
            check_type(argname="argument criteria", value=criteria, expected_type=type_hints["criteria"])
            check_type(argname="argument ip_addresses", value=ip_addresses, expected_type=type_hints["ip_addresses"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "criteria": criteria,
            "ip_addresses": ip_addresses,
        }

    @builtins.property
    def criteria(self) -> builtins.str:
        '''Criteria to use for IP address matching the HTTP request. Options - IS_IN, IS_NOT_IN.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_resp_rules#criteria NsxtAlbVirtualServiceHttpRespRules#criteria}
        '''
        result = self._values.get("criteria")
        assert result is not None, "Required property 'criteria' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def ip_addresses(self) -> typing.List[builtins.str]:
        '''A set of IP addresses.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_resp_rules#ip_addresses NsxtAlbVirtualServiceHttpRespRules#ip_addresses}
        '''
        result = self._values.get("ip_addresses")
        assert result is not None, "Required property 'ip_addresses' is missing"
        return typing.cast(typing.List[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NsxtAlbVirtualServiceHttpRespRulesRuleMatchCriteriaClientIpAddress(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class NsxtAlbVirtualServiceHttpRespRulesRuleMatchCriteriaClientIpAddressOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="vcd.nsxtAlbVirtualServiceHttpRespRules.NsxtAlbVirtualServiceHttpRespRulesRuleMatchCriteriaClientIpAddressOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c02fb0e6bab2aa2c949dbe64185cb6d86f8180c216aa813c0af8725287167c01)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ffd2891df488d28afd8f7737f841f1488d500caa900658c27d752814707da952)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "criteria", value)

    @builtins.property
    @jsii.member(jsii_name="ipAddresses")
    def ip_addresses(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "ipAddresses"))

    @ip_addresses.setter
    def ip_addresses(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b6f9ce6e4d5f0361d3f987c0cfdac4d02ef5961d044633769488ff841568751c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ipAddresses", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[NsxtAlbVirtualServiceHttpRespRulesRuleMatchCriteriaClientIpAddress]:
        return typing.cast(typing.Optional[NsxtAlbVirtualServiceHttpRespRulesRuleMatchCriteriaClientIpAddress], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[NsxtAlbVirtualServiceHttpRespRulesRuleMatchCriteriaClientIpAddress],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__71cf34dbd405e944611a529537f572317f9697185388099d80fc179322fa12a6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="vcd.nsxtAlbVirtualServiceHttpRespRules.NsxtAlbVirtualServiceHttpRespRulesRuleMatchCriteriaCookie",
    jsii_struct_bases=[],
    name_mapping={"criteria": "criteria", "name": "name", "value": "value"},
)
class NsxtAlbVirtualServiceHttpRespRulesRuleMatchCriteriaCookie:
    def __init__(
        self,
        *,
        criteria: builtins.str,
        name: builtins.str,
        value: builtins.str,
    ) -> None:
        '''
        :param criteria: Criteria to use for matching cookies in the HTTP request. Options - EXISTS, DOES_NOT_EXIST, BEGINS_WITH, DOES_NOT_BEGIN_WITH, CONTAINS, DOES_NOT_CONTAIN, ENDS_WITH, DOES_NOT_END_WITH, EQUALS, DOES_NOT_EQUAL Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_resp_rules#criteria NsxtAlbVirtualServiceHttpRespRules#criteria}
        :param name: Name of the HTTP cookie whose value is to be matched. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_resp_rules#name NsxtAlbVirtualServiceHttpRespRules#name}
        :param value: String values to match for an HTTP cookie. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_resp_rules#value NsxtAlbVirtualServiceHttpRespRules#value}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__13c846265ff3d0e3196dd753a40258869a07fb461a79c0cdd5c792afd116373d)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_resp_rules#criteria NsxtAlbVirtualServiceHttpRespRules#criteria}
        '''
        result = self._values.get("criteria")
        assert result is not None, "Required property 'criteria' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Name of the HTTP cookie whose value is to be matched.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_resp_rules#name NsxtAlbVirtualServiceHttpRespRules#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> builtins.str:
        '''String values to match for an HTTP cookie.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_resp_rules#value NsxtAlbVirtualServiceHttpRespRules#value}
        '''
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NsxtAlbVirtualServiceHttpRespRulesRuleMatchCriteriaCookie(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class NsxtAlbVirtualServiceHttpRespRulesRuleMatchCriteriaCookieOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="vcd.nsxtAlbVirtualServiceHttpRespRules.NsxtAlbVirtualServiceHttpRespRulesRuleMatchCriteriaCookieOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__cb4626c39d9d2ddf6a3dd902ebd323ede5d422c8f09641e66a13dd4e931bb24e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9030b33e52a7a2d92c1c09f10ba829da8fad03d4032c9cf866baf9931f16fe31)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "criteria", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f5fae20e151e2a11bf81aec58b1552f0de1a241b251acb921a470f64f51b1b9a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c20b1e4131aa919ba737e3f32510d461cea56914a8d38bb2433ff02e708a9691)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[NsxtAlbVirtualServiceHttpRespRulesRuleMatchCriteriaCookie]:
        return typing.cast(typing.Optional[NsxtAlbVirtualServiceHttpRespRulesRuleMatchCriteriaCookie], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[NsxtAlbVirtualServiceHttpRespRulesRuleMatchCriteriaCookie],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3a6cf7966fb622588ceecb3f97c87401ff8a1cd4f9362d227b93fd7419f462fd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="vcd.nsxtAlbVirtualServiceHttpRespRules.NsxtAlbVirtualServiceHttpRespRulesRuleMatchCriteriaHttpMethods",
    jsii_struct_bases=[],
    name_mapping={"criteria": "criteria", "methods": "methods"},
)
class NsxtAlbVirtualServiceHttpRespRulesRuleMatchCriteriaHttpMethods:
    def __init__(
        self,
        *,
        criteria: builtins.str,
        methods: typing.Sequence[builtins.str],
    ) -> None:
        '''
        :param criteria: Criteria to use for IP address matching the HTTP request. Options - IS_IN, IS_NOT_IN. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_resp_rules#criteria NsxtAlbVirtualServiceHttpRespRules#criteria}
        :param methods: HTTP methods to match. Options - GET, PUT, POST, DELETE, HEAD, OPTIONS, TRACE, CONNECT, PATCH, PROPFIND, PROPPATCH, MKCOL, COPY, MOVE, LOCK, UNLOCK Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_resp_rules#methods NsxtAlbVirtualServiceHttpRespRules#methods}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__adbda982c5b277987cc15b6149d11e71a2145f6efc2f56bd5e566d2b44428f55)
            check_type(argname="argument criteria", value=criteria, expected_type=type_hints["criteria"])
            check_type(argname="argument methods", value=methods, expected_type=type_hints["methods"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "criteria": criteria,
            "methods": methods,
        }

    @builtins.property
    def criteria(self) -> builtins.str:
        '''Criteria to use for IP address matching the HTTP request. Options - IS_IN, IS_NOT_IN.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_resp_rules#criteria NsxtAlbVirtualServiceHttpRespRules#criteria}
        '''
        result = self._values.get("criteria")
        assert result is not None, "Required property 'criteria' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def methods(self) -> typing.List[builtins.str]:
        '''HTTP methods to match.

        Options - GET, PUT, POST, DELETE, HEAD, OPTIONS, TRACE, CONNECT, PATCH, PROPFIND, PROPPATCH, MKCOL, COPY, MOVE, LOCK, UNLOCK

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_resp_rules#methods NsxtAlbVirtualServiceHttpRespRules#methods}
        '''
        result = self._values.get("methods")
        assert result is not None, "Required property 'methods' is missing"
        return typing.cast(typing.List[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NsxtAlbVirtualServiceHttpRespRulesRuleMatchCriteriaHttpMethods(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class NsxtAlbVirtualServiceHttpRespRulesRuleMatchCriteriaHttpMethodsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="vcd.nsxtAlbVirtualServiceHttpRespRules.NsxtAlbVirtualServiceHttpRespRulesRuleMatchCriteriaHttpMethodsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fdfcc0ca9aee2a82c33704bbeccb446ff68be82d35ce6d093eefaf6350bf1203)
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
            type_hints = typing.get_type_hints(_typecheckingstub__474988e03530475b23ced2120d0272e90491432f64ecb40b6d56c9889693df31)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "criteria", value)

    @builtins.property
    @jsii.member(jsii_name="methods")
    def methods(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "methods"))

    @methods.setter
    def methods(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d29a7b2afbb326d9172f9fe70107d7758945babf357966ebe64e9e37b355b4db)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "methods", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[NsxtAlbVirtualServiceHttpRespRulesRuleMatchCriteriaHttpMethods]:
        return typing.cast(typing.Optional[NsxtAlbVirtualServiceHttpRespRulesRuleMatchCriteriaHttpMethods], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[NsxtAlbVirtualServiceHttpRespRulesRuleMatchCriteriaHttpMethods],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__70b2bf665ba89faea018ea2add31fba8405c73a7985c3757141aaf1fec37c22a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="vcd.nsxtAlbVirtualServiceHttpRespRules.NsxtAlbVirtualServiceHttpRespRulesRuleMatchCriteriaLocationHeader",
    jsii_struct_bases=[],
    name_mapping={"criteria": "criteria", "values": "values"},
)
class NsxtAlbVirtualServiceHttpRespRulesRuleMatchCriteriaLocationHeader:
    def __init__(
        self,
        *,
        criteria: builtins.str,
        values: typing.Sequence[builtins.str],
    ) -> None:
        '''
        :param criteria: Criteria to use for matching location header. Options - BEGINS_WITH, DOES_NOT_BEGIN_WITH, CONTAINS, DOES_NOT_CONTAIN, ENDS_WITH, DOES_NOT_END_WITH, EQUALS, DOES_NOT_EQUAL, REGEX_MATCH, REGEX_DOES_NOT_MATCH. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_resp_rules#criteria NsxtAlbVirtualServiceHttpRespRules#criteria}
        :param values: A set of values to match for criteria. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_resp_rules#values NsxtAlbVirtualServiceHttpRespRules#values}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7e7c479f8a1ac5e7e56a3269c1ed8ec639db0c12ca7f8f6dc8f958f1d763cb0b)
            check_type(argname="argument criteria", value=criteria, expected_type=type_hints["criteria"])
            check_type(argname="argument values", value=values, expected_type=type_hints["values"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "criteria": criteria,
            "values": values,
        }

    @builtins.property
    def criteria(self) -> builtins.str:
        '''Criteria to use for matching location header. Options - BEGINS_WITH, DOES_NOT_BEGIN_WITH, CONTAINS, DOES_NOT_CONTAIN, ENDS_WITH, DOES_NOT_END_WITH, EQUALS, DOES_NOT_EQUAL, REGEX_MATCH, REGEX_DOES_NOT_MATCH.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_resp_rules#criteria NsxtAlbVirtualServiceHttpRespRules#criteria}
        '''
        result = self._values.get("criteria")
        assert result is not None, "Required property 'criteria' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def values(self) -> typing.List[builtins.str]:
        '''A set of values to match for criteria.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_resp_rules#values NsxtAlbVirtualServiceHttpRespRules#values}
        '''
        result = self._values.get("values")
        assert result is not None, "Required property 'values' is missing"
        return typing.cast(typing.List[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NsxtAlbVirtualServiceHttpRespRulesRuleMatchCriteriaLocationHeader(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class NsxtAlbVirtualServiceHttpRespRulesRuleMatchCriteriaLocationHeaderOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="vcd.nsxtAlbVirtualServiceHttpRespRules.NsxtAlbVirtualServiceHttpRespRulesRuleMatchCriteriaLocationHeaderOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5198f90eb3daf9bb6958c68a61b81ee89c91f1089a55a9e668dc91cb0eb0a46c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="criteriaInput")
    def criteria_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "criteriaInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__4b419fe111ecd4d677f839ab3f10e33ffca7ce8e115a9aa1bf9cfafc2a34fad5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "criteria", value)

    @builtins.property
    @jsii.member(jsii_name="values")
    def values(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "values"))

    @values.setter
    def values(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1c3ab4edddf61d295fed1b21569481f972897887793421f10dc66b6c47a31f48)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "values", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[NsxtAlbVirtualServiceHttpRespRulesRuleMatchCriteriaLocationHeader]:
        return typing.cast(typing.Optional[NsxtAlbVirtualServiceHttpRespRulesRuleMatchCriteriaLocationHeader], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[NsxtAlbVirtualServiceHttpRespRulesRuleMatchCriteriaLocationHeader],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1c027a336ad1daca62a2db9b8ab5f869e00ccfd0df7f79656fc6a01f506f2232)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class NsxtAlbVirtualServiceHttpRespRulesRuleMatchCriteriaOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="vcd.nsxtAlbVirtualServiceHttpRespRules.NsxtAlbVirtualServiceHttpRespRulesRuleMatchCriteriaOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6f741dd2a2c2d4e57017f8e793c32099eb0ffc2ca6d0d9de5fd281a47ed338ff)
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
        :param criteria: Criteria to use for IP address matching the HTTP request. Options - IS_IN, IS_NOT_IN. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_resp_rules#criteria NsxtAlbVirtualServiceHttpRespRules#criteria}
        :param ip_addresses: A set of IP addresses. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_resp_rules#ip_addresses NsxtAlbVirtualServiceHttpRespRules#ip_addresses}
        '''
        value = NsxtAlbVirtualServiceHttpRespRulesRuleMatchCriteriaClientIpAddress(
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
        :param criteria: Criteria to use for matching cookies in the HTTP request. Options - EXISTS, DOES_NOT_EXIST, BEGINS_WITH, DOES_NOT_BEGIN_WITH, CONTAINS, DOES_NOT_CONTAIN, ENDS_WITH, DOES_NOT_END_WITH, EQUALS, DOES_NOT_EQUAL Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_resp_rules#criteria NsxtAlbVirtualServiceHttpRespRules#criteria}
        :param name: Name of the HTTP cookie whose value is to be matched. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_resp_rules#name NsxtAlbVirtualServiceHttpRespRules#name}
        :param value: String values to match for an HTTP cookie. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_resp_rules#value NsxtAlbVirtualServiceHttpRespRules#value}
        '''
        value_ = NsxtAlbVirtualServiceHttpRespRulesRuleMatchCriteriaCookie(
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
        :param criteria: Criteria to use for IP address matching the HTTP request. Options - IS_IN, IS_NOT_IN. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_resp_rules#criteria NsxtAlbVirtualServiceHttpRespRules#criteria}
        :param methods: HTTP methods to match. Options - GET, PUT, POST, DELETE, HEAD, OPTIONS, TRACE, CONNECT, PATCH, PROPFIND, PROPPATCH, MKCOL, COPY, MOVE, LOCK, UNLOCK Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_resp_rules#methods NsxtAlbVirtualServiceHttpRespRules#methods}
        '''
        value = NsxtAlbVirtualServiceHttpRespRulesRuleMatchCriteriaHttpMethods(
            criteria=criteria, methods=methods
        )

        return typing.cast(None, jsii.invoke(self, "putHttpMethods", [value]))

    @jsii.member(jsii_name="putLocationHeader")
    def put_location_header(
        self,
        *,
        criteria: builtins.str,
        values: typing.Sequence[builtins.str],
    ) -> None:
        '''
        :param criteria: Criteria to use for matching location header. Options - BEGINS_WITH, DOES_NOT_BEGIN_WITH, CONTAINS, DOES_NOT_CONTAIN, ENDS_WITH, DOES_NOT_END_WITH, EQUALS, DOES_NOT_EQUAL, REGEX_MATCH, REGEX_DOES_NOT_MATCH. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_resp_rules#criteria NsxtAlbVirtualServiceHttpRespRules#criteria}
        :param values: A set of values to match for criteria. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_resp_rules#values NsxtAlbVirtualServiceHttpRespRules#values}
        '''
        value = NsxtAlbVirtualServiceHttpRespRulesRuleMatchCriteriaLocationHeader(
            criteria=criteria, values=values
        )

        return typing.cast(None, jsii.invoke(self, "putLocationHeader", [value]))

    @jsii.member(jsii_name="putPath")
    def put_path(
        self,
        *,
        criteria: builtins.str,
        paths: typing.Sequence[builtins.str],
    ) -> None:
        '''
        :param criteria: Criteria to use for matching the path in the HTTP request URI. Options - BEGINS_WITH, DOES_NOT_BEGIN_WITH, CONTAINS, DOES_NOT_CONTAIN, ENDS_WITH, DOES_NOT_END_WITH, EQUALS, DOES_NOT_EQUAL, REGEX_MATCH, REGEX_DOES_NOT_MATCH Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_resp_rules#criteria NsxtAlbVirtualServiceHttpRespRules#criteria}
        :param paths: String values to match the path. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_resp_rules#paths NsxtAlbVirtualServiceHttpRespRules#paths}
        '''
        value = NsxtAlbVirtualServiceHttpRespRulesRuleMatchCriteriaPath(
            criteria=criteria, paths=paths
        )

        return typing.cast(None, jsii.invoke(self, "putPath", [value]))

    @jsii.member(jsii_name="putRequestHeaders")
    def put_request_headers(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["NsxtAlbVirtualServiceHttpRespRulesRuleMatchCriteriaRequestHeaders", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__417424f053dfad5e1923d1ba6a8e2201a8f0b9f1a6588b0720292b364397565e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putRequestHeaders", [value]))

    @jsii.member(jsii_name="putResponseHeaders")
    def put_response_headers(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["NsxtAlbVirtualServiceHttpRespRulesRuleMatchCriteriaResponseHeaders", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7600f3c9ea57e870672c24d71a51599da108b6dacba0a7141ba58a2d36438384)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putResponseHeaders", [value]))

    @jsii.member(jsii_name="putServicePorts")
    def put_service_ports(
        self,
        *,
        criteria: builtins.str,
        ports: typing.Sequence[jsii.Number],
    ) -> None:
        '''
        :param criteria: Criteria to use for IP address matching the HTTP request. Options - IS_IN, IS_NOT_IN. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_resp_rules#criteria NsxtAlbVirtualServiceHttpRespRules#criteria}
        :param ports: A set of TCP ports. Allowed values are 1-65535. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_resp_rules#ports NsxtAlbVirtualServiceHttpRespRules#ports}
        '''
        value = NsxtAlbVirtualServiceHttpRespRulesRuleMatchCriteriaServicePorts(
            criteria=criteria, ports=ports
        )

        return typing.cast(None, jsii.invoke(self, "putServicePorts", [value]))

    @jsii.member(jsii_name="putStatusCode")
    def put_status_code(
        self,
        *,
        criteria: builtins.str,
        http_status_code: builtins.str,
    ) -> None:
        '''
        :param criteria: Criteria to use for IP address matching the HTTP request. Options - IS_IN, IS_NOT_IN. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_resp_rules#criteria NsxtAlbVirtualServiceHttpRespRules#criteria}
        :param http_status_code: Enter a http status code or range. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_resp_rules#http_status_code NsxtAlbVirtualServiceHttpRespRules#http_status_code}
        '''
        value = NsxtAlbVirtualServiceHttpRespRulesRuleMatchCriteriaStatusCode(
            criteria=criteria, http_status_code=http_status_code
        )

        return typing.cast(None, jsii.invoke(self, "putStatusCode", [value]))

    @jsii.member(jsii_name="resetClientIpAddress")
    def reset_client_ip_address(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetClientIpAddress", []))

    @jsii.member(jsii_name="resetCookie")
    def reset_cookie(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCookie", []))

    @jsii.member(jsii_name="resetHttpMethods")
    def reset_http_methods(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHttpMethods", []))

    @jsii.member(jsii_name="resetLocationHeader")
    def reset_location_header(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLocationHeader", []))

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

    @jsii.member(jsii_name="resetResponseHeaders")
    def reset_response_headers(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetResponseHeaders", []))

    @jsii.member(jsii_name="resetServicePorts")
    def reset_service_ports(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetServicePorts", []))

    @jsii.member(jsii_name="resetStatusCode")
    def reset_status_code(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStatusCode", []))

    @builtins.property
    @jsii.member(jsii_name="clientIpAddress")
    def client_ip_address(
        self,
    ) -> NsxtAlbVirtualServiceHttpRespRulesRuleMatchCriteriaClientIpAddressOutputReference:
        return typing.cast(NsxtAlbVirtualServiceHttpRespRulesRuleMatchCriteriaClientIpAddressOutputReference, jsii.get(self, "clientIpAddress"))

    @builtins.property
    @jsii.member(jsii_name="cookie")
    def cookie(
        self,
    ) -> NsxtAlbVirtualServiceHttpRespRulesRuleMatchCriteriaCookieOutputReference:
        return typing.cast(NsxtAlbVirtualServiceHttpRespRulesRuleMatchCriteriaCookieOutputReference, jsii.get(self, "cookie"))

    @builtins.property
    @jsii.member(jsii_name="httpMethods")
    def http_methods(
        self,
    ) -> NsxtAlbVirtualServiceHttpRespRulesRuleMatchCriteriaHttpMethodsOutputReference:
        return typing.cast(NsxtAlbVirtualServiceHttpRespRulesRuleMatchCriteriaHttpMethodsOutputReference, jsii.get(self, "httpMethods"))

    @builtins.property
    @jsii.member(jsii_name="locationHeader")
    def location_header(
        self,
    ) -> NsxtAlbVirtualServiceHttpRespRulesRuleMatchCriteriaLocationHeaderOutputReference:
        return typing.cast(NsxtAlbVirtualServiceHttpRespRulesRuleMatchCriteriaLocationHeaderOutputReference, jsii.get(self, "locationHeader"))

    @builtins.property
    @jsii.member(jsii_name="path")
    def path(
        self,
    ) -> "NsxtAlbVirtualServiceHttpRespRulesRuleMatchCriteriaPathOutputReference":
        return typing.cast("NsxtAlbVirtualServiceHttpRespRulesRuleMatchCriteriaPathOutputReference", jsii.get(self, "path"))

    @builtins.property
    @jsii.member(jsii_name="requestHeaders")
    def request_headers(
        self,
    ) -> "NsxtAlbVirtualServiceHttpRespRulesRuleMatchCriteriaRequestHeadersList":
        return typing.cast("NsxtAlbVirtualServiceHttpRespRulesRuleMatchCriteriaRequestHeadersList", jsii.get(self, "requestHeaders"))

    @builtins.property
    @jsii.member(jsii_name="responseHeaders")
    def response_headers(
        self,
    ) -> "NsxtAlbVirtualServiceHttpRespRulesRuleMatchCriteriaResponseHeadersList":
        return typing.cast("NsxtAlbVirtualServiceHttpRespRulesRuleMatchCriteriaResponseHeadersList", jsii.get(self, "responseHeaders"))

    @builtins.property
    @jsii.member(jsii_name="servicePorts")
    def service_ports(
        self,
    ) -> "NsxtAlbVirtualServiceHttpRespRulesRuleMatchCriteriaServicePortsOutputReference":
        return typing.cast("NsxtAlbVirtualServiceHttpRespRulesRuleMatchCriteriaServicePortsOutputReference", jsii.get(self, "servicePorts"))

    @builtins.property
    @jsii.member(jsii_name="statusCode")
    def status_code(
        self,
    ) -> "NsxtAlbVirtualServiceHttpRespRulesRuleMatchCriteriaStatusCodeOutputReference":
        return typing.cast("NsxtAlbVirtualServiceHttpRespRulesRuleMatchCriteriaStatusCodeOutputReference", jsii.get(self, "statusCode"))

    @builtins.property
    @jsii.member(jsii_name="clientIpAddressInput")
    def client_ip_address_input(
        self,
    ) -> typing.Optional[NsxtAlbVirtualServiceHttpRespRulesRuleMatchCriteriaClientIpAddress]:
        return typing.cast(typing.Optional[NsxtAlbVirtualServiceHttpRespRulesRuleMatchCriteriaClientIpAddress], jsii.get(self, "clientIpAddressInput"))

    @builtins.property
    @jsii.member(jsii_name="cookieInput")
    def cookie_input(
        self,
    ) -> typing.Optional[NsxtAlbVirtualServiceHttpRespRulesRuleMatchCriteriaCookie]:
        return typing.cast(typing.Optional[NsxtAlbVirtualServiceHttpRespRulesRuleMatchCriteriaCookie], jsii.get(self, "cookieInput"))

    @builtins.property
    @jsii.member(jsii_name="httpMethodsInput")
    def http_methods_input(
        self,
    ) -> typing.Optional[NsxtAlbVirtualServiceHttpRespRulesRuleMatchCriteriaHttpMethods]:
        return typing.cast(typing.Optional[NsxtAlbVirtualServiceHttpRespRulesRuleMatchCriteriaHttpMethods], jsii.get(self, "httpMethodsInput"))

    @builtins.property
    @jsii.member(jsii_name="locationHeaderInput")
    def location_header_input(
        self,
    ) -> typing.Optional[NsxtAlbVirtualServiceHttpRespRulesRuleMatchCriteriaLocationHeader]:
        return typing.cast(typing.Optional[NsxtAlbVirtualServiceHttpRespRulesRuleMatchCriteriaLocationHeader], jsii.get(self, "locationHeaderInput"))

    @builtins.property
    @jsii.member(jsii_name="pathInput")
    def path_input(
        self,
    ) -> typing.Optional["NsxtAlbVirtualServiceHttpRespRulesRuleMatchCriteriaPath"]:
        return typing.cast(typing.Optional["NsxtAlbVirtualServiceHttpRespRulesRuleMatchCriteriaPath"], jsii.get(self, "pathInput"))

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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["NsxtAlbVirtualServiceHttpRespRulesRuleMatchCriteriaRequestHeaders"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["NsxtAlbVirtualServiceHttpRespRulesRuleMatchCriteriaRequestHeaders"]]], jsii.get(self, "requestHeadersInput"))

    @builtins.property
    @jsii.member(jsii_name="responseHeadersInput")
    def response_headers_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["NsxtAlbVirtualServiceHttpRespRulesRuleMatchCriteriaResponseHeaders"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["NsxtAlbVirtualServiceHttpRespRulesRuleMatchCriteriaResponseHeaders"]]], jsii.get(self, "responseHeadersInput"))

    @builtins.property
    @jsii.member(jsii_name="servicePortsInput")
    def service_ports_input(
        self,
    ) -> typing.Optional["NsxtAlbVirtualServiceHttpRespRulesRuleMatchCriteriaServicePorts"]:
        return typing.cast(typing.Optional["NsxtAlbVirtualServiceHttpRespRulesRuleMatchCriteriaServicePorts"], jsii.get(self, "servicePortsInput"))

    @builtins.property
    @jsii.member(jsii_name="statusCodeInput")
    def status_code_input(
        self,
    ) -> typing.Optional["NsxtAlbVirtualServiceHttpRespRulesRuleMatchCriteriaStatusCode"]:
        return typing.cast(typing.Optional["NsxtAlbVirtualServiceHttpRespRulesRuleMatchCriteriaStatusCode"], jsii.get(self, "statusCodeInput"))

    @builtins.property
    @jsii.member(jsii_name="protocolType")
    def protocol_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "protocolType"))

    @protocol_type.setter
    def protocol_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__488962c2baccbbc82229ab3ea78bfcb8b2f2a05bd5f162d1b82134163a6e6aac)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "protocolType", value)

    @builtins.property
    @jsii.member(jsii_name="query")
    def query(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "query"))

    @query.setter
    def query(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a1b5ea97bdd28ed4e8d7ef7712a5b0915baa7bf67cc7ecfc21e5737897d84bed)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "query", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[NsxtAlbVirtualServiceHttpRespRulesRuleMatchCriteria]:
        return typing.cast(typing.Optional[NsxtAlbVirtualServiceHttpRespRulesRuleMatchCriteria], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[NsxtAlbVirtualServiceHttpRespRulesRuleMatchCriteria],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d7d53139c037fac8a305ece5bb8827c2cecad77627383b912c58d4c84352a264)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="vcd.nsxtAlbVirtualServiceHttpRespRules.NsxtAlbVirtualServiceHttpRespRulesRuleMatchCriteriaPath",
    jsii_struct_bases=[],
    name_mapping={"criteria": "criteria", "paths": "paths"},
)
class NsxtAlbVirtualServiceHttpRespRulesRuleMatchCriteriaPath:
    def __init__(
        self,
        *,
        criteria: builtins.str,
        paths: typing.Sequence[builtins.str],
    ) -> None:
        '''
        :param criteria: Criteria to use for matching the path in the HTTP request URI. Options - BEGINS_WITH, DOES_NOT_BEGIN_WITH, CONTAINS, DOES_NOT_CONTAIN, ENDS_WITH, DOES_NOT_END_WITH, EQUALS, DOES_NOT_EQUAL, REGEX_MATCH, REGEX_DOES_NOT_MATCH Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_resp_rules#criteria NsxtAlbVirtualServiceHttpRespRules#criteria}
        :param paths: String values to match the path. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_resp_rules#paths NsxtAlbVirtualServiceHttpRespRules#paths}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1b3a6f11c82d3c031bc16317a10c4299481f58dd3ef95fe5136dec6d7f521ecf)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_resp_rules#criteria NsxtAlbVirtualServiceHttpRespRules#criteria}
        '''
        result = self._values.get("criteria")
        assert result is not None, "Required property 'criteria' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def paths(self) -> typing.List[builtins.str]:
        '''String values to match the path.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_resp_rules#paths NsxtAlbVirtualServiceHttpRespRules#paths}
        '''
        result = self._values.get("paths")
        assert result is not None, "Required property 'paths' is missing"
        return typing.cast(typing.List[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NsxtAlbVirtualServiceHttpRespRulesRuleMatchCriteriaPath(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class NsxtAlbVirtualServiceHttpRespRulesRuleMatchCriteriaPathOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="vcd.nsxtAlbVirtualServiceHttpRespRules.NsxtAlbVirtualServiceHttpRespRulesRuleMatchCriteriaPathOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__550ee11065880d21c803f337b7979604584fbe619ca8440283044daf5df8bfff)
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
            type_hints = typing.get_type_hints(_typecheckingstub__85ab07a920aba08f979cbf5e6fd427b61d0f2ca503b9e7a91f9abbe056842af6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "criteria", value)

    @builtins.property
    @jsii.member(jsii_name="paths")
    def paths(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "paths"))

    @paths.setter
    def paths(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7b7a4cd6324b2e71bb2dddd2346b873abb08d289589783bd7f48398f0e23a351)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "paths", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[NsxtAlbVirtualServiceHttpRespRulesRuleMatchCriteriaPath]:
        return typing.cast(typing.Optional[NsxtAlbVirtualServiceHttpRespRulesRuleMatchCriteriaPath], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[NsxtAlbVirtualServiceHttpRespRulesRuleMatchCriteriaPath],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c8373b9f09c8e2886a0d131569edfcb18e7bbd9cba80ff25c734d04d1b04eb2f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="vcd.nsxtAlbVirtualServiceHttpRespRules.NsxtAlbVirtualServiceHttpRespRulesRuleMatchCriteriaRequestHeaders",
    jsii_struct_bases=[],
    name_mapping={"criteria": "criteria", "name": "name", "values": "values"},
)
class NsxtAlbVirtualServiceHttpRespRulesRuleMatchCriteriaRequestHeaders:
    def __init__(
        self,
        *,
        criteria: builtins.str,
        name: builtins.str,
        values: typing.Sequence[builtins.str],
    ) -> None:
        '''
        :param criteria: Criteria to use for matching headers and cookies in the HTTP request amd response. Options - EXISTS, DOES_NOT_EXIST, BEGINS_WITH, DOES_NOT_BEGIN_WITH, CONTAINS, DOES_NOT_CONTAIN, ENDS_WITH, DOES_NOT_END_WITH, EQUALS, DOES_NOT_EQUAL Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_resp_rules#criteria NsxtAlbVirtualServiceHttpRespRules#criteria}
        :param name: Name of the HTTP header whose value is to be matched. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_resp_rules#name NsxtAlbVirtualServiceHttpRespRules#name}
        :param values: String values to match for an HTTP header. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_resp_rules#values NsxtAlbVirtualServiceHttpRespRules#values}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e4ec8e58d0e9fcb7b45651a14652f6428b595ab27de4c8e4b3631e3435261e6f)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_resp_rules#criteria NsxtAlbVirtualServiceHttpRespRules#criteria}
        '''
        result = self._values.get("criteria")
        assert result is not None, "Required property 'criteria' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Name of the HTTP header whose value is to be matched.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_resp_rules#name NsxtAlbVirtualServiceHttpRespRules#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def values(self) -> typing.List[builtins.str]:
        '''String values to match for an HTTP header.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_resp_rules#values NsxtAlbVirtualServiceHttpRespRules#values}
        '''
        result = self._values.get("values")
        assert result is not None, "Required property 'values' is missing"
        return typing.cast(typing.List[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NsxtAlbVirtualServiceHttpRespRulesRuleMatchCriteriaRequestHeaders(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class NsxtAlbVirtualServiceHttpRespRulesRuleMatchCriteriaRequestHeadersList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="vcd.nsxtAlbVirtualServiceHttpRespRules.NsxtAlbVirtualServiceHttpRespRulesRuleMatchCriteriaRequestHeadersList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ca19fa6aa04083108b24fb2dd5236ad009d5a6314eb164107dbccb46c028d2a6)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "NsxtAlbVirtualServiceHttpRespRulesRuleMatchCriteriaRequestHeadersOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__16d7dd31a75582e3f331aa4466a020daa21c08a1347697bc1a6d5fa36867c477)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("NsxtAlbVirtualServiceHttpRespRulesRuleMatchCriteriaRequestHeadersOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cf2677a1f27c4b8fab9e7a6a2aeaf2c34ea2fe4089812a9792a754423733b563)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2bf406f318c817a3d151e72cf189f5e81204d2b18d50edd3bd352e1293486bc5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__659eb46fdac0566ee4459ce6dc91a213db5f4ac7fd1cb8726f73fa8a2f3f1cf2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NsxtAlbVirtualServiceHttpRespRulesRuleMatchCriteriaRequestHeaders]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NsxtAlbVirtualServiceHttpRespRulesRuleMatchCriteriaRequestHeaders]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NsxtAlbVirtualServiceHttpRespRulesRuleMatchCriteriaRequestHeaders]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f2eadcdaa8705f6088d20b2be1b522cae28aa967b1e205bfc0802a216e988501)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class NsxtAlbVirtualServiceHttpRespRulesRuleMatchCriteriaRequestHeadersOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="vcd.nsxtAlbVirtualServiceHttpRespRules.NsxtAlbVirtualServiceHttpRespRulesRuleMatchCriteriaRequestHeadersOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__99f50bb85711bbafce509adc5111f3b11ec1b8d20c33fc8b9a3092742fe97308)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2a08b7165880160c7e96c0ebc46628bf8acc53eb6bdce705d84221c07d0c87d1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "criteria", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6c58726aea9589d8cd8c10e8c5f119121f5d2979f91865324fe3a583bc8a7d2c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="values")
    def values(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "values"))

    @values.setter
    def values(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3723d31a2cf0716f09bdc13576a7ab7f7e0a221b2f958963c6e71f04726c639e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "values", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NsxtAlbVirtualServiceHttpRespRulesRuleMatchCriteriaRequestHeaders]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NsxtAlbVirtualServiceHttpRespRulesRuleMatchCriteriaRequestHeaders]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NsxtAlbVirtualServiceHttpRespRulesRuleMatchCriteriaRequestHeaders]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7b05e5994dcc8d1678b3c405cabec0ac2dc0b79ce63ce3bda23d8970b9a8b2e4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="vcd.nsxtAlbVirtualServiceHttpRespRules.NsxtAlbVirtualServiceHttpRespRulesRuleMatchCriteriaResponseHeaders",
    jsii_struct_bases=[],
    name_mapping={"criteria": "criteria", "name": "name", "values": "values"},
)
class NsxtAlbVirtualServiceHttpRespRulesRuleMatchCriteriaResponseHeaders:
    def __init__(
        self,
        *,
        criteria: builtins.str,
        name: typing.Optional[builtins.str] = None,
        values: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param criteria: Criteria to use for matching headers and cookies in the HTTP request amd response. Options - EXISTS, DOES_NOT_EXIST, BEGINS_WITH, DOES_NOT_BEGIN_WITH, CONTAINS, DOES_NOT_CONTAIN, ENDS_WITH, DOES_NOT_END_WITH, EQUALS, DOES_NOT_EQUAL Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_resp_rules#criteria NsxtAlbVirtualServiceHttpRespRules#criteria}
        :param name: Name of the HTTP header whose value is to be matched. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_resp_rules#name NsxtAlbVirtualServiceHttpRespRules#name}
        :param values: A set of values to match for an HTTP header. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_resp_rules#values NsxtAlbVirtualServiceHttpRespRules#values}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dd287c3bbcfcb241eca66a3939832a127bfd2c941b9fac16d2441283bb6993ca)
            check_type(argname="argument criteria", value=criteria, expected_type=type_hints["criteria"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument values", value=values, expected_type=type_hints["values"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "criteria": criteria,
        }
        if name is not None:
            self._values["name"] = name
        if values is not None:
            self._values["values"] = values

    @builtins.property
    def criteria(self) -> builtins.str:
        '''Criteria to use for matching headers and cookies in the HTTP request amd response.

        Options - EXISTS, DOES_NOT_EXIST, BEGINS_WITH, DOES_NOT_BEGIN_WITH, CONTAINS, DOES_NOT_CONTAIN, ENDS_WITH, DOES_NOT_END_WITH, EQUALS, DOES_NOT_EQUAL

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_resp_rules#criteria NsxtAlbVirtualServiceHttpRespRules#criteria}
        '''
        result = self._values.get("criteria")
        assert result is not None, "Required property 'criteria' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Name of the HTTP header whose value is to be matched.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_resp_rules#name NsxtAlbVirtualServiceHttpRespRules#name}
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def values(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A set of values to match for an HTTP header.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_resp_rules#values NsxtAlbVirtualServiceHttpRespRules#values}
        '''
        result = self._values.get("values")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NsxtAlbVirtualServiceHttpRespRulesRuleMatchCriteriaResponseHeaders(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class NsxtAlbVirtualServiceHttpRespRulesRuleMatchCriteriaResponseHeadersList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="vcd.nsxtAlbVirtualServiceHttpRespRules.NsxtAlbVirtualServiceHttpRespRulesRuleMatchCriteriaResponseHeadersList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f1e01f283e56f62f07d5019926c5f5e751a70a633b7953a79e8ba1ae1a0aafa0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "NsxtAlbVirtualServiceHttpRespRulesRuleMatchCriteriaResponseHeadersOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__00e109aef4375b49ed4c1abaacbe8ffddff96f0ef3eac65749c3eb26d5328e17)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("NsxtAlbVirtualServiceHttpRespRulesRuleMatchCriteriaResponseHeadersOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f82c7055829579f928b28ea654b70667126fabc9b68261b8076549df8a42c877)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d7244bdda286ca9a9ff161f244945f4aee6b86cc7d040afeb686692443e83751)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a1f3654938bd47c567128fb8110b9bce14df4c9dceb73ad519fa6926ede010bc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NsxtAlbVirtualServiceHttpRespRulesRuleMatchCriteriaResponseHeaders]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NsxtAlbVirtualServiceHttpRespRulesRuleMatchCriteriaResponseHeaders]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NsxtAlbVirtualServiceHttpRespRulesRuleMatchCriteriaResponseHeaders]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ef746bcd981748b07f2aa2ecbb79fd307f0785eff703dd279b4df1e1bc5d3b20)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class NsxtAlbVirtualServiceHttpRespRulesRuleMatchCriteriaResponseHeadersOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="vcd.nsxtAlbVirtualServiceHttpRespRules.NsxtAlbVirtualServiceHttpRespRulesRuleMatchCriteriaResponseHeadersOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a03208e70c39c886b506ca098ab7bd08ed29bf101f12a14a74ed71c74855bef7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

    @jsii.member(jsii_name="resetValues")
    def reset_values(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetValues", []))

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
            type_hints = typing.get_type_hints(_typecheckingstub__1e4202bc996f1b5a1801f47109161dc0325317fbb4b44d9d164a570b568d9039)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "criteria", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7f575246ea51c855926003916888ba86820d36f0a67bffbddc2b553d5ab9129c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="values")
    def values(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "values"))

    @values.setter
    def values(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d27e21db720d2ad5040fa9cb80bc870535dc86fea3058b8f0b166b03524f7f38)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "values", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NsxtAlbVirtualServiceHttpRespRulesRuleMatchCriteriaResponseHeaders]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NsxtAlbVirtualServiceHttpRespRulesRuleMatchCriteriaResponseHeaders]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NsxtAlbVirtualServiceHttpRespRulesRuleMatchCriteriaResponseHeaders]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__14b923977e2697558fa7f6ec2362b02b48844ca04d36e60bc25cd51d75973fd5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="vcd.nsxtAlbVirtualServiceHttpRespRules.NsxtAlbVirtualServiceHttpRespRulesRuleMatchCriteriaServicePorts",
    jsii_struct_bases=[],
    name_mapping={"criteria": "criteria", "ports": "ports"},
)
class NsxtAlbVirtualServiceHttpRespRulesRuleMatchCriteriaServicePorts:
    def __init__(
        self,
        *,
        criteria: builtins.str,
        ports: typing.Sequence[jsii.Number],
    ) -> None:
        '''
        :param criteria: Criteria to use for IP address matching the HTTP request. Options - IS_IN, IS_NOT_IN. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_resp_rules#criteria NsxtAlbVirtualServiceHttpRespRules#criteria}
        :param ports: A set of TCP ports. Allowed values are 1-65535. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_resp_rules#ports NsxtAlbVirtualServiceHttpRespRules#ports}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7804047ae2eae18536652567b8f934b68c1bc29f183e12e4bd11ec0c8b03b513)
            check_type(argname="argument criteria", value=criteria, expected_type=type_hints["criteria"])
            check_type(argname="argument ports", value=ports, expected_type=type_hints["ports"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "criteria": criteria,
            "ports": ports,
        }

    @builtins.property
    def criteria(self) -> builtins.str:
        '''Criteria to use for IP address matching the HTTP request. Options - IS_IN, IS_NOT_IN.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_resp_rules#criteria NsxtAlbVirtualServiceHttpRespRules#criteria}
        '''
        result = self._values.get("criteria")
        assert result is not None, "Required property 'criteria' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def ports(self) -> typing.List[jsii.Number]:
        '''A set of TCP ports. Allowed values are 1-65535.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_resp_rules#ports NsxtAlbVirtualServiceHttpRespRules#ports}
        '''
        result = self._values.get("ports")
        assert result is not None, "Required property 'ports' is missing"
        return typing.cast(typing.List[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NsxtAlbVirtualServiceHttpRespRulesRuleMatchCriteriaServicePorts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class NsxtAlbVirtualServiceHttpRespRulesRuleMatchCriteriaServicePortsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="vcd.nsxtAlbVirtualServiceHttpRespRules.NsxtAlbVirtualServiceHttpRespRulesRuleMatchCriteriaServicePortsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9898d4bb1d2060005a21013220a512a8b660f9cd3bfde58816421fedea51060c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__87b466c9c6b6c4f31df27414adb14f2aa0193c97e924ce0fe34a3e5452dc5c6d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "criteria", value)

    @builtins.property
    @jsii.member(jsii_name="ports")
    def ports(self) -> typing.List[jsii.Number]:
        return typing.cast(typing.List[jsii.Number], jsii.get(self, "ports"))

    @ports.setter
    def ports(self, value: typing.List[jsii.Number]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5a8b89bd2fa461a9c60b6fa4588659605cc7c6ba5cdb8ce307a8813982eb9539)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ports", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[NsxtAlbVirtualServiceHttpRespRulesRuleMatchCriteriaServicePorts]:
        return typing.cast(typing.Optional[NsxtAlbVirtualServiceHttpRespRulesRuleMatchCriteriaServicePorts], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[NsxtAlbVirtualServiceHttpRespRulesRuleMatchCriteriaServicePorts],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1b1f0b237c6ec90b35d45861971ce1a9559e8c67a7a86f7b3e4d4d33ef82a4b0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="vcd.nsxtAlbVirtualServiceHttpRespRules.NsxtAlbVirtualServiceHttpRespRulesRuleMatchCriteriaStatusCode",
    jsii_struct_bases=[],
    name_mapping={"criteria": "criteria", "http_status_code": "httpStatusCode"},
)
class NsxtAlbVirtualServiceHttpRespRulesRuleMatchCriteriaStatusCode:
    def __init__(
        self,
        *,
        criteria: builtins.str,
        http_status_code: builtins.str,
    ) -> None:
        '''
        :param criteria: Criteria to use for IP address matching the HTTP request. Options - IS_IN, IS_NOT_IN. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_resp_rules#criteria NsxtAlbVirtualServiceHttpRespRules#criteria}
        :param http_status_code: Enter a http status code or range. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_resp_rules#http_status_code NsxtAlbVirtualServiceHttpRespRules#http_status_code}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8278111a2a5ba0785f937e0d9d761e0afc572749863a9aa2d9792c2948867662)
            check_type(argname="argument criteria", value=criteria, expected_type=type_hints["criteria"])
            check_type(argname="argument http_status_code", value=http_status_code, expected_type=type_hints["http_status_code"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "criteria": criteria,
            "http_status_code": http_status_code,
        }

    @builtins.property
    def criteria(self) -> builtins.str:
        '''Criteria to use for IP address matching the HTTP request. Options - IS_IN, IS_NOT_IN.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_resp_rules#criteria NsxtAlbVirtualServiceHttpRespRules#criteria}
        '''
        result = self._values.get("criteria")
        assert result is not None, "Required property 'criteria' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def http_status_code(self) -> builtins.str:
        '''Enter a http status code or range.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_resp_rules#http_status_code NsxtAlbVirtualServiceHttpRespRules#http_status_code}
        '''
        result = self._values.get("http_status_code")
        assert result is not None, "Required property 'http_status_code' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NsxtAlbVirtualServiceHttpRespRulesRuleMatchCriteriaStatusCode(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class NsxtAlbVirtualServiceHttpRespRulesRuleMatchCriteriaStatusCodeOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="vcd.nsxtAlbVirtualServiceHttpRespRules.NsxtAlbVirtualServiceHttpRespRulesRuleMatchCriteriaStatusCodeOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d6c1994be32be07ada2708d9d7023f5fdffc2d5bc8887868d8ce77118655319f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="criteriaInput")
    def criteria_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "criteriaInput"))

    @builtins.property
    @jsii.member(jsii_name="httpStatusCodeInput")
    def http_status_code_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "httpStatusCodeInput"))

    @builtins.property
    @jsii.member(jsii_name="criteria")
    def criteria(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "criteria"))

    @criteria.setter
    def criteria(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5980359121d7275de8363ccf938abced5dd24b2d804c63c37f41f5fbfe18fb7d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "criteria", value)

    @builtins.property
    @jsii.member(jsii_name="httpStatusCode")
    def http_status_code(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "httpStatusCode"))

    @http_status_code.setter
    def http_status_code(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cdfc19e27543dcf7f495feaf284d8c817c2079e641471ae780117921339aff1a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "httpStatusCode", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[NsxtAlbVirtualServiceHttpRespRulesRuleMatchCriteriaStatusCode]:
        return typing.cast(typing.Optional[NsxtAlbVirtualServiceHttpRespRulesRuleMatchCriteriaStatusCode], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[NsxtAlbVirtualServiceHttpRespRulesRuleMatchCriteriaStatusCode],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__258114cc715513919ee40ec7e39840427d10a140a66cdd7a7336f8d339bd4346)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class NsxtAlbVirtualServiceHttpRespRulesRuleOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="vcd.nsxtAlbVirtualServiceHttpRespRules.NsxtAlbVirtualServiceHttpRespRulesRuleOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4f5b857db81e87d3ca37f0033a83a64494dc06e125693d3a3d655368a6c11bff)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putActions")
    def put_actions(
        self,
        *,
        modify_header: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[NsxtAlbVirtualServiceHttpRespRulesRuleActionsModifyHeader, typing.Dict[builtins.str, typing.Any]]]]] = None,
        rewrite_location_header: typing.Optional[typing.Union[NsxtAlbVirtualServiceHttpRespRulesRuleActionsRewriteLocationHeader, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param modify_header: modify_header block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_resp_rules#modify_header NsxtAlbVirtualServiceHttpRespRules#modify_header}
        :param rewrite_location_header: rewrite_location_header block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_resp_rules#rewrite_location_header NsxtAlbVirtualServiceHttpRespRules#rewrite_location_header}
        '''
        value = NsxtAlbVirtualServiceHttpRespRulesRuleActions(
            modify_header=modify_header,
            rewrite_location_header=rewrite_location_header,
        )

        return typing.cast(None, jsii.invoke(self, "putActions", [value]))

    @jsii.member(jsii_name="putMatchCriteria")
    def put_match_criteria(
        self,
        *,
        client_ip_address: typing.Optional[typing.Union[NsxtAlbVirtualServiceHttpRespRulesRuleMatchCriteriaClientIpAddress, typing.Dict[builtins.str, typing.Any]]] = None,
        cookie: typing.Optional[typing.Union[NsxtAlbVirtualServiceHttpRespRulesRuleMatchCriteriaCookie, typing.Dict[builtins.str, typing.Any]]] = None,
        http_methods: typing.Optional[typing.Union[NsxtAlbVirtualServiceHttpRespRulesRuleMatchCriteriaHttpMethods, typing.Dict[builtins.str, typing.Any]]] = None,
        location_header: typing.Optional[typing.Union[NsxtAlbVirtualServiceHttpRespRulesRuleMatchCriteriaLocationHeader, typing.Dict[builtins.str, typing.Any]]] = None,
        path: typing.Optional[typing.Union[NsxtAlbVirtualServiceHttpRespRulesRuleMatchCriteriaPath, typing.Dict[builtins.str, typing.Any]]] = None,
        protocol_type: typing.Optional[builtins.str] = None,
        query: typing.Optional[typing.Sequence[builtins.str]] = None,
        request_headers: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[NsxtAlbVirtualServiceHttpRespRulesRuleMatchCriteriaRequestHeaders, typing.Dict[builtins.str, typing.Any]]]]] = None,
        response_headers: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[NsxtAlbVirtualServiceHttpRespRulesRuleMatchCriteriaResponseHeaders, typing.Dict[builtins.str, typing.Any]]]]] = None,
        service_ports: typing.Optional[typing.Union[NsxtAlbVirtualServiceHttpRespRulesRuleMatchCriteriaServicePorts, typing.Dict[builtins.str, typing.Any]]] = None,
        status_code: typing.Optional[typing.Union[NsxtAlbVirtualServiceHttpRespRulesRuleMatchCriteriaStatusCode, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param client_ip_address: client_ip_address block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_resp_rules#client_ip_address NsxtAlbVirtualServiceHttpRespRules#client_ip_address}
        :param cookie: cookie block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_resp_rules#cookie NsxtAlbVirtualServiceHttpRespRules#cookie}
        :param http_methods: http_methods block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_resp_rules#http_methods NsxtAlbVirtualServiceHttpRespRules#http_methods}
        :param location_header: location_header block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_resp_rules#location_header NsxtAlbVirtualServiceHttpRespRules#location_header}
        :param path: path block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_resp_rules#path NsxtAlbVirtualServiceHttpRespRules#path}
        :param protocol_type: Protocol to match - 'HTTP' or 'HTTPS'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_resp_rules#protocol_type NsxtAlbVirtualServiceHttpRespRules#protocol_type}
        :param query: HTTP request query strings to match. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_resp_rules#query NsxtAlbVirtualServiceHttpRespRules#query}
        :param request_headers: request_headers block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_resp_rules#request_headers NsxtAlbVirtualServiceHttpRespRules#request_headers}
        :param response_headers: response_headers block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_resp_rules#response_headers NsxtAlbVirtualServiceHttpRespRules#response_headers}
        :param service_ports: service_ports block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_resp_rules#service_ports NsxtAlbVirtualServiceHttpRespRules#service_ports}
        :param status_code: status_code block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_alb_virtual_service_http_resp_rules#status_code NsxtAlbVirtualServiceHttpRespRules#status_code}
        '''
        value = NsxtAlbVirtualServiceHttpRespRulesRuleMatchCriteria(
            client_ip_address=client_ip_address,
            cookie=cookie,
            http_methods=http_methods,
            location_header=location_header,
            path=path,
            protocol_type=protocol_type,
            query=query,
            request_headers=request_headers,
            response_headers=response_headers,
            service_ports=service_ports,
            status_code=status_code,
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
    def actions(self) -> NsxtAlbVirtualServiceHttpRespRulesRuleActionsOutputReference:
        return typing.cast(NsxtAlbVirtualServiceHttpRespRulesRuleActionsOutputReference, jsii.get(self, "actions"))

    @builtins.property
    @jsii.member(jsii_name="matchCriteria")
    def match_criteria(
        self,
    ) -> NsxtAlbVirtualServiceHttpRespRulesRuleMatchCriteriaOutputReference:
        return typing.cast(NsxtAlbVirtualServiceHttpRespRulesRuleMatchCriteriaOutputReference, jsii.get(self, "matchCriteria"))

    @builtins.property
    @jsii.member(jsii_name="actionsInput")
    def actions_input(
        self,
    ) -> typing.Optional[NsxtAlbVirtualServiceHttpRespRulesRuleActions]:
        return typing.cast(typing.Optional[NsxtAlbVirtualServiceHttpRespRulesRuleActions], jsii.get(self, "actionsInput"))

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
    ) -> typing.Optional[NsxtAlbVirtualServiceHttpRespRulesRuleMatchCriteria]:
        return typing.cast(typing.Optional[NsxtAlbVirtualServiceHttpRespRulesRuleMatchCriteria], jsii.get(self, "matchCriteriaInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__07d48045b85b9e489c87d1ebe1f2437986e40187ec45deb832f9fd49ea247787)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c55482a8f090026aa06c61901441bf4c28384fe3421bbd45253264f6b9d15e54)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "logging", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3e4748b42da2c9391d9b6752b4d0ae46b47facb0f281640b0469c4ddebc1446d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NsxtAlbVirtualServiceHttpRespRulesRule]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NsxtAlbVirtualServiceHttpRespRulesRule]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NsxtAlbVirtualServiceHttpRespRulesRule]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7b5009a40b3dd0277cbb21997b04e517935c3308451bc393a4fc962bedeb6153)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


__all__ = [
    "NsxtAlbVirtualServiceHttpRespRules",
    "NsxtAlbVirtualServiceHttpRespRulesConfig",
    "NsxtAlbVirtualServiceHttpRespRulesRule",
    "NsxtAlbVirtualServiceHttpRespRulesRuleActions",
    "NsxtAlbVirtualServiceHttpRespRulesRuleActionsModifyHeader",
    "NsxtAlbVirtualServiceHttpRespRulesRuleActionsModifyHeaderList",
    "NsxtAlbVirtualServiceHttpRespRulesRuleActionsModifyHeaderOutputReference",
    "NsxtAlbVirtualServiceHttpRespRulesRuleActionsOutputReference",
    "NsxtAlbVirtualServiceHttpRespRulesRuleActionsRewriteLocationHeader",
    "NsxtAlbVirtualServiceHttpRespRulesRuleActionsRewriteLocationHeaderOutputReference",
    "NsxtAlbVirtualServiceHttpRespRulesRuleList",
    "NsxtAlbVirtualServiceHttpRespRulesRuleMatchCriteria",
    "NsxtAlbVirtualServiceHttpRespRulesRuleMatchCriteriaClientIpAddress",
    "NsxtAlbVirtualServiceHttpRespRulesRuleMatchCriteriaClientIpAddressOutputReference",
    "NsxtAlbVirtualServiceHttpRespRulesRuleMatchCriteriaCookie",
    "NsxtAlbVirtualServiceHttpRespRulesRuleMatchCriteriaCookieOutputReference",
    "NsxtAlbVirtualServiceHttpRespRulesRuleMatchCriteriaHttpMethods",
    "NsxtAlbVirtualServiceHttpRespRulesRuleMatchCriteriaHttpMethodsOutputReference",
    "NsxtAlbVirtualServiceHttpRespRulesRuleMatchCriteriaLocationHeader",
    "NsxtAlbVirtualServiceHttpRespRulesRuleMatchCriteriaLocationHeaderOutputReference",
    "NsxtAlbVirtualServiceHttpRespRulesRuleMatchCriteriaOutputReference",
    "NsxtAlbVirtualServiceHttpRespRulesRuleMatchCriteriaPath",
    "NsxtAlbVirtualServiceHttpRespRulesRuleMatchCriteriaPathOutputReference",
    "NsxtAlbVirtualServiceHttpRespRulesRuleMatchCriteriaRequestHeaders",
    "NsxtAlbVirtualServiceHttpRespRulesRuleMatchCriteriaRequestHeadersList",
    "NsxtAlbVirtualServiceHttpRespRulesRuleMatchCriteriaRequestHeadersOutputReference",
    "NsxtAlbVirtualServiceHttpRespRulesRuleMatchCriteriaResponseHeaders",
    "NsxtAlbVirtualServiceHttpRespRulesRuleMatchCriteriaResponseHeadersList",
    "NsxtAlbVirtualServiceHttpRespRulesRuleMatchCriteriaResponseHeadersOutputReference",
    "NsxtAlbVirtualServiceHttpRespRulesRuleMatchCriteriaServicePorts",
    "NsxtAlbVirtualServiceHttpRespRulesRuleMatchCriteriaServicePortsOutputReference",
    "NsxtAlbVirtualServiceHttpRespRulesRuleMatchCriteriaStatusCode",
    "NsxtAlbVirtualServiceHttpRespRulesRuleMatchCriteriaStatusCodeOutputReference",
    "NsxtAlbVirtualServiceHttpRespRulesRuleOutputReference",
]

publication.publish()

def _typecheckingstub__1e93eeef6e93221a7712a46a29a6d88b0e4296ae46d1f7af7c5fd7e33d8f0258(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    rule: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[NsxtAlbVirtualServiceHttpRespRulesRule, typing.Dict[builtins.str, typing.Any]]]],
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

def _typecheckingstub__505b44e42f91db7ba016efa2130ff4a05f0471ddb8a5b1a29b55ce777496bc18(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__369fbc63ad12532e0bbda6e18d254ae47b8c639a077e08cd6c0aec58c8e13b74(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[NsxtAlbVirtualServiceHttpRespRulesRule, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__801bc3787d22ad161cf6b92a27f0060b256387758ff752f6fddd8c434decbb19(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8224dcadbbb461308d03f66e5045075ec517ef2ed5a8e7d1f7f67fc7a58007e7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__72a54bd19a903e366ff57d92833ac40b635375ac7c79e118fd24377146fd984b(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    rule: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[NsxtAlbVirtualServiceHttpRespRulesRule, typing.Dict[builtins.str, typing.Any]]]],
    virtual_service_id: builtins.str,
    id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0bfe42c3e56e02a383811a27251e50357e965479d025e68c6a26592bf41ca20c(
    *,
    actions: typing.Union[NsxtAlbVirtualServiceHttpRespRulesRuleActions, typing.Dict[builtins.str, typing.Any]],
    match_criteria: typing.Union[NsxtAlbVirtualServiceHttpRespRulesRuleMatchCriteria, typing.Dict[builtins.str, typing.Any]],
    name: builtins.str,
    active: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    logging: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e3a18e1cea62902490b550d53bfe31fe5c4c28859dd524c20cb83c185235a5b(
    *,
    modify_header: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[NsxtAlbVirtualServiceHttpRespRulesRuleActionsModifyHeader, typing.Dict[builtins.str, typing.Any]]]]] = None,
    rewrite_location_header: typing.Optional[typing.Union[NsxtAlbVirtualServiceHttpRespRulesRuleActionsRewriteLocationHeader, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e1c7d23999d9f256b2761f47d79e043fbdc0d7aa954ff7279ed3bd5f51df9b46(
    *,
    action: builtins.str,
    name: builtins.str,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__418e133dad57c7d861c96988e341403cd749e33b0864028eb5048cba1a3b463d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__24421a291e443551e591ec28bbdced4635752f100fc0d09659155f26c66a6182(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__44583dfb97a1601a3252487de7e30442450902c642427b42edbf3d76e763cc28(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ed11c3c1baea1a8cdd2c2451df720515042355f0cff9db99e7e0614e1c9d644(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5fde7890512ba78efc3fa4379c6f65496d02b54b290f1bfba9ae7f6f5005f67d(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d69325acee440b9c20cd1201a7083042db50b85bbc3d9e5c4b9e5153688a765(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NsxtAlbVirtualServiceHttpRespRulesRuleActionsModifyHeader]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ad67dca77b4006fe8d7ef36b2fde003518ba6110269c900b15c6fa43e997b36(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f515157e000d3743d0d883f7cee0d9f60fa5758a62b1dab5e45f6757bf2dd71(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9289fb046fc3a2a5cce7a17ef9637a6cbad189f4f4fa0346fedd9d044d4bee28(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a9a1baa2f3fba7ee8ab83600423b9e3c4ecf6329f79b9fe43ad8e70c9d625092(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f06289aecb7bb9e6cccee5a2de4f43223dacbe7150aca3af49697dcc2422f7dc(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NsxtAlbVirtualServiceHttpRespRulesRuleActionsModifyHeader]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a89bab0028f21fcf4d527d3da9fb0dea8b74b8bb7ef4806015c456e196c0307b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d2789cf2a4b6b305b9629b94066da8946672c8893ce1c8da04440080723efe25(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[NsxtAlbVirtualServiceHttpRespRulesRuleActionsModifyHeader, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__488c78fcd667efb9d73bd731c01ef27e086ba07b5d8006b12f52ce1dc4e8c2f4(
    value: typing.Optional[NsxtAlbVirtualServiceHttpRespRulesRuleActions],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__74456f32d0cb74d158b582574af125fcca2bdbf2b5088b8e9e9e15c18e8b8a26(
    *,
    port: builtins.str,
    protocol: builtins.str,
    host: typing.Optional[builtins.str] = None,
    keep_query: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    path: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ecb87e122a1070f12110ce6ecf9a4da0b11b93fcc9f4f929373498c3bf462f33(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__18d3b51901c48e4c062700dc7ccf4d0c3ff7a66e616f39aabf31311668f007e9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__126120cb9fab731357e3aa4762f7d7dba8bd1c14cdb2719c02f1b7ba88ae3017(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__668af1f155ca400b0840ca1250346553181bae7ed517b42e4cf6d82b3f40f010(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de229e1e1235d261062dd6c8aa76d5891a5151b708557db5c7405f4907267611(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e4354f39a706b55584562b33fcdc7af945dad42f14a09b1878dcec8a1564193(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f9f00bd79b5497f809a9f99988d654c40ff6e4eb31a352be53a39a0dd616b2d(
    value: typing.Optional[NsxtAlbVirtualServiceHttpRespRulesRuleActionsRewriteLocationHeader],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__10cef74aecc6fd3236efe882d130c18816fbbbd1d5c7171270aeaf39e13a1b3b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b575cd57bf8dace6da2a53f2f6ebed0ea8136457aae76148dc592eb89be9a5b8(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc2f156044a92288296f6b8c29c8278d8e30efa568c0f69bf73aaa79e0490b6a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__801aef5770551fd0095036181b49fb1f13ddc6ae313fb731382450801e56f3a4(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b1899298cfe45d3f3e3f171bfa937bf482d922f755ad83532b1d9cbcb5b92175(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__15cda5f6bed6bbf972cda09c5f35431984976640dfb84d63ba5d057e435bb3dd(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NsxtAlbVirtualServiceHttpRespRulesRule]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cfd79fb675b980a21f40544248ddef82d3da488eb3c8cfc0f42836b7309461de(
    *,
    client_ip_address: typing.Optional[typing.Union[NsxtAlbVirtualServiceHttpRespRulesRuleMatchCriteriaClientIpAddress, typing.Dict[builtins.str, typing.Any]]] = None,
    cookie: typing.Optional[typing.Union[NsxtAlbVirtualServiceHttpRespRulesRuleMatchCriteriaCookie, typing.Dict[builtins.str, typing.Any]]] = None,
    http_methods: typing.Optional[typing.Union[NsxtAlbVirtualServiceHttpRespRulesRuleMatchCriteriaHttpMethods, typing.Dict[builtins.str, typing.Any]]] = None,
    location_header: typing.Optional[typing.Union[NsxtAlbVirtualServiceHttpRespRulesRuleMatchCriteriaLocationHeader, typing.Dict[builtins.str, typing.Any]]] = None,
    path: typing.Optional[typing.Union[NsxtAlbVirtualServiceHttpRespRulesRuleMatchCriteriaPath, typing.Dict[builtins.str, typing.Any]]] = None,
    protocol_type: typing.Optional[builtins.str] = None,
    query: typing.Optional[typing.Sequence[builtins.str]] = None,
    request_headers: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[NsxtAlbVirtualServiceHttpRespRulesRuleMatchCriteriaRequestHeaders, typing.Dict[builtins.str, typing.Any]]]]] = None,
    response_headers: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[NsxtAlbVirtualServiceHttpRespRulesRuleMatchCriteriaResponseHeaders, typing.Dict[builtins.str, typing.Any]]]]] = None,
    service_ports: typing.Optional[typing.Union[NsxtAlbVirtualServiceHttpRespRulesRuleMatchCriteriaServicePorts, typing.Dict[builtins.str, typing.Any]]] = None,
    status_code: typing.Optional[typing.Union[NsxtAlbVirtualServiceHttpRespRulesRuleMatchCriteriaStatusCode, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b79df52a155703debf15261c9e302b20666a14e801e73262cd10a06d6b2551e9(
    *,
    criteria: builtins.str,
    ip_addresses: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c02fb0e6bab2aa2c949dbe64185cb6d86f8180c216aa813c0af8725287167c01(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ffd2891df488d28afd8f7737f841f1488d500caa900658c27d752814707da952(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b6f9ce6e4d5f0361d3f987c0cfdac4d02ef5961d044633769488ff841568751c(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__71cf34dbd405e944611a529537f572317f9697185388099d80fc179322fa12a6(
    value: typing.Optional[NsxtAlbVirtualServiceHttpRespRulesRuleMatchCriteriaClientIpAddress],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__13c846265ff3d0e3196dd753a40258869a07fb461a79c0cdd5c792afd116373d(
    *,
    criteria: builtins.str,
    name: builtins.str,
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb4626c39d9d2ddf6a3dd902ebd323ede5d422c8f09641e66a13dd4e931bb24e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9030b33e52a7a2d92c1c09f10ba829da8fad03d4032c9cf866baf9931f16fe31(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f5fae20e151e2a11bf81aec58b1552f0de1a241b251acb921a470f64f51b1b9a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c20b1e4131aa919ba737e3f32510d461cea56914a8d38bb2433ff02e708a9691(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a6cf7966fb622588ceecb3f97c87401ff8a1cd4f9362d227b93fd7419f462fd(
    value: typing.Optional[NsxtAlbVirtualServiceHttpRespRulesRuleMatchCriteriaCookie],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__adbda982c5b277987cc15b6149d11e71a2145f6efc2f56bd5e566d2b44428f55(
    *,
    criteria: builtins.str,
    methods: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fdfcc0ca9aee2a82c33704bbeccb446ff68be82d35ce6d093eefaf6350bf1203(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__474988e03530475b23ced2120d0272e90491432f64ecb40b6d56c9889693df31(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d29a7b2afbb326d9172f9fe70107d7758945babf357966ebe64e9e37b355b4db(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__70b2bf665ba89faea018ea2add31fba8405c73a7985c3757141aaf1fec37c22a(
    value: typing.Optional[NsxtAlbVirtualServiceHttpRespRulesRuleMatchCriteriaHttpMethods],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e7c479f8a1ac5e7e56a3269c1ed8ec639db0c12ca7f8f6dc8f958f1d763cb0b(
    *,
    criteria: builtins.str,
    values: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5198f90eb3daf9bb6958c68a61b81ee89c91f1089a55a9e668dc91cb0eb0a46c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b419fe111ecd4d677f839ab3f10e33ffca7ce8e115a9aa1bf9cfafc2a34fad5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c3ab4edddf61d295fed1b21569481f972897887793421f10dc66b6c47a31f48(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c027a336ad1daca62a2db9b8ab5f869e00ccfd0df7f79656fc6a01f506f2232(
    value: typing.Optional[NsxtAlbVirtualServiceHttpRespRulesRuleMatchCriteriaLocationHeader],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f741dd2a2c2d4e57017f8e793c32099eb0ffc2ca6d0d9de5fd281a47ed338ff(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__417424f053dfad5e1923d1ba6a8e2201a8f0b9f1a6588b0720292b364397565e(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[NsxtAlbVirtualServiceHttpRespRulesRuleMatchCriteriaRequestHeaders, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7600f3c9ea57e870672c24d71a51599da108b6dacba0a7141ba58a2d36438384(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[NsxtAlbVirtualServiceHttpRespRulesRuleMatchCriteriaResponseHeaders, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__488962c2baccbbc82229ab3ea78bfcb8b2f2a05bd5f162d1b82134163a6e6aac(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a1b5ea97bdd28ed4e8d7ef7712a5b0915baa7bf67cc7ecfc21e5737897d84bed(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d7d53139c037fac8a305ece5bb8827c2cecad77627383b912c58d4c84352a264(
    value: typing.Optional[NsxtAlbVirtualServiceHttpRespRulesRuleMatchCriteria],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b3a6f11c82d3c031bc16317a10c4299481f58dd3ef95fe5136dec6d7f521ecf(
    *,
    criteria: builtins.str,
    paths: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__550ee11065880d21c803f337b7979604584fbe619ca8440283044daf5df8bfff(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__85ab07a920aba08f979cbf5e6fd427b61d0f2ca503b9e7a91f9abbe056842af6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b7a4cd6324b2e71bb2dddd2346b873abb08d289589783bd7f48398f0e23a351(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c8373b9f09c8e2886a0d131569edfcb18e7bbd9cba80ff25c734d04d1b04eb2f(
    value: typing.Optional[NsxtAlbVirtualServiceHttpRespRulesRuleMatchCriteriaPath],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e4ec8e58d0e9fcb7b45651a14652f6428b595ab27de4c8e4b3631e3435261e6f(
    *,
    criteria: builtins.str,
    name: builtins.str,
    values: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca19fa6aa04083108b24fb2dd5236ad009d5a6314eb164107dbccb46c028d2a6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__16d7dd31a75582e3f331aa4466a020daa21c08a1347697bc1a6d5fa36867c477(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf2677a1f27c4b8fab9e7a6a2aeaf2c34ea2fe4089812a9792a754423733b563(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2bf406f318c817a3d151e72cf189f5e81204d2b18d50edd3bd352e1293486bc5(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__659eb46fdac0566ee4459ce6dc91a213db5f4ac7fd1cb8726f73fa8a2f3f1cf2(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f2eadcdaa8705f6088d20b2be1b522cae28aa967b1e205bfc0802a216e988501(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NsxtAlbVirtualServiceHttpRespRulesRuleMatchCriteriaRequestHeaders]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__99f50bb85711bbafce509adc5111f3b11ec1b8d20c33fc8b9a3092742fe97308(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a08b7165880160c7e96c0ebc46628bf8acc53eb6bdce705d84221c07d0c87d1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c58726aea9589d8cd8c10e8c5f119121f5d2979f91865324fe3a583bc8a7d2c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3723d31a2cf0716f09bdc13576a7ab7f7e0a221b2f958963c6e71f04726c639e(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b05e5994dcc8d1678b3c405cabec0ac2dc0b79ce63ce3bda23d8970b9a8b2e4(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NsxtAlbVirtualServiceHttpRespRulesRuleMatchCriteriaRequestHeaders]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd287c3bbcfcb241eca66a3939832a127bfd2c941b9fac16d2441283bb6993ca(
    *,
    criteria: builtins.str,
    name: typing.Optional[builtins.str] = None,
    values: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f1e01f283e56f62f07d5019926c5f5e751a70a633b7953a79e8ba1ae1a0aafa0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__00e109aef4375b49ed4c1abaacbe8ffddff96f0ef3eac65749c3eb26d5328e17(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f82c7055829579f928b28ea654b70667126fabc9b68261b8076549df8a42c877(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d7244bdda286ca9a9ff161f244945f4aee6b86cc7d040afeb686692443e83751(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a1f3654938bd47c567128fb8110b9bce14df4c9dceb73ad519fa6926ede010bc(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef746bcd981748b07f2aa2ecbb79fd307f0785eff703dd279b4df1e1bc5d3b20(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NsxtAlbVirtualServiceHttpRespRulesRuleMatchCriteriaResponseHeaders]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a03208e70c39c886b506ca098ab7bd08ed29bf101f12a14a74ed71c74855bef7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e4202bc996f1b5a1801f47109161dc0325317fbb4b44d9d164a570b568d9039(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f575246ea51c855926003916888ba86820d36f0a67bffbddc2b553d5ab9129c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d27e21db720d2ad5040fa9cb80bc870535dc86fea3058b8f0b166b03524f7f38(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__14b923977e2697558fa7f6ec2362b02b48844ca04d36e60bc25cd51d75973fd5(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NsxtAlbVirtualServiceHttpRespRulesRuleMatchCriteriaResponseHeaders]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7804047ae2eae18536652567b8f934b68c1bc29f183e12e4bd11ec0c8b03b513(
    *,
    criteria: builtins.str,
    ports: typing.Sequence[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9898d4bb1d2060005a21013220a512a8b660f9cd3bfde58816421fedea51060c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__87b466c9c6b6c4f31df27414adb14f2aa0193c97e924ce0fe34a3e5452dc5c6d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a8b89bd2fa461a9c60b6fa4588659605cc7c6ba5cdb8ce307a8813982eb9539(
    value: typing.List[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b1f0b237c6ec90b35d45861971ce1a9559e8c67a7a86f7b3e4d4d33ef82a4b0(
    value: typing.Optional[NsxtAlbVirtualServiceHttpRespRulesRuleMatchCriteriaServicePorts],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8278111a2a5ba0785f937e0d9d761e0afc572749863a9aa2d9792c2948867662(
    *,
    criteria: builtins.str,
    http_status_code: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d6c1994be32be07ada2708d9d7023f5fdffc2d5bc8887868d8ce77118655319f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5980359121d7275de8363ccf938abced5dd24b2d804c63c37f41f5fbfe18fb7d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cdfc19e27543dcf7f495feaf284d8c817c2079e641471ae780117921339aff1a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__258114cc715513919ee40ec7e39840427d10a140a66cdd7a7336f8d339bd4346(
    value: typing.Optional[NsxtAlbVirtualServiceHttpRespRulesRuleMatchCriteriaStatusCode],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f5b857db81e87d3ca37f0033a83a64494dc06e125693d3a3d655368a6c11bff(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__07d48045b85b9e489c87d1ebe1f2437986e40187ec45deb832f9fd49ea247787(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c55482a8f090026aa06c61901441bf4c28384fe3421bbd45253264f6b9d15e54(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e4748b42da2c9391d9b6752b4d0ae46b47facb0f281640b0469c4ddebc1446d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b5009a40b3dd0277cbb21997b04e517935c3308451bc393a4fc962bedeb6153(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NsxtAlbVirtualServiceHttpRespRulesRule]],
) -> None:
    """Type checking stubs"""
    pass
