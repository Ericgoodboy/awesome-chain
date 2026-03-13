
=== 结构体 Ebs 及其依赖定义 ===

// Ebs
type Ebs struct {
	Asset
	Region
	EbsInfo
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


// EbsInfo
type EbsInfo struct {
	Attached bool `json:"attached" bson:"attached"`
	Encrypted bool `json:"encrypted" bson:"encrypted"`
	Status modelasset.StatusEnum `json:"status" bson:"status"`
}


