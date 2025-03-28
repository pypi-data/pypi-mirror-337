'''
# `vcd_nsxt_ipsec_vpn_tunnel`

Refer to the Terraform Registry for docs: [`vcd_nsxt_ipsec_vpn_tunnel`](https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_ipsec_vpn_tunnel).
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


class NsxtIpsecVpnTunnel(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="vcd.nsxtIpsecVpnTunnel.NsxtIpsecVpnTunnel",
):
    '''Represents a {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_ipsec_vpn_tunnel vcd_nsxt_ipsec_vpn_tunnel}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        edge_gateway_id: builtins.str,
        local_ip_address: builtins.str,
        local_networks: typing.Sequence[builtins.str],
        name: builtins.str,
        pre_shared_key: builtins.str,
        remote_ip_address: builtins.str,
        authentication_mode: typing.Optional[builtins.str] = None,
        ca_certificate_id: typing.Optional[builtins.str] = None,
        certificate_id: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        logging: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        org: typing.Optional[builtins.str] = None,
        remote_id: typing.Optional[builtins.str] = None,
        remote_networks: typing.Optional[typing.Sequence[builtins.str]] = None,
        security_profile_customization: typing.Optional[typing.Union["NsxtIpsecVpnTunnelSecurityProfileCustomization", typing.Dict[builtins.str, typing.Any]]] = None,
        vdc: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_ipsec_vpn_tunnel vcd_nsxt_ipsec_vpn_tunnel} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param edge_gateway_id: Edge gateway name in which IP Sec VPN configuration is located. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_ipsec_vpn_tunnel#edge_gateway_id NsxtIpsecVpnTunnel#edge_gateway_id}
        :param local_ip_address: IPv4 Address for the endpoint. This has to be a sub-allocated IP on the Edge Gateway. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_ipsec_vpn_tunnel#local_ip_address NsxtIpsecVpnTunnel#local_ip_address}
        :param local_networks: Set of local networks in CIDR format. At least one value is required. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_ipsec_vpn_tunnel#local_networks NsxtIpsecVpnTunnel#local_networks}
        :param name: Name of IP Sec VPN Tunnel. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_ipsec_vpn_tunnel#name NsxtIpsecVpnTunnel#name}
        :param pre_shared_key: Pre-Shared Key (PSK). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_ipsec_vpn_tunnel#pre_shared_key NsxtIpsecVpnTunnel#pre_shared_key}
        :param remote_ip_address: Public IPv4 Address of the remote device terminating the VPN connection. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_ipsec_vpn_tunnel#remote_ip_address NsxtIpsecVpnTunnel#remote_ip_address}
        :param authentication_mode: One of 'PSK' (default), 'CERTIFICATE'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_ipsec_vpn_tunnel#authentication_mode NsxtIpsecVpnTunnel#authentication_mode}
        :param ca_certificate_id: Optional CA certificate ID to use for authentication. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_ipsec_vpn_tunnel#ca_certificate_id NsxtIpsecVpnTunnel#ca_certificate_id}
        :param certificate_id: Optional certificate ID to use for authentication. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_ipsec_vpn_tunnel#certificate_id NsxtIpsecVpnTunnel#certificate_id}
        :param description: Description IP Sec VPN Tunnel. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_ipsec_vpn_tunnel#description NsxtIpsecVpnTunnel#description}
        :param enabled: Enables or disables this configuration (default true). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_ipsec_vpn_tunnel#enabled NsxtIpsecVpnTunnel#enabled}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_ipsec_vpn_tunnel#id NsxtIpsecVpnTunnel#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param logging: Sets whether logging for the tunnel is enabled or not. (default - false). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_ipsec_vpn_tunnel#logging NsxtIpsecVpnTunnel#logging}
        :param org: The name of organization to use, optional if defined at provider level. Useful when connected as sysadmin working across different organizations Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_ipsec_vpn_tunnel#org NsxtIpsecVpnTunnel#org}
        :param remote_id: Custom remote ID of the peer site. 'remote_ip_address' is used by default. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_ipsec_vpn_tunnel#remote_id NsxtIpsecVpnTunnel#remote_id}
        :param remote_networks: Set of remote networks in CIDR format. Leaving it empty is interpreted as 0.0.0.0/0. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_ipsec_vpn_tunnel#remote_networks NsxtIpsecVpnTunnel#remote_networks}
        :param security_profile_customization: security_profile_customization block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_ipsec_vpn_tunnel#security_profile_customization NsxtIpsecVpnTunnel#security_profile_customization}
        :param vdc: The name of VDC to use, optional if defined at provider level. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_ipsec_vpn_tunnel#vdc NsxtIpsecVpnTunnel#vdc}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9d636efabf297d57331630ede2a71abdbf2a275ee172ea8cc37ca9ceb88afadb)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = NsxtIpsecVpnTunnelConfig(
            edge_gateway_id=edge_gateway_id,
            local_ip_address=local_ip_address,
            local_networks=local_networks,
            name=name,
            pre_shared_key=pre_shared_key,
            remote_ip_address=remote_ip_address,
            authentication_mode=authentication_mode,
            ca_certificate_id=ca_certificate_id,
            certificate_id=certificate_id,
            description=description,
            enabled=enabled,
            id=id,
            logging=logging,
            org=org,
            remote_id=remote_id,
            remote_networks=remote_networks,
            security_profile_customization=security_profile_customization,
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
        '''Generates CDKTF code for importing a NsxtIpsecVpnTunnel resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the NsxtIpsecVpnTunnel to import.
        :param import_from_id: The id of the existing NsxtIpsecVpnTunnel that should be imported. Refer to the {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_ipsec_vpn_tunnel#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the NsxtIpsecVpnTunnel to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7128e5e54ac728f5aad1a2ff914c4bf709d4f27bf96dcbfbe71b7aaf2700f15f)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putSecurityProfileCustomization")
    def put_security_profile_customization(
        self,
        *,
        ike_dh_groups: typing.Sequence[builtins.str],
        ike_encryption_algorithms: typing.Sequence[builtins.str],
        ike_version: builtins.str,
        tunnel_dh_groups: typing.Sequence[builtins.str],
        tunnel_encryption_algorithms: typing.Sequence[builtins.str],
        dpd_probe_internal: typing.Optional[jsii.Number] = None,
        ike_digest_algorithms: typing.Optional[typing.Sequence[builtins.str]] = None,
        ike_sa_lifetime: typing.Optional[jsii.Number] = None,
        tunnel_df_policy: typing.Optional[builtins.str] = None,
        tunnel_digest_algorithms: typing.Optional[typing.Sequence[builtins.str]] = None,
        tunnel_pfs_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        tunnel_sa_lifetime: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param ike_dh_groups: Diffie-Hellman groups to be used if Perfect Forward Secrecy is enabled. One of GROUP2, GROUP5, GROUP14, GROUP15, GROUP16, GROUP19, GROUP20, GROUP21 Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_ipsec_vpn_tunnel#ike_dh_groups NsxtIpsecVpnTunnel#ike_dh_groups}
        :param ike_encryption_algorithms: Encryption algorithms. One of SHA1, SHA2_256, SHA2_384, SHA2_512. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_ipsec_vpn_tunnel#ike_encryption_algorithms NsxtIpsecVpnTunnel#ike_encryption_algorithms}
        :param ike_version: IKE version one of IKE_V1, IKE_V2, IKE_FLEX. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_ipsec_vpn_tunnel#ike_version NsxtIpsecVpnTunnel#ike_version}
        :param tunnel_dh_groups: Diffie-Hellman groups to be used is PFS is enabled. One of GROUP2, GROUP5, GROUP14, GROUP15, GROUP16, GROUP19, GROUP20, GROUP21. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_ipsec_vpn_tunnel#tunnel_dh_groups NsxtIpsecVpnTunnel#tunnel_dh_groups}
        :param tunnel_encryption_algorithms: Encryption algorithms to use in IPSec tunnel establishment. One of AES_128, AES_256, AES_GCM_128, AES_GCM_192, AES_GCM_256, NO_ENCRYPTION_AUTH_AES_GMAC_128, NO_ENCRYPTION_AUTH_AES_GMAC_192, NO_ENCRYPTION_AUTH_AES_GMAC_256, NO_ENCRYPTION. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_ipsec_vpn_tunnel#tunnel_encryption_algorithms NsxtIpsecVpnTunnel#tunnel_encryption_algorithms}
        :param dpd_probe_internal: Value in seconds of dead probe detection interval. Minimum is 3 seconds and the maximum is 60 seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_ipsec_vpn_tunnel#dpd_probe_internal NsxtIpsecVpnTunnel#dpd_probe_internal}
        :param ike_digest_algorithms: Secure hashing algorithms to use during the IKE negotiation. One of SHA1, SHA2_256, SHA2_384, SHA2_512. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_ipsec_vpn_tunnel#ike_digest_algorithms NsxtIpsecVpnTunnel#ike_digest_algorithms}
        :param ike_sa_lifetime: Security Association life time (in seconds). It is number of seconds before the IPsec tunnel needs to reestablish. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_ipsec_vpn_tunnel#ike_sa_lifetime NsxtIpsecVpnTunnel#ike_sa_lifetime}
        :param tunnel_df_policy: Policy for handling defragmentation bit. One of COPY, CLEAR. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_ipsec_vpn_tunnel#tunnel_df_policy NsxtIpsecVpnTunnel#tunnel_df_policy}
        :param tunnel_digest_algorithms: Digest algorithms to be used for message digest. One of SHA1, SHA2_256, SHA2_384, SHA2_512. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_ipsec_vpn_tunnel#tunnel_digest_algorithms NsxtIpsecVpnTunnel#tunnel_digest_algorithms}
        :param tunnel_pfs_enabled: Perfect Forward Secrecy Enabled or Disabled. Default (enabled). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_ipsec_vpn_tunnel#tunnel_pfs_enabled NsxtIpsecVpnTunnel#tunnel_pfs_enabled}
        :param tunnel_sa_lifetime: Security Association life time (in seconds). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_ipsec_vpn_tunnel#tunnel_sa_lifetime NsxtIpsecVpnTunnel#tunnel_sa_lifetime}
        '''
        value = NsxtIpsecVpnTunnelSecurityProfileCustomization(
            ike_dh_groups=ike_dh_groups,
            ike_encryption_algorithms=ike_encryption_algorithms,
            ike_version=ike_version,
            tunnel_dh_groups=tunnel_dh_groups,
            tunnel_encryption_algorithms=tunnel_encryption_algorithms,
            dpd_probe_internal=dpd_probe_internal,
            ike_digest_algorithms=ike_digest_algorithms,
            ike_sa_lifetime=ike_sa_lifetime,
            tunnel_df_policy=tunnel_df_policy,
            tunnel_digest_algorithms=tunnel_digest_algorithms,
            tunnel_pfs_enabled=tunnel_pfs_enabled,
            tunnel_sa_lifetime=tunnel_sa_lifetime,
        )

        return typing.cast(None, jsii.invoke(self, "putSecurityProfileCustomization", [value]))

    @jsii.member(jsii_name="resetAuthenticationMode")
    def reset_authentication_mode(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAuthenticationMode", []))

    @jsii.member(jsii_name="resetCaCertificateId")
    def reset_ca_certificate_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCaCertificateId", []))

    @jsii.member(jsii_name="resetCertificateId")
    def reset_certificate_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCertificateId", []))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetEnabled")
    def reset_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnabled", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetLogging")
    def reset_logging(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLogging", []))

    @jsii.member(jsii_name="resetOrg")
    def reset_org(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOrg", []))

    @jsii.member(jsii_name="resetRemoteId")
    def reset_remote_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRemoteId", []))

    @jsii.member(jsii_name="resetRemoteNetworks")
    def reset_remote_networks(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRemoteNetworks", []))

    @jsii.member(jsii_name="resetSecurityProfileCustomization")
    def reset_security_profile_customization(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSecurityProfileCustomization", []))

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
    @jsii.member(jsii_name="ikeFailReason")
    def ike_fail_reason(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ikeFailReason"))

    @builtins.property
    @jsii.member(jsii_name="ikeServiceStatus")
    def ike_service_status(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ikeServiceStatus"))

    @builtins.property
    @jsii.member(jsii_name="securityProfile")
    def security_profile(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "securityProfile"))

    @builtins.property
    @jsii.member(jsii_name="securityProfileCustomization")
    def security_profile_customization(
        self,
    ) -> "NsxtIpsecVpnTunnelSecurityProfileCustomizationOutputReference":
        return typing.cast("NsxtIpsecVpnTunnelSecurityProfileCustomizationOutputReference", jsii.get(self, "securityProfileCustomization"))

    @builtins.property
    @jsii.member(jsii_name="status")
    def status(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "status"))

    @builtins.property
    @jsii.member(jsii_name="authenticationModeInput")
    def authentication_mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "authenticationModeInput"))

    @builtins.property
    @jsii.member(jsii_name="caCertificateIdInput")
    def ca_certificate_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "caCertificateIdInput"))

    @builtins.property
    @jsii.member(jsii_name="certificateIdInput")
    def certificate_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "certificateIdInput"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="edgeGatewayIdInput")
    def edge_gateway_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "edgeGatewayIdInput"))

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
    @jsii.member(jsii_name="localIpAddressInput")
    def local_ip_address_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "localIpAddressInput"))

    @builtins.property
    @jsii.member(jsii_name="localNetworksInput")
    def local_networks_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "localNetworksInput"))

    @builtins.property
    @jsii.member(jsii_name="loggingInput")
    def logging_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "loggingInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="orgInput")
    def org_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "orgInput"))

    @builtins.property
    @jsii.member(jsii_name="preSharedKeyInput")
    def pre_shared_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "preSharedKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="remoteIdInput")
    def remote_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "remoteIdInput"))

    @builtins.property
    @jsii.member(jsii_name="remoteIpAddressInput")
    def remote_ip_address_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "remoteIpAddressInput"))

    @builtins.property
    @jsii.member(jsii_name="remoteNetworksInput")
    def remote_networks_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "remoteNetworksInput"))

    @builtins.property
    @jsii.member(jsii_name="securityProfileCustomizationInput")
    def security_profile_customization_input(
        self,
    ) -> typing.Optional["NsxtIpsecVpnTunnelSecurityProfileCustomization"]:
        return typing.cast(typing.Optional["NsxtIpsecVpnTunnelSecurityProfileCustomization"], jsii.get(self, "securityProfileCustomizationInput"))

    @builtins.property
    @jsii.member(jsii_name="vdcInput")
    def vdc_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "vdcInput"))

    @builtins.property
    @jsii.member(jsii_name="authenticationMode")
    def authentication_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "authenticationMode"))

    @authentication_mode.setter
    def authentication_mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b2fa4f92ff439c2a7cd92440d0770b2e6d522eaf5f7f680cdf07311db657f560)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "authenticationMode", value)

    @builtins.property
    @jsii.member(jsii_name="caCertificateId")
    def ca_certificate_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "caCertificateId"))

    @ca_certificate_id.setter
    def ca_certificate_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__63610208b3b238d83483f392725efc2276dac712942e5573e93993c182bf4c87)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "caCertificateId", value)

    @builtins.property
    @jsii.member(jsii_name="certificateId")
    def certificate_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "certificateId"))

    @certificate_id.setter
    def certificate_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e567531075115ded3d1a3b9f5389368d663f79ab82c635a37c3388a5894b2715)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "certificateId", value)

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__26cbda9cb6cd2e76a86a94814fba6e1d7b50f68b8c2bd84de2b9efadf7497049)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value)

    @builtins.property
    @jsii.member(jsii_name="edgeGatewayId")
    def edge_gateway_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "edgeGatewayId"))

    @edge_gateway_id.setter
    def edge_gateway_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5fdd00fdca93879ba004b250e036692a94779c10701b887d9e0c202992c69fe3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "edgeGatewayId", value)

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
            type_hints = typing.get_type_hints(_typecheckingstub__6989f4691e2b491dd6dbb73f85d6936ffe5029ff267bc343f5831250fa314a95)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value)

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__99179aae83c2e52760e5480ea139ba000e89e237ca0cc0691e01ba374182da08)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="localIpAddress")
    def local_ip_address(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "localIpAddress"))

    @local_ip_address.setter
    def local_ip_address(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__37f76249fe8bcd6aeca04c4b526274ede716ae1cd6f177b049b7bb9094a00a87)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "localIpAddress", value)

    @builtins.property
    @jsii.member(jsii_name="localNetworks")
    def local_networks(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "localNetworks"))

    @local_networks.setter
    def local_networks(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7c76f008072490656f79acacf7810c79621f9ec048ec1bef1d28be22df58e5d1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "localNetworks", value)

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
            type_hints = typing.get_type_hints(_typecheckingstub__0fcca17d1766716558544d9d525383c28707ffd6f9803d07c536e665d2a0ef7c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "logging", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5ae15aeddf58577a28768f5512a14e6ee03f781f96df53966e367b464ba6ba5f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="org")
    def org(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "org"))

    @org.setter
    def org(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d726504acc54e26f7d9b73a48109b07b10fac19dd2b2a4715c1c079009081bab)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "org", value)

    @builtins.property
    @jsii.member(jsii_name="preSharedKey")
    def pre_shared_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "preSharedKey"))

    @pre_shared_key.setter
    def pre_shared_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d7f4218c05a7eee3845d375fa6be3300512e32fd9f05e5b6be4364e68aeb15be)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "preSharedKey", value)

    @builtins.property
    @jsii.member(jsii_name="remoteId")
    def remote_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "remoteId"))

    @remote_id.setter
    def remote_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9b84444762edcd91d7777c188efc80a3735ddfcd29291865307605d8223b669f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "remoteId", value)

    @builtins.property
    @jsii.member(jsii_name="remoteIpAddress")
    def remote_ip_address(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "remoteIpAddress"))

    @remote_ip_address.setter
    def remote_ip_address(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c1b864063d26b13124cd73c82942d19451cb12c7b1bb817aac7395be3932cb12)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "remoteIpAddress", value)

    @builtins.property
    @jsii.member(jsii_name="remoteNetworks")
    def remote_networks(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "remoteNetworks"))

    @remote_networks.setter
    def remote_networks(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9807e37410a1f60d15ccae4b36fb025146f7088420a8c1041da246df2794da33)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "remoteNetworks", value)

    @builtins.property
    @jsii.member(jsii_name="vdc")
    def vdc(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "vdc"))

    @vdc.setter
    def vdc(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3897e46541afc238bea23848c0853c6fd6e5852e4d1559fcd27e37eb004e3711)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vdc", value)


@jsii.data_type(
    jsii_type="vcd.nsxtIpsecVpnTunnel.NsxtIpsecVpnTunnelConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "edge_gateway_id": "edgeGatewayId",
        "local_ip_address": "localIpAddress",
        "local_networks": "localNetworks",
        "name": "name",
        "pre_shared_key": "preSharedKey",
        "remote_ip_address": "remoteIpAddress",
        "authentication_mode": "authenticationMode",
        "ca_certificate_id": "caCertificateId",
        "certificate_id": "certificateId",
        "description": "description",
        "enabled": "enabled",
        "id": "id",
        "logging": "logging",
        "org": "org",
        "remote_id": "remoteId",
        "remote_networks": "remoteNetworks",
        "security_profile_customization": "securityProfileCustomization",
        "vdc": "vdc",
    },
)
class NsxtIpsecVpnTunnelConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        edge_gateway_id: builtins.str,
        local_ip_address: builtins.str,
        local_networks: typing.Sequence[builtins.str],
        name: builtins.str,
        pre_shared_key: builtins.str,
        remote_ip_address: builtins.str,
        authentication_mode: typing.Optional[builtins.str] = None,
        ca_certificate_id: typing.Optional[builtins.str] = None,
        certificate_id: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        logging: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        org: typing.Optional[builtins.str] = None,
        remote_id: typing.Optional[builtins.str] = None,
        remote_networks: typing.Optional[typing.Sequence[builtins.str]] = None,
        security_profile_customization: typing.Optional[typing.Union["NsxtIpsecVpnTunnelSecurityProfileCustomization", typing.Dict[builtins.str, typing.Any]]] = None,
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
        :param edge_gateway_id: Edge gateway name in which IP Sec VPN configuration is located. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_ipsec_vpn_tunnel#edge_gateway_id NsxtIpsecVpnTunnel#edge_gateway_id}
        :param local_ip_address: IPv4 Address for the endpoint. This has to be a sub-allocated IP on the Edge Gateway. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_ipsec_vpn_tunnel#local_ip_address NsxtIpsecVpnTunnel#local_ip_address}
        :param local_networks: Set of local networks in CIDR format. At least one value is required. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_ipsec_vpn_tunnel#local_networks NsxtIpsecVpnTunnel#local_networks}
        :param name: Name of IP Sec VPN Tunnel. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_ipsec_vpn_tunnel#name NsxtIpsecVpnTunnel#name}
        :param pre_shared_key: Pre-Shared Key (PSK). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_ipsec_vpn_tunnel#pre_shared_key NsxtIpsecVpnTunnel#pre_shared_key}
        :param remote_ip_address: Public IPv4 Address of the remote device terminating the VPN connection. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_ipsec_vpn_tunnel#remote_ip_address NsxtIpsecVpnTunnel#remote_ip_address}
        :param authentication_mode: One of 'PSK' (default), 'CERTIFICATE'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_ipsec_vpn_tunnel#authentication_mode NsxtIpsecVpnTunnel#authentication_mode}
        :param ca_certificate_id: Optional CA certificate ID to use for authentication. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_ipsec_vpn_tunnel#ca_certificate_id NsxtIpsecVpnTunnel#ca_certificate_id}
        :param certificate_id: Optional certificate ID to use for authentication. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_ipsec_vpn_tunnel#certificate_id NsxtIpsecVpnTunnel#certificate_id}
        :param description: Description IP Sec VPN Tunnel. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_ipsec_vpn_tunnel#description NsxtIpsecVpnTunnel#description}
        :param enabled: Enables or disables this configuration (default true). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_ipsec_vpn_tunnel#enabled NsxtIpsecVpnTunnel#enabled}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_ipsec_vpn_tunnel#id NsxtIpsecVpnTunnel#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param logging: Sets whether logging for the tunnel is enabled or not. (default - false). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_ipsec_vpn_tunnel#logging NsxtIpsecVpnTunnel#logging}
        :param org: The name of organization to use, optional if defined at provider level. Useful when connected as sysadmin working across different organizations Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_ipsec_vpn_tunnel#org NsxtIpsecVpnTunnel#org}
        :param remote_id: Custom remote ID of the peer site. 'remote_ip_address' is used by default. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_ipsec_vpn_tunnel#remote_id NsxtIpsecVpnTunnel#remote_id}
        :param remote_networks: Set of remote networks in CIDR format. Leaving it empty is interpreted as 0.0.0.0/0. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_ipsec_vpn_tunnel#remote_networks NsxtIpsecVpnTunnel#remote_networks}
        :param security_profile_customization: security_profile_customization block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_ipsec_vpn_tunnel#security_profile_customization NsxtIpsecVpnTunnel#security_profile_customization}
        :param vdc: The name of VDC to use, optional if defined at provider level. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_ipsec_vpn_tunnel#vdc NsxtIpsecVpnTunnel#vdc}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(security_profile_customization, dict):
            security_profile_customization = NsxtIpsecVpnTunnelSecurityProfileCustomization(**security_profile_customization)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__99a5243fd93167cc768527b58062e75272cdda017086cdbadb5682d4f382b147)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument edge_gateway_id", value=edge_gateway_id, expected_type=type_hints["edge_gateway_id"])
            check_type(argname="argument local_ip_address", value=local_ip_address, expected_type=type_hints["local_ip_address"])
            check_type(argname="argument local_networks", value=local_networks, expected_type=type_hints["local_networks"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument pre_shared_key", value=pre_shared_key, expected_type=type_hints["pre_shared_key"])
            check_type(argname="argument remote_ip_address", value=remote_ip_address, expected_type=type_hints["remote_ip_address"])
            check_type(argname="argument authentication_mode", value=authentication_mode, expected_type=type_hints["authentication_mode"])
            check_type(argname="argument ca_certificate_id", value=ca_certificate_id, expected_type=type_hints["ca_certificate_id"])
            check_type(argname="argument certificate_id", value=certificate_id, expected_type=type_hints["certificate_id"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument logging", value=logging, expected_type=type_hints["logging"])
            check_type(argname="argument org", value=org, expected_type=type_hints["org"])
            check_type(argname="argument remote_id", value=remote_id, expected_type=type_hints["remote_id"])
            check_type(argname="argument remote_networks", value=remote_networks, expected_type=type_hints["remote_networks"])
            check_type(argname="argument security_profile_customization", value=security_profile_customization, expected_type=type_hints["security_profile_customization"])
            check_type(argname="argument vdc", value=vdc, expected_type=type_hints["vdc"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "edge_gateway_id": edge_gateway_id,
            "local_ip_address": local_ip_address,
            "local_networks": local_networks,
            "name": name,
            "pre_shared_key": pre_shared_key,
            "remote_ip_address": remote_ip_address,
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
        if authentication_mode is not None:
            self._values["authentication_mode"] = authentication_mode
        if ca_certificate_id is not None:
            self._values["ca_certificate_id"] = ca_certificate_id
        if certificate_id is not None:
            self._values["certificate_id"] = certificate_id
        if description is not None:
            self._values["description"] = description
        if enabled is not None:
            self._values["enabled"] = enabled
        if id is not None:
            self._values["id"] = id
        if logging is not None:
            self._values["logging"] = logging
        if org is not None:
            self._values["org"] = org
        if remote_id is not None:
            self._values["remote_id"] = remote_id
        if remote_networks is not None:
            self._values["remote_networks"] = remote_networks
        if security_profile_customization is not None:
            self._values["security_profile_customization"] = security_profile_customization
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
    def edge_gateway_id(self) -> builtins.str:
        '''Edge gateway name in which IP Sec VPN configuration is located.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_ipsec_vpn_tunnel#edge_gateway_id NsxtIpsecVpnTunnel#edge_gateway_id}
        '''
        result = self._values.get("edge_gateway_id")
        assert result is not None, "Required property 'edge_gateway_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def local_ip_address(self) -> builtins.str:
        '''IPv4 Address for the endpoint. This has to be a sub-allocated IP on the Edge Gateway.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_ipsec_vpn_tunnel#local_ip_address NsxtIpsecVpnTunnel#local_ip_address}
        '''
        result = self._values.get("local_ip_address")
        assert result is not None, "Required property 'local_ip_address' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def local_networks(self) -> typing.List[builtins.str]:
        '''Set of local networks in CIDR format. At least one value is required.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_ipsec_vpn_tunnel#local_networks NsxtIpsecVpnTunnel#local_networks}
        '''
        result = self._values.get("local_networks")
        assert result is not None, "Required property 'local_networks' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Name of IP Sec VPN Tunnel.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_ipsec_vpn_tunnel#name NsxtIpsecVpnTunnel#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def pre_shared_key(self) -> builtins.str:
        '''Pre-Shared Key (PSK).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_ipsec_vpn_tunnel#pre_shared_key NsxtIpsecVpnTunnel#pre_shared_key}
        '''
        result = self._values.get("pre_shared_key")
        assert result is not None, "Required property 'pre_shared_key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def remote_ip_address(self) -> builtins.str:
        '''Public IPv4 Address of the remote device terminating the VPN connection.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_ipsec_vpn_tunnel#remote_ip_address NsxtIpsecVpnTunnel#remote_ip_address}
        '''
        result = self._values.get("remote_ip_address")
        assert result is not None, "Required property 'remote_ip_address' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def authentication_mode(self) -> typing.Optional[builtins.str]:
        '''One of 'PSK' (default), 'CERTIFICATE'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_ipsec_vpn_tunnel#authentication_mode NsxtIpsecVpnTunnel#authentication_mode}
        '''
        result = self._values.get("authentication_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ca_certificate_id(self) -> typing.Optional[builtins.str]:
        '''Optional CA certificate ID to use for authentication.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_ipsec_vpn_tunnel#ca_certificate_id NsxtIpsecVpnTunnel#ca_certificate_id}
        '''
        result = self._values.get("ca_certificate_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def certificate_id(self) -> typing.Optional[builtins.str]:
        '''Optional certificate ID to use for authentication.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_ipsec_vpn_tunnel#certificate_id NsxtIpsecVpnTunnel#certificate_id}
        '''
        result = self._values.get("certificate_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Description IP Sec VPN Tunnel.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_ipsec_vpn_tunnel#description NsxtIpsecVpnTunnel#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Enables or disables this configuration (default true).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_ipsec_vpn_tunnel#enabled NsxtIpsecVpnTunnel#enabled}
        '''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_ipsec_vpn_tunnel#id NsxtIpsecVpnTunnel#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def logging(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Sets whether logging for the tunnel is enabled or not. (default - false).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_ipsec_vpn_tunnel#logging NsxtIpsecVpnTunnel#logging}
        '''
        result = self._values.get("logging")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def org(self) -> typing.Optional[builtins.str]:
        '''The name of organization to use, optional if defined at provider level.

        Useful when connected as sysadmin working across different organizations

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_ipsec_vpn_tunnel#org NsxtIpsecVpnTunnel#org}
        '''
        result = self._values.get("org")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def remote_id(self) -> typing.Optional[builtins.str]:
        '''Custom remote ID of the peer site. 'remote_ip_address' is used by default.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_ipsec_vpn_tunnel#remote_id NsxtIpsecVpnTunnel#remote_id}
        '''
        result = self._values.get("remote_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def remote_networks(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Set of remote networks in CIDR format. Leaving it empty is interpreted as 0.0.0.0/0.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_ipsec_vpn_tunnel#remote_networks NsxtIpsecVpnTunnel#remote_networks}
        '''
        result = self._values.get("remote_networks")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def security_profile_customization(
        self,
    ) -> typing.Optional["NsxtIpsecVpnTunnelSecurityProfileCustomization"]:
        '''security_profile_customization block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_ipsec_vpn_tunnel#security_profile_customization NsxtIpsecVpnTunnel#security_profile_customization}
        '''
        result = self._values.get("security_profile_customization")
        return typing.cast(typing.Optional["NsxtIpsecVpnTunnelSecurityProfileCustomization"], result)

    @builtins.property
    def vdc(self) -> typing.Optional[builtins.str]:
        '''The name of VDC to use, optional if defined at provider level.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_ipsec_vpn_tunnel#vdc NsxtIpsecVpnTunnel#vdc}
        '''
        result = self._values.get("vdc")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NsxtIpsecVpnTunnelConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="vcd.nsxtIpsecVpnTunnel.NsxtIpsecVpnTunnelSecurityProfileCustomization",
    jsii_struct_bases=[],
    name_mapping={
        "ike_dh_groups": "ikeDhGroups",
        "ike_encryption_algorithms": "ikeEncryptionAlgorithms",
        "ike_version": "ikeVersion",
        "tunnel_dh_groups": "tunnelDhGroups",
        "tunnel_encryption_algorithms": "tunnelEncryptionAlgorithms",
        "dpd_probe_internal": "dpdProbeInternal",
        "ike_digest_algorithms": "ikeDigestAlgorithms",
        "ike_sa_lifetime": "ikeSaLifetime",
        "tunnel_df_policy": "tunnelDfPolicy",
        "tunnel_digest_algorithms": "tunnelDigestAlgorithms",
        "tunnel_pfs_enabled": "tunnelPfsEnabled",
        "tunnel_sa_lifetime": "tunnelSaLifetime",
    },
)
class NsxtIpsecVpnTunnelSecurityProfileCustomization:
    def __init__(
        self,
        *,
        ike_dh_groups: typing.Sequence[builtins.str],
        ike_encryption_algorithms: typing.Sequence[builtins.str],
        ike_version: builtins.str,
        tunnel_dh_groups: typing.Sequence[builtins.str],
        tunnel_encryption_algorithms: typing.Sequence[builtins.str],
        dpd_probe_internal: typing.Optional[jsii.Number] = None,
        ike_digest_algorithms: typing.Optional[typing.Sequence[builtins.str]] = None,
        ike_sa_lifetime: typing.Optional[jsii.Number] = None,
        tunnel_df_policy: typing.Optional[builtins.str] = None,
        tunnel_digest_algorithms: typing.Optional[typing.Sequence[builtins.str]] = None,
        tunnel_pfs_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        tunnel_sa_lifetime: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param ike_dh_groups: Diffie-Hellman groups to be used if Perfect Forward Secrecy is enabled. One of GROUP2, GROUP5, GROUP14, GROUP15, GROUP16, GROUP19, GROUP20, GROUP21 Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_ipsec_vpn_tunnel#ike_dh_groups NsxtIpsecVpnTunnel#ike_dh_groups}
        :param ike_encryption_algorithms: Encryption algorithms. One of SHA1, SHA2_256, SHA2_384, SHA2_512. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_ipsec_vpn_tunnel#ike_encryption_algorithms NsxtIpsecVpnTunnel#ike_encryption_algorithms}
        :param ike_version: IKE version one of IKE_V1, IKE_V2, IKE_FLEX. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_ipsec_vpn_tunnel#ike_version NsxtIpsecVpnTunnel#ike_version}
        :param tunnel_dh_groups: Diffie-Hellman groups to be used is PFS is enabled. One of GROUP2, GROUP5, GROUP14, GROUP15, GROUP16, GROUP19, GROUP20, GROUP21. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_ipsec_vpn_tunnel#tunnel_dh_groups NsxtIpsecVpnTunnel#tunnel_dh_groups}
        :param tunnel_encryption_algorithms: Encryption algorithms to use in IPSec tunnel establishment. One of AES_128, AES_256, AES_GCM_128, AES_GCM_192, AES_GCM_256, NO_ENCRYPTION_AUTH_AES_GMAC_128, NO_ENCRYPTION_AUTH_AES_GMAC_192, NO_ENCRYPTION_AUTH_AES_GMAC_256, NO_ENCRYPTION. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_ipsec_vpn_tunnel#tunnel_encryption_algorithms NsxtIpsecVpnTunnel#tunnel_encryption_algorithms}
        :param dpd_probe_internal: Value in seconds of dead probe detection interval. Minimum is 3 seconds and the maximum is 60 seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_ipsec_vpn_tunnel#dpd_probe_internal NsxtIpsecVpnTunnel#dpd_probe_internal}
        :param ike_digest_algorithms: Secure hashing algorithms to use during the IKE negotiation. One of SHA1, SHA2_256, SHA2_384, SHA2_512. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_ipsec_vpn_tunnel#ike_digest_algorithms NsxtIpsecVpnTunnel#ike_digest_algorithms}
        :param ike_sa_lifetime: Security Association life time (in seconds). It is number of seconds before the IPsec tunnel needs to reestablish. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_ipsec_vpn_tunnel#ike_sa_lifetime NsxtIpsecVpnTunnel#ike_sa_lifetime}
        :param tunnel_df_policy: Policy for handling defragmentation bit. One of COPY, CLEAR. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_ipsec_vpn_tunnel#tunnel_df_policy NsxtIpsecVpnTunnel#tunnel_df_policy}
        :param tunnel_digest_algorithms: Digest algorithms to be used for message digest. One of SHA1, SHA2_256, SHA2_384, SHA2_512. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_ipsec_vpn_tunnel#tunnel_digest_algorithms NsxtIpsecVpnTunnel#tunnel_digest_algorithms}
        :param tunnel_pfs_enabled: Perfect Forward Secrecy Enabled or Disabled. Default (enabled). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_ipsec_vpn_tunnel#tunnel_pfs_enabled NsxtIpsecVpnTunnel#tunnel_pfs_enabled}
        :param tunnel_sa_lifetime: Security Association life time (in seconds). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_ipsec_vpn_tunnel#tunnel_sa_lifetime NsxtIpsecVpnTunnel#tunnel_sa_lifetime}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4ca323f8922401e6a91fdc09b86a72d5230006ce750c35068e4568b2d5e3891c)
            check_type(argname="argument ike_dh_groups", value=ike_dh_groups, expected_type=type_hints["ike_dh_groups"])
            check_type(argname="argument ike_encryption_algorithms", value=ike_encryption_algorithms, expected_type=type_hints["ike_encryption_algorithms"])
            check_type(argname="argument ike_version", value=ike_version, expected_type=type_hints["ike_version"])
            check_type(argname="argument tunnel_dh_groups", value=tunnel_dh_groups, expected_type=type_hints["tunnel_dh_groups"])
            check_type(argname="argument tunnel_encryption_algorithms", value=tunnel_encryption_algorithms, expected_type=type_hints["tunnel_encryption_algorithms"])
            check_type(argname="argument dpd_probe_internal", value=dpd_probe_internal, expected_type=type_hints["dpd_probe_internal"])
            check_type(argname="argument ike_digest_algorithms", value=ike_digest_algorithms, expected_type=type_hints["ike_digest_algorithms"])
            check_type(argname="argument ike_sa_lifetime", value=ike_sa_lifetime, expected_type=type_hints["ike_sa_lifetime"])
            check_type(argname="argument tunnel_df_policy", value=tunnel_df_policy, expected_type=type_hints["tunnel_df_policy"])
            check_type(argname="argument tunnel_digest_algorithms", value=tunnel_digest_algorithms, expected_type=type_hints["tunnel_digest_algorithms"])
            check_type(argname="argument tunnel_pfs_enabled", value=tunnel_pfs_enabled, expected_type=type_hints["tunnel_pfs_enabled"])
            check_type(argname="argument tunnel_sa_lifetime", value=tunnel_sa_lifetime, expected_type=type_hints["tunnel_sa_lifetime"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "ike_dh_groups": ike_dh_groups,
            "ike_encryption_algorithms": ike_encryption_algorithms,
            "ike_version": ike_version,
            "tunnel_dh_groups": tunnel_dh_groups,
            "tunnel_encryption_algorithms": tunnel_encryption_algorithms,
        }
        if dpd_probe_internal is not None:
            self._values["dpd_probe_internal"] = dpd_probe_internal
        if ike_digest_algorithms is not None:
            self._values["ike_digest_algorithms"] = ike_digest_algorithms
        if ike_sa_lifetime is not None:
            self._values["ike_sa_lifetime"] = ike_sa_lifetime
        if tunnel_df_policy is not None:
            self._values["tunnel_df_policy"] = tunnel_df_policy
        if tunnel_digest_algorithms is not None:
            self._values["tunnel_digest_algorithms"] = tunnel_digest_algorithms
        if tunnel_pfs_enabled is not None:
            self._values["tunnel_pfs_enabled"] = tunnel_pfs_enabled
        if tunnel_sa_lifetime is not None:
            self._values["tunnel_sa_lifetime"] = tunnel_sa_lifetime

    @builtins.property
    def ike_dh_groups(self) -> typing.List[builtins.str]:
        '''Diffie-Hellman groups to be used if Perfect Forward Secrecy is enabled.

        One of GROUP2, GROUP5, GROUP14, GROUP15, GROUP16, GROUP19, GROUP20, GROUP21

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_ipsec_vpn_tunnel#ike_dh_groups NsxtIpsecVpnTunnel#ike_dh_groups}
        '''
        result = self._values.get("ike_dh_groups")
        assert result is not None, "Required property 'ike_dh_groups' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def ike_encryption_algorithms(self) -> typing.List[builtins.str]:
        '''Encryption algorithms. One of SHA1, SHA2_256, SHA2_384, SHA2_512.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_ipsec_vpn_tunnel#ike_encryption_algorithms NsxtIpsecVpnTunnel#ike_encryption_algorithms}
        '''
        result = self._values.get("ike_encryption_algorithms")
        assert result is not None, "Required property 'ike_encryption_algorithms' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def ike_version(self) -> builtins.str:
        '''IKE version one of IKE_V1, IKE_V2, IKE_FLEX.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_ipsec_vpn_tunnel#ike_version NsxtIpsecVpnTunnel#ike_version}
        '''
        result = self._values.get("ike_version")
        assert result is not None, "Required property 'ike_version' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def tunnel_dh_groups(self) -> typing.List[builtins.str]:
        '''Diffie-Hellman groups to be used is PFS is enabled. One of GROUP2, GROUP5, GROUP14, GROUP15, GROUP16, GROUP19, GROUP20, GROUP21.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_ipsec_vpn_tunnel#tunnel_dh_groups NsxtIpsecVpnTunnel#tunnel_dh_groups}
        '''
        result = self._values.get("tunnel_dh_groups")
        assert result is not None, "Required property 'tunnel_dh_groups' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def tunnel_encryption_algorithms(self) -> typing.List[builtins.str]:
        '''Encryption algorithms to use in IPSec tunnel establishment. One of AES_128, AES_256, AES_GCM_128, AES_GCM_192, AES_GCM_256, NO_ENCRYPTION_AUTH_AES_GMAC_128, NO_ENCRYPTION_AUTH_AES_GMAC_192, NO_ENCRYPTION_AUTH_AES_GMAC_256, NO_ENCRYPTION.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_ipsec_vpn_tunnel#tunnel_encryption_algorithms NsxtIpsecVpnTunnel#tunnel_encryption_algorithms}
        '''
        result = self._values.get("tunnel_encryption_algorithms")
        assert result is not None, "Required property 'tunnel_encryption_algorithms' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def dpd_probe_internal(self) -> typing.Optional[jsii.Number]:
        '''Value in seconds of dead probe detection interval. Minimum is 3 seconds and the maximum is 60 seconds.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_ipsec_vpn_tunnel#dpd_probe_internal NsxtIpsecVpnTunnel#dpd_probe_internal}
        '''
        result = self._values.get("dpd_probe_internal")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def ike_digest_algorithms(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Secure hashing algorithms to use during the IKE negotiation. One of SHA1, SHA2_256, SHA2_384, SHA2_512.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_ipsec_vpn_tunnel#ike_digest_algorithms NsxtIpsecVpnTunnel#ike_digest_algorithms}
        '''
        result = self._values.get("ike_digest_algorithms")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def ike_sa_lifetime(self) -> typing.Optional[jsii.Number]:
        '''Security Association life time (in seconds). It is number of seconds before the IPsec tunnel needs to reestablish.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_ipsec_vpn_tunnel#ike_sa_lifetime NsxtIpsecVpnTunnel#ike_sa_lifetime}
        '''
        result = self._values.get("ike_sa_lifetime")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def tunnel_df_policy(self) -> typing.Optional[builtins.str]:
        '''Policy for handling defragmentation bit. One of COPY, CLEAR.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_ipsec_vpn_tunnel#tunnel_df_policy NsxtIpsecVpnTunnel#tunnel_df_policy}
        '''
        result = self._values.get("tunnel_df_policy")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tunnel_digest_algorithms(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Digest algorithms to be used for message digest. One of SHA1, SHA2_256, SHA2_384, SHA2_512.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_ipsec_vpn_tunnel#tunnel_digest_algorithms NsxtIpsecVpnTunnel#tunnel_digest_algorithms}
        '''
        result = self._values.get("tunnel_digest_algorithms")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def tunnel_pfs_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Perfect Forward Secrecy Enabled or Disabled. Default (enabled).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_ipsec_vpn_tunnel#tunnel_pfs_enabled NsxtIpsecVpnTunnel#tunnel_pfs_enabled}
        '''
        result = self._values.get("tunnel_pfs_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def tunnel_sa_lifetime(self) -> typing.Optional[jsii.Number]:
        '''Security Association life time (in seconds).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/vmware/vcd/3.14.1/docs/resources/nsxt_ipsec_vpn_tunnel#tunnel_sa_lifetime NsxtIpsecVpnTunnel#tunnel_sa_lifetime}
        '''
        result = self._values.get("tunnel_sa_lifetime")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NsxtIpsecVpnTunnelSecurityProfileCustomization(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class NsxtIpsecVpnTunnelSecurityProfileCustomizationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="vcd.nsxtIpsecVpnTunnel.NsxtIpsecVpnTunnelSecurityProfileCustomizationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__77b10d4d6fc47663a281f484eb599c712d3676445efe51a9905cfffecfa4d225)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetDpdProbeInternal")
    def reset_dpd_probe_internal(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDpdProbeInternal", []))

    @jsii.member(jsii_name="resetIkeDigestAlgorithms")
    def reset_ike_digest_algorithms(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIkeDigestAlgorithms", []))

    @jsii.member(jsii_name="resetIkeSaLifetime")
    def reset_ike_sa_lifetime(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIkeSaLifetime", []))

    @jsii.member(jsii_name="resetTunnelDfPolicy")
    def reset_tunnel_df_policy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTunnelDfPolicy", []))

    @jsii.member(jsii_name="resetTunnelDigestAlgorithms")
    def reset_tunnel_digest_algorithms(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTunnelDigestAlgorithms", []))

    @jsii.member(jsii_name="resetTunnelPfsEnabled")
    def reset_tunnel_pfs_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTunnelPfsEnabled", []))

    @jsii.member(jsii_name="resetTunnelSaLifetime")
    def reset_tunnel_sa_lifetime(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTunnelSaLifetime", []))

    @builtins.property
    @jsii.member(jsii_name="dpdProbeInternalInput")
    def dpd_probe_internal_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "dpdProbeInternalInput"))

    @builtins.property
    @jsii.member(jsii_name="ikeDhGroupsInput")
    def ike_dh_groups_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "ikeDhGroupsInput"))

    @builtins.property
    @jsii.member(jsii_name="ikeDigestAlgorithmsInput")
    def ike_digest_algorithms_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "ikeDigestAlgorithmsInput"))

    @builtins.property
    @jsii.member(jsii_name="ikeEncryptionAlgorithmsInput")
    def ike_encryption_algorithms_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "ikeEncryptionAlgorithmsInput"))

    @builtins.property
    @jsii.member(jsii_name="ikeSaLifetimeInput")
    def ike_sa_lifetime_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "ikeSaLifetimeInput"))

    @builtins.property
    @jsii.member(jsii_name="ikeVersionInput")
    def ike_version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "ikeVersionInput"))

    @builtins.property
    @jsii.member(jsii_name="tunnelDfPolicyInput")
    def tunnel_df_policy_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tunnelDfPolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="tunnelDhGroupsInput")
    def tunnel_dh_groups_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "tunnelDhGroupsInput"))

    @builtins.property
    @jsii.member(jsii_name="tunnelDigestAlgorithmsInput")
    def tunnel_digest_algorithms_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "tunnelDigestAlgorithmsInput"))

    @builtins.property
    @jsii.member(jsii_name="tunnelEncryptionAlgorithmsInput")
    def tunnel_encryption_algorithms_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "tunnelEncryptionAlgorithmsInput"))

    @builtins.property
    @jsii.member(jsii_name="tunnelPfsEnabledInput")
    def tunnel_pfs_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "tunnelPfsEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="tunnelSaLifetimeInput")
    def tunnel_sa_lifetime_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "tunnelSaLifetimeInput"))

    @builtins.property
    @jsii.member(jsii_name="dpdProbeInternal")
    def dpd_probe_internal(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "dpdProbeInternal"))

    @dpd_probe_internal.setter
    def dpd_probe_internal(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__478841f4754533c69b46270aec8f09e93e37da1613553e754a62f504125dba97)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dpdProbeInternal", value)

    @builtins.property
    @jsii.member(jsii_name="ikeDhGroups")
    def ike_dh_groups(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "ikeDhGroups"))

    @ike_dh_groups.setter
    def ike_dh_groups(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cab6a989300005af46d69c1bc0054cbf9fca127fbbf9d2886a1fc20998d6cbf0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ikeDhGroups", value)

    @builtins.property
    @jsii.member(jsii_name="ikeDigestAlgorithms")
    def ike_digest_algorithms(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "ikeDigestAlgorithms"))

    @ike_digest_algorithms.setter
    def ike_digest_algorithms(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3ffea8aa9a04138b96379ef2c82dd980df75f12caae4d906642cabbb13f6bc05)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ikeDigestAlgorithms", value)

    @builtins.property
    @jsii.member(jsii_name="ikeEncryptionAlgorithms")
    def ike_encryption_algorithms(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "ikeEncryptionAlgorithms"))

    @ike_encryption_algorithms.setter
    def ike_encryption_algorithms(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ff44e7da6ad313b9c2f0326d1ab0db88b609a747993f3ec6330367926a9c4d98)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ikeEncryptionAlgorithms", value)

    @builtins.property
    @jsii.member(jsii_name="ikeSaLifetime")
    def ike_sa_lifetime(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "ikeSaLifetime"))

    @ike_sa_lifetime.setter
    def ike_sa_lifetime(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__50a6108f1c088738c0ae2a9380bb9d1c8622a6501cf54371db33ef616eaa919d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ikeSaLifetime", value)

    @builtins.property
    @jsii.member(jsii_name="ikeVersion")
    def ike_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ikeVersion"))

    @ike_version.setter
    def ike_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__17fd28c6f6b1378282c9c32cc68ecb438f2f45d76c47344f7de18a203d617bc4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ikeVersion", value)

    @builtins.property
    @jsii.member(jsii_name="tunnelDfPolicy")
    def tunnel_df_policy(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tunnelDfPolicy"))

    @tunnel_df_policy.setter
    def tunnel_df_policy(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__51cb2f7bb559fcfac1dec1972cfe002def920976bea237ba7e7fbc50fb57a702)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tunnelDfPolicy", value)

    @builtins.property
    @jsii.member(jsii_name="tunnelDhGroups")
    def tunnel_dh_groups(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "tunnelDhGroups"))

    @tunnel_dh_groups.setter
    def tunnel_dh_groups(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e318ae51e84de0e1ed6cde9067ad7d03902c184a68e7821b4870e32d65d48e7c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tunnelDhGroups", value)

    @builtins.property
    @jsii.member(jsii_name="tunnelDigestAlgorithms")
    def tunnel_digest_algorithms(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "tunnelDigestAlgorithms"))

    @tunnel_digest_algorithms.setter
    def tunnel_digest_algorithms(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1605028697d6dafe48fdce7013d2b6461d39dbccf1666478c23f1ad335ea4585)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tunnelDigestAlgorithms", value)

    @builtins.property
    @jsii.member(jsii_name="tunnelEncryptionAlgorithms")
    def tunnel_encryption_algorithms(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "tunnelEncryptionAlgorithms"))

    @tunnel_encryption_algorithms.setter
    def tunnel_encryption_algorithms(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8fad8c790db488aed15d2f1c71f0cda5b351136dd7663588aa54af62d687bc32)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tunnelEncryptionAlgorithms", value)

    @builtins.property
    @jsii.member(jsii_name="tunnelPfsEnabled")
    def tunnel_pfs_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "tunnelPfsEnabled"))

    @tunnel_pfs_enabled.setter
    def tunnel_pfs_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0cd4f206090aeb6669f4cfa860de1045ea225a413ce0066db772813f3fc89d41)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tunnelPfsEnabled", value)

    @builtins.property
    @jsii.member(jsii_name="tunnelSaLifetime")
    def tunnel_sa_lifetime(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "tunnelSaLifetime"))

    @tunnel_sa_lifetime.setter
    def tunnel_sa_lifetime(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3e2524394f6fd31819819ecebf15600c2a44a6e716b95556ee0b269394840c65)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tunnelSaLifetime", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[NsxtIpsecVpnTunnelSecurityProfileCustomization]:
        return typing.cast(typing.Optional[NsxtIpsecVpnTunnelSecurityProfileCustomization], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[NsxtIpsecVpnTunnelSecurityProfileCustomization],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__31083c75ab742ff887d024fbd1ee11aee3637b61fe5b83afc96d8d4085f0d6f4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


__all__ = [
    "NsxtIpsecVpnTunnel",
    "NsxtIpsecVpnTunnelConfig",
    "NsxtIpsecVpnTunnelSecurityProfileCustomization",
    "NsxtIpsecVpnTunnelSecurityProfileCustomizationOutputReference",
]

publication.publish()

def _typecheckingstub__9d636efabf297d57331630ede2a71abdbf2a275ee172ea8cc37ca9ceb88afadb(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    edge_gateway_id: builtins.str,
    local_ip_address: builtins.str,
    local_networks: typing.Sequence[builtins.str],
    name: builtins.str,
    pre_shared_key: builtins.str,
    remote_ip_address: builtins.str,
    authentication_mode: typing.Optional[builtins.str] = None,
    ca_certificate_id: typing.Optional[builtins.str] = None,
    certificate_id: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    logging: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    org: typing.Optional[builtins.str] = None,
    remote_id: typing.Optional[builtins.str] = None,
    remote_networks: typing.Optional[typing.Sequence[builtins.str]] = None,
    security_profile_customization: typing.Optional[typing.Union[NsxtIpsecVpnTunnelSecurityProfileCustomization, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__7128e5e54ac728f5aad1a2ff914c4bf709d4f27bf96dcbfbe71b7aaf2700f15f(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b2fa4f92ff439c2a7cd92440d0770b2e6d522eaf5f7f680cdf07311db657f560(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__63610208b3b238d83483f392725efc2276dac712942e5573e93993c182bf4c87(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e567531075115ded3d1a3b9f5389368d663f79ab82c635a37c3388a5894b2715(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__26cbda9cb6cd2e76a86a94814fba6e1d7b50f68b8c2bd84de2b9efadf7497049(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5fdd00fdca93879ba004b250e036692a94779c10701b887d9e0c202992c69fe3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6989f4691e2b491dd6dbb73f85d6936ffe5029ff267bc343f5831250fa314a95(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__99179aae83c2e52760e5480ea139ba000e89e237ca0cc0691e01ba374182da08(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__37f76249fe8bcd6aeca04c4b526274ede716ae1cd6f177b049b7bb9094a00a87(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c76f008072490656f79acacf7810c79621f9ec048ec1bef1d28be22df58e5d1(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0fcca17d1766716558544d9d525383c28707ffd6f9803d07c536e665d2a0ef7c(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ae15aeddf58577a28768f5512a14e6ee03f781f96df53966e367b464ba6ba5f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d726504acc54e26f7d9b73a48109b07b10fac19dd2b2a4715c1c079009081bab(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d7f4218c05a7eee3845d375fa6be3300512e32fd9f05e5b6be4364e68aeb15be(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b84444762edcd91d7777c188efc80a3735ddfcd29291865307605d8223b669f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c1b864063d26b13124cd73c82942d19451cb12c7b1bb817aac7395be3932cb12(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9807e37410a1f60d15ccae4b36fb025146f7088420a8c1041da246df2794da33(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3897e46541afc238bea23848c0853c6fd6e5852e4d1559fcd27e37eb004e3711(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__99a5243fd93167cc768527b58062e75272cdda017086cdbadb5682d4f382b147(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    edge_gateway_id: builtins.str,
    local_ip_address: builtins.str,
    local_networks: typing.Sequence[builtins.str],
    name: builtins.str,
    pre_shared_key: builtins.str,
    remote_ip_address: builtins.str,
    authentication_mode: typing.Optional[builtins.str] = None,
    ca_certificate_id: typing.Optional[builtins.str] = None,
    certificate_id: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    logging: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    org: typing.Optional[builtins.str] = None,
    remote_id: typing.Optional[builtins.str] = None,
    remote_networks: typing.Optional[typing.Sequence[builtins.str]] = None,
    security_profile_customization: typing.Optional[typing.Union[NsxtIpsecVpnTunnelSecurityProfileCustomization, typing.Dict[builtins.str, typing.Any]]] = None,
    vdc: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4ca323f8922401e6a91fdc09b86a72d5230006ce750c35068e4568b2d5e3891c(
    *,
    ike_dh_groups: typing.Sequence[builtins.str],
    ike_encryption_algorithms: typing.Sequence[builtins.str],
    ike_version: builtins.str,
    tunnel_dh_groups: typing.Sequence[builtins.str],
    tunnel_encryption_algorithms: typing.Sequence[builtins.str],
    dpd_probe_internal: typing.Optional[jsii.Number] = None,
    ike_digest_algorithms: typing.Optional[typing.Sequence[builtins.str]] = None,
    ike_sa_lifetime: typing.Optional[jsii.Number] = None,
    tunnel_df_policy: typing.Optional[builtins.str] = None,
    tunnel_digest_algorithms: typing.Optional[typing.Sequence[builtins.str]] = None,
    tunnel_pfs_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    tunnel_sa_lifetime: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__77b10d4d6fc47663a281f484eb599c712d3676445efe51a9905cfffecfa4d225(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__478841f4754533c69b46270aec8f09e93e37da1613553e754a62f504125dba97(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cab6a989300005af46d69c1bc0054cbf9fca127fbbf9d2886a1fc20998d6cbf0(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ffea8aa9a04138b96379ef2c82dd980df75f12caae4d906642cabbb13f6bc05(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff44e7da6ad313b9c2f0326d1ab0db88b609a747993f3ec6330367926a9c4d98(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__50a6108f1c088738c0ae2a9380bb9d1c8622a6501cf54371db33ef616eaa919d(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__17fd28c6f6b1378282c9c32cc68ecb438f2f45d76c47344f7de18a203d617bc4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__51cb2f7bb559fcfac1dec1972cfe002def920976bea237ba7e7fbc50fb57a702(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e318ae51e84de0e1ed6cde9067ad7d03902c184a68e7821b4870e32d65d48e7c(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1605028697d6dafe48fdce7013d2b6461d39dbccf1666478c23f1ad335ea4585(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8fad8c790db488aed15d2f1c71f0cda5b351136dd7663588aa54af62d687bc32(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0cd4f206090aeb6669f4cfa860de1045ea225a413ce0066db772813f3fc89d41(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e2524394f6fd31819819ecebf15600c2a44a6e716b95556ee0b269394840c65(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__31083c75ab742ff887d024fbd1ee11aee3637b61fe5b83afc96d8d4085f0d6f4(
    value: typing.Optional[NsxtIpsecVpnTunnelSecurityProfileCustomization],
) -> None:
    """Type checking stubs"""
    pass
