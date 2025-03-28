'''
# `vcd_org_oidc`

Refer to the Terraform Registry for docs: [`vcd_org_oidc`](https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_oidc).
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


class OrgOidc(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="vcd.orgOidc.OrgOidc",
):
    '''Represents a {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_oidc vcd_org_oidc}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        client_id: builtins.str,
        client_secret: builtins.str,
        enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        org_id: builtins.str,
        access_token_endpoint: typing.Optional[builtins.str] = None,
        claims_mapping: typing.Optional[typing.Union["OrgOidcClaimsMapping", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        issuer_id: typing.Optional[builtins.str] = None,
        key: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["OrgOidcKey", typing.Dict[builtins.str, typing.Any]]]]] = None,
        key_expire_duration_hours: typing.Optional[jsii.Number] = None,
        key_refresh_endpoint: typing.Optional[builtins.str] = None,
        key_refresh_period_hours: typing.Optional[jsii.Number] = None,
        key_refresh_strategy: typing.Optional[builtins.str] = None,
        max_clock_skew_seconds: typing.Optional[jsii.Number] = None,
        prefer_id_token: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        scopes: typing.Optional[typing.Sequence[builtins.str]] = None,
        ui_button_label: typing.Optional[builtins.str] = None,
        user_authorization_endpoint: typing.Optional[builtins.str] = None,
        userinfo_endpoint: typing.Optional[builtins.str] = None,
        wellknown_endpoint: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_oidc vcd_org_oidc} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param client_id: Client ID to use when talking to the OpenID Connect Identity Provider. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_oidc#client_id OrgOidc#client_id}
        :param client_secret: Client Secret to use when talking to the OpenID Connect Identity Provider. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_oidc#client_secret OrgOidc#client_secret}
        :param enabled: Enables or disables OpenID Connect authentication for the specified Organization. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_oidc#enabled OrgOidc#enabled}
        :param org_id: ID of the Organization that will have the OpenID Connect settings configured. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_oidc#org_id OrgOidc#org_id}
        :param access_token_endpoint: The access token endpoint of the OpenID Connect Identity Provider. If 'wellknown_endpoint' is set, this attribute overrides the obtained access token endpoint Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_oidc#access_token_endpoint OrgOidc#access_token_endpoint}
        :param claims_mapping: claims_mapping block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_oidc#claims_mapping OrgOidc#claims_mapping}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_oidc#id OrgOidc#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param issuer_id: The issuer identifier of the OpenID Connect Identity Provider. If 'wellknown_endpoint' is set, this attribute overrides the obtained issuer identifier Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_oidc#issuer_id OrgOidc#issuer_id}
        :param key: key block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_oidc#key OrgOidc#key}
        :param key_expire_duration_hours: Defines the expiration period of the key, only when 'key_refresh_strategy=EXPIRE_AFTER'. Maximum is 24 hours. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_oidc#key_expire_duration_hours OrgOidc#key_expire_duration_hours}
        :param key_refresh_endpoint: Endpoint used to refresh the keys. If 'wellknown_endpoint' is set, then this argumentwill override the obtained endpoint. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_oidc#key_refresh_endpoint OrgOidc#key_refresh_endpoint}
        :param key_refresh_period_hours: Defines the frequency of key refresh. Maximum is 720 hours. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_oidc#key_refresh_period_hours OrgOidc#key_refresh_period_hours}
        :param key_refresh_strategy: Defines the strategy of key refresh. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_oidc#key_refresh_strategy OrgOidc#key_refresh_strategy}
        :param max_clock_skew_seconds: The maximum clock skew is the maximum allowable time difference between the client and server. This time compensates for any small-time differences in the timestamps when verifying tokens Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_oidc#max_clock_skew_seconds OrgOidc#max_clock_skew_seconds}
        :param prefer_id_token: If you want to combine claims from 'userinfo_endpoint' and the ID Token, set this to 'true'. The identity providers do not provide all the required claims set in 'userinfo_endpoint'.By setting this argument to 'true', VMware Cloud Director can fetch and consume claims from both sources Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_oidc#prefer_id_token OrgOidc#prefer_id_token}
        :param scopes: A set of scopes to use with the OpenID Connect provider. They are used to authorize access to user details, by defining the permissions that the access tokens have to access user information. If 'wellknown_endpoint' is set, this attribute overrides the obtained scopes Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_oidc#scopes OrgOidc#scopes}
        :param ui_button_label: Customizes the label of the UI button of the login screen. Only available since VCD 10.5.1. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_oidc#ui_button_label OrgOidc#ui_button_label}
        :param user_authorization_endpoint: The user authorization endpoint of the OpenID Connect Identity Provider. If 'wellknown_endpoint' is set, this attribute overrides the obtained user authorization endpoint Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_oidc#user_authorization_endpoint OrgOidc#user_authorization_endpoint}
        :param userinfo_endpoint: The user info endpoint of the OpenID Connect Identity Provider. If 'wellknown_endpoint' is set, this attribute overrides the obtained user info endpoint Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_oidc#userinfo_endpoint OrgOidc#userinfo_endpoint}
        :param wellknown_endpoint: Endpoint from the OpenID Connect Identity Provider that serves all the configuration values. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_oidc#wellknown_endpoint OrgOidc#wellknown_endpoint}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0e08fdfd481a4d08a44d8532aa0033b739cee96d2ef0b19d6c04506ea0f64eb4)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = OrgOidcConfig(
            client_id=client_id,
            client_secret=client_secret,
            enabled=enabled,
            org_id=org_id,
            access_token_endpoint=access_token_endpoint,
            claims_mapping=claims_mapping,
            id=id,
            issuer_id=issuer_id,
            key=key,
            key_expire_duration_hours=key_expire_duration_hours,
            key_refresh_endpoint=key_refresh_endpoint,
            key_refresh_period_hours=key_refresh_period_hours,
            key_refresh_strategy=key_refresh_strategy,
            max_clock_skew_seconds=max_clock_skew_seconds,
            prefer_id_token=prefer_id_token,
            scopes=scopes,
            ui_button_label=ui_button_label,
            user_authorization_endpoint=user_authorization_endpoint,
            userinfo_endpoint=userinfo_endpoint,
            wellknown_endpoint=wellknown_endpoint,
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
        '''Generates CDKTF code for importing a OrgOidc resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the OrgOidc to import.
        :param import_from_id: The id of the existing OrgOidc that should be imported. Refer to the {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_oidc#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the OrgOidc to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__01fb65300cacc3c49841ecffc096065df9018da58213a186780939b047aae04d)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putClaimsMapping")
    def put_claims_mapping(
        self,
        *,
        email: typing.Optional[builtins.str] = None,
        first_name: typing.Optional[builtins.str] = None,
        full_name: typing.Optional[builtins.str] = None,
        groups: typing.Optional[builtins.str] = None,
        last_name: typing.Optional[builtins.str] = None,
        roles: typing.Optional[builtins.str] = None,
        subject: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param email: Email claim mapping. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_oidc#email OrgOidc#email}
        :param first_name: First name claim mapping. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_oidc#first_name OrgOidc#first_name}
        :param full_name: Full name claim mapping. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_oidc#full_name OrgOidc#full_name}
        :param groups: Groups claim mapping. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_oidc#groups OrgOidc#groups}
        :param last_name: Last name claim mapping. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_oidc#last_name OrgOidc#last_name}
        :param roles: Roles claim mapping. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_oidc#roles OrgOidc#roles}
        :param subject: Subject claim mapping. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_oidc#subject OrgOidc#subject}
        '''
        value = OrgOidcClaimsMapping(
            email=email,
            first_name=first_name,
            full_name=full_name,
            groups=groups,
            last_name=last_name,
            roles=roles,
            subject=subject,
        )

        return typing.cast(None, jsii.invoke(self, "putClaimsMapping", [value]))

    @jsii.member(jsii_name="putKey")
    def put_key(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["OrgOidcKey", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__43855745fe63f7ef9f2a27ed67a55b0335f6bd73f7b10b246fdee224b76afdf5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putKey", [value]))

    @jsii.member(jsii_name="resetAccessTokenEndpoint")
    def reset_access_token_endpoint(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAccessTokenEndpoint", []))

    @jsii.member(jsii_name="resetClaimsMapping")
    def reset_claims_mapping(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetClaimsMapping", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetIssuerId")
    def reset_issuer_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIssuerId", []))

    @jsii.member(jsii_name="resetKey")
    def reset_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKey", []))

    @jsii.member(jsii_name="resetKeyExpireDurationHours")
    def reset_key_expire_duration_hours(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKeyExpireDurationHours", []))

    @jsii.member(jsii_name="resetKeyRefreshEndpoint")
    def reset_key_refresh_endpoint(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKeyRefreshEndpoint", []))

    @jsii.member(jsii_name="resetKeyRefreshPeriodHours")
    def reset_key_refresh_period_hours(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKeyRefreshPeriodHours", []))

    @jsii.member(jsii_name="resetKeyRefreshStrategy")
    def reset_key_refresh_strategy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKeyRefreshStrategy", []))

    @jsii.member(jsii_name="resetMaxClockSkewSeconds")
    def reset_max_clock_skew_seconds(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxClockSkewSeconds", []))

    @jsii.member(jsii_name="resetPreferIdToken")
    def reset_prefer_id_token(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPreferIdToken", []))

    @jsii.member(jsii_name="resetScopes")
    def reset_scopes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetScopes", []))

    @jsii.member(jsii_name="resetUiButtonLabel")
    def reset_ui_button_label(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUiButtonLabel", []))

    @jsii.member(jsii_name="resetUserAuthorizationEndpoint")
    def reset_user_authorization_endpoint(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUserAuthorizationEndpoint", []))

    @jsii.member(jsii_name="resetUserinfoEndpoint")
    def reset_userinfo_endpoint(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUserinfoEndpoint", []))

    @jsii.member(jsii_name="resetWellknownEndpoint")
    def reset_wellknown_endpoint(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWellknownEndpoint", []))

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
    @jsii.member(jsii_name="claimsMapping")
    def claims_mapping(self) -> "OrgOidcClaimsMappingOutputReference":
        return typing.cast("OrgOidcClaimsMappingOutputReference", jsii.get(self, "claimsMapping"))

    @builtins.property
    @jsii.member(jsii_name="key")
    def key(self) -> "OrgOidcKeyList":
        return typing.cast("OrgOidcKeyList", jsii.get(self, "key"))

    @builtins.property
    @jsii.member(jsii_name="redirectUri")
    def redirect_uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "redirectUri"))

    @builtins.property
    @jsii.member(jsii_name="accessTokenEndpointInput")
    def access_token_endpoint_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "accessTokenEndpointInput"))

    @builtins.property
    @jsii.member(jsii_name="claimsMappingInput")
    def claims_mapping_input(self) -> typing.Optional["OrgOidcClaimsMapping"]:
        return typing.cast(typing.Optional["OrgOidcClaimsMapping"], jsii.get(self, "claimsMappingInput"))

    @builtins.property
    @jsii.member(jsii_name="clientIdInput")
    def client_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clientIdInput"))

    @builtins.property
    @jsii.member(jsii_name="clientSecretInput")
    def client_secret_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clientSecretInput"))

    @builtins.property
    @jsii.member(jsii_name="enabledInput")
    def enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enabledInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="issuerIdInput")
    def issuer_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "issuerIdInput"))

    @builtins.property
    @jsii.member(jsii_name="keyExpireDurationHoursInput")
    def key_expire_duration_hours_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "keyExpireDurationHoursInput"))

    @builtins.property
    @jsii.member(jsii_name="keyInput")
    def key_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OrgOidcKey"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OrgOidcKey"]]], jsii.get(self, "keyInput"))

    @builtins.property
    @jsii.member(jsii_name="keyRefreshEndpointInput")
    def key_refresh_endpoint_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keyRefreshEndpointInput"))

    @builtins.property
    @jsii.member(jsii_name="keyRefreshPeriodHoursInput")
    def key_refresh_period_hours_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "keyRefreshPeriodHoursInput"))

    @builtins.property
    @jsii.member(jsii_name="keyRefreshStrategyInput")
    def key_refresh_strategy_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keyRefreshStrategyInput"))

    @builtins.property
    @jsii.member(jsii_name="maxClockSkewSecondsInput")
    def max_clock_skew_seconds_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxClockSkewSecondsInput"))

    @builtins.property
    @jsii.member(jsii_name="orgIdInput")
    def org_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "orgIdInput"))

    @builtins.property
    @jsii.member(jsii_name="preferIdTokenInput")
    def prefer_id_token_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "preferIdTokenInput"))

    @builtins.property
    @jsii.member(jsii_name="scopesInput")
    def scopes_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "scopesInput"))

    @builtins.property
    @jsii.member(jsii_name="uiButtonLabelInput")
    def ui_button_label_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "uiButtonLabelInput"))

    @builtins.property
    @jsii.member(jsii_name="userAuthorizationEndpointInput")
    def user_authorization_endpoint_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "userAuthorizationEndpointInput"))

    @builtins.property
    @jsii.member(jsii_name="userinfoEndpointInput")
    def userinfo_endpoint_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "userinfoEndpointInput"))

    @builtins.property
    @jsii.member(jsii_name="wellknownEndpointInput")
    def wellknown_endpoint_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "wellknownEndpointInput"))

    @builtins.property
    @jsii.member(jsii_name="accessTokenEndpoint")
    def access_token_endpoint(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "accessTokenEndpoint"))

    @access_token_endpoint.setter
    def access_token_endpoint(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__72bf00d4ad3913321c30a45173fe1f9b1db8d9857660bea20c2962d4ab80cdaa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accessTokenEndpoint", value)

    @builtins.property
    @jsii.member(jsii_name="clientId")
    def client_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clientId"))

    @client_id.setter
    def client_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__069261b6a57b48300b354a029cf794e4f0e3c870326473e79e5ec843f944a7ac)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientId", value)

    @builtins.property
    @jsii.member(jsii_name="clientSecret")
    def client_secret(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clientSecret"))

    @client_secret.setter
    def client_secret(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a1652902f7f6c2b7a724395f51180828c8b576ca12d3b1a6cfd7c6f1cf7ca1c1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientSecret", value)

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
            type_hints = typing.get_type_hints(_typecheckingstub__de26253fdf5476fe9b6bd762040cc5073ac4ddda0f51d19ee09c49b0466fdcfb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value)

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d77f82a6970d8977fb46af517a30b3a1ef6317893abb3e4fc7bbe94965437c74)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="issuerId")
    def issuer_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "issuerId"))

    @issuer_id.setter
    def issuer_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__39feac4c332c5c1364e68a068ae6ec291b54d92d607c076161571b6f5224aeaf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "issuerId", value)

    @builtins.property
    @jsii.member(jsii_name="keyExpireDurationHours")
    def key_expire_duration_hours(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "keyExpireDurationHours"))

    @key_expire_duration_hours.setter
    def key_expire_duration_hours(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5931af2e00e1b381aefd07b701120062999f272ef888054cbe5eaae6359c7de7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "keyExpireDurationHours", value)

    @builtins.property
    @jsii.member(jsii_name="keyRefreshEndpoint")
    def key_refresh_endpoint(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "keyRefreshEndpoint"))

    @key_refresh_endpoint.setter
    def key_refresh_endpoint(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3b4937a016d97e862eac887dcb2a9bde4f8c00eb0670b56dc55ffe4ad5a16654)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "keyRefreshEndpoint", value)

    @builtins.property
    @jsii.member(jsii_name="keyRefreshPeriodHours")
    def key_refresh_period_hours(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "keyRefreshPeriodHours"))

    @key_refresh_period_hours.setter
    def key_refresh_period_hours(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eebb97c1ff2641e5195a5bb3ee47ffab9485850e3a2ffa3c46627196d9f7da81)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "keyRefreshPeriodHours", value)

    @builtins.property
    @jsii.member(jsii_name="keyRefreshStrategy")
    def key_refresh_strategy(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "keyRefreshStrategy"))

    @key_refresh_strategy.setter
    def key_refresh_strategy(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f5bb838c81e64eabe180c5699906e77ad297a98855e447087351b0c91c62be54)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "keyRefreshStrategy", value)

    @builtins.property
    @jsii.member(jsii_name="maxClockSkewSeconds")
    def max_clock_skew_seconds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxClockSkewSeconds"))

    @max_clock_skew_seconds.setter
    def max_clock_skew_seconds(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8c1b84037b8d92ab33918e41b9d511857885bac1b20c5ead441aec313d73cdc3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxClockSkewSeconds", value)

    @builtins.property
    @jsii.member(jsii_name="orgId")
    def org_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "orgId"))

    @org_id.setter
    def org_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__704011e38dce4ee3b1659e632f44157eb941e862301805322e69e05c6070e164)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "orgId", value)

    @builtins.property
    @jsii.member(jsii_name="preferIdToken")
    def prefer_id_token(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "preferIdToken"))

    @prefer_id_token.setter
    def prefer_id_token(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2b9e0860647d2f80aece0d627cac60bce634a199dd76d24d1d463b039f8555c5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "preferIdToken", value)

    @builtins.property
    @jsii.member(jsii_name="scopes")
    def scopes(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "scopes"))

    @scopes.setter
    def scopes(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__035cc8f0f1e939187d79ef0dc22fa66f5b5b26c70d62b39d097524127bc4d6a5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "scopes", value)

    @builtins.property
    @jsii.member(jsii_name="uiButtonLabel")
    def ui_button_label(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "uiButtonLabel"))

    @ui_button_label.setter
    def ui_button_label(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__37c99c557d54e7ffa1b8e562b8b764abd7347263be398c520c531556ba9ec40f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "uiButtonLabel", value)

    @builtins.property
    @jsii.member(jsii_name="userAuthorizationEndpoint")
    def user_authorization_endpoint(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "userAuthorizationEndpoint"))

    @user_authorization_endpoint.setter
    def user_authorization_endpoint(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__10c50fdbbcc67620f9573a7ebe3f85fd8843dc9e8a24bd6f8b3a52112d1f1dc8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "userAuthorizationEndpoint", value)

    @builtins.property
    @jsii.member(jsii_name="userinfoEndpoint")
    def userinfo_endpoint(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "userinfoEndpoint"))

    @userinfo_endpoint.setter
    def userinfo_endpoint(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3c39d3dff18b657f7cba21236d4d8cfc2c8ea9e67d95ba902efa05f1307063ee)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "userinfoEndpoint", value)

    @builtins.property
    @jsii.member(jsii_name="wellknownEndpoint")
    def wellknown_endpoint(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "wellknownEndpoint"))

    @wellknown_endpoint.setter
    def wellknown_endpoint(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__573c1f62208de26411d6e472ee5c0d90efdfa4eeb1167644040c04adf9382da5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wellknownEndpoint", value)


@jsii.data_type(
    jsii_type="vcd.orgOidc.OrgOidcClaimsMapping",
    jsii_struct_bases=[],
    name_mapping={
        "email": "email",
        "first_name": "firstName",
        "full_name": "fullName",
        "groups": "groups",
        "last_name": "lastName",
        "roles": "roles",
        "subject": "subject",
    },
)
class OrgOidcClaimsMapping:
    def __init__(
        self,
        *,
        email: typing.Optional[builtins.str] = None,
        first_name: typing.Optional[builtins.str] = None,
        full_name: typing.Optional[builtins.str] = None,
        groups: typing.Optional[builtins.str] = None,
        last_name: typing.Optional[builtins.str] = None,
        roles: typing.Optional[builtins.str] = None,
        subject: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param email: Email claim mapping. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_oidc#email OrgOidc#email}
        :param first_name: First name claim mapping. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_oidc#first_name OrgOidc#first_name}
        :param full_name: Full name claim mapping. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_oidc#full_name OrgOidc#full_name}
        :param groups: Groups claim mapping. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_oidc#groups OrgOidc#groups}
        :param last_name: Last name claim mapping. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_oidc#last_name OrgOidc#last_name}
        :param roles: Roles claim mapping. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_oidc#roles OrgOidc#roles}
        :param subject: Subject claim mapping. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_oidc#subject OrgOidc#subject}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e84d00525e789c1087d53b107540fdd56b5c0212e0fd05d217754c6601dbf273)
            check_type(argname="argument email", value=email, expected_type=type_hints["email"])
            check_type(argname="argument first_name", value=first_name, expected_type=type_hints["first_name"])
            check_type(argname="argument full_name", value=full_name, expected_type=type_hints["full_name"])
            check_type(argname="argument groups", value=groups, expected_type=type_hints["groups"])
            check_type(argname="argument last_name", value=last_name, expected_type=type_hints["last_name"])
            check_type(argname="argument roles", value=roles, expected_type=type_hints["roles"])
            check_type(argname="argument subject", value=subject, expected_type=type_hints["subject"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if email is not None:
            self._values["email"] = email
        if first_name is not None:
            self._values["first_name"] = first_name
        if full_name is not None:
            self._values["full_name"] = full_name
        if groups is not None:
            self._values["groups"] = groups
        if last_name is not None:
            self._values["last_name"] = last_name
        if roles is not None:
            self._values["roles"] = roles
        if subject is not None:
            self._values["subject"] = subject

    @builtins.property
    def email(self) -> typing.Optional[builtins.str]:
        '''Email claim mapping.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_oidc#email OrgOidc#email}
        '''
        result = self._values.get("email")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def first_name(self) -> typing.Optional[builtins.str]:
        '''First name claim mapping.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_oidc#first_name OrgOidc#first_name}
        '''
        result = self._values.get("first_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def full_name(self) -> typing.Optional[builtins.str]:
        '''Full name claim mapping.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_oidc#full_name OrgOidc#full_name}
        '''
        result = self._values.get("full_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def groups(self) -> typing.Optional[builtins.str]:
        '''Groups claim mapping.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_oidc#groups OrgOidc#groups}
        '''
        result = self._values.get("groups")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def last_name(self) -> typing.Optional[builtins.str]:
        '''Last name claim mapping.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_oidc#last_name OrgOidc#last_name}
        '''
        result = self._values.get("last_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def roles(self) -> typing.Optional[builtins.str]:
        '''Roles claim mapping.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_oidc#roles OrgOidc#roles}
        '''
        result = self._values.get("roles")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def subject(self) -> typing.Optional[builtins.str]:
        '''Subject claim mapping.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_oidc#subject OrgOidc#subject}
        '''
        result = self._values.get("subject")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OrgOidcClaimsMapping(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OrgOidcClaimsMappingOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="vcd.orgOidc.OrgOidcClaimsMappingOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__056049bcd01b57e0dd8960bf053f4f18faff121b001ff0cd8d29e05a6f86663a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetEmail")
    def reset_email(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEmail", []))

    @jsii.member(jsii_name="resetFirstName")
    def reset_first_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFirstName", []))

    @jsii.member(jsii_name="resetFullName")
    def reset_full_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFullName", []))

    @jsii.member(jsii_name="resetGroups")
    def reset_groups(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGroups", []))

    @jsii.member(jsii_name="resetLastName")
    def reset_last_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLastName", []))

    @jsii.member(jsii_name="resetRoles")
    def reset_roles(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRoles", []))

    @jsii.member(jsii_name="resetSubject")
    def reset_subject(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSubject", []))

    @builtins.property
    @jsii.member(jsii_name="emailInput")
    def email_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "emailInput"))

    @builtins.property
    @jsii.member(jsii_name="firstNameInput")
    def first_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "firstNameInput"))

    @builtins.property
    @jsii.member(jsii_name="fullNameInput")
    def full_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "fullNameInput"))

    @builtins.property
    @jsii.member(jsii_name="groupsInput")
    def groups_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "groupsInput"))

    @builtins.property
    @jsii.member(jsii_name="lastNameInput")
    def last_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "lastNameInput"))

    @builtins.property
    @jsii.member(jsii_name="rolesInput")
    def roles_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "rolesInput"))

    @builtins.property
    @jsii.member(jsii_name="subjectInput")
    def subject_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "subjectInput"))

    @builtins.property
    @jsii.member(jsii_name="email")
    def email(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "email"))

    @email.setter
    def email(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a02035d2ef5589eff6a5c920e11de25958f8f3ace3ce11d9df71c21bd5732568)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "email", value)

    @builtins.property
    @jsii.member(jsii_name="firstName")
    def first_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "firstName"))

    @first_name.setter
    def first_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__54ec074ecfe3c5fec061811fce1ccfb5526765ecaf54432ccd19f929addd4cf3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "firstName", value)

    @builtins.property
    @jsii.member(jsii_name="fullName")
    def full_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "fullName"))

    @full_name.setter
    def full_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ba443fe01e910fb49b2749e06b53871134845f6759df1a68e4ad2e96518df594)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fullName", value)

    @builtins.property
    @jsii.member(jsii_name="groups")
    def groups(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "groups"))

    @groups.setter
    def groups(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a66fdef9099b9667425256046b42ed068493d56660c4d253d21ebe0d325de2f3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "groups", value)

    @builtins.property
    @jsii.member(jsii_name="lastName")
    def last_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "lastName"))

    @last_name.setter
    def last_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__90e27b54890c99a2e10d474ca7cf32f61c4ac5e0f796de0660f7d1cce7b48a6c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "lastName", value)

    @builtins.property
    @jsii.member(jsii_name="roles")
    def roles(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "roles"))

    @roles.setter
    def roles(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__42ffc9e5c7528df0afaa0085b659b9d5c040b9165180e16d5bef208122d5f48d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "roles", value)

    @builtins.property
    @jsii.member(jsii_name="subject")
    def subject(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "subject"))

    @subject.setter
    def subject(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9c98e66368ab1a84ea62e5fc0af08860e4f199fc90c9ba06006e60a3bb7e3062)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subject", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[OrgOidcClaimsMapping]:
        return typing.cast(typing.Optional[OrgOidcClaimsMapping], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[OrgOidcClaimsMapping]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__55fbf2ac9c0b41a9d7cc6b255c9b6a914bc17dd4c2bfbd1ebf1e93473d15fb43)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="vcd.orgOidc.OrgOidcConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "client_id": "clientId",
        "client_secret": "clientSecret",
        "enabled": "enabled",
        "org_id": "orgId",
        "access_token_endpoint": "accessTokenEndpoint",
        "claims_mapping": "claimsMapping",
        "id": "id",
        "issuer_id": "issuerId",
        "key": "key",
        "key_expire_duration_hours": "keyExpireDurationHours",
        "key_refresh_endpoint": "keyRefreshEndpoint",
        "key_refresh_period_hours": "keyRefreshPeriodHours",
        "key_refresh_strategy": "keyRefreshStrategy",
        "max_clock_skew_seconds": "maxClockSkewSeconds",
        "prefer_id_token": "preferIdToken",
        "scopes": "scopes",
        "ui_button_label": "uiButtonLabel",
        "user_authorization_endpoint": "userAuthorizationEndpoint",
        "userinfo_endpoint": "userinfoEndpoint",
        "wellknown_endpoint": "wellknownEndpoint",
    },
)
class OrgOidcConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        client_id: builtins.str,
        client_secret: builtins.str,
        enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        org_id: builtins.str,
        access_token_endpoint: typing.Optional[builtins.str] = None,
        claims_mapping: typing.Optional[typing.Union[OrgOidcClaimsMapping, typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        issuer_id: typing.Optional[builtins.str] = None,
        key: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["OrgOidcKey", typing.Dict[builtins.str, typing.Any]]]]] = None,
        key_expire_duration_hours: typing.Optional[jsii.Number] = None,
        key_refresh_endpoint: typing.Optional[builtins.str] = None,
        key_refresh_period_hours: typing.Optional[jsii.Number] = None,
        key_refresh_strategy: typing.Optional[builtins.str] = None,
        max_clock_skew_seconds: typing.Optional[jsii.Number] = None,
        prefer_id_token: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        scopes: typing.Optional[typing.Sequence[builtins.str]] = None,
        ui_button_label: typing.Optional[builtins.str] = None,
        user_authorization_endpoint: typing.Optional[builtins.str] = None,
        userinfo_endpoint: typing.Optional[builtins.str] = None,
        wellknown_endpoint: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param client_id: Client ID to use when talking to the OpenID Connect Identity Provider. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_oidc#client_id OrgOidc#client_id}
        :param client_secret: Client Secret to use when talking to the OpenID Connect Identity Provider. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_oidc#client_secret OrgOidc#client_secret}
        :param enabled: Enables or disables OpenID Connect authentication for the specified Organization. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_oidc#enabled OrgOidc#enabled}
        :param org_id: ID of the Organization that will have the OpenID Connect settings configured. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_oidc#org_id OrgOidc#org_id}
        :param access_token_endpoint: The access token endpoint of the OpenID Connect Identity Provider. If 'wellknown_endpoint' is set, this attribute overrides the obtained access token endpoint Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_oidc#access_token_endpoint OrgOidc#access_token_endpoint}
        :param claims_mapping: claims_mapping block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_oidc#claims_mapping OrgOidc#claims_mapping}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_oidc#id OrgOidc#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param issuer_id: The issuer identifier of the OpenID Connect Identity Provider. If 'wellknown_endpoint' is set, this attribute overrides the obtained issuer identifier Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_oidc#issuer_id OrgOidc#issuer_id}
        :param key: key block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_oidc#key OrgOidc#key}
        :param key_expire_duration_hours: Defines the expiration period of the key, only when 'key_refresh_strategy=EXPIRE_AFTER'. Maximum is 24 hours. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_oidc#key_expire_duration_hours OrgOidc#key_expire_duration_hours}
        :param key_refresh_endpoint: Endpoint used to refresh the keys. If 'wellknown_endpoint' is set, then this argumentwill override the obtained endpoint. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_oidc#key_refresh_endpoint OrgOidc#key_refresh_endpoint}
        :param key_refresh_period_hours: Defines the frequency of key refresh. Maximum is 720 hours. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_oidc#key_refresh_period_hours OrgOidc#key_refresh_period_hours}
        :param key_refresh_strategy: Defines the strategy of key refresh. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_oidc#key_refresh_strategy OrgOidc#key_refresh_strategy}
        :param max_clock_skew_seconds: The maximum clock skew is the maximum allowable time difference between the client and server. This time compensates for any small-time differences in the timestamps when verifying tokens Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_oidc#max_clock_skew_seconds OrgOidc#max_clock_skew_seconds}
        :param prefer_id_token: If you want to combine claims from 'userinfo_endpoint' and the ID Token, set this to 'true'. The identity providers do not provide all the required claims set in 'userinfo_endpoint'.By setting this argument to 'true', VMware Cloud Director can fetch and consume claims from both sources Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_oidc#prefer_id_token OrgOidc#prefer_id_token}
        :param scopes: A set of scopes to use with the OpenID Connect provider. They are used to authorize access to user details, by defining the permissions that the access tokens have to access user information. If 'wellknown_endpoint' is set, this attribute overrides the obtained scopes Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_oidc#scopes OrgOidc#scopes}
        :param ui_button_label: Customizes the label of the UI button of the login screen. Only available since VCD 10.5.1. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_oidc#ui_button_label OrgOidc#ui_button_label}
        :param user_authorization_endpoint: The user authorization endpoint of the OpenID Connect Identity Provider. If 'wellknown_endpoint' is set, this attribute overrides the obtained user authorization endpoint Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_oidc#user_authorization_endpoint OrgOidc#user_authorization_endpoint}
        :param userinfo_endpoint: The user info endpoint of the OpenID Connect Identity Provider. If 'wellknown_endpoint' is set, this attribute overrides the obtained user info endpoint Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_oidc#userinfo_endpoint OrgOidc#userinfo_endpoint}
        :param wellknown_endpoint: Endpoint from the OpenID Connect Identity Provider that serves all the configuration values. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_oidc#wellknown_endpoint OrgOidc#wellknown_endpoint}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(claims_mapping, dict):
            claims_mapping = OrgOidcClaimsMapping(**claims_mapping)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__94c43d31413160d5752c616fd9c6e483354c8ebbc7d07a31d04a51b9018f2133)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument client_id", value=client_id, expected_type=type_hints["client_id"])
            check_type(argname="argument client_secret", value=client_secret, expected_type=type_hints["client_secret"])
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument org_id", value=org_id, expected_type=type_hints["org_id"])
            check_type(argname="argument access_token_endpoint", value=access_token_endpoint, expected_type=type_hints["access_token_endpoint"])
            check_type(argname="argument claims_mapping", value=claims_mapping, expected_type=type_hints["claims_mapping"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument issuer_id", value=issuer_id, expected_type=type_hints["issuer_id"])
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument key_expire_duration_hours", value=key_expire_duration_hours, expected_type=type_hints["key_expire_duration_hours"])
            check_type(argname="argument key_refresh_endpoint", value=key_refresh_endpoint, expected_type=type_hints["key_refresh_endpoint"])
            check_type(argname="argument key_refresh_period_hours", value=key_refresh_period_hours, expected_type=type_hints["key_refresh_period_hours"])
            check_type(argname="argument key_refresh_strategy", value=key_refresh_strategy, expected_type=type_hints["key_refresh_strategy"])
            check_type(argname="argument max_clock_skew_seconds", value=max_clock_skew_seconds, expected_type=type_hints["max_clock_skew_seconds"])
            check_type(argname="argument prefer_id_token", value=prefer_id_token, expected_type=type_hints["prefer_id_token"])
            check_type(argname="argument scopes", value=scopes, expected_type=type_hints["scopes"])
            check_type(argname="argument ui_button_label", value=ui_button_label, expected_type=type_hints["ui_button_label"])
            check_type(argname="argument user_authorization_endpoint", value=user_authorization_endpoint, expected_type=type_hints["user_authorization_endpoint"])
            check_type(argname="argument userinfo_endpoint", value=userinfo_endpoint, expected_type=type_hints["userinfo_endpoint"])
            check_type(argname="argument wellknown_endpoint", value=wellknown_endpoint, expected_type=type_hints["wellknown_endpoint"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "client_id": client_id,
            "client_secret": client_secret,
            "enabled": enabled,
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
        if access_token_endpoint is not None:
            self._values["access_token_endpoint"] = access_token_endpoint
        if claims_mapping is not None:
            self._values["claims_mapping"] = claims_mapping
        if id is not None:
            self._values["id"] = id
        if issuer_id is not None:
            self._values["issuer_id"] = issuer_id
        if key is not None:
            self._values["key"] = key
        if key_expire_duration_hours is not None:
            self._values["key_expire_duration_hours"] = key_expire_duration_hours
        if key_refresh_endpoint is not None:
            self._values["key_refresh_endpoint"] = key_refresh_endpoint
        if key_refresh_period_hours is not None:
            self._values["key_refresh_period_hours"] = key_refresh_period_hours
        if key_refresh_strategy is not None:
            self._values["key_refresh_strategy"] = key_refresh_strategy
        if max_clock_skew_seconds is not None:
            self._values["max_clock_skew_seconds"] = max_clock_skew_seconds
        if prefer_id_token is not None:
            self._values["prefer_id_token"] = prefer_id_token
        if scopes is not None:
            self._values["scopes"] = scopes
        if ui_button_label is not None:
            self._values["ui_button_label"] = ui_button_label
        if user_authorization_endpoint is not None:
            self._values["user_authorization_endpoint"] = user_authorization_endpoint
        if userinfo_endpoint is not None:
            self._values["userinfo_endpoint"] = userinfo_endpoint
        if wellknown_endpoint is not None:
            self._values["wellknown_endpoint"] = wellknown_endpoint

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
    def client_id(self) -> builtins.str:
        '''Client ID to use when talking to the OpenID Connect Identity Provider.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_oidc#client_id OrgOidc#client_id}
        '''
        result = self._values.get("client_id")
        assert result is not None, "Required property 'client_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def client_secret(self) -> builtins.str:
        '''Client Secret to use when talking to the OpenID Connect Identity Provider.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_oidc#client_secret OrgOidc#client_secret}
        '''
        result = self._values.get("client_secret")
        assert result is not None, "Required property 'client_secret' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''Enables or disables OpenID Connect authentication for the specified Organization.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_oidc#enabled OrgOidc#enabled}
        '''
        result = self._values.get("enabled")
        assert result is not None, "Required property 'enabled' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    @builtins.property
    def org_id(self) -> builtins.str:
        '''ID of the Organization that will have the OpenID Connect settings configured.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_oidc#org_id OrgOidc#org_id}
        '''
        result = self._values.get("org_id")
        assert result is not None, "Required property 'org_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def access_token_endpoint(self) -> typing.Optional[builtins.str]:
        '''The access token endpoint of the OpenID Connect Identity Provider.

        If 'wellknown_endpoint' is set, this attribute overrides the obtained access token endpoint

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_oidc#access_token_endpoint OrgOidc#access_token_endpoint}
        '''
        result = self._values.get("access_token_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def claims_mapping(self) -> typing.Optional[OrgOidcClaimsMapping]:
        '''claims_mapping block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_oidc#claims_mapping OrgOidc#claims_mapping}
        '''
        result = self._values.get("claims_mapping")
        return typing.cast(typing.Optional[OrgOidcClaimsMapping], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_oidc#id OrgOidc#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def issuer_id(self) -> typing.Optional[builtins.str]:
        '''The issuer identifier of the OpenID Connect Identity Provider.

        If 'wellknown_endpoint' is set, this attribute overrides the obtained issuer identifier

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_oidc#issuer_id OrgOidc#issuer_id}
        '''
        result = self._values.get("issuer_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def key(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OrgOidcKey"]]]:
        '''key block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_oidc#key OrgOidc#key}
        '''
        result = self._values.get("key")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OrgOidcKey"]]], result)

    @builtins.property
    def key_expire_duration_hours(self) -> typing.Optional[jsii.Number]:
        '''Defines the expiration period of the key, only when 'key_refresh_strategy=EXPIRE_AFTER'. Maximum is 24 hours.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_oidc#key_expire_duration_hours OrgOidc#key_expire_duration_hours}
        '''
        result = self._values.get("key_expire_duration_hours")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def key_refresh_endpoint(self) -> typing.Optional[builtins.str]:
        '''Endpoint used to refresh the keys. If 'wellknown_endpoint' is set, then this argumentwill override the obtained endpoint.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_oidc#key_refresh_endpoint OrgOidc#key_refresh_endpoint}
        '''
        result = self._values.get("key_refresh_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def key_refresh_period_hours(self) -> typing.Optional[jsii.Number]:
        '''Defines the frequency of key refresh. Maximum is 720 hours.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_oidc#key_refresh_period_hours OrgOidc#key_refresh_period_hours}
        '''
        result = self._values.get("key_refresh_period_hours")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def key_refresh_strategy(self) -> typing.Optional[builtins.str]:
        '''Defines the strategy of key refresh.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_oidc#key_refresh_strategy OrgOidc#key_refresh_strategy}
        '''
        result = self._values.get("key_refresh_strategy")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def max_clock_skew_seconds(self) -> typing.Optional[jsii.Number]:
        '''The maximum clock skew is the maximum allowable time difference between the client and server.

        This time compensates for any small-time differences in the timestamps when verifying tokens

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_oidc#max_clock_skew_seconds OrgOidc#max_clock_skew_seconds}
        '''
        result = self._values.get("max_clock_skew_seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def prefer_id_token(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If you want to combine claims from 'userinfo_endpoint' and the ID Token, set this to 'true'.

        The identity providers do not provide all the required claims set in 'userinfo_endpoint'.By setting this argument to 'true', VMware Cloud Director can fetch and consume claims from both sources

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_oidc#prefer_id_token OrgOidc#prefer_id_token}
        '''
        result = self._values.get("prefer_id_token")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def scopes(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A set of scopes to use with the OpenID Connect provider.

        They are used to authorize access to user details, by defining the permissions that the access tokens have to access user information. If 'wellknown_endpoint' is set, this attribute overrides the obtained scopes

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_oidc#scopes OrgOidc#scopes}
        '''
        result = self._values.get("scopes")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def ui_button_label(self) -> typing.Optional[builtins.str]:
        '''Customizes the label of the UI button of the login screen. Only available since VCD 10.5.1.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_oidc#ui_button_label OrgOidc#ui_button_label}
        '''
        result = self._values.get("ui_button_label")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def user_authorization_endpoint(self) -> typing.Optional[builtins.str]:
        '''The user authorization endpoint of the OpenID Connect Identity Provider.

        If 'wellknown_endpoint' is set, this attribute overrides the obtained user authorization endpoint

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_oidc#user_authorization_endpoint OrgOidc#user_authorization_endpoint}
        '''
        result = self._values.get("user_authorization_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def userinfo_endpoint(self) -> typing.Optional[builtins.str]:
        '''The user info endpoint of the OpenID Connect Identity Provider.

        If 'wellknown_endpoint' is set, this attribute overrides the obtained user info endpoint

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_oidc#userinfo_endpoint OrgOidc#userinfo_endpoint}
        '''
        result = self._values.get("userinfo_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def wellknown_endpoint(self) -> typing.Optional[builtins.str]:
        '''Endpoint from the OpenID Connect Identity Provider that serves all the configuration values.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_oidc#wellknown_endpoint OrgOidc#wellknown_endpoint}
        '''
        result = self._values.get("wellknown_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OrgOidcConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="vcd.orgOidc.OrgOidcKey",
    jsii_struct_bases=[],
    name_mapping={
        "algorithm": "algorithm",
        "certificate": "certificate",
        "id": "id",
        "expiration_date": "expirationDate",
    },
)
class OrgOidcKey:
    def __init__(
        self,
        *,
        algorithm: builtins.str,
        certificate: builtins.str,
        id: builtins.str,
        expiration_date: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param algorithm: Algorithm of the key, either RSA or EC. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_oidc#algorithm OrgOidc#algorithm}
        :param certificate: The certificate contents. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_oidc#certificate OrgOidc#certificate}
        :param id: ID of the key. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_oidc#id OrgOidc#id} Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param expiration_date: Expiration date for the certificate. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_oidc#expiration_date OrgOidc#expiration_date}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__49385857150f55f5e68559f92b316ebc01c20b09e8e3fe6510afab209daf08df)
            check_type(argname="argument algorithm", value=algorithm, expected_type=type_hints["algorithm"])
            check_type(argname="argument certificate", value=certificate, expected_type=type_hints["certificate"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument expiration_date", value=expiration_date, expected_type=type_hints["expiration_date"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "algorithm": algorithm,
            "certificate": certificate,
            "id": id,
        }
        if expiration_date is not None:
            self._values["expiration_date"] = expiration_date

    @builtins.property
    def algorithm(self) -> builtins.str:
        '''Algorithm of the key, either RSA or EC.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_oidc#algorithm OrgOidc#algorithm}
        '''
        result = self._values.get("algorithm")
        assert result is not None, "Required property 'algorithm' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def certificate(self) -> builtins.str:
        '''The certificate contents.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_oidc#certificate OrgOidc#certificate}
        '''
        result = self._values.get("certificate")
        assert result is not None, "Required property 'certificate' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def id(self) -> builtins.str:
        '''ID of the key.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_oidc#id OrgOidc#id}

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        assert result is not None, "Required property 'id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def expiration_date(self) -> typing.Optional[builtins.str]:
        '''Expiration date for the certificate.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/org_oidc#expiration_date OrgOidc#expiration_date}
        '''
        result = self._values.get("expiration_date")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OrgOidcKey(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OrgOidcKeyList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="vcd.orgOidc.OrgOidcKeyList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4c50429104e5928283da1f445ffb715dccdbf2496ebcdb0cc8a878198c494191)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "OrgOidcKeyOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__822bc2add637e48dc48ef3f3b81fcf78c6bae4ad6c8e23c046f65020cd0718d4)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("OrgOidcKeyOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9564df21175305b089d24db15077be4020cbff1c9c0c366bff18234df889cd08)
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
            type_hints = typing.get_type_hints(_typecheckingstub__511cc2fb582193a7c7cfd1e38ff054acc6fadf5c9026b4ce60f38ba57fe058ea)
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
            type_hints = typing.get_type_hints(_typecheckingstub__665833e5183a87c27145d54f41634e1288b41ed885e453ebfb1b132bbd1eefef)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OrgOidcKey]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OrgOidcKey]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OrgOidcKey]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5db4cd0314f66c576fe0676b3d4c88de9c402592d0c11df3181ec10909d4ac46)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class OrgOidcKeyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="vcd.orgOidc.OrgOidcKeyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b76b57afba73525c402e1821bcbc5b982936cf1edf37cfb9695ea35f524cc07d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetExpirationDate")
    def reset_expiration_date(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExpirationDate", []))

    @builtins.property
    @jsii.member(jsii_name="algorithmInput")
    def algorithm_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "algorithmInput"))

    @builtins.property
    @jsii.member(jsii_name="certificateInput")
    def certificate_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "certificateInput"))

    @builtins.property
    @jsii.member(jsii_name="expirationDateInput")
    def expiration_date_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "expirationDateInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="algorithm")
    def algorithm(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "algorithm"))

    @algorithm.setter
    def algorithm(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b633054fc30b6d5b43821988247c46610d6e3d99c0e4cac06890e118b1d31f46)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "algorithm", value)

    @builtins.property
    @jsii.member(jsii_name="certificate")
    def certificate(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "certificate"))

    @certificate.setter
    def certificate(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aa6da6e1c365322369dfa5ecb4e460c513c41fef0d7ab7c5333000a737fad003)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "certificate", value)

    @builtins.property
    @jsii.member(jsii_name="expirationDate")
    def expiration_date(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "expirationDate"))

    @expiration_date.setter
    def expiration_date(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3614c2e3ca05bb1076bfd1acfbea9e400e093e4686e28d280602011c29e236de)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "expirationDate", value)

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8797603ad4428c009829df721b8f41ede87cd0f2ae037b2552ff6729052af1b4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OrgOidcKey]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OrgOidcKey]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OrgOidcKey]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__737cf78b035468534c84a9500c2873fbbcd625d0f73e1a9d1801127eab959381)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


__all__ = [
    "OrgOidc",
    "OrgOidcClaimsMapping",
    "OrgOidcClaimsMappingOutputReference",
    "OrgOidcConfig",
    "OrgOidcKey",
    "OrgOidcKeyList",
    "OrgOidcKeyOutputReference",
]

publication.publish()

def _typecheckingstub__0e08fdfd481a4d08a44d8532aa0033b739cee96d2ef0b19d6c04506ea0f64eb4(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    client_id: builtins.str,
    client_secret: builtins.str,
    enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    org_id: builtins.str,
    access_token_endpoint: typing.Optional[builtins.str] = None,
    claims_mapping: typing.Optional[typing.Union[OrgOidcClaimsMapping, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    issuer_id: typing.Optional[builtins.str] = None,
    key: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OrgOidcKey, typing.Dict[builtins.str, typing.Any]]]]] = None,
    key_expire_duration_hours: typing.Optional[jsii.Number] = None,
    key_refresh_endpoint: typing.Optional[builtins.str] = None,
    key_refresh_period_hours: typing.Optional[jsii.Number] = None,
    key_refresh_strategy: typing.Optional[builtins.str] = None,
    max_clock_skew_seconds: typing.Optional[jsii.Number] = None,
    prefer_id_token: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    scopes: typing.Optional[typing.Sequence[builtins.str]] = None,
    ui_button_label: typing.Optional[builtins.str] = None,
    user_authorization_endpoint: typing.Optional[builtins.str] = None,
    userinfo_endpoint: typing.Optional[builtins.str] = None,
    wellknown_endpoint: typing.Optional[builtins.str] = None,
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

def _typecheckingstub__01fb65300cacc3c49841ecffc096065df9018da58213a186780939b047aae04d(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__43855745fe63f7ef9f2a27ed67a55b0335f6bd73f7b10b246fdee224b76afdf5(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OrgOidcKey, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__72bf00d4ad3913321c30a45173fe1f9b1db8d9857660bea20c2962d4ab80cdaa(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__069261b6a57b48300b354a029cf794e4f0e3c870326473e79e5ec843f944a7ac(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a1652902f7f6c2b7a724395f51180828c8b576ca12d3b1a6cfd7c6f1cf7ca1c1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de26253fdf5476fe9b6bd762040cc5073ac4ddda0f51d19ee09c49b0466fdcfb(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d77f82a6970d8977fb46af517a30b3a1ef6317893abb3e4fc7bbe94965437c74(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__39feac4c332c5c1364e68a068ae6ec291b54d92d607c076161571b6f5224aeaf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5931af2e00e1b381aefd07b701120062999f272ef888054cbe5eaae6359c7de7(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b4937a016d97e862eac887dcb2a9bde4f8c00eb0670b56dc55ffe4ad5a16654(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eebb97c1ff2641e5195a5bb3ee47ffab9485850e3a2ffa3c46627196d9f7da81(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f5bb838c81e64eabe180c5699906e77ad297a98855e447087351b0c91c62be54(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8c1b84037b8d92ab33918e41b9d511857885bac1b20c5ead441aec313d73cdc3(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__704011e38dce4ee3b1659e632f44157eb941e862301805322e69e05c6070e164(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b9e0860647d2f80aece0d627cac60bce634a199dd76d24d1d463b039f8555c5(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__035cc8f0f1e939187d79ef0dc22fa66f5b5b26c70d62b39d097524127bc4d6a5(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__37c99c557d54e7ffa1b8e562b8b764abd7347263be398c520c531556ba9ec40f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__10c50fdbbcc67620f9573a7ebe3f85fd8843dc9e8a24bd6f8b3a52112d1f1dc8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c39d3dff18b657f7cba21236d4d8cfc2c8ea9e67d95ba902efa05f1307063ee(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__573c1f62208de26411d6e472ee5c0d90efdfa4eeb1167644040c04adf9382da5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e84d00525e789c1087d53b107540fdd56b5c0212e0fd05d217754c6601dbf273(
    *,
    email: typing.Optional[builtins.str] = None,
    first_name: typing.Optional[builtins.str] = None,
    full_name: typing.Optional[builtins.str] = None,
    groups: typing.Optional[builtins.str] = None,
    last_name: typing.Optional[builtins.str] = None,
    roles: typing.Optional[builtins.str] = None,
    subject: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__056049bcd01b57e0dd8960bf053f4f18faff121b001ff0cd8d29e05a6f86663a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a02035d2ef5589eff6a5c920e11de25958f8f3ace3ce11d9df71c21bd5732568(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__54ec074ecfe3c5fec061811fce1ccfb5526765ecaf54432ccd19f929addd4cf3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba443fe01e910fb49b2749e06b53871134845f6759df1a68e4ad2e96518df594(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a66fdef9099b9667425256046b42ed068493d56660c4d253d21ebe0d325de2f3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__90e27b54890c99a2e10d474ca7cf32f61c4ac5e0f796de0660f7d1cce7b48a6c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__42ffc9e5c7528df0afaa0085b659b9d5c040b9165180e16d5bef208122d5f48d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c98e66368ab1a84ea62e5fc0af08860e4f199fc90c9ba06006e60a3bb7e3062(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__55fbf2ac9c0b41a9d7cc6b255c9b6a914bc17dd4c2bfbd1ebf1e93473d15fb43(
    value: typing.Optional[OrgOidcClaimsMapping],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__94c43d31413160d5752c616fd9c6e483354c8ebbc7d07a31d04a51b9018f2133(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    client_id: builtins.str,
    client_secret: builtins.str,
    enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    org_id: builtins.str,
    access_token_endpoint: typing.Optional[builtins.str] = None,
    claims_mapping: typing.Optional[typing.Union[OrgOidcClaimsMapping, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    issuer_id: typing.Optional[builtins.str] = None,
    key: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OrgOidcKey, typing.Dict[builtins.str, typing.Any]]]]] = None,
    key_expire_duration_hours: typing.Optional[jsii.Number] = None,
    key_refresh_endpoint: typing.Optional[builtins.str] = None,
    key_refresh_period_hours: typing.Optional[jsii.Number] = None,
    key_refresh_strategy: typing.Optional[builtins.str] = None,
    max_clock_skew_seconds: typing.Optional[jsii.Number] = None,
    prefer_id_token: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    scopes: typing.Optional[typing.Sequence[builtins.str]] = None,
    ui_button_label: typing.Optional[builtins.str] = None,
    user_authorization_endpoint: typing.Optional[builtins.str] = None,
    userinfo_endpoint: typing.Optional[builtins.str] = None,
    wellknown_endpoint: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__49385857150f55f5e68559f92b316ebc01c20b09e8e3fe6510afab209daf08df(
    *,
    algorithm: builtins.str,
    certificate: builtins.str,
    id: builtins.str,
    expiration_date: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c50429104e5928283da1f445ffb715dccdbf2496ebcdb0cc8a878198c494191(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__822bc2add637e48dc48ef3f3b81fcf78c6bae4ad6c8e23c046f65020cd0718d4(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9564df21175305b089d24db15077be4020cbff1c9c0c366bff18234df889cd08(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__511cc2fb582193a7c7cfd1e38ff054acc6fadf5c9026b4ce60f38ba57fe058ea(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__665833e5183a87c27145d54f41634e1288b41ed885e453ebfb1b132bbd1eefef(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5db4cd0314f66c576fe0676b3d4c88de9c402592d0c11df3181ec10909d4ac46(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OrgOidcKey]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b76b57afba73525c402e1821bcbc5b982936cf1edf37cfb9695ea35f524cc07d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b633054fc30b6d5b43821988247c46610d6e3d99c0e4cac06890e118b1d31f46(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa6da6e1c365322369dfa5ecb4e460c513c41fef0d7ab7c5333000a737fad003(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3614c2e3ca05bb1076bfd1acfbea9e400e093e4686e28d280602011c29e236de(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8797603ad4428c009829df721b8f41ede87cd0f2ae037b2552ff6729052af1b4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__737cf78b035468534c84a9500c2873fbbcd625d0f73e1a9d1801127eab959381(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OrgOidcKey]],
) -> None:
    """Type checking stubs"""
    pass
