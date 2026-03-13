
=== 结构体 Eni 及其依赖定义 ===

// Eni
type Eni struct {
	Asset
	BriefVpc
	BriefSubnet
	RegionZone
	Project
	PublicIp []*PublicInfo `json:"publicIp" bson:"publicIp"`
	PrivateIp []string `json:"privateIp" bson:"privateIp"`
	SecurityGroupIds
	SecurityGroup []*SecurityGroup `json:"securityGroup" bson:"securityGroup"`
	Status modelasset.StatusEnum `json:"status" bson:"status"`
	CloudSource int64 `json:"cloudSource" bson:"cloudSource"`
	MacAddress string `json:"macAddress" bson:"macAddress"`
	Description string `json:"description" bson:"description"`
	Primary bool `json:"primary" json:"primary"`
	AppSecGroupIds []string `json:"appSecGroupIds" bson:"appSecGroupIds"`
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


// PublicInfo
type PublicInfo struct {
	Ip string `json:"ip" bson:"ip"`
	IpAddressId string `json:"ipAddressId" bson:"ipAddressId"`
	RelationIpAddressId string `json:"relationIpAddressId" bson:"relationIpAddressId"`
}


// SecurityGroup
type SecurityGroup struct {
	Asset
	Region
	Rule SecRules `json:"rule" bson:"rule"`
	InnerAccessPolicy string `json:"innerAccessPolicy" bson:"innerAccessPolicy"`
	Priority int32 `json:"priority" bson:"priority"`
}


