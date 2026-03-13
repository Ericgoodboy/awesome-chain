
=== 结构体 NatFirewall 及其依赖定义 ===

// NatFirewall
type NatFirewall struct {
	Asset
	Region
	NatFirewallInfo
}


// Asset
// Asset 资产
type Asset struct {
	TenantId int64 `json:"tenantId"`
	CloudAccountId string `json:"cloudAccountId"`
	ResourceType string `json:"resourceType"`
	Source string `json:"source"`
	LocalRegion string `json:"-"`
	RawAssetInfo
}


// RawAssetInfo
type RawAssetInfo struct {
	RawId string `json:"rawId"`
	RawIdShow string `json:"rawIdShow"`
	Name string `json:"name"`
	CreateTime time.Time `json:"createTime"`
	AssetVersion string `json:"assetVersion"`
}


// Region
type Region struct {
	RegionId string `json:"regionId" bson:"regionId"`
	RegionName string `json:"regionName" bson:"regionName"`
}


// NatFirewallInfo
type NatFirewallInfo struct {
	NatFirewallAssets []*NatFirewallAsset `json:"natGatewayList" bson:"natGatewayList"`
}


// NatFirewallAsset
type NatFirewallAsset struct {
	InstanceId string `json:"instanceId" bson:"instanceId"`
	InstanceName string `json:"instanceName" bson:"instanceName"`
	ProtectionStatus modelasset.StatusEnum `json:"protectionStatus" bson:"protectionStatus"`
	Region
	BriefVpc
	IpInfo
	Acl modelasset.Acl `json:"acl" bson:"acl"`
	TencentFwMode TencentNatFwModeType `json:"tencentFwMode" bson:"tencentFwMode"`
	StrictMode NatFwStrictModeType `json:"strictMode" bson:"strictMode"`
}


// BriefVpc
type BriefVpc struct {
	VpcId string `json:"vpcId" bson:"vpcId"`
	VpcName string `json:"vpcName" bson:"vpcName"`
	RelationVpcId string `json:"relationVpcId" bson:"relationVpcId"`
	VpcCidr []string `json:"vpcCidr" bson:"vpcCidr"`
}


// IpInfo
type IpInfo struct {
	PublicIp []string `json:"publicIp" bson:"publicIp"`
	PrivateIp []string `json:"privateIp" bson:"privateIp"`
}


