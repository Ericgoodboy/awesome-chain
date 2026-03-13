
=== 结构体 ContainerImage 及其依赖定义 ===

// ContainerImage
type ContainerImage struct {
	Asset
	Region
	ContainerImageInfo
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


// ContainerImageInfo
type ContainerImageInfo struct {
	ImageId string `json:"imageId"`
	Tag string `json:"tag"`
	ImageSize int64 `json:"imageSize"`
	Repository string `json:"repository"`
	ImageUri string `json:"imageUri"`
	ContainerCount int32 `json:"containerCount"`
	PushTime time.Time `json:"pushTime"`
	Digest string `json:"digest"`
	InstanceId string `json:"instanceId"`
	Location string `json:"location"`
}


