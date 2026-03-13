
=== 结构体 LaunchTemplates 及其依赖定义 ===

// LaunchTemplates
type LaunchTemplates struct {
	Asset
	Region
	Project
	Versions []*Version `json:"versions"`
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


// Version
type Version struct {
	HttpEndpoint string `json:"httpEndpoint"`
	HttpTokens string `json:"httpTokens"`
	VersionNumber int `json:"versionNumber"`
	NetworkInterfaces []NetworkInterface `json:"networkInterfaces"`
}


// NetworkInterface
// NetworkInterface 网络接口信息
type NetworkInterface struct {
	AssociatePublicIpAddress bool `json:"associatePublicIpAddress"`
	DeviceIndex int `json:"deviceIndex"`
}


