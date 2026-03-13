
=== 结构体 Firewall 及其依赖定义 ===

// Firewall
type Firewall struct {
	Asset
	IpInfo
	Project
	Region
	BriefVpc
	BriefSubnets []*BriefSubnet `json:"briefSubnets" bson:"briefSubnets"`
	FirewallAssets []*HelpFirewall `json:"firewallAssets" bson:"firewallAssets"`
	FirewallEndpoints []*FirewallEndpoint `json:"firewallEndpoints" bson:"firewallEndpoints"`
	FirewallStatus modelasset.StatusEnum `json:"FirewallStatus" bson:"FirewallStatus"`
	AclCollectionGroup []*modelasset.AclCollectionGroup `json:"aclCollectionGroup" bson:"aclCollectionGroup"`
	Acl modelasset.Acl `json:"acl" bson:"acl"`
	PublicAccess bool `json:"publicAccess" bson:"publicAccess"`
	PublicIgwIds []string `json:"publicIgwIds" bson:"publicIgwIds"`
	SupportNatRule bool `json:"supportNatRule" bson:"supportNatRule"`
	WhiteMode bool `json:"whiteMode" bson:"whiteMode"`
	DeleteProtection bool `json:"deleteProtection" bson:"deleteProtection"`
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


// IpInfo
type IpInfo struct {
	PublicIp []string `json:"publicIp" bson:"publicIp"`
	PrivateIp []string `json:"privateIp" bson:"privateIp"`
}


// Project
type Project struct {
	ProjectId string `json:"projectId" bson:"projectId"`
	ProjectName string `json:"projectName" bson:"projectName"`
	ProjectParentId string `json:"projectParentId" bson:"projectParentId"`
}


// Region
type Region struct {
	RegionId string `json:"regionId" bson:"regionId"`
	RegionName string `json:"regionName" bson:"regionName"`
}


// BriefVpc
type BriefVpc struct {
	VpcId string `json:"vpcId" bson:"vpcId"`
	VpcName string `json:"vpcName" bson:"vpcName"`
	RelationVpcId string `json:"relationVpcId" bson:"relationVpcId"`
	VpcCidr []string `json:"vpcCidr" bson:"vpcCidr"`
}


// BriefSubnet
type BriefSubnet struct {
	SubnetId string `json:"subnetId" bson:"subnetId"`
	SubnetName string `json:"subnetName" bson:"subnetName"`
	RelationSubnetId string `json:"relationSubnetId" bson:"relationSubnetId"`
	PublicAccess bool `json:"publicAccess" bson:"publicAccess"`
	SubnetCidr string `json:"subnetCidr" bson:"subnetCidr"`
}


// HelpFirewall
type HelpFirewall struct {
	FirewallProtection
	RegionId string `json:"regionId" bson:"regionId"`
}


// FirewallProtection
type FirewallProtection struct {
	BriefFirewallProtection
}


// BriefFirewallProtection
type BriefFirewallProtection struct {
	InstanceId string `json:"instanceId" bson:"instanceId"`
	IpAddress string `json:"ipAddress" bson:"ipAddress"`
	ProtectionStatus modelasset.StatusEnum `json:"protectionStatus" bson:"protectionStatus"`
	ResourceType string `json:"resourceType" bson:"resourceType"`
	Name string `json:"name" bson:"name"`
	InstanceVpcId string `json:"instanceVpcId" bson:"instanceVpcId"`
}


// FirewallEndpoint
type FirewallEndpoint struct {
	EndpointId string `json:"endpointId" bson:"endpointId"`
	Status modelasset.StatusEnum `json:"status" bson:"status"`
	SubnetId string `json:"subnetId" bson:"subnetId"`
	RegionId string `json:"regionId" bson:"regionId"`
}


