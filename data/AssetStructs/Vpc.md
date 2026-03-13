
=== 结构体 Vpc 及其依赖定义 ===

// Vpc
type Vpc struct {
	Asset
	Region
	Project
	Cidrs []string
	Subnet []BriefSubnet
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


// Project
type Project struct {
	ProjectId string `json:"projectId" bson:"projectId"`
	ProjectName string `json:"projectName" bson:"projectName"`
	ProjectParentId string `json:"projectParentId" bson:"projectParentId"`
}


// BriefSubnet
type BriefSubnet struct {
	SubnetId string `json:"subnetId" bson:"subnetId"`
	SubnetName string `json:"subnetName" bson:"subnetName"`
	RelationSubnetId string `json:"relationSubnetId" bson:"relationSubnetId"`
	PublicAccess bool `json:"publicAccess" bson:"publicAccess"`
	SubnetCidr string `json:"subnetCidr" bson:"subnetCidr"`
}


