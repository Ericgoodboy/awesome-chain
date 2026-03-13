
=== 结构体 Subnet 及其依赖定义 ===

// Subnet
type Subnet struct {
	Asset
	Project
	SubnetInfo
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


// Project
type Project struct {
	ProjectId string `json:"projectId" bson:"projectId"`
	ProjectName string `json:"projectName" bson:"projectName"`
	ProjectParentId string `json:"projectParentId" bson:"projectParentId"`
}


// SubnetInfo
type SubnetInfo struct {
	Region
	Description string `json:"description" bson:"description"`
	Cidr string `json:"cidr" bson:"cidr"`
	GatewayIp string `json:"gatewayIp" bson:"gatewayIp"`
	BriefVpc
	Status modelasset.StatusEnum `json:"status" bson:"status"`
	RouteTableId string `json:"routeTableId" bson:"routeTableId"`
	PublicAccess bool `json:"publicAccess" bson:"publicAccess"`
	PublicNatIds []string `json:"publicNatIds" bson:"publicNatIds"`
	PublicIgwIds []string `json:"publicIgwIds" bson:"publicIgwIds"`
	PublicFWIds []string `json:"publicFWIds" bson:"publicFWIds"`
	IsVirtual bool `json:"isVirtual" json:"isVirtual"`
	SecurityGroupIds
	SecurityGroup []*SecurityGroup `json:"securityGroup" bson:"securityGroup"`
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


// SecurityGroup
type SecurityGroup struct {
	Asset
	Region
	Rule SecRules `json:"rule" bson:"rule"`
	InnerAccessPolicy string `json:"innerAccessPolicy" bson:"innerAccessPolicy"`
	Priority int32 `json:"priority" bson:"priority"`
}


