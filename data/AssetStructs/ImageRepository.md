
=== 结构体 ImageRepository 及其依赖定义 ===

// ImageRepository
type ImageRepository struct {
	Asset
	Region
	ImageRepositoryInfo
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


// ImageRepositoryInfo
type ImageRepositoryInfo struct {
	RepositoryId string `json:"repositoryId"`
	InstanceId string `json:"instanceId"`
	Path string `json:"path"`
	Namespace string `json:"Namespace"`
	Repository string `json:"repository"`
	RealRepository string `json:"realRepository"`
	EndPoint string `json:"endpoint"`
	Location string `json:"location"`
}


