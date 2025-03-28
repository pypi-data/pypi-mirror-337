'''
# `vcd_org_ldap`

Refer to the Terraform Registry for docs: [`vcd_org_ldap`](https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_ldap).
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


class OrgLdap(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="vcd.orgLdap.OrgLdap",
):
    '''Represents a {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_ldap vcd_org_ldap}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        ldap_mode: builtins.str,
        org_id: builtins.str,
        custom_settings: typing.Optional[typing.Union["OrgLdapCustomSettings", typing.Dict[builtins.str, typing.Any]]] = None,
        custom_user_ou: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_ldap vcd_org_ldap} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param ldap_mode: Type of LDAP settings (one of NONE, SYSTEM, CUSTOM). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_ldap#ldap_mode OrgLdap#ldap_mode}
        :param org_id: Organization ID. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_ldap#org_id OrgLdap#org_id}
        :param custom_settings: custom_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_ldap#custom_settings OrgLdap#custom_settings}
        :param custom_user_ou: If ldap_mode is SYSTEM, specifies a LDAP attribute=value pair to use for OU (organizational unit). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_ldap#custom_user_ou OrgLdap#custom_user_ou}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_ldap#id OrgLdap#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cb6b70a528aa992bb290b4788ff72fae5122e7fa20fa119f95dc77ef9814ee38)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = OrgLdapConfig(
            ldap_mode=ldap_mode,
            org_id=org_id,
            custom_settings=custom_settings,
            custom_user_ou=custom_user_ou,
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
        '''Generates CDKTF code for importing a OrgLdap resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the OrgLdap to import.
        :param import_from_id: The id of the existing OrgLdap that should be imported. Refer to the {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_ldap#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the OrgLdap to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f4a0294ff62f8de4e7810a3de73dd142ad53535c8f5705898a4df1977658c674)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putCustomSettings")
    def put_custom_settings(
        self,
        *,
        authentication_method: builtins.str,
        connector_type: builtins.str,
        group_attributes: typing.Union["OrgLdapCustomSettingsGroupAttributes", typing.Dict[builtins.str, typing.Any]],
        port: jsii.Number,
        server: builtins.str,
        user_attributes: typing.Union["OrgLdapCustomSettingsUserAttributes", typing.Dict[builtins.str, typing.Any]],
        base_distinguished_name: typing.Optional[builtins.str] = None,
        is_ssl: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        password: typing.Optional[builtins.str] = None,
        username: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param authentication_method: authentication method: one of SIMPLE, MD5DIGEST, NTLM. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_ldap#authentication_method OrgLdap#authentication_method}
        :param connector_type: type of connector: one of OPEN_LDAP, ACTIVE_DIRECTORY. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_ldap#connector_type OrgLdap#connector_type}
        :param group_attributes: group_attributes block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_ldap#group_attributes OrgLdap#group_attributes}
        :param port: Port number for LDAP service. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_ldap#port OrgLdap#port}
        :param server: host name or IP of the LDAP server. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_ldap#server OrgLdap#server}
        :param user_attributes: user_attributes block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_ldap#user_attributes OrgLdap#user_attributes}
        :param base_distinguished_name: LDAP search base. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_ldap#base_distinguished_name OrgLdap#base_distinguished_name}
        :param is_ssl: True if the LDAP service requires an SSL connection. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_ldap#is_ssl OrgLdap#is_ssl}
        :param password: Password for the user identified by UserName. This value is never returned by GET. It is inspected on create and modify. On modify, the absence of this element indicates that the password should not be changed Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_ldap#password OrgLdap#password}
        :param username: Username to use when logging in to LDAP, specified using LDAP attribute=value pairs (for example: cn="ldap-admin", c="example", dc="com"). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_ldap#username OrgLdap#username}
        '''
        value = OrgLdapCustomSettings(
            authentication_method=authentication_method,
            connector_type=connector_type,
            group_attributes=group_attributes,
            port=port,
            server=server,
            user_attributes=user_attributes,
            base_distinguished_name=base_distinguished_name,
            is_ssl=is_ssl,
            password=password,
            username=username,
        )

        return typing.cast(None, jsii.invoke(self, "putCustomSettings", [value]))

    @jsii.member(jsii_name="resetCustomSettings")
    def reset_custom_settings(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCustomSettings", []))

    @jsii.member(jsii_name="resetCustomUserOu")
    def reset_custom_user_ou(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCustomUserOu", []))

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
    @jsii.member(jsii_name="customSettings")
    def custom_settings(self) -> "OrgLdapCustomSettingsOutputReference":
        return typing.cast("OrgLdapCustomSettingsOutputReference", jsii.get(self, "customSettings"))

    @builtins.property
    @jsii.member(jsii_name="customSettingsInput")
    def custom_settings_input(self) -> typing.Optional["OrgLdapCustomSettings"]:
        return typing.cast(typing.Optional["OrgLdapCustomSettings"], jsii.get(self, "customSettingsInput"))

    @builtins.property
    @jsii.member(jsii_name="customUserOuInput")
    def custom_user_ou_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "customUserOuInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="ldapModeInput")
    def ldap_mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "ldapModeInput"))

    @builtins.property
    @jsii.member(jsii_name="orgIdInput")
    def org_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "orgIdInput"))

    @builtins.property
    @jsii.member(jsii_name="customUserOu")
    def custom_user_ou(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "customUserOu"))

    @custom_user_ou.setter
    def custom_user_ou(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ffd97bedc73fdf34031f86119a751d374bebbe045d4a3d56f4b11666565cfab6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "customUserOu", value)

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b0ac415b8f2e0ef7f07a38387cb50845c2a5584f93e7e1372ba6fe19058f1b43)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="ldapMode")
    def ldap_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ldapMode"))

    @ldap_mode.setter
    def ldap_mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3d8c8df8fcb2041108a90e571f808fcd02a3731d74775398ff99010fdc87d80c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ldapMode", value)

    @builtins.property
    @jsii.member(jsii_name="orgId")
    def org_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "orgId"))

    @org_id.setter
    def org_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__78f6915b69a65b5fc40bcc6c2a62357c1b6ab4cea53ad1035f366dfb9a8999f0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "orgId", value)


@jsii.data_type(
    jsii_type="vcd.orgLdap.OrgLdapConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "ldap_mode": "ldapMode",
        "org_id": "orgId",
        "custom_settings": "customSettings",
        "custom_user_ou": "customUserOu",
        "id": "id",
    },
)
class OrgLdapConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        ldap_mode: builtins.str,
        org_id: builtins.str,
        custom_settings: typing.Optional[typing.Union["OrgLdapCustomSettings", typing.Dict[builtins.str, typing.Any]]] = None,
        custom_user_ou: typing.Optional[builtins.str] = None,
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
        :param ldap_mode: Type of LDAP settings (one of NONE, SYSTEM, CUSTOM). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_ldap#ldap_mode OrgLdap#ldap_mode}
        :param org_id: Organization ID. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_ldap#org_id OrgLdap#org_id}
        :param custom_settings: custom_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_ldap#custom_settings OrgLdap#custom_settings}
        :param custom_user_ou: If ldap_mode is SYSTEM, specifies a LDAP attribute=value pair to use for OU (organizational unit). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_ldap#custom_user_ou OrgLdap#custom_user_ou}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_ldap#id OrgLdap#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(custom_settings, dict):
            custom_settings = OrgLdapCustomSettings(**custom_settings)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e3592d0adc7b6328ea28fa7147bd347f3c0de99e827b9385ec4691a7713c866e)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument ldap_mode", value=ldap_mode, expected_type=type_hints["ldap_mode"])
            check_type(argname="argument org_id", value=org_id, expected_type=type_hints["org_id"])
            check_type(argname="argument custom_settings", value=custom_settings, expected_type=type_hints["custom_settings"])
            check_type(argname="argument custom_user_ou", value=custom_user_ou, expected_type=type_hints["custom_user_ou"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "ldap_mode": ldap_mode,
            "org_id": org_id,
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
        if custom_settings is not None:
            self._values["custom_settings"] = custom_settings
        if custom_user_ou is not None:
            self._values["custom_user_ou"] = custom_user_ou
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
    def ldap_mode(self) -> builtins.str:
        '''Type of LDAP settings (one of NONE, SYSTEM, CUSTOM).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_ldap#ldap_mode OrgLdap#ldap_mode}
        '''
        result = self._values.get("ldap_mode")
        assert result is not None, "Required property 'ldap_mode' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def org_id(self) -> builtins.str:
        '''Organization ID.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_ldap#org_id OrgLdap#org_id}
        '''
        result = self._values.get("org_id")
        assert result is not None, "Required property 'org_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def custom_settings(self) -> typing.Optional["OrgLdapCustomSettings"]:
        '''custom_settings block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_ldap#custom_settings OrgLdap#custom_settings}
        '''
        result = self._values.get("custom_settings")
        return typing.cast(typing.Optional["OrgLdapCustomSettings"], result)

    @builtins.property
    def custom_user_ou(self) -> typing.Optional[builtins.str]:
        '''If ldap_mode is SYSTEM, specifies a LDAP attribute=value pair to use for OU (organizational unit).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_ldap#custom_user_ou OrgLdap#custom_user_ou}
        '''
        result = self._values.get("custom_user_ou")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_ldap#id OrgLdap#id}.

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
        return "OrgLdapConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="vcd.orgLdap.OrgLdapCustomSettings",
    jsii_struct_bases=[],
    name_mapping={
        "authentication_method": "authenticationMethod",
        "connector_type": "connectorType",
        "group_attributes": "groupAttributes",
        "port": "port",
        "server": "server",
        "user_attributes": "userAttributes",
        "base_distinguished_name": "baseDistinguishedName",
        "is_ssl": "isSsl",
        "password": "password",
        "username": "username",
    },
)
class OrgLdapCustomSettings:
    def __init__(
        self,
        *,
        authentication_method: builtins.str,
        connector_type: builtins.str,
        group_attributes: typing.Union["OrgLdapCustomSettingsGroupAttributes", typing.Dict[builtins.str, typing.Any]],
        port: jsii.Number,
        server: builtins.str,
        user_attributes: typing.Union["OrgLdapCustomSettingsUserAttributes", typing.Dict[builtins.str, typing.Any]],
        base_distinguished_name: typing.Optional[builtins.str] = None,
        is_ssl: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        password: typing.Optional[builtins.str] = None,
        username: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param authentication_method: authentication method: one of SIMPLE, MD5DIGEST, NTLM. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_ldap#authentication_method OrgLdap#authentication_method}
        :param connector_type: type of connector: one of OPEN_LDAP, ACTIVE_DIRECTORY. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_ldap#connector_type OrgLdap#connector_type}
        :param group_attributes: group_attributes block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_ldap#group_attributes OrgLdap#group_attributes}
        :param port: Port number for LDAP service. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_ldap#port OrgLdap#port}
        :param server: host name or IP of the LDAP server. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_ldap#server OrgLdap#server}
        :param user_attributes: user_attributes block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_ldap#user_attributes OrgLdap#user_attributes}
        :param base_distinguished_name: LDAP search base. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_ldap#base_distinguished_name OrgLdap#base_distinguished_name}
        :param is_ssl: True if the LDAP service requires an SSL connection. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_ldap#is_ssl OrgLdap#is_ssl}
        :param password: Password for the user identified by UserName. This value is never returned by GET. It is inspected on create and modify. On modify, the absence of this element indicates that the password should not be changed Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_ldap#password OrgLdap#password}
        :param username: Username to use when logging in to LDAP, specified using LDAP attribute=value pairs (for example: cn="ldap-admin", c="example", dc="com"). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_ldap#username OrgLdap#username}
        '''
        if isinstance(group_attributes, dict):
            group_attributes = OrgLdapCustomSettingsGroupAttributes(**group_attributes)
        if isinstance(user_attributes, dict):
            user_attributes = OrgLdapCustomSettingsUserAttributes(**user_attributes)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__27e344e592b64fff18c2fa7352dfe2d850c68b4a574681e3ec82933d35c584dd)
            check_type(argname="argument authentication_method", value=authentication_method, expected_type=type_hints["authentication_method"])
            check_type(argname="argument connector_type", value=connector_type, expected_type=type_hints["connector_type"])
            check_type(argname="argument group_attributes", value=group_attributes, expected_type=type_hints["group_attributes"])
            check_type(argname="argument port", value=port, expected_type=type_hints["port"])
            check_type(argname="argument server", value=server, expected_type=type_hints["server"])
            check_type(argname="argument user_attributes", value=user_attributes, expected_type=type_hints["user_attributes"])
            check_type(argname="argument base_distinguished_name", value=base_distinguished_name, expected_type=type_hints["base_distinguished_name"])
            check_type(argname="argument is_ssl", value=is_ssl, expected_type=type_hints["is_ssl"])
            check_type(argname="argument password", value=password, expected_type=type_hints["password"])
            check_type(argname="argument username", value=username, expected_type=type_hints["username"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "authentication_method": authentication_method,
            "connector_type": connector_type,
            "group_attributes": group_attributes,
            "port": port,
            "server": server,
            "user_attributes": user_attributes,
        }
        if base_distinguished_name is not None:
            self._values["base_distinguished_name"] = base_distinguished_name
        if is_ssl is not None:
            self._values["is_ssl"] = is_ssl
        if password is not None:
            self._values["password"] = password
        if username is not None:
            self._values["username"] = username

    @builtins.property
    def authentication_method(self) -> builtins.str:
        '''authentication method: one of SIMPLE, MD5DIGEST, NTLM.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_ldap#authentication_method OrgLdap#authentication_method}
        '''
        result = self._values.get("authentication_method")
        assert result is not None, "Required property 'authentication_method' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def connector_type(self) -> builtins.str:
        '''type of connector: one of OPEN_LDAP, ACTIVE_DIRECTORY.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_ldap#connector_type OrgLdap#connector_type}
        '''
        result = self._values.get("connector_type")
        assert result is not None, "Required property 'connector_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def group_attributes(self) -> "OrgLdapCustomSettingsGroupAttributes":
        '''group_attributes block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_ldap#group_attributes OrgLdap#group_attributes}
        '''
        result = self._values.get("group_attributes")
        assert result is not None, "Required property 'group_attributes' is missing"
        return typing.cast("OrgLdapCustomSettingsGroupAttributes", result)

    @builtins.property
    def port(self) -> jsii.Number:
        '''Port number for LDAP service.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_ldap#port OrgLdap#port}
        '''
        result = self._values.get("port")
        assert result is not None, "Required property 'port' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def server(self) -> builtins.str:
        '''host name or IP of the LDAP server.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_ldap#server OrgLdap#server}
        '''
        result = self._values.get("server")
        assert result is not None, "Required property 'server' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def user_attributes(self) -> "OrgLdapCustomSettingsUserAttributes":
        '''user_attributes block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_ldap#user_attributes OrgLdap#user_attributes}
        '''
        result = self._values.get("user_attributes")
        assert result is not None, "Required property 'user_attributes' is missing"
        return typing.cast("OrgLdapCustomSettingsUserAttributes", result)

    @builtins.property
    def base_distinguished_name(self) -> typing.Optional[builtins.str]:
        '''LDAP search base.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_ldap#base_distinguished_name OrgLdap#base_distinguished_name}
        '''
        result = self._values.get("base_distinguished_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def is_ssl(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''True if the LDAP service requires an SSL connection.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_ldap#is_ssl OrgLdap#is_ssl}
        '''
        result = self._values.get("is_ssl")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def password(self) -> typing.Optional[builtins.str]:
        '''Password for the user identified by UserName.

        This value is never returned by GET. It is inspected on create and modify. On modify, the absence of this element indicates that the password should not be changed

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_ldap#password OrgLdap#password}
        '''
        result = self._values.get("password")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def username(self) -> typing.Optional[builtins.str]:
        '''Username to use when logging in to LDAP, specified using LDAP attribute=value pairs (for example: cn="ldap-admin", c="example", dc="com").

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_ldap#username OrgLdap#username}
        '''
        result = self._values.get("username")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OrgLdapCustomSettings(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="vcd.orgLdap.OrgLdapCustomSettingsGroupAttributes",
    jsii_struct_bases=[],
    name_mapping={
        "group_membership_identifier": "groupMembershipIdentifier",
        "membership": "membership",
        "name": "name",
        "object_class": "objectClass",
        "unique_identifier": "uniqueIdentifier",
        "group_back_link_identifier": "groupBackLinkIdentifier",
    },
)
class OrgLdapCustomSettingsGroupAttributes:
    def __init__(
        self,
        *,
        group_membership_identifier: builtins.str,
        membership: builtins.str,
        name: builtins.str,
        object_class: builtins.str,
        unique_identifier: builtins.str,
        group_back_link_identifier: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param group_membership_identifier: LDAP attribute that identifies a group as a member of another group. For example, dn. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_ldap#group_membership_identifier OrgLdap#group_membership_identifier}
        :param membership: LDAP attribute to use when getting the members of a group. For example, member. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_ldap#membership OrgLdap#membership}
        :param name: LDAP attribute to use for the group name. For example, cn. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_ldap#name OrgLdap#name}
        :param object_class: LDAP objectClass of which imported groups are members. For example, group. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_ldap#object_class OrgLdap#object_class}
        :param unique_identifier: LDAP attribute to use as the unique identifier for a group. For example, objectGuid. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_ldap#unique_identifier OrgLdap#unique_identifier}
        :param group_back_link_identifier: LDAP group attribute used to identify a group member. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_ldap#group_back_link_identifier OrgLdap#group_back_link_identifier}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fd25735985ea80e8c5159d80c38f0614615aae7f1edf2d9bb7d539685945c9ec)
            check_type(argname="argument group_membership_identifier", value=group_membership_identifier, expected_type=type_hints["group_membership_identifier"])
            check_type(argname="argument membership", value=membership, expected_type=type_hints["membership"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument object_class", value=object_class, expected_type=type_hints["object_class"])
            check_type(argname="argument unique_identifier", value=unique_identifier, expected_type=type_hints["unique_identifier"])
            check_type(argname="argument group_back_link_identifier", value=group_back_link_identifier, expected_type=type_hints["group_back_link_identifier"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "group_membership_identifier": group_membership_identifier,
            "membership": membership,
            "name": name,
            "object_class": object_class,
            "unique_identifier": unique_identifier,
        }
        if group_back_link_identifier is not None:
            self._values["group_back_link_identifier"] = group_back_link_identifier

    @builtins.property
    def group_membership_identifier(self) -> builtins.str:
        '''LDAP attribute that identifies a group as a member of another group. For example, dn.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_ldap#group_membership_identifier OrgLdap#group_membership_identifier}
        '''
        result = self._values.get("group_membership_identifier")
        assert result is not None, "Required property 'group_membership_identifier' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def membership(self) -> builtins.str:
        '''LDAP attribute to use when getting the members of a group. For example, member.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_ldap#membership OrgLdap#membership}
        '''
        result = self._values.get("membership")
        assert result is not None, "Required property 'membership' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''LDAP attribute to use for the group name. For example, cn.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_ldap#name OrgLdap#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def object_class(self) -> builtins.str:
        '''LDAP objectClass of which imported groups are members. For example, group.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_ldap#object_class OrgLdap#object_class}
        '''
        result = self._values.get("object_class")
        assert result is not None, "Required property 'object_class' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def unique_identifier(self) -> builtins.str:
        '''LDAP attribute to use as the unique identifier for a group. For example, objectGuid.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_ldap#unique_identifier OrgLdap#unique_identifier}
        '''
        result = self._values.get("unique_identifier")
        assert result is not None, "Required property 'unique_identifier' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def group_back_link_identifier(self) -> typing.Optional[builtins.str]:
        '''LDAP group attribute used to identify a group member.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_ldap#group_back_link_identifier OrgLdap#group_back_link_identifier}
        '''
        result = self._values.get("group_back_link_identifier")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OrgLdapCustomSettingsGroupAttributes(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OrgLdapCustomSettingsGroupAttributesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="vcd.orgLdap.OrgLdapCustomSettingsGroupAttributesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e7d0af7705f34c7cfd3e4527d0118339b36be276f17bad31c26d77c111da527a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetGroupBackLinkIdentifier")
    def reset_group_back_link_identifier(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGroupBackLinkIdentifier", []))

    @builtins.property
    @jsii.member(jsii_name="groupBackLinkIdentifierInput")
    def group_back_link_identifier_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "groupBackLinkIdentifierInput"))

    @builtins.property
    @jsii.member(jsii_name="groupMembershipIdentifierInput")
    def group_membership_identifier_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "groupMembershipIdentifierInput"))

    @builtins.property
    @jsii.member(jsii_name="membershipInput")
    def membership_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "membershipInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="objectClassInput")
    def object_class_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "objectClassInput"))

    @builtins.property
    @jsii.member(jsii_name="uniqueIdentifierInput")
    def unique_identifier_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "uniqueIdentifierInput"))

    @builtins.property
    @jsii.member(jsii_name="groupBackLinkIdentifier")
    def group_back_link_identifier(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "groupBackLinkIdentifier"))

    @group_back_link_identifier.setter
    def group_back_link_identifier(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__18d3ef7ecfa680317ebb6910eb121e26f356372bf64fa0ae14f3f030705ab1be)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "groupBackLinkIdentifier", value)

    @builtins.property
    @jsii.member(jsii_name="groupMembershipIdentifier")
    def group_membership_identifier(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "groupMembershipIdentifier"))

    @group_membership_identifier.setter
    def group_membership_identifier(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cb6bda7c3777f7ece632f62be1b1a0bc7226503206f267651208211412cc0b59)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "groupMembershipIdentifier", value)

    @builtins.property
    @jsii.member(jsii_name="membership")
    def membership(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "membership"))

    @membership.setter
    def membership(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__83361e41e234b4abfd8353f938077210986bbe752aa50117c451581ee7df2ca8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "membership", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__549ad5b4784aa86c33c96f29c1e70e770efaa116f933344353c39661a2604b66)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="objectClass")
    def object_class(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "objectClass"))

    @object_class.setter
    def object_class(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c4f94733081aac4232c9b5c5efff7c750d321d07f473b708fd44b74733f472f8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "objectClass", value)

    @builtins.property
    @jsii.member(jsii_name="uniqueIdentifier")
    def unique_identifier(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "uniqueIdentifier"))

    @unique_identifier.setter
    def unique_identifier(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c7b5045f1bbdf999211dd18b6783717d875b36692dc6e18f913f161d8367408a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "uniqueIdentifier", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[OrgLdapCustomSettingsGroupAttributes]:
        return typing.cast(typing.Optional[OrgLdapCustomSettingsGroupAttributes], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[OrgLdapCustomSettingsGroupAttributes],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__758b67a2b6bbf4e84e4bc521d11a2849cf3d8e27c4c89716b62bcc295537dc71)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class OrgLdapCustomSettingsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="vcd.orgLdap.OrgLdapCustomSettingsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__835eaeee164fee12952f31320bc9639ddc48cf3b74c7863bd91932518e8d83db)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putGroupAttributes")
    def put_group_attributes(
        self,
        *,
        group_membership_identifier: builtins.str,
        membership: builtins.str,
        name: builtins.str,
        object_class: builtins.str,
        unique_identifier: builtins.str,
        group_back_link_identifier: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param group_membership_identifier: LDAP attribute that identifies a group as a member of another group. For example, dn. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_ldap#group_membership_identifier OrgLdap#group_membership_identifier}
        :param membership: LDAP attribute to use when getting the members of a group. For example, member. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_ldap#membership OrgLdap#membership}
        :param name: LDAP attribute to use for the group name. For example, cn. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_ldap#name OrgLdap#name}
        :param object_class: LDAP objectClass of which imported groups are members. For example, group. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_ldap#object_class OrgLdap#object_class}
        :param unique_identifier: LDAP attribute to use as the unique identifier for a group. For example, objectGuid. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_ldap#unique_identifier OrgLdap#unique_identifier}
        :param group_back_link_identifier: LDAP group attribute used to identify a group member. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_ldap#group_back_link_identifier OrgLdap#group_back_link_identifier}
        '''
        value = OrgLdapCustomSettingsGroupAttributes(
            group_membership_identifier=group_membership_identifier,
            membership=membership,
            name=name,
            object_class=object_class,
            unique_identifier=unique_identifier,
            group_back_link_identifier=group_back_link_identifier,
        )

        return typing.cast(None, jsii.invoke(self, "putGroupAttributes", [value]))

    @jsii.member(jsii_name="putUserAttributes")
    def put_user_attributes(
        self,
        *,
        display_name: builtins.str,
        email: builtins.str,
        given_name: builtins.str,
        group_membership_identifier: builtins.str,
        object_class: builtins.str,
        surname: builtins.str,
        telephone: builtins.str,
        unique_identifier: builtins.str,
        username: builtins.str,
        group_back_link_identifier: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param display_name: LDAP attribute to use for the user's full name. For example, displayName. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_ldap#display_name OrgLdap#display_name}
        :param email: LDAP attribute to use for the user's email address. For example, mail. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_ldap#email OrgLdap#email}
        :param given_name: LDAP attribute to use for the user's given name. For example, givenName. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_ldap#given_name OrgLdap#given_name}
        :param group_membership_identifier: LDAP attribute that identifies a user as a member of a group. For example, dn. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_ldap#group_membership_identifier OrgLdap#group_membership_identifier}
        :param object_class: LDAP objectClass of which imported users are members. For example, user or person. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_ldap#object_class OrgLdap#object_class}
        :param surname: LDAP attribute to use for the user's surname. For example, sn. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_ldap#surname OrgLdap#surname}
        :param telephone: LDAP attribute to use for the user's telephone number. For example, telephoneNumber. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_ldap#telephone OrgLdap#telephone}
        :param unique_identifier: LDAP attribute to use as the unique identifier for a user. For example, objectGuid. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_ldap#unique_identifier OrgLdap#unique_identifier}
        :param username: LDAP attribute to use when looking up a user name to import. For example, userPrincipalName or samAccountName. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_ldap#username OrgLdap#username}
        :param group_back_link_identifier: LDAP attribute that returns the identifiers of all the groups of which the user is a member. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_ldap#group_back_link_identifier OrgLdap#group_back_link_identifier}
        '''
        value = OrgLdapCustomSettingsUserAttributes(
            display_name=display_name,
            email=email,
            given_name=given_name,
            group_membership_identifier=group_membership_identifier,
            object_class=object_class,
            surname=surname,
            telephone=telephone,
            unique_identifier=unique_identifier,
            username=username,
            group_back_link_identifier=group_back_link_identifier,
        )

        return typing.cast(None, jsii.invoke(self, "putUserAttributes", [value]))

    @jsii.member(jsii_name="resetBaseDistinguishedName")
    def reset_base_distinguished_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBaseDistinguishedName", []))

    @jsii.member(jsii_name="resetIsSsl")
    def reset_is_ssl(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIsSsl", []))

    @jsii.member(jsii_name="resetPassword")
    def reset_password(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPassword", []))

    @jsii.member(jsii_name="resetUsername")
    def reset_username(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUsername", []))

    @builtins.property
    @jsii.member(jsii_name="groupAttributes")
    def group_attributes(self) -> OrgLdapCustomSettingsGroupAttributesOutputReference:
        return typing.cast(OrgLdapCustomSettingsGroupAttributesOutputReference, jsii.get(self, "groupAttributes"))

    @builtins.property
    @jsii.member(jsii_name="userAttributes")
    def user_attributes(self) -> "OrgLdapCustomSettingsUserAttributesOutputReference":
        return typing.cast("OrgLdapCustomSettingsUserAttributesOutputReference", jsii.get(self, "userAttributes"))

    @builtins.property
    @jsii.member(jsii_name="authenticationMethodInput")
    def authentication_method_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "authenticationMethodInput"))

    @builtins.property
    @jsii.member(jsii_name="baseDistinguishedNameInput")
    def base_distinguished_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "baseDistinguishedNameInput"))

    @builtins.property
    @jsii.member(jsii_name="connectorTypeInput")
    def connector_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "connectorTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="groupAttributesInput")
    def group_attributes_input(
        self,
    ) -> typing.Optional[OrgLdapCustomSettingsGroupAttributes]:
        return typing.cast(typing.Optional[OrgLdapCustomSettingsGroupAttributes], jsii.get(self, "groupAttributesInput"))

    @builtins.property
    @jsii.member(jsii_name="isSslInput")
    def is_ssl_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "isSslInput"))

    @builtins.property
    @jsii.member(jsii_name="passwordInput")
    def password_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "passwordInput"))

    @builtins.property
    @jsii.member(jsii_name="portInput")
    def port_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "portInput"))

    @builtins.property
    @jsii.member(jsii_name="serverInput")
    def server_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "serverInput"))

    @builtins.property
    @jsii.member(jsii_name="userAttributesInput")
    def user_attributes_input(
        self,
    ) -> typing.Optional["OrgLdapCustomSettingsUserAttributes"]:
        return typing.cast(typing.Optional["OrgLdapCustomSettingsUserAttributes"], jsii.get(self, "userAttributesInput"))

    @builtins.property
    @jsii.member(jsii_name="usernameInput")
    def username_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "usernameInput"))

    @builtins.property
    @jsii.member(jsii_name="authenticationMethod")
    def authentication_method(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "authenticationMethod"))

    @authentication_method.setter
    def authentication_method(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a28e5963cba785cb66a8a4cc96ad5e62c61599a76b7be5283c47085707c2dcfe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "authenticationMethod", value)

    @builtins.property
    @jsii.member(jsii_name="baseDistinguishedName")
    def base_distinguished_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "baseDistinguishedName"))

    @base_distinguished_name.setter
    def base_distinguished_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__76e076bee39cf8b19be52e3dd00832f45a58c0c40c9fd6465b3ec076e92fc2a3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "baseDistinguishedName", value)

    @builtins.property
    @jsii.member(jsii_name="connectorType")
    def connector_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "connectorType"))

    @connector_type.setter
    def connector_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__410bc2f66ebfc2afb33d3eecbd8c5873e171712dbffcc5c687cb313f896b93af)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "connectorType", value)

    @builtins.property
    @jsii.member(jsii_name="isSsl")
    def is_ssl(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "isSsl"))

    @is_ssl.setter
    def is_ssl(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f1084f35eec82cea9ab501cff728653fdb0afd3760fba8a7c0ffe07a44b69169)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "isSsl", value)

    @builtins.property
    @jsii.member(jsii_name="password")
    def password(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "password"))

    @password.setter
    def password(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fef27d88150f565df70fc2e75ec151d1eb7205ad98a81981bf48df033d0090c0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "password", value)

    @builtins.property
    @jsii.member(jsii_name="port")
    def port(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "port"))

    @port.setter
    def port(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__93ed471f5c97a682e9e9fe807cc5ee748fe48fefa2ae2dfb8f5a02fb8c0d5896)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "port", value)

    @builtins.property
    @jsii.member(jsii_name="server")
    def server(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "server"))

    @server.setter
    def server(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__68ce1f1cad50b19a7cedf751cae697717a95ec139a9d3c5cd2c34ce3afe24c90)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "server", value)

    @builtins.property
    @jsii.member(jsii_name="username")
    def username(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "username"))

    @username.setter
    def username(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7034ef9cbc859c77c535401d9ec82a3da7876c0184a9e3dacbac0dc78ad33637)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "username", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[OrgLdapCustomSettings]:
        return typing.cast(typing.Optional[OrgLdapCustomSettings], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[OrgLdapCustomSettings]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__572efdb1d685d93f91c501dda1e260eb6698d6434389e144d313ec36b6b556c7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="vcd.orgLdap.OrgLdapCustomSettingsUserAttributes",
    jsii_struct_bases=[],
    name_mapping={
        "display_name": "displayName",
        "email": "email",
        "given_name": "givenName",
        "group_membership_identifier": "groupMembershipIdentifier",
        "object_class": "objectClass",
        "surname": "surname",
        "telephone": "telephone",
        "unique_identifier": "uniqueIdentifier",
        "username": "username",
        "group_back_link_identifier": "groupBackLinkIdentifier",
    },
)
class OrgLdapCustomSettingsUserAttributes:
    def __init__(
        self,
        *,
        display_name: builtins.str,
        email: builtins.str,
        given_name: builtins.str,
        group_membership_identifier: builtins.str,
        object_class: builtins.str,
        surname: builtins.str,
        telephone: builtins.str,
        unique_identifier: builtins.str,
        username: builtins.str,
        group_back_link_identifier: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param display_name: LDAP attribute to use for the user's full name. For example, displayName. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_ldap#display_name OrgLdap#display_name}
        :param email: LDAP attribute to use for the user's email address. For example, mail. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_ldap#email OrgLdap#email}
        :param given_name: LDAP attribute to use for the user's given name. For example, givenName. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_ldap#given_name OrgLdap#given_name}
        :param group_membership_identifier: LDAP attribute that identifies a user as a member of a group. For example, dn. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_ldap#group_membership_identifier OrgLdap#group_membership_identifier}
        :param object_class: LDAP objectClass of which imported users are members. For example, user or person. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_ldap#object_class OrgLdap#object_class}
        :param surname: LDAP attribute to use for the user's surname. For example, sn. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_ldap#surname OrgLdap#surname}
        :param telephone: LDAP attribute to use for the user's telephone number. For example, telephoneNumber. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_ldap#telephone OrgLdap#telephone}
        :param unique_identifier: LDAP attribute to use as the unique identifier for a user. For example, objectGuid. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_ldap#unique_identifier OrgLdap#unique_identifier}
        :param username: LDAP attribute to use when looking up a user name to import. For example, userPrincipalName or samAccountName. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_ldap#username OrgLdap#username}
        :param group_back_link_identifier: LDAP attribute that returns the identifiers of all the groups of which the user is a member. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_ldap#group_back_link_identifier OrgLdap#group_back_link_identifier}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__88c36af6baf8ebc4551632c474c88df12cf7ff80a24062684c888ca4c7715733)
            check_type(argname="argument display_name", value=display_name, expected_type=type_hints["display_name"])
            check_type(argname="argument email", value=email, expected_type=type_hints["email"])
            check_type(argname="argument given_name", value=given_name, expected_type=type_hints["given_name"])
            check_type(argname="argument group_membership_identifier", value=group_membership_identifier, expected_type=type_hints["group_membership_identifier"])
            check_type(argname="argument object_class", value=object_class, expected_type=type_hints["object_class"])
            check_type(argname="argument surname", value=surname, expected_type=type_hints["surname"])
            check_type(argname="argument telephone", value=telephone, expected_type=type_hints["telephone"])
            check_type(argname="argument unique_identifier", value=unique_identifier, expected_type=type_hints["unique_identifier"])
            check_type(argname="argument username", value=username, expected_type=type_hints["username"])
            check_type(argname="argument group_back_link_identifier", value=group_back_link_identifier, expected_type=type_hints["group_back_link_identifier"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "display_name": display_name,
            "email": email,
            "given_name": given_name,
            "group_membership_identifier": group_membership_identifier,
            "object_class": object_class,
            "surname": surname,
            "telephone": telephone,
            "unique_identifier": unique_identifier,
            "username": username,
        }
        if group_back_link_identifier is not None:
            self._values["group_back_link_identifier"] = group_back_link_identifier

    @builtins.property
    def display_name(self) -> builtins.str:
        '''LDAP attribute to use for the user's full name. For example, displayName.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_ldap#display_name OrgLdap#display_name}
        '''
        result = self._values.get("display_name")
        assert result is not None, "Required property 'display_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def email(self) -> builtins.str:
        '''LDAP attribute to use for the user's email address. For example, mail.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_ldap#email OrgLdap#email}
        '''
        result = self._values.get("email")
        assert result is not None, "Required property 'email' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def given_name(self) -> builtins.str:
        '''LDAP attribute to use for the user's given name. For example, givenName.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_ldap#given_name OrgLdap#given_name}
        '''
        result = self._values.get("given_name")
        assert result is not None, "Required property 'given_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def group_membership_identifier(self) -> builtins.str:
        '''LDAP attribute that identifies a user as a member of a group. For example, dn.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_ldap#group_membership_identifier OrgLdap#group_membership_identifier}
        '''
        result = self._values.get("group_membership_identifier")
        assert result is not None, "Required property 'group_membership_identifier' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def object_class(self) -> builtins.str:
        '''LDAP objectClass of which imported users are members. For example, user or person.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_ldap#object_class OrgLdap#object_class}
        '''
        result = self._values.get("object_class")
        assert result is not None, "Required property 'object_class' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def surname(self) -> builtins.str:
        '''LDAP attribute to use for the user's surname. For example, sn.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_ldap#surname OrgLdap#surname}
        '''
        result = self._values.get("surname")
        assert result is not None, "Required property 'surname' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def telephone(self) -> builtins.str:
        '''LDAP attribute to use for the user's telephone number. For example, telephoneNumber.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_ldap#telephone OrgLdap#telephone}
        '''
        result = self._values.get("telephone")
        assert result is not None, "Required property 'telephone' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def unique_identifier(self) -> builtins.str:
        '''LDAP attribute to use as the unique identifier for a user. For example, objectGuid.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_ldap#unique_identifier OrgLdap#unique_identifier}
        '''
        result = self._values.get("unique_identifier")
        assert result is not None, "Required property 'unique_identifier' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def username(self) -> builtins.str:
        '''LDAP attribute to use when looking up a user name to import. For example, userPrincipalName or samAccountName.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_ldap#username OrgLdap#username}
        '''
        result = self._values.get("username")
        assert result is not None, "Required property 'username' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def group_back_link_identifier(self) -> typing.Optional[builtins.str]:
        '''LDAP attribute that returns the identifiers of all the groups of which the user is a member.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_ldap#group_back_link_identifier OrgLdap#group_back_link_identifier}
        '''
        result = self._values.get("group_back_link_identifier")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OrgLdapCustomSettingsUserAttributes(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OrgLdapCustomSettingsUserAttributesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="vcd.orgLdap.OrgLdapCustomSettingsUserAttributesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__baceade406342a2add9b46271f5d292e804134f5de8053271bcf5e6cd6f74546)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetGroupBackLinkIdentifier")
    def reset_group_back_link_identifier(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGroupBackLinkIdentifier", []))

    @builtins.property
    @jsii.member(jsii_name="displayNameInput")
    def display_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "displayNameInput"))

    @builtins.property
    @jsii.member(jsii_name="emailInput")
    def email_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "emailInput"))

    @builtins.property
    @jsii.member(jsii_name="givenNameInput")
    def given_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "givenNameInput"))

    @builtins.property
    @jsii.member(jsii_name="groupBackLinkIdentifierInput")
    def group_back_link_identifier_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "groupBackLinkIdentifierInput"))

    @builtins.property
    @jsii.member(jsii_name="groupMembershipIdentifierInput")
    def group_membership_identifier_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "groupMembershipIdentifierInput"))

    @builtins.property
    @jsii.member(jsii_name="objectClassInput")
    def object_class_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "objectClassInput"))

    @builtins.property
    @jsii.member(jsii_name="surnameInput")
    def surname_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "surnameInput"))

    @builtins.property
    @jsii.member(jsii_name="telephoneInput")
    def telephone_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "telephoneInput"))

    @builtins.property
    @jsii.member(jsii_name="uniqueIdentifierInput")
    def unique_identifier_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "uniqueIdentifierInput"))

    @builtins.property
    @jsii.member(jsii_name="usernameInput")
    def username_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "usernameInput"))

    @builtins.property
    @jsii.member(jsii_name="displayName")
    def display_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "displayName"))

    @display_name.setter
    def display_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e2deb08882ebbd9a3a7662e4f27c6bd78fcca2810aa2d580592e00dd5d2929fe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "displayName", value)

    @builtins.property
    @jsii.member(jsii_name="email")
    def email(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "email"))

    @email.setter
    def email(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f0b31a8f468e4b5132fd43db593758b6fdc9188b6ea6f88e4833316ceffc23e8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "email", value)

    @builtins.property
    @jsii.member(jsii_name="givenName")
    def given_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "givenName"))

    @given_name.setter
    def given_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a95a9b20c170e9a1fce21d4f3beabf3070fc2175956a641d193ec2c04d1438a4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "givenName", value)

    @builtins.property
    @jsii.member(jsii_name="groupBackLinkIdentifier")
    def group_back_link_identifier(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "groupBackLinkIdentifier"))

    @group_back_link_identifier.setter
    def group_back_link_identifier(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c4202dc706cd44e8f47590ca112ac237582ba9e1bb1df2d71d42de41fb249355)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "groupBackLinkIdentifier", value)

    @builtins.property
    @jsii.member(jsii_name="groupMembershipIdentifier")
    def group_membership_identifier(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "groupMembershipIdentifier"))

    @group_membership_identifier.setter
    def group_membership_identifier(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5d68437267dd32fff2433ad7fb8c3fa5c1d17996a9d463eede97afd0ae064313)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "groupMembershipIdentifier", value)

    @builtins.property
    @jsii.member(jsii_name="objectClass")
    def object_class(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "objectClass"))

    @object_class.setter
    def object_class(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__714fea931d72815e4f989e91011e846145d36adf085c8f8b8653693c77dea343)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "objectClass", value)

    @builtins.property
    @jsii.member(jsii_name="surname")
    def surname(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "surname"))

    @surname.setter
    def surname(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3cb158f9fc47ada4d4cb9b2dedc1c63c035b65ff57e5b248ab86b5e30a77c93c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "surname", value)

    @builtins.property
    @jsii.member(jsii_name="telephone")
    def telephone(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "telephone"))

    @telephone.setter
    def telephone(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b43127b6521bc5c280c7d8780c97e78531357ef4c453cef2e4765556ab9d2a45)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "telephone", value)

    @builtins.property
    @jsii.member(jsii_name="uniqueIdentifier")
    def unique_identifier(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "uniqueIdentifier"))

    @unique_identifier.setter
    def unique_identifier(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5155097626ec8d8ec2422e7bbdcfdf17756698af64241133ef352cad7ed7bc3f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "uniqueIdentifier", value)

    @builtins.property
    @jsii.member(jsii_name="username")
    def username(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "username"))

    @username.setter
    def username(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5caaf155c99a2bbacf7aa2cb2448b3915576ea9221d5fe3d6264c3052dbea962)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "username", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[OrgLdapCustomSettingsUserAttributes]:
        return typing.cast(typing.Optional[OrgLdapCustomSettingsUserAttributes], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[OrgLdapCustomSettingsUserAttributes],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__36dbdbfb4869afab16e9b44473328ab56307e646d86e798b70b83f12927503bf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


__all__ = [
    "OrgLdap",
    "OrgLdapConfig",
    "OrgLdapCustomSettings",
    "OrgLdapCustomSettingsGroupAttributes",
    "OrgLdapCustomSettingsGroupAttributesOutputReference",
    "OrgLdapCustomSettingsOutputReference",
    "OrgLdapCustomSettingsUserAttributes",
    "OrgLdapCustomSettingsUserAttributesOutputReference",
]

publication.publish()

def _typecheckingstub__cb6b70a528aa992bb290b4788ff72fae5122e7fa20fa119f95dc77ef9814ee38(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    ldap_mode: builtins.str,
    org_id: builtins.str,
    custom_settings: typing.Optional[typing.Union[OrgLdapCustomSettings, typing.Dict[builtins.str, typing.Any]]] = None,
    custom_user_ou: typing.Optional[builtins.str] = None,
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

def _typecheckingstub__f4a0294ff62f8de4e7810a3de73dd142ad53535c8f5705898a4df1977658c674(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ffd97bedc73fdf34031f86119a751d374bebbe045d4a3d56f4b11666565cfab6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b0ac415b8f2e0ef7f07a38387cb50845c2a5584f93e7e1372ba6fe19058f1b43(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d8c8df8fcb2041108a90e571f808fcd02a3731d74775398ff99010fdc87d80c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__78f6915b69a65b5fc40bcc6c2a62357c1b6ab4cea53ad1035f366dfb9a8999f0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e3592d0adc7b6328ea28fa7147bd347f3c0de99e827b9385ec4691a7713c866e(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ldap_mode: builtins.str,
    org_id: builtins.str,
    custom_settings: typing.Optional[typing.Union[OrgLdapCustomSettings, typing.Dict[builtins.str, typing.Any]]] = None,
    custom_user_ou: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__27e344e592b64fff18c2fa7352dfe2d850c68b4a574681e3ec82933d35c584dd(
    *,
    authentication_method: builtins.str,
    connector_type: builtins.str,
    group_attributes: typing.Union[OrgLdapCustomSettingsGroupAttributes, typing.Dict[builtins.str, typing.Any]],
    port: jsii.Number,
    server: builtins.str,
    user_attributes: typing.Union[OrgLdapCustomSettingsUserAttributes, typing.Dict[builtins.str, typing.Any]],
    base_distinguished_name: typing.Optional[builtins.str] = None,
    is_ssl: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    password: typing.Optional[builtins.str] = None,
    username: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fd25735985ea80e8c5159d80c38f0614615aae7f1edf2d9bb7d539685945c9ec(
    *,
    group_membership_identifier: builtins.str,
    membership: builtins.str,
    name: builtins.str,
    object_class: builtins.str,
    unique_identifier: builtins.str,
    group_back_link_identifier: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e7d0af7705f34c7cfd3e4527d0118339b36be276f17bad31c26d77c111da527a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__18d3ef7ecfa680317ebb6910eb121e26f356372bf64fa0ae14f3f030705ab1be(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb6bda7c3777f7ece632f62be1b1a0bc7226503206f267651208211412cc0b59(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__83361e41e234b4abfd8353f938077210986bbe752aa50117c451581ee7df2ca8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__549ad5b4784aa86c33c96f29c1e70e770efaa116f933344353c39661a2604b66(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c4f94733081aac4232c9b5c5efff7c750d321d07f473b708fd44b74733f472f8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c7b5045f1bbdf999211dd18b6783717d875b36692dc6e18f913f161d8367408a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__758b67a2b6bbf4e84e4bc521d11a2849cf3d8e27c4c89716b62bcc295537dc71(
    value: typing.Optional[OrgLdapCustomSettingsGroupAttributes],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__835eaeee164fee12952f31320bc9639ddc48cf3b74c7863bd91932518e8d83db(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a28e5963cba785cb66a8a4cc96ad5e62c61599a76b7be5283c47085707c2dcfe(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__76e076bee39cf8b19be52e3dd00832f45a58c0c40c9fd6465b3ec076e92fc2a3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__410bc2f66ebfc2afb33d3eecbd8c5873e171712dbffcc5c687cb313f896b93af(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f1084f35eec82cea9ab501cff728653fdb0afd3760fba8a7c0ffe07a44b69169(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fef27d88150f565df70fc2e75ec151d1eb7205ad98a81981bf48df033d0090c0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__93ed471f5c97a682e9e9fe807cc5ee748fe48fefa2ae2dfb8f5a02fb8c0d5896(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__68ce1f1cad50b19a7cedf751cae697717a95ec139a9d3c5cd2c34ce3afe24c90(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7034ef9cbc859c77c535401d9ec82a3da7876c0184a9e3dacbac0dc78ad33637(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__572efdb1d685d93f91c501dda1e260eb6698d6434389e144d313ec36b6b556c7(
    value: typing.Optional[OrgLdapCustomSettings],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__88c36af6baf8ebc4551632c474c88df12cf7ff80a24062684c888ca4c7715733(
    *,
    display_name: builtins.str,
    email: builtins.str,
    given_name: builtins.str,
    group_membership_identifier: builtins.str,
    object_class: builtins.str,
    surname: builtins.str,
    telephone: builtins.str,
    unique_identifier: builtins.str,
    username: builtins.str,
    group_back_link_identifier: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__baceade406342a2add9b46271f5d292e804134f5de8053271bcf5e6cd6f74546(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e2deb08882ebbd9a3a7662e4f27c6bd78fcca2810aa2d580592e00dd5d2929fe(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f0b31a8f468e4b5132fd43db593758b6fdc9188b6ea6f88e4833316ceffc23e8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a95a9b20c170e9a1fce21d4f3beabf3070fc2175956a641d193ec2c04d1438a4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c4202dc706cd44e8f47590ca112ac237582ba9e1bb1df2d71d42de41fb249355(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5d68437267dd32fff2433ad7fb8c3fa5c1d17996a9d463eede97afd0ae064313(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__714fea931d72815e4f989e91011e846145d36adf085c8f8b8653693c77dea343(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3cb158f9fc47ada4d4cb9b2dedc1c63c035b65ff57e5b248ab86b5e30a77c93c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b43127b6521bc5c280c7d8780c97e78531357ef4c453cef2e4765556ab9d2a45(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5155097626ec8d8ec2422e7bbdcfdf17756698af64241133ef352cad7ed7bc3f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5caaf155c99a2bbacf7aa2cb2448b3915576ea9221d5fe3d6264c3052dbea962(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__36dbdbfb4869afab16e9b44473328ab56307e646d86e798b70b83f12927503bf(
    value: typing.Optional[OrgLdapCustomSettingsUserAttributes],
) -> None:
    """Type checking stubs"""
    pass
