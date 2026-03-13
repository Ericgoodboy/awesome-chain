
=== 结构体 Mq 及其依赖定义 ===

// Mq
type Mq struct {
	Asset
	MqInfo
	AssetTag []string `json:"assetTag" bson:"assetTag"`
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


// MqInfo
type MqInfo struct {
	RegionZone
	Project
	IpInfo
	BriefVpc
	BriefSubnet
	SecurityGroupIds
	SecurityGroup []*SecurityGroup `json:"securityGroup"`
	Status modelasset.StatusEnum
	Description string
	MqType MqEnum
	WhiteList []*WhiteList `json:"whiteList"`
	SubnetGroup []string `json:"subnetGroup"`
	SubnetGroupInfo SubnetGroupInfo `json:"subnetGroupInfo"`
	SubnetCidrList []string `json:"subnetCidrList"`
	SubnetPrivateIpMap map[string]string `json:"subnetPrivateIpMap"`
	EndPointPort int `json:"endPointPort"`
	LogEnabled bool `json:"logEnabled" bson:"logEnabled"`
	PublicAccessEnabled bool `json:"publicAccessEnabled" bson:"publicAccessEnabled"`
}


// RegionZone
type RegionZone struct {
	Region
	Zone
}


// Region
type Region struct {
	RegionId string `json:"regionId" bson:"regionId"`
	RegionName string `json:"regionName" bson:"regionName"`
}


// Zone
type Zone struct {
	ZoneId string `json:"zoneId" bson:"zoneId"`
	ZoneName string `json:"zoneName" bson:"zoneName"`
}


// Project
type Project struct {
	ProjectId string `json:"projectId" bson:"projectId"`
	ProjectName string `json:"projectName" bson:"projectName"`
	ProjectParentId string `json:"projectParentId" bson:"projectParentId"`
}


// IpInfo
type IpInfo struct {
	PublicIp []string `json:"publicIp" bson:"publicIp"`
	PrivateIp []string `json:"privateIp" bson:"privateIp"`
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


// SecurityGroup
type SecurityGroup struct {
	Asset
	Region
	Rule SecRules `json:"rule" bson:"rule"`
	InnerAccessPolicy string `json:"innerAccessPolicy" bson:"innerAccessPolicy"`
	Priority int32 `json:"priority" bson:"priority"`
}


// WhiteList
type WhiteList struct {
	IpList []string `json:"ipList" bson:"ipList"`
	Enable bool `json:"enable" bson:"enable"`
	Name string `json:"name" bson:"name"`
	VirtualNetworkRules []string `json:"virtualNetworkRules" bson:"virtualNetworkRules"`
}


// SubnetGroupInfo
type SubnetGroupInfo struct {
	SubnetId string `json:"subnetId" bson:"subnetId"`
	SubnetName string `json:"subnetName" bson:"subnetName"`
	RawSubnetId string `json:"rawSubnetId" bson:"rawSubnetId"`
	OriginSubnetId string `json:"originSubnetId" bson:"originSubnetId"`
}


